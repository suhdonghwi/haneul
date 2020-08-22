# -*- coding: utf-8 -*-


class HaneulError(Exception):
  def __init__(self, message):
    self.message = message
    self.error_line = 0


class InvalidType(HaneulError):
  def __init__(self, message):
    HaneulError.__init__(self, message)


class ArgNumberMismatch(HaneulError):
  def __init__(self, message):
    HaneulError.__init__(self, message)


class UnboundVariable(HaneulError):
  def __init__(self, message):
    HaneulError.__init__(self, message)


class UnboundJosa(HaneulError):
  def __init__(self, message):
    HaneulError.__init__(self, message)


class UndefinedFunction(HaneulError):
  def __init__(self, message):
    HaneulError.__init__(self, message)

class DivideByZero(HaneulError):
  def __init__(self, message):
    HaneulError.__init__(self, message)


def binary_typeerror(lhs, rhs, operation):
  raise InvalidType(u"%s 타입의 값과 %s 타입의 값은 %s 연산을 지원하지 않습니다." %
                    (lhs.type_name(), rhs.type_name(), operation))


def unary_typeerror(value, operation):
  raise InvalidType(u"%s 타입의 값은 %s 연산을 지원하지 않습니다." %
                    (value.type_name(), operation))
