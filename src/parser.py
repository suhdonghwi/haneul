import math

from rpython.rlib.rstruct.runpack import runpack
from rpython.rlib.rarithmetic import intmask

from instruction import *
from constant import *
from dump import dump_constant, dump_inst
from interpreter import BytecodeInterpreter


def bytes_to_int(bytes):
  result = 0
  for b in bytes:
    result = result * 256 + int(b)
  return result


class BytecodeParser:
  def __init__(self, code):
    self.code = str(code)
    self.pos = 0

  def consume_raw(self, offset=1):
    consumed = self.code[self.pos:self.pos+offset]
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
    is_bigint = self.consume_ubyte()
    if is_bigint == 0:
      data = self.consume_int()
      return ConstInteger(data)
    else:
      sign = self.consume_byte()
      bytes_count = self.consume_ulonglong()
      data = list(self.consume_raw(bytes_count))
      data.reverse()
      value = ConstInteger(bytes_to_int(data))
      return value if sign == 1 else value.negate()

  def parse_double(self):
    base = self.parse_integer().intval
    exp = self.consume_longlong()
    return ConstDouble(math.pow(base * 2, exp))

  def parse_char(self):
    head = self.consume_ubyte()
    head_chr = chr(head)
    result = ''

    if head < 0x80:
      result = str(head_chr).decode('utf-8')
    elif head < 0xe0:
      result = (head_chr + self.consume_raw(1)).decode('utf-8')
    elif head < 0xf0:
      result = (head_chr + self.consume_raw(2)).decode('utf-8')
    else:
      result = (head_chr + self.consume_raw(3)).decode('utf-8')

    return ConstChar(result)

  def parse_string(self):
    count = self.consume_ulonglong()

    result = u''
    for i in range(0, count):
      result += self.parse_char().charval

    return result

  def parse_boolean(self):
    value = self.consume_ubyte()
    return ConstBoolean(value == 1)

  def parse_instruction(self):
    line_number = self.consume_uint()
    opcode = self.consume_ubyte()

    inst = Instruction(line_number, opcode)
    if opcode in [INST_PUSH, INST_STORE, INST_LOAD, INST_CALL, INST_JMP_FORWARD, INST_POP_JMP_IF_FALSE]:
      inst.operand_int = self.consume_int()
    elif opcode in [INST_STORE_GLOBAL, INST_LOAD_GLOBAL]:
      inst.operand_str = self.parse_string()

    return inst

  def parse_constant_list(self):
    count = self.consume_ulonglong()

    result = []
    for i in range(count):
      const_type = self.consume_ubyte()

      if const_type == 0:
        result.append(self.parse_integer())
      elif const_type == 1:
        result.append(self.parse_double())
      elif const_type == 2:
        result.append(self.parse_char())
      elif const_type == 3:
        result.append(self.parse_boolean())
      elif const_type == 4:
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

  def parse_funcobject(self):
    arity = self.consume_ushort()
    insts = self.parse_instruction_list()
    const_table = self.parse_constant_list()
    var_names = self.parse_string_list()

    return ConstFunc(FuncObject(arity, insts, const_table, var_names))

  def parse_buildinternal(self):
    const_table = self.parse_constant_list()
    print "YEP ITS OVER_-----------------"
    var_names = self.parse_string_list()

    return (const_table, var_names)

  def parse_code(self):
    (const_table, var_names) = self.parse_buildinternal()
    code = self.parse_instruction_list()

    return (const_table, var_names, code)


parser = BytecodeParser(
    b'\x00\x00\x00\x00\x00\x00\x00\x02\x04\x00\x01\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x02\x03\x00\x00\x00\x00\x00\x00\x00\x01\xea\xb0\x92\x00\x00\x00\x03\x04\x00\x00\x00\x00\x00\x00\x00\x03\x05\x00\x00\x00\x00\x00\x00\x00\x01\xea\xb0\x92\x00\x00\x00\x03\x0a\x00\x00\x00\x03\x09\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\xec\x88\x98\x00\x00\x00\x00\x00\x0a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x03\x00\x00\x00\x00\x00\x00\x00\x03\xed\x85\x8c\xec\x8a\xa4\xed\x8a\xb8\x00\x00\x00\x05\x05\x00\x00\x00\x00\x00\x00\x00\x03\xed\x85\x8c\xec\x8a\xa4\xed\x8a\xb8\x00\x00\x00\x05\x00\x00\x00\x00\x01\x00\x00\x00\x05\x06\x00\x00\x00\x01\x00\x00\x00\x05\x01'
)
(const_table, var_names, code) = parser.parse_code()

print "\n# Bytecode parsing result: "
print "[const table]"
for constant in const_table:
  dump_constant(constant)
print "[var names]"
for name in var_names:
  print name + "."
print "[code]"
for inst in code:
  dump_inst(inst)

interpreter = BytecodeInterpreter(const_table)
interpreter.run(code)
