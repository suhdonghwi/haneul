# -*- coding: utf-8 -*-

from instruction import *
from constant import *
from error import HaneulError, ArgNumberMismatch


class CallFrame:
  def __init__(self, slot_start, const_table):
    self.slot_start = slot_start
    self.const_table = const_table


class BytecodeInterpreter:
  def __init__(self, const_table):
    self.global_vars = {}

    self.stack = []
    self.call_frames = [CallFrame(0, const_table)]

  def run(self, code):
    code_iter = iter(code)
    for inst in code_iter:
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
          self.stack[self.call_frames[-1].slot_start +
                     inst.operand_int + 1] = self.stack.pop()
        elif inst.opcode == INST_STORE_GLOBAL:
          # print "STORE_GLOBAL"
          self.global_vars[inst.operand_str] = self.stack.pop()
        elif inst.opcode == INST_LOAD:
          # print "LOAD"
          self.stack.append(
              self.stack[self.call_frames[-1].slot_start + inst.operand_int + 1])
        elif inst.opcode == INST_LOAD_GLOBAL:
          # print "LOAD_GLOBAL"
          self.stack.append(self.global_vars[inst.operand_str])
        elif inst.opcode == INST_CALL:
          # print "CALL"
          func_object = self.stack[len(
              self.stack) - inst.operand_int - 1].funcval

          if func_object.arity != inst.operand_int:
            raise ArgNumberMismatch("이 함수는 " + str(func_object.arity) +
                                    "개의 인수를 받지만 " + str(inst.operand_int) + "개의 인수가 주어졌습니다.")

          new_slot_start = len(self.stack) - inst.operand_int - 1
          self.call_frames.append(
              CallFrame(new_slot_start, func_object.const_table))
          self.run(func_object.code)
        elif inst.opcode == INST_JMP_FORWARD:
          # print "JMPFORWARD"
          for i in range(inst.operand_int):
            next(code_iter)
        elif inst.opcode == INST_POP_JMP_IF_FALSE:
          # print "POPJMPIFFALSE"
          value = self.stack.pop().boolval
          if value == False:
            for i in range(inst.operand_int):
              next(code_iter)
        elif inst.opcode == INST_RETURN:
          # print "RETURN"
          return_value = self.stack.pop()

          for i in range(len(self.stack) - self.call_frames[-1].slot_start):
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
      except HaneulError as e:
        if e.error_line == 0:
          e.error_line = inst.line_number
        raise e

      """
      # print "[",
      for c in self.stack:
        if c.type == TYPE_INT:
          # print c.intval,
        if c.type == TYPE_DOUBLE:
          # print c.doubleval,
        if c.type == TYPE_CHAR:
          # print c.charval,
        if c.type == TYPE_BOOLEAN:
          # print c.boolval,
        if c.type == TYPE_FUNC:
          # print c.funcval,
          # print ", ",
          # print "]"
      """
