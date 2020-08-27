# -*- coding: utf-8 -*-


class HaneulError(Exception):
  def __init__(self, message):
    self.message = message
    self.error_line = 0


class InvalidType(HaneulError):
  def __init__(self, expected, given):
    HaneulError.__init__(self, u"%s 타입의 값을 받아야하는데 %s 타입의 값이 주어졌습니다." % (expected, given))


class UnboundVariable(HaneulError):
  def __init__(self, name):
    HaneulError.__init__(self, u"변수 '%s'를 찾을 수 없습니다." % name)


class UnboundJosa(HaneulError):
  def __init__(self, name):
    HaneulError.__init__(self, u"조사 '%s'를 찾을 수 없습니다." % name)


class UndefinedFunction(HaneulError):
  def __init__(self):
    HaneulError.__init__(self, u"선언은 되었으나 정의되지 않은 함수를 호출할 수 없습니다.")

class UndefinedStruct(HaneulError):
  def __init__(self, name):
    HaneulError.__init__(self, u"구조체 '%s'를 찾을 수 없습니다." % name)

class UnknownField(HaneulError):
  def __init__(self, field):
    HaneulError.__init__(self, u"'%s'라는 필드를 찾을 수 없습니다." % field)

class FieldNumberMismatch(HaneulError):
  def __init__(self, expected, given):
    HaneulError.__init__(self, u"구조체에 %d개의 필드가 있는데 %d가 주어졌습니다." % (expected, given))

class DivideByZero(HaneulError):
  def __init__(self):
    HaneulError.__init__(self, u"0으로 나눌 수 없습니다.")

class BinaryTypeError(HaneulError):
  def __init__(self, lhs, rhs, operation):
    HaneulError.__init__(self, u"%s 타입의 값과 %s 타입의 값은 %s 연산을 지원하지 않습니다." % (lhs.type_name(), rhs.type_name(), operation))

class UnaryTypeError(HaneulError):
  def __init__(self, value, operation):
    HaneulError.__init__(self, u"%s 타입의 값은 %s 연산을 지원하지 않습니다." % (value.type_name(), operation))
