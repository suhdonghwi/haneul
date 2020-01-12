# -*- coding: utf-8 -*-

import os

from interpreter import BytecodeInterpreter
from parser import BytecodeParser
from error import HaneulError

from constant import ConstBuiltin, ConstNone,  BuiltinObject


def print_builtin_func(args):
  print args[0].stringval.encode('utf-8')
  return ConstNone()


print_builtin = ConstBuiltin(BuiltinObject(1, print_builtin_func))
default_globals = {
    u'보여주다': print_builtin
}


def entry_point(argv):
  try:
    filename = argv[1]
  except IndexError:
    print "Give me the file!"
    return 1

  fp = os.open(filename, os.O_RDONLY, 0777)
  content = ""
  while True:
    read = os.read(fp, 4096)
    if len(read) == 0:
      break
    content += read
  os.close(fp)

  parser = BytecodeParser(content)
  (const_table, var_names, code) = parser.parse_code()

  interpreter = BytecodeInterpreter(const_table, default_globals)
  try:
    interpreter.run(code)
  except HaneulError as e:
    print (u"에러 발생 @ %d : %s" % (e.error_line, e.message)).encode('utf-8')
  return 0


def target(*args):
  return entry_point, None
