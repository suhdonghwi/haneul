# -*- coding: utf-8 -*-
import os

from interpreter import Interpreter, CodeObject, Env
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
  func_object = parser.parse_funcobject()

  code_object = func_object.funcval
  interpreter = Interpreter(Env(default_globals))
  try:
    interpreter.run(code_object, [])
  except HaneulError as e:
    for (name, path, line) in reversed(interpreter.stack_trace):
      print (u"파일 '%s', %d번째 줄, %s:" % (path, line, name)).encode('utf-8')

    print e.message.encode('utf-8')

  return 0


def target(*args):
  return entry_point, None


def jitpolicy(driver):
  from rpython.jit.codewriter.policy import JitPolicy
  return JitPolicy()
