# -*- coding: utf-8 -*-
from rpython.rlib.jit import JitDriver, promote, elidable

from instruction import *
from constant import *
from error import HaneulError, InvalidType, ArgNumberMismatch, UnboundVariable, CannotReturn, NotCallable


jitdriver = JitDriver(greens=['pc', 'code'],
                      reds=['program'])


class CallFrame:
  _immutable_fields_ = ['const_table']

  def __init__(self, const_table):
    self.const_table = const_table

  @elidable
  def const(self, index):
    return self.const_table[index]


class Program:
  _immutable_fields_ = ['var_list', 'const_table', 'stack']

  def __init__(self, const_table, var_list):
    self.var_list = var_list
    self.const_table = const_table

    self.stack = []

  def push(self, v):
    self.stack.append(v)

  def pop(self):
    return self.stack.pop()

  def peek(self, n=0):
    return self.stack[len(self.stack) - n - 1]

  def find_var(self, var_name):
    for i in range(len(self.var_list) - 1, -1, -1):
      var = self.var_list[i]
      if var[0] == var_name:
        return var[1]

    return None


def run_code(program, code):
  program = promote(program)

  pc = 0
  while pc < len(code):
    jitdriver.jit_merge_point(pc=pc, code=code, program=program)

    inst = code[pc]
    inst = promote(inst)
    try:
      if inst.opcode == INST_PUSH:
        # print "PUSH"
        program.push(program.const_table[inst.operand_int])

      elif inst.opcode == INST_POP:
        # print "POP"
        program.pop()

      elif inst.opcode == INST_STORE:
        # print "STORE"
        program.var_list.append((inst.operand_str, program.pop()))

      elif inst.opcode == INST_LOAD:
        # print "LOAD"
        result = program.find_var(inst.operand_str)
        if result is None:
          # print inst.operand_str
          raise UnboundVariable(u"상수 %s를 찾을 수 없습니다." % inst.operand_str)
        program.push(result)

      elif inst.opcode == INST_POP_NAME:
        program.var_list.pop()

      elif inst.opcode == INST_CALL:
        # print "CALL"
        args = []
        given_arity = inst.operand_int

        for _ in range(given_arity):
          args.insert(0, program.pop())

        callee = program.pop()

        if callee.type == TYPE_FUNC:
          func_object = callee.funcval

          arity = len(func_object.arg_names)
          if arity != given_arity:
            raise ArgNumberMismatch(
                u"이 함수 %d개의 인수를 받지만 %d개의 인수가 주어졌습니다." % (arity, given_arity))

          new_var_list = []
          for i, arg in enumerate(args):
            new_var_list.append((func_object.arg_names[i], arg))

          func_program = Program(func_object.const_table,
                                 program.var_list + new_var_list)
          result = run_code(func_program, func_object.code)
          program.push(result.pop())

        elif callee.type == TYPE_BUILTIN:
          func_object = callee.builtinval

          if func_object.arity != inst.operand_int:
            raise ArgNumberMismatch(
                u"이 함수 %d개의 인수를 받지만 %d개의 인수가 주어졌습니다." % (func_object.arity, inst.operand_int))

          return_val = func_object.func(args)
          program.push(return_val)
        else:
          raise NotCallable(
              u"%s 타입의 값은 호출 가능하지 않습니다." % get_type_name(callee.type))

      elif inst.opcode == INST_JMP:
        # print "JMP"
        pc = inst.operand_int
        # jitdriver.can_enter_jit(pc=pc, code=code, program=program)
        continue

      elif inst.opcode == INST_POP_JMP_IF_FALSE:
        # print "POPJMPIFFALSE"
        value = program.pop()
        if value.type != TYPE_BOOLEAN:
          raise InvalidType(u"여기에는 참 또는 거짓 타입을 필요로 합니다.")

        if value.boolval == False:
          pc = inst.operand_int
          continue

      # elif inst.opcode == INST_RETURN:
      #   # print "RETURN"
      #   if len(program.call_frames) <= 1:
      #     raise CannotReturn(u"여기에서는 값을 반환할 수 없습니다.")

      #   return_value = program.pop()
      #   for _ in range(len(program.stack) - program.current_frame().slot_start):
      #     program.pop()

      #   program.call_frames.pop()
      #   program.push(return_value)
      #   break
      # elif inst.opcode == INST_BUILD_LIST:
      #   list_value = []

      #   for _ in range(inst.operand_int):
      #     list_value.insert(0, program.pop())

      #   program.push(ConstList(list_value))

      elif inst.opcode == INST_NEGATE:
        # print "NEGATE"
        value = program.pop()
        program.push(value.negate())
      else:
        rhs, lhs = program.pop(), program.pop()
        if inst.opcode == INST_ADD:
          # print "ADD"
          program.push(lhs.add(rhs))
        elif inst.opcode == INST_SUBTRACT:
          # print "SUBTRACT"
          program.push(lhs.subtract(rhs))
        elif inst.opcode == INST_MULTIPLY:
          # print "MULTIPLY"
          program.push(lhs.multiply(rhs))
        elif inst.opcode == INST_DIVIDE:
          # print "DIVIDE"
          program.push(lhs.divide(rhs))
        elif inst.opcode == INST_MOD:
          # print "MOD"
          program.push(lhs.mod(rhs))
        elif inst.opcode == INST_EQUAL:
          # print "EQUAL"
          program.push(lhs.equal(rhs))
        elif inst.opcode == INST_LESS_THAN:
          # print "LESS_THAN"
          program.push(lhs.less_than(rhs))
        elif inst.opcode == INST_GREATER_THAN:
          # print "GREATER_THAN"
          program.push(lhs.greater_than(rhs))

      pc += 1
    except HaneulError as e:
      if e.error_line == 0:
        e.error_line = inst.line_number
      raise e

  return program

  """
    # print "[",
    for c in self.stack:
      if c.type == TYPE_INTEGER:
        # print c.intval,
      if c.type == TYPE_REAL:
        # print c.doubleval,
      if c.type == TYPE_STRING:
        # print c.stringval,
      if c.type == TYPE_BOOLEAN:
        # print c.boolval,
      if c.type == TYPE_FUNC:
        # print c.funcval,
        # print ", ",
        # print "]"
    """
