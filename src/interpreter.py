# -*- coding: utf-8 -*-

from instruction import *
from constant import *
from error import HaneulError, ArgNumberMismatch, UnboundVariable, CannotReturn, NotCallable


class CallFrame:
  def __init__(self, slot_start, const_table):
    self.slot_start = slot_start
    self.const_table = const_table


class BytecodeInterpreter:
  def __init__(self, const_table, global_vars):
    self.global_vars = global_vars

    self.stack = []
    self.call_frames = [CallFrame(0, const_table)]

  def run(self, code):
    i = 0
    code_length = len(code)
    while i < code_length:
      inst = code[i]
      try:
        if inst.opcode == INST_PUSH:
          # print "PUSH"
          self.stack.append(
              self.call_frames[-1].const_table[inst.operand_int])
        elif inst.opcode == INST_POP:
          # print "POP"
          self.stack.pop()
        elif inst.opcode == INST_STORE:
          # print "STORE"
          store_index = self.call_frames[-1].slot_start + inst.operand_int + 1

          if store_index != len(self.stack) - 1:
            self.stack[store_index] = self.stack.pop()
        elif inst.opcode == INST_STORE_GLOBAL:
          # print "STORE_GLOBAL"
          self.global_vars[inst.operand_str] = self.stack.pop()
        elif inst.opcode == INST_LOAD:
          # print "LOAD"
          self.stack.append(
              self.stack[self.call_frames[-1].slot_start + inst.operand_int + 1])
        elif inst.opcode == INST_LOAD_GLOBAL:
          # print "LOAD_GLOBAL"
          if inst.operand_str in self.global_vars:
            self.stack.append(self.global_vars[inst.operand_str])
          else:
            raise UnboundVariable(
                u"변수 '%s'을(를) 찾을 수 없습니다." % inst.operand_str)

        elif inst.opcode == INST_CALL:
          # print "CALL"
          callee = self.stack[len(self.stack) - inst.operand_int - 1]

          if callee.type == TYPE_FUNC:
            func_object = callee.funcval

            if func_object.arity != inst.operand_int:
              raise ArgNumberMismatch(
                  u"이 함수 %d개의 인수를 받지만 %d개의 인수가 주어졌습니다." % (func_object.arity, inst.operand_int))

            new_slot_start = len(self.stack) - inst.operand_int - 1
            self.call_frames.append(
                CallFrame(new_slot_start, func_object.const_table))
            self.run(func_object.code)
          elif callee.type == TYPE_BUILTIN:
            func_object = callee.builtinval

            if func_object.arity != inst.operand_int:
              raise ArgNumberMismatch(
                  u"이 함수 %d개의 인수를 받지만 %d개의 인수가 주어졌습니다." % (func_object.arity, inst.operand_int))

            args = []
            for _ in range(inst.operand_int):
              args.insert(0, self.stack.pop())

            return_val = func_object.func(args)
            self.stack.append(return_val)
          else:
            raise NotCallable(
                u"%s 타입의 값은 호출 가능하지 않습니다." % get_type_name(callee.type))
        elif inst.opcode == INST_JMP_FORWARD:
          # print "JMPFORWARD"
          i += inst.operand_int + 1
          continue
        elif inst.opcode == INST_JMP_BACKWARD:
          # print "JMPBACKWARD"
          i -= inst.operand_int
          continue
        elif inst.opcode == INST_POP_JMP_IF_FALSE:
          # print "POPJMPIFFALSE"
          value = self.stack.pop().boolval
          if value == False:
            i += inst.operand_int + 1
            continue
        elif inst.opcode == INST_RETURN:
          # print "RETURN"
          if len(self.call_frames) <= 1:
            raise CannotReturn(u"여기에서는 값을 반환할 수 없습니다.")

          return_value = self.stack.pop()
          for _ in range(len(self.stack) - self.call_frames[-1].slot_start):
            self.stack.pop()

          self.call_frames.pop()
          self.stack.append(return_value)
          break
        elif inst.opcode == INST_NEGATE:
          # print "NEGATE"
          value = self.stack.pop()
          self.stack.append(value.negate())
        else:
          rhs, lhs = self.stack.pop(), self.stack.pop()
          if inst.opcode == INST_ADD:
            # print "ADD"
            self.stack.append(lhs.add(rhs))
          elif inst.opcode == INST_SUBTRACT:
            # print "SUBTRACT"
            self.stack.append(lhs.subtract(rhs))
          elif inst.opcode == INST_MULTIPLY:
            # print "MULTIPLY"
            self.stack.append(lhs.multiply(rhs))
          elif inst.opcode == INST_DIVIDE:
            # print "DIVIDE"
            self.stack.append(lhs.divide(rhs))
          elif inst.opcode == INST_MOD:
            # print "MOD"
            self.stack.append(lhs.mod(rhs))
          elif inst.opcode == INST_EQUAL:
            # print "EQUAL"
            self.stack.append(lhs.equal(rhs))
          elif inst.opcode == INST_LESS_THAN:
            # print "LESS_THAN"
            self.stack.append(lhs.less_than(rhs))
          elif inst.opcode == INST_GREATER_THAN:
            # print "GREATER_THAN"
            self.stack.append(lhs.greater_than(rhs))

        i += 1
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
