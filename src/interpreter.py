# -*- coding: utf-8 -*-
# from rpython.rlib.jit import JitDriver, promote, elidable

from instruction import *
from constant import *
from error import HaneulError, InvalidType, ArgNumberMismatch, UnboundVariable, CannotReturn, NotCallable


# jitdriver = JitDriver(greens=['pc', 'code'],
#                       reds=['program'])


class CallFrame:
  _immutable_fields_ = ['const_table', 'code', 'free_vars', 'slot_start']

  def __init__(self, const_table, code, free_vars, slot_start):
    self.const_table = const_table
    self.code = code
    self.free_vars = free_vars
    self.slot_start = slot_start

  # @elidable
  def const(self, index):
    return self.const_table[index]


class Program:
  _immutable_fields_ = ['global_vars', 'const_table', 'stack']

  def __init__(self, global_var_names, global_vars):
    self.global_var_names = global_var_names
    self.global_vars = global_vars + [None] * \
        (len(global_var_names) - len(global_vars))

    self.stack = []

  def push(self, v):
    self.stack.append(v)

  def pop(self):
    return self.stack.pop()

  def peek(self, n=0):
    return self.stack[len(self.stack) - n - 1]

  def run(self, frame):
    pc = 0
    while pc < len(frame.code):
      # jitdriver.jit_merge_point(pc=pc, code=frame.code, program=program)

      inst = frame.code[pc]
      # inst = promote(inst)
      try:
        if inst.opcode == INST_PUSH:
          # print "PUSH"
          self.push(frame.const_table[inst.operand_int])

        elif inst.opcode == INST_POP:
          # print "POP"
          self.pop()

        elif inst.opcode == INST_LOAD:
          # print "LOAD"
          self.push(self.stack[frame.slot_start + inst.operand_int])

        elif inst.opcode == INST_LOAD_DEREF:
          self.push(frame.free_vars[inst.operand_int])

        elif inst.opcode == INST_LOAD_GLOBAL:
          result = self.global_vars[inst.operand_int]
          if result == None:
            raise UnboundVariable(u"변수 '%s'를 찾을 수 없습니다." %
                                  self.global_var_names[inst.operand_int])
          else:
            self.push(result)

        elif inst.opcode == INST_STORE_GLOBAL:
          self.global_vars[inst.operand_int] = self.pop()

        elif inst.opcode == INST_CALL:
          # print "CALL"
          given_arity = len(inst.operand_str)

          value = self.pop()
          if value.type == TYPE_FUNC:
            for (i, josa) in enumerate(inst.operand_str):
              if josa == "_":
                for (k, v) in value.josa_map.iteritems():
                  if v == None:
                    value.josa_map[k] = self.pop()
                    break
              else:
                if josa in value.josa_map:
                  value.josa_map[josa] = self.pop()
                else:
                  # TODO: JOSA NOT FOUND ERROR
                  exit(-1)

            args = value.josa_map.values()
            rest_arity = 0
            for v in args:
              if v == None:
                rest_arity += 1

            if rest_arity > 0:
              self.push(value)
            else:  # rest_arity == 0
              func_object = value.funcval
              func_frame = CallFrame(func_object.const_table, func_object.code,
                                     func_object.free_vars, len(self.stack))
              self.stack.extend(args)

              self.run(func_frame)

              func_result = self.pop()

              for _ in range(len(args)):
                self.pop()

              self.push(func_result)
          else:
            raise NotCallable(
                u"%s 타입의 값은 호출 가능하지 않습니다." % get_type_name(value.type))

          #   raise argnumbermismatch(
          #       u"이 함수 %d개의 인수를 받지만 %d개의 인수가 주어졌습니다." % (func_object.arity, inst.operand_int))

        elif inst.opcode == INST_JMP:
          # print "JMP"
          pc = inst.operand_int
          # jitdriver.can_enter_jit(pc=pc, code=code, program=program)
          continue

        elif inst.opcode == INST_POP_JMP_IF_FALSE:
          # print "POPJMPIFFALSE"
          value = self.pop()
          if value.type != TYPE_BOOLEAN:
            raise InvalidType(u"여기에는 참 또는 거짓 타입을 필요로 합니다.")

          if value.boolval == False:
            pc = inst.operand_int
            continue

        elif inst.opcode == INST_FREE_VAR_LOCAL:
          if self.stack[-1] != TYPE_FUNC:
            # TODO: impossible
            exit(-1)

          value = self.stack[frame.slot_start + inst.operand_int]
          self.stack[-1].funcval.free_vars.push(value)

        elif inst.opcode == INST_FREE_VAR_FREE:
          if self.stack[-1] != TYPE_FUNC:
            # TODO: impossible
            exit(-1)

          value = frame.free_vars[inst.operand_int]
          self.stack[-1].funcval.free_vars.push(value)

        elif inst.opcode == INST_NEGATE:
          # print "NEGATE"
          value = program.pop()
          self.push(value.negate())
        else:
          rhs, lhs = self.pop(), self.pop()
          if inst.opcode == INST_ADD:
            # print "ADD"
            self.push(lhs.add(rhs))
          elif inst.opcode == INST_SUBTRACT:
            # print "SUBTRACT"
            self.push(lhs.subtract(rhs))
          elif inst.opcode == INST_MULTIPLY:
            # print "MULTIPLY"
            self.push(lhs.multiply(rhs))
          elif inst.opcode == INST_DIVIDE:
            # print "DIVIDE"
            self.push(lhs.divide(rhs))
          elif inst.opcode == INST_MOD:
            # print "MOD"
            self.push(lhs.mod(rhs))
          elif inst.opcode == INST_EQUAL:
            # print "EQUAL"
            self.push(lhs.equal(rhs))
          elif inst.opcode == INST_LESS_THAN:
            # print "LESS_THAN"
            self.push(lhs.less_than(rhs))
          elif inst.opcode == INST_GREATER_THAN:
            # print "GREATER_THAN"
            self.push(lhs.greater_than(rhs))

        pc += 1
      except HaneulError as e:
        if e.error_line == 0:
          e.error_line = inst.line_number
        raise e

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
