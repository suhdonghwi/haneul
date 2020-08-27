# -*- coding: utf-8 -*-
from constant import Constant, ConstFunc, ConstNone, ConstChar
from error import InvalidType
import os


def print_builtin_func(args):
  print args[0].show().encode('utf-8')
  return ConstNone()


def print_char_builtin_func(args):
  ch = args[0]
  assert ch is not None
  if isinstance(ch, ConstChar):
    os.write(1, ch.charval.encode('utf-8'))
    return ConstNone()
  else:
    raise InvalidType(u"문자", ch.type_name())


print_builtin = ConstFunc([(u"을", None)], None, print_builtin_func)
print_char_builtin = ConstFunc([(u"을", None)], None, print_char_builtin_func)

default_globals = {
    u"보여주다": print_builtin,
    u"문자로_보여주다": print_char_builtin,
}
default_structs = {}
