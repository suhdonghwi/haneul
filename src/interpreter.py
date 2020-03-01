# -*- coding: utf-8 -*-
from rpython.rlib import jit

from instruction import *
from constant import *
from error import HaneulError, InvalidType, ArgNumberMismatch, UnboundVariable, UnboundJosa

import copy


def get_location(pc, code_object):
  """Add debug information.
  PYPYLOG=jit-log-opt,jit-backend,jit-summary:<filename>
  """
  inst = code_object.code[pc]
  return "#%d_%s_%d" % (pc, INSTRUCTION_NAMES[inst.opcode], inst.operand_int)


jitdriver = jit.JitDriver(greens=['pc', 'code_object'],
                          reds=['stack', 'frame', 'self'], get_printable_location=get_location)


@jit.unroll_safe
def resolve_josa(josa, josa_map):
  if josa == u"_":
    for (j, (k, v)) in enumerate(josa_map):
      if v is None:
        return (k, j)
    raise InvalidType(u"이 함수에는 더 이상 값을 적용할 수 없습니다.")
  else:
    for (j, (k, v)) in enumerate(josa_map):
      if josa == k:
        return (josa, j)
    raise UnboundJosa(u"조사 '%s'를 찾을 수 없습니다." % josa)


class Env:
  """
  전역인 값들을 담아두는 Environment 입니다.
  """
  _immutable_fields_ = ['var_names[*]']

  def __init__(self, var_names, vars):
    self.var_names = var_names
    self.vars = vars + [None] * (len(var_names) - len(vars))

  def store(self, value, index):
    self.vars[index] = value

  @jit.elidable
  def lookup(self, index):
    result = self.vars[index]
    if result is None:
      raise UnboundVariable(u"변수 '%s'를 찾을 수 없습니다." %
                            self.var_names[index])
    else:
      return result


class Frame:
  """
  지역 변수들을 담아두는 스택 프레임입니다.
  """
  _immutable_fields_ = ['locals']

  def __init__(self, values):
    self.locals = values

  @jit.elidable
  def load(self, index):
    return self.locals[index]

  def store(self, value):
    self.locals.append(value)


class Interpreter:
  def __init__(self, env):
    self.env = env

  def run(self, code_object, args):
    pc = 0
    stack = []
    frame = Frame(args)
    code_object = jit.promote(code_object)

    while pc < len(code_object.code):
      # print pc
      jitdriver.jit_merge_point(
          pc=pc, code_object=code_object,
          stack=stack, frame=frame, self=self)

      inst = jit.promote(code_object.code[pc])
      op = jit.promote(inst.opcode)
      try:
        if op == INST_PUSH:
          stack.append(code_object.get_constant(inst.operand_int))

        elif op == INST_POP:
          stack.pop()

        elif op == INST_LOAD:
          stack.append(frame.load(inst.operand_int))

        elif op == INST_STORE:
          frame.store(stack.pop())

        elif op == INST_LOAD_DEREF:
          stack.append(code_object.free_vars[inst.operand_int])

        elif op == INST_LOAD_GLOBAL:
          stack.append(self.env.lookup(inst.operand_int))

        elif op == INST_STORE_GLOBAL:
          self.env.store(stack.pop(), inst.operand_int)

        elif op == INST_CALL:
          given_arity = len(inst.operand_str)

          value = stack.pop()
          josa_map = list(value.josa_map)
          if value.type == TYPE_FUNC:
            args = []
            rest_arity = 0

            if len(josa_map) == 1 and josa_map[0][0] == inst.operand_str[0]:
              args.append(stack.pop())
            else:
              for josa in inst.operand_str:
                (j, index) = resolve_josa(josa, josa_map)
                josa_map[index] = (j, stack.pop())

              for (_, v) in josa_map:
                args.append(v)
                if v is None:
                  rest_arity += 1

            if rest_arity > 0:
              func = ConstFunc([], value.funcval, value.builtinval)
              func.josa_map = josa_map
              stack.append(func)
            else:  # rest_arity == 0
              if value.builtinval is None:
                result = self.run(value.funcval, args)
                stack.append(result)
              else:
                func_result = value.builtinval(args)
                stack.append(func_result)

          else:
            raise InvalidType(
                u"%s 타입의 값은 호출 가능하지 않습니다." % get_type_name(value.type))

        elif op == INST_JMP:
          pc = inst.operand_int
          continue

        elif op == INST_POP_JMP_IF_FALSE:
          value = stack.pop()
          if value.type != TYPE_BOOLEAN:
            raise InvalidType(u"여기에는 참 또는 거짓 타입을 필요로 합니다.")

          if value.boolval == False:
            pc = inst.operand_int
            continue

        elif op == INST_FREE_VAR_LOCAL:
          value = frame.locals[inst.operand_int]
          func = stack.pop().copy()
          func.funcval.free_vars.append(value)
          stack.append(func)

        elif op == INST_FREE_VAR_FREE:
          value = code_object.free_vars[inst.operand_int]
          func = stack.pop().copy()
          func.funcval.free_vars.append(value)
          stack.append(func)

        elif op == INST_NEGATE:
          value = stack.pop()
          stack.append(value.negate())
        else:
          rhs, lhs = stack.pop(), stack.pop()
          if op == INST_ADD:
            stack.append(lhs.add(rhs))
          elif op == INST_SUBTRACT:
            stack.append(lhs.subtract(rhs))
          elif op == INST_MULTIPLY:
            stack.append(lhs.multiply(rhs))
          elif op == INST_DIVIDE:
            stack.append(lhs.divide(rhs))
          elif op == INST_MOD:
            stack.append(lhs.mod(rhs))
          elif op == INST_EQUAL:
            stack.append(lhs.equal(rhs))
          elif op == INST_LESS_THAN:
            stack.append(lhs.less_than(rhs))
          elif op == INST_GREATER_THAN:
            stack.append(lhs.greater_than(rhs))

        pc += 1
      except HaneulError as e:
        if e.error_line == 0:
          e.error_line = inst.line_number
        raise e

    if len(stack) == 0:
      return None
    else:
      # jitdriver.can_enter_jit(
      #     pc=pc, code_object=code_object,
      #     stack=stack, self=self)
      return stack.pop()
