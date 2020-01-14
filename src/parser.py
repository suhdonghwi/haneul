# -*- coding: utf-8 -*-

import math

from rpython.rlib.rstruct.runpack import runpack
from rpython.rlib.rarithmetic import intmask

from instruction import *
from constant import *


def bytes_to_int(data, length):
  result = 0
  for i in range(length):
    result = result * 256 + data[i]
  return result


class BytecodeParser:
  def __init__(self, code):
    self.code = str(code)
    self.pos = 0

  def consume_raw(self, offset=1):
    consumed = self.code[self.pos:self.pos+offset]
    self.pos += offset
    return consumed

  def consume_raw_reverse(self, offset=1):
    consumed = ''
    for i in range(self.pos+offset-1, intmask(self.pos)-1, -1):
      consumed += self.code[i]

    self.pos += offset
    return consumed

  def consume_ubyte(self):
    return runpack(">B", self.consume_raw(1))

  def consume_byte(self):
    return runpack(">b", self.consume_raw(1))

  def consume_ushort(self):
    return runpack(">H", self.consume_raw(2))

  def consume_int(self):
    return runpack(">i", self.consume_raw(4))

  def consume_uint(self):
    return runpack(">I", self.consume_raw(4))

  def consume_longlong(self):
    return runpack(">q", self.consume_raw(8))

  def consume_ulonglong(self):
    return runpack(">Q", self.consume_raw(8))

  def parse_integer(self):
    data = self.consume_longlong()
    return ConstInteger(data)

  def parse_double(self):
    base = self.consume_longlong()
    exp = self.consume_longlong()
    return ConstDouble(base * math.pow(2, exp))

  def parse_char(self):
    head = self.consume_ubyte()
    result = u''

    if head < 0x80:
      result = unichr(head)
    elif head < 0xe0:
      result = (chr(head) + self.consume_raw(1)).decode('utf-8')
    elif head < 0xf0:
      result = (chr(head) + self.consume_raw(2)).decode('utf-8')
    else:
      result = (chr(head) + self.consume_raw(3)).decode('utf-8')

    return ConstString(result)

  def parse_string(self):
    count = self.consume_ulonglong()

    result = u''
    for i in range(count):
      result += self.parse_char().stringval

    return ConstString(result)

  def parse_boolean(self):
    value = self.consume_ubyte()
    return ConstBoolean(value == 1)

  def parse_instruction(self):
    line_number = self.consume_uint()
    opcode = self.consume_ubyte()

    inst = Instruction(line_number, opcode)
    if opcode in [INST_PUSH, INST_STORE, INST_LOAD, INST_CALL, INST_JMP_FORWARD, INST_JMP_BACKWARD, INST_POP_JMP_IF_FALSE]:
      inst.operand_int = self.consume_int()
    elif opcode in [INST_STORE_GLOBAL, INST_LOAD_GLOBAL]:
      inst.operand_str = self.parse_string().stringval

    return inst

  def parse_constant_list(self):
    count = self.consume_ulonglong()

    result = []
    for i in range(count):
      const_type = self.consume_ubyte()

      if const_type == TYPE_NONE:
        result.append(ConstNone())
      elif const_type == TYPE_INTEGER:
        result.append(self.parse_integer())
      elif const_type == TYPE_REAL:
        result.append(self.parse_double())
      elif const_type == TYPE_STRING:
        result.append(self.parse_string())
      elif const_type == TYPE_BOOLEAN:
        result.append(self.parse_boolean())
      elif const_type == TYPE_FUNC:
        result.append(self.parse_funcobject())

    return result

  def parse_instruction_list(self):
    count = self.consume_ulonglong()

    result = []
    for i in range(0, count):
      result.append(self.parse_instruction())

    return result

  def parse_string_list(self):
    count = self.consume_ulonglong()

    result = []
    for i in range(0, count):
      result.append(self.parse_string().stringval)

    return result

  def parse_funcobject(self):
    arity = self.consume_ushort()
    const_table = self.parse_constant_list()
    insts = self.parse_instruction_list()

    return ConstFunc(FuncObject(arity, insts, const_table))

  def parse_code(self):
    const_table = self.parse_constant_list()
    code = self.parse_instruction_list()

    return (const_table, code)


