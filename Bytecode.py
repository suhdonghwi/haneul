from rpython.rlib.rstruct.runpack import runpack


def signed_bytes_to_int(data):
  encoded = str(data).encode('hex')
  return int(encoded, 16)


class BytecodeParser:
  def __init__(self, code):
    self.code = code
    self.pos = 0

  def consume_raw(self, offset=1):
    consumed = b''

    for i in range(0, offset):
      consumed += self.code[self.pos]
      print "Consumed : " + str(ord(self.code[self.pos]))
      self.pos += 1

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
    result = ''
    for i in range(0, count):
      result += self.parse_char()

    return result

  def parse_boolean(self):
    value = self.consume('B')
    return value == 1


parser = BytecodeParser(
    b'\x00\x00\x00\x00\x00\x00\x00\x08\x48\x65\x6c\x6c\x6f\xea\xb0\x80\xeb\x82\x98\xeb\x8b\xa4'
)
print parser.parse_string()
