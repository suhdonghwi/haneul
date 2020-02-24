# -*- coding: utf-8 -*-
import os

from interpreter import CallFrame, Program
from parser import BytecodeParser
from error import HaneulError
from constant import ConstInteger

from environment import default_globals


def entry_point(argv):
  try:
    filename = argv[1]
  except IndexError:
    print "파일이 필요합니다."
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
  (global_var_names, const_table, code) = parser.parse_code()

  frame = CallFrame(const_table, code, [], 0)
  program = Program(global_var_names, default_globals)
  try:
    program.run(frame)
  except HaneulError as e:
    print (u"%d번째 라인에서 에러 발생 : %s" % (e.error_line, e.message)).encode('utf-8')

  return 0


def target(*args):
  return entry_point, None


def jitpolicy(driver):
  from rpython.jit.codewriter.policy import JitPolicy
  return JitPolicy()