"""
parser = BytecodeParser(
    b'\x00\x00\x00\x00\x00\x00\x00\x04\x00\x05\x00\x01\x00\x00\x00\x00\x00\x00\x00\x03\x00\x01\x00\x00\x00\x00\x02\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x15\x00\x00\x00\x02\x04\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x01\x00\x00\x00\x02\x10\x00\x00\x00\x02\x08\x00\x00\x00\x03\x00\x00\x00\x03\x00\x00\x00\x00\x02\x00\x00\x00\x03\x09\x00\x00\x00\x03\x07\x00\x00\x00\x0c\x00\x00\x00\x05\x05\x00\x00\x00\x00\x00\x00\x00\x0a\xed\x94\xbc\xeb\xb3\xb4\xeb\x82\x98\xec\xb9\x98\x20\xec\x88\x98\x20\xea\xb5\xac\xed\x95\x98\xeb\x8b\xa4\x00\x00\x00\x05\x04\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x02\x00\x00\x00\x05\x0b\x00\x00\x00\x05\x06\x00\x00\x00\x01\x00\x00\x00\x05\x05\x00\x00\x00\x00\x00\x00\x00\x0a\xed\x94\xbc\xeb\xb3\xb4\xeb\x82\x98\xec\xb9\x98\x20\xec\x88\x98\x20\xea\xb5\xac\xed\x95\x98\xeb\x8b\xa4\x00\x00\x00\x05\x04\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x01\x00\x00\x00\x05\x0b\x00\x00\x00\x05\x06\x00\x00\x00\x01\x00\x00\x00\x05\x0a\x00\x00\x00\x05\x09\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x05\x09\x05\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02\x00\x01\x00\x00\x00\x00\x0a\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x08\x04\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x01\x00\x00\x00\x08\x0a\x00\x00\x00\x08\x09\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x08\x09\x01\x00\x00\x00\x00\x28\x00\x00\x00\x00\x00\x00\x00\x0a\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x01\x03\x00\x00\x00\x00\x00\x00\x00\x0a\xed\x94\xbc\xeb\xb3\xb4\xeb\x82\x98\xec\xb9\x98\x20\xec\x88\x98\x20\xea\xb5\xac\xed\x95\x98\xeb\x8b\xa4\x00\x00\x00\x07\x00\x00\x00\x00\x02\x00\x00\x00\x07\x03\x00\x00\x00\x00\x00\x00\x00\x03\xed\x85\x8c\xec\x8a\xa4\xed\x8a\xb8\x00\x00\x00\x0a\x05\x00\x00\x00\x00\x00\x00\x00\x04\xeb\xb3\xb4\xec\x97\xac\xec\xa3\xbc\xeb\x8b\xa4\x00\x00\x00\x0a\x05\x00\x00\x00\x00\x00\x00\x00\x0a\xed\x94\xbc\xeb\xb3\xb4\xeb\x82\x98\xec\xb9\x98\x20\xec\x88\x98\x20\xea\xb5\xac\xed\x95\x98\xeb\x8b\xa4\x00\x00\x00\x0a\x00\x00\x00\x00\x03\x00\x00\x00\x0a\x06\x00\x00\x00\x01\x00\x00\x00\x0a\x06\x00\x00\x00\x01\x00\x00\x00\x0a\x01'
)
(const_table,  code) = parser.parse_code()


def print_builtin_func(args):
  print args[0].stringval
  return ConstNone()


print_builtin = ConstBuiltin(BuiltinObject(1, print_builtin_func))
default_globals = {
    u'보여주다': print_builtin
}

interpreter = BytecodeInterpreter(const_table, default_globals)
interpreter.run(code)
"""
