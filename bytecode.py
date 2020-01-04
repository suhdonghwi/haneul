from rpython.rlib.rstruct.runpack import runpack

from instruction import *
from constant import FuncObject


def signed_bytes_to_int(data):
  encoded = str(data).encode('hex')
  return int(encoded, 16)


class BytecodeParser:
  def __init__(self, code):
    self.code = code
    self.pos = 0

  def consume_raw(self, offset=1):
    consumed = b''
    consumed_str = ''

    for i in range(0, offset):
      consumed += self.code[self.pos]
      consumed_str += str(ord(self.code[self.pos])) + ' '
      self.pos += 1

    print "Consumed : " + consumed_str
    return consumed

  def consume(self, fmt, offset=1):
    return runpack(">" + fmt, self.consume_raw(offset))

  def parse_integer(self):
    is_bigint = self.consume('B')
    if is_bigint == 0:
      data = self.consume('i', 4)
      return data
    else:
      sign = self.consume('B')
      bytes_count = self.consume('Q', 8)
      data = self.consume_raw(bytes_count)
      value = signed_bytes_to_int(data[::-1])
      return value if sign == 1 else -value

  def parse_double(self):
    base = self.parse_integer()
    exp = self.consume('q', 8)
    return base * 2 ** exp

  def parse_char(self):
    head = self.consume('B')
    head_chr = chr(head)

    if head < 0x80:
      return head_chr
    elif head < 0xe0:
      return (head_chr + self.consume_raw(1)).decode('utf-8')
    elif head < 0xf0:
      return (head_chr + self.consume_raw(2)).decode('utf-8')
    else:
      return (head_chr + self.consume_raw(3)).decode('utf-8')

  def parse_string(self):
    count = self.consume('Q', 8)
    print "string!!! :: " + str(count)

    result = ''
    for i in range(0, count):
      result += self.parse_char()

    print "it was !!! ::: " + result
    return result

  def parse_boolean(self):
    value = self.consume('B')
    return value == 1

  def parse_list(self, f):
    count = self.consume('Q', 8)
    print "list!!! :: " + str(count)

    result = []
    for i in range(0, count):
      result.append(f())

    return result

  def parse_instruction(self):
    line_number = self.consume('I', 4)
    opcode = self.consume('B')

    if opcode in [INST_PUSH, INST_STORE, INST_LOAD, INST_CALL, INST_JMP_FORWARD, INST_POP_JMP_IF_FALSE]:
      return Instruction(line_number, opcode, self.consume('i', 4))
    else:
      return Instruction(line_number, opcode)

  def parse_constant(self):
    const_type = self.consume('B')

    if const_type == 0:
      return self.parse_integer()
    elif const_type == 1:
      return self.parse_double()
    elif const_type == 2:
      return self.parse_char()
    elif const_type == 3:
      return self.parse_boolean()
    elif const_type == 4:
      return self.parse_funcobject()

  def parse_funcobject(self):
    arity = self.consume('H', 2)
    insts = self.parse_list(self.parse_instruction)
    const_table = self.parse_list(self.parse_constant)
    var_names = self.parse_list(self.parse_string)

    return FuncObject(arity, insts, const_table, var_names)


parser = BytecodeParser(
    b'\x04\x00\x02\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x02\x01\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x0a\x02\x61\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x02\xec\x95\x88\xeb\x85\x95\x00\x00\x00\x00\x00\x00\x00\x06\x77\x61\x73\x73\x75\x70'
)
result = parser.parse_constant()
print result.arity
print result.insts
print result.const_table
print result.var_names
