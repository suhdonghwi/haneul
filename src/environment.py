# -*- coding: utf-8 -*-
from constant import ConstFunc, ConstNone


def print_builtin_func(args):
  print args[0].show().encode('utf-8')
  return ConstNone()


print_builtin = ConstFunc([(u"을", None)], None, print_builtin_func)
default_globals = {u"보여주다": print_builtin}
