# -*- coding: utf-8 -*-
from rpython.rlib import rfile

from constant import Constant, ConstFunc, ConstNone, ConstChar, ConstInteger, list_to_struct, collect_string
from bytecode_parser import BytecodeParser
from error import InvalidType
import os

LINE_BUFFER_LENGTH = 1024

def print_char_builtin_func(args):
  ch = args[0]
  assert ch is not None
  if isinstance(ch, ConstChar):
    os.write(1, ch.charval.encode('utf-8'))
    return ConstNone()
  else:
    raise InvalidType(u"문자", ch.type_name())

def stringize_builtin_func(args):
  l = []
  for ch in args[0].show():
    l.append(ConstChar(ch))

  return list_to_struct(l)

def input_builtin_func(args):
  stdin, stdout, stderr = rfile.create_stdio()
  line = stdin.readline(LINE_BUFFER_LENGTH)
  parser = BytecodeParser(line)

  result = []
  while parser.code[parser.pos] != '\n':
    result.append(parser.parse_char())

  return list_to_struct(result)

def to_integer_builtin_func(args):
  a = args[0]
  s = collect_string(a)
  try:
    return ConstInteger(int(s.encode('utf-8')))
  except:
    return ConstNone()

print_char_builtin = ConstFunc([(u"을", None)], None, print_char_builtin_func)
stringize_builtin = ConstFunc([(u"을", None)], None, stringize_builtin_func)
input_builtin = ConstFunc([], None, input_builtin_func)
to_integer_builtin = ConstFunc([(u"을", None)], None, to_integer_builtin_func)

default_globals = {
    u"문자_출력하다": print_char_builtin,
    u"문자열화하다": stringize_builtin,
    u"입력받다": input_builtin,
    u"정수화하다": to_integer_builtin,
}

