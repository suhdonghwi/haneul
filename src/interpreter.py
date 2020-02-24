# -*- coding: utf-8 -*-
# from rpython.rlib.jit import JitDriver, promote, elidable

from instruction import *
from constant import *
from error import HaneulError, InvalidType, ArgNumberMismatch, UnboundVariable, UnboundJosa


# jitdriver = JitDriver(greens=['pc', 'slot_start', 'const_table', 'code', 'free_vars', 'frame'],
#                       reds=['stack', 'global_vars', 'self'])


class CallFrame:
  # _immutable_fields_ = ['const_table',
  #                       'code', 'free_vars[*]', 'slot_start']

  def __init__(self, const_table, code, free_vars, slot_start):
    self.pc = 0
    self.const_table = const_table
    self.code = code
    self.free_vars = free_vars
    self.slot_start = slot_start

  # @elidable
  def get_constant(self, index):
    return self.const_table[index]


class Program:
  def __init__(self, global_var_names, global_vars, frame):
    self.global_var_names = global_var_names
    self.global_vars = global_vars + [None] *\
        (len(global_var_names) - len(global_vars))

    self.stack = []
    self.call_stack = [frame]

  def push(self, v):
    self.stack.append(v)

  def pop(self):
    return self.stack.pop()

  def peek(self, n=0):
    return self.stack[len(self.stack) - n - 1]

  def current_frame(self):
    return self.call_stack[-1]

  def run(self):
    while True:
      frame = self.current_frame()

      if frame.pc >= len(frame.code):
        if len(self.call_stack) == 1:
          break

        result = self.pop()
        while len(self.stack) != frame.slot_start:
          self.stack.pop()
        self.push(result)

        self.call_stack.pop()
        continue

      # jitdriver.jit_merge_point(
      #     pc=pc, const_table=frame.const_table, code=frame.code, free_vars=frame.free_vars, slot_start=frame.slot_start, frame=frame,
      #     stack=self.stack, global_vars=self.global_vars, self=self)

      inst = frame.code[frame.pc]
      # inst = promote(inst)
      try:
        if inst.opcode == INST_PUSH:
          # print "PUSH"
          self.push(frame.get_constant(inst.operand_int))

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
          if result is None:
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
              if josa == u"_":
                for (k, v) in value.josa_map.iteritems():
                  if v is None:
                    value.josa_map[k] = self.pop()
                    break
              else:
                if josa in value.josa_map:
                  value.josa_map[josa] = self.pop()
                else:
                  raise UnboundJosa(u"조사 '%s'를 찾을 수 없습니다." % josa)
                  return

            args = value.josa_map.values()
            rest_arity = 0
            for v in args:
              if v is None:
                rest_arity += 1

            if rest_arity > 0:
              self.push(value)
            else:  # rest_arity == 0
              if value.builtinval is None:
                func_object = value.funcval
                func_frame = CallFrame(func_object.const_table, func_object.code,
                                       func_object.free_vars, len(self.stack))
                self.stack.extend(args)
                self.call_stack.append(func_frame)

              else:
                func_result = value.builtinval(args)
                self.push(func_result)

          else:
            raise InvalidType(
                u"%s 타입의 값은 호출 가능하지 않습니다." % get_type_name(value.type))

          #   raise argnumbermismatch(
          #       u"이 함수 %d개의 인수를 받지만 %d개의 인수가 주어졌습니다." % (func_object.arity, inst.operand_int))

        elif inst.opcode == INST_JMP:
          # print "JMP"
          frame.pc = inst.operand_int
          # jitdriver.can_enter_jit(pc=pc, code=code, program=program)
          continue

        elif inst.opcode == INST_POP_JMP_IF_FALSE:
          # print "POPJMPIFFALSE"
          value = self.pop()
          if value.type != TYPE_BOOLEAN:
            raise InvalidType(u"여기에는 참 또는 거짓 타입을 필요로 합니다.")

          if value.boolval == False:
            frame.pc = inst.operand_int
            continue

        elif inst.opcode == INST_FREE_VAR_LOCAL:
          value = self.stack[frame.slot_start + inst.operand_int]
          self.stack[-1].funcval.free_vars.append(value)

        elif inst.opcode == INST_FREE_VAR_FREE:
          value = frame.free_vars[inst.operand_int]
          self.stack[-1].funcval.free_vars.append(value)

        elif inst.opcode == INST_NEGATE:
          # print "NEGATE"
          value = self.pop()
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

        frame.pc += 1
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
