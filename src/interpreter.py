# -*- coding: utf-8 -*-
from rpython.rlib.jit import JitDriver, promote, elidable

from instruction import *
from constant import *
from error import HaneulError, InvalidType, ArgNumberMismatch, UnboundVariable, CannotReturn, NotCallable


jitdriver = JitDriver(greens=['pc', 'code'],
                      reds=['program'])


class CallFrame:
  _immutable_fields_ = ['slot_start', 'const_table']

  def __init__(self, slot_start, const_table):
    self.slot_start = slot_start
    self.const_table = const_table

  @elidable
  def const(self, index):
    return self.const_table[index]


class Program:
  _immutable_fields_ = ['global_vars', 'call_frames', 'stack']

  def __init__(self, const_table, global_vars):
    self.global_vars = global_vars
    self.call_frames = [CallFrame(0, const_table)]

    self.stack = []

  def push(self, v):
    self.stack.append(v)

  def pop(self):
    return self.stack.pop()

  def peek(self, n=0):
    return self.stack[len(self.stack) - n]

  def current_frame(self):
    return self.call_frames[-1]


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
        program.push(program.current_frame().const(inst.operand_int))
      elif inst.opcode == INST_POP:
        # print "POP"
        program.pop()
      elif inst.opcode == INST_STORE:
        # print "STORE"
        store_index = program.current_frame().slot_start + inst.operand_int + 1
        if store_index != len(program.stack) - 1:
          program.stack[store_index] = program.pop()
      elif inst.opcode == INST_STORE_GLOBAL:
        # print "STORE_GLOBAL"
        program.global_vars[inst.operand_str] = program.pop()
      elif inst.opcode == INST_LOAD:
        # print "LOAD"
        program.push(
            program.stack[program.current_frame().slot_start + inst.operand_int + 1])
      elif inst.opcode == INST_LOAD_GLOBAL:
        # print "LOAD_GLOBAL"
        if inst.operand_str in program.global_vars:
          program.push(program.global_vars[inst.operand_str])
        else:
          raise UnboundVariable(
              u"변수 '%s'을(를) 찾을 수 없습니다." % inst.operand_str)

      elif inst.opcode == INST_CALL:
        # print "CALL"
        callee = program.peek(inst.operand_int + 1)

        if callee.type == TYPE_FUNC:
          func_object = callee.funcval

          if func_object.arity != inst.operand_int:
            raise ArgNumberMismatch(
                u"이 함수 %d개의 인수를 받지만 %d개의 인수가 주어졌습니다." % (func_object.arity, inst.operand_int))

          new_slot_start = len(program.stack) - inst.operand_int - 1
          program.call_frames.append(
              CallFrame(new_slot_start, func_object.const_table))
          run_code(program, func_object.code)
        elif callee.type == TYPE_BUILTIN:
          func_object = callee.builtinval

          if func_object.arity != inst.operand_int:
            raise ArgNumberMismatch(
                u"이 함수 %d개의 인수를 받지만 %d개의 인수가 주어졌습니다." % (func_object.arity, inst.operand_int))

          args = []
          for _ in range(inst.operand_int):
            args.insert(0, program.pop())

          return_val = func_object.func(args)
          program.push(return_val)
        else:
          raise NotCallable(
              u"%s 타입의 값은 호출 가능하지 않습니다." % get_type_name(callee.type))
      elif inst.opcode == INST_JMP_FORWARD:
        # print "JMPFORWARD"
        pc += inst.operand_int + 1
        continue
      elif inst.opcode == INST_JMP_BACKWARD:
        # print "JMPBACKWARD"
        pc -= inst.operand_int
        jitdriver.can_enter_jit(pc=pc, code=code, program=program)
        continue
      elif inst.opcode == INST_POP_JMP_IF_FALSE:
        # print "POPJMPIFFALSE"
        value = program.pop()
        if value.type != TYPE_BOOLEAN:
          raise InvalidType(u"여기에는 참 또는 거짓 타입을 필요로 합니다.")

        if value.boolval == False:
          pc += inst.operand_int + 1
          continue
      elif inst.opcode == INST_RETURN:
        # print "RETURN"
        if len(program.call_frames) <= 1:
          raise CannotReturn(u"여기에서는 값을 반환할 수 없습니다.")

        return_value = program.pop()
        for _ in range(len(program.stack) - program.current_frame().slot_start):
          program.pop()

        program.call_frames.pop()
        program.push(return_value)
        break
      elif inst.opcode == INST_BUILD_LIST:
        list_value = []

        for _ in range(inst.operand_int):
          list_value.insert(0, program.pop())

        program.push(ConstList(list_value))
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
