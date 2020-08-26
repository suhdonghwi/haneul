# -*- coding: utf-8 -*-
import sys
import os
sys.path.append('/Users/suhdonghwi/Documents/utils/pypy')

import math

from instruction import *
from constant import *
from interpreter import *
from environment import default_globals

from rpython.rlib.rarithmetic import intmask
from rpython.rlib.rstruct.runpack import runpack

from target import *

TYPE_NAMES = ['NONE', 'INTEGER', 'REAL', 'CHAR', 'BOOLEAN', 'FUNC']
for (i, typename) in enumerate(TYPE_NAMES):
  globals()['TYPE_' + typename] = i


class BytecodeParser:
  def __init__(self, code):
    self.code = str(code)
    self.pos = 0

  def consume_raw(self, offset=1):
    consumed = self.code[self.pos:self.pos + offset]
    self.pos += offset
    return consumed

  def consume_raw_reverse(self, offset=1):
    consumed = ''
    for i in range(self.pos + offset - 1, intmask(self.pos) - 1, -1):
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

  def consume_double(self):
    return runpack(">d", self.consume_raw(8))

  def parse_integer(self):
    data = self.consume_longlong()
    return ConstInteger(data)

  def parse_double(self):
    data = self.consume_double()
    return ConstReal(data)

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

    return ConstChar(result)

  def parse_string(self):
    count = self.consume_ulonglong()

    result = u''
    for i in range(count):
      result += self.parse_char().charval

    return result

  def parse_string_ubyte(self):
    count = self.consume_ubyte()

    result = u''
    for i in range(count):
      result += self.parse_char().charval

    return result

  def parse_boolean(self):
    value = self.consume_ubyte()
    return ConstBoolean(value == 1)

  def parse_instruction(self):
    opcode = self.consume_ubyte()

    inst = Instruction(opcode)
    if opcode in (INST_PUSH, INST_LOAD_LOCAL, INST_STORE_LOCAL, INST_LOAD_DEREF, INST_STORE_GLOBAL, INST_LOAD_GLOBAL, INST_POP_JMP_IF_FALSE, INST_JMP):
      inst.operand_int = self.consume_uint()
    elif opcode == INST_FREE_VAR:
      inst.operand_free_var_list = self.parse_free_var_list()
    elif opcode == INST_CALL:
      inst.operand_josa_list = self.parse_josa_list()
    elif opcode in (INST_ADD_STRUCT, INST_MAKE_STRUCT):
      inst.operand_str = self.parse_string_ubyte()
      inst.operand_josa_list = self.parse_josa_list()
    elif opcode == INST_GET_FIELD:
      inst.operand_str = self.parse_string_ubyte()


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
      elif const_type == TYPE_CHAR:
        result.append(self.parse_char())
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
      result.append(self.parse_string())

    return result

  def parse_josa_list(self):
    count = self.consume_ubyte()

    result = []
    for i in range(0, count):
      result.append(self.parse_string_ubyte())

    return result

  def parse_free_var_list(self):
    count = self.consume_ubyte()

    result = []
    for i in range(0, count):
      is_free_var = self.consume_ubyte() == 1
      index = self.consume_ubyte()

      result.append((is_free_var, index))

    return result

  def parse_line_no_table(self):
    count = self.consume_ulonglong()

    result = []
    for i in range(0, count):
      inst_offset = self.consume_uint()
      line_diff = self.consume_ushort()
      result.append((inst_offset, line_diff))

    return result

  def parse_funcobject(self):
    josa_list = self.parse_josa_list()
    var_names = self.parse_string_list()
    stack_size = self.consume_ulonglong()
    local_number = self.consume_uint()
    const_table = self.parse_constant_list()
    name = self.parse_string()
    file_path = self.parse_string()
    line_no = self.consume_ushort()
    line_no_table = self.parse_line_no_table()
    insts = self.parse_instruction_list()

    josa_map = []
    for josa in josa_list:
      josa_map.append((josa, None))

    return ConstFunc(josa_map, CodeObject(var_names, const_table, name, file_path, insts, local_number, stack_size, line_no, line_no_table))


if __name__ == "__main__":
  entry_point(sys.argv)
