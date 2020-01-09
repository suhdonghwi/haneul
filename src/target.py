# -*- coding: utf-8 -*-

import os

from interpreter import BytecodeInterpreter
from parser import BytecodeParser
from error import HaneulError


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

  print content
  parser = BytecodeParser(content)
  (const_table, var_names, code) = parser.parse_code()

  interpreter = BytecodeInterpreter(const_table)
  try:
    interpreter.run(code)
  except HaneulError as e:
    print "에러 발생 @ " + str(e.error_line) + " : " + e.message
  return 0


def target(*args):
  return entry_point, None
