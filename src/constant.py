# -*- coding: utf-8 -*-

from error import TypeError

types = ['NONE', 'INTEGER', 'REAL', 'STRING', 'BOOLEAN', 'FUNC']
for (i, typename) in enumerate(types):
  globals()['TYPE_' + typename] = i


def get_type_name(t):
  if t == TYPE_INTEGER:
    return u"정수"
  elif t == TYPE_REAL:
    return u"실수"
  elif t == TYPE_STRING:
    return u"문자열"
  elif t == TYPE_BOOLEAN:
    return u"참 또는 거짓"
  elif t == TYPE_FUNC:
    return u"함수"
  else:
    return u"(없음)"


def binary_typeerror(type1, type2, operation):
  raise TypeError(u"%s 타입의 값과 %s 타입의 값은 %s 연산을 지원하지 않습니다." %
                  (get_type_name(type1), get_type_name(type2), operation))


def unary_typeerror(type1, operation):
  raise TypeError(u"%s 타입의 값은 %s 연산을 지원하지 않습니다." %
                  (get_type_name(type1), operation))


class Constant:
  def add(self, other):
    binary_typeerror(self.type, other.type, u"더하기")

  def subtract(self, other):
    binary_typeerror(self.type, other.type, u"빼기")

  def multiply(self, other):
    binary_typeerror(self.type, other.type, u"곱하기")

  def divide(self, other):
    binary_typeerror(self.type, other.type, u"나누기")

  def mod(self, other):
    binary_typeerror(self.type, other.type, u"나머지")

  def equal(self, other):
    binary_typeerror(self.type, other.type, u"비교")

  def less_than(self, other):
    binary_typeerror(self.type, other.type, u"대소 비교")

  def greater_than(self, other):
    binary_typeerror(self.type, other.type, u"대소 비교")

  def negate(self):
    unary_typeerror(self.type, u"반전")


class ConstNone(Constant):
  def __init__(self):
    self.type = TYPE_NONE

  def equal(self, other):
    if other.type == TYPE_NONE:
      return ConstBoolean(True)
    else:
      return ConstBoolean(False)


class ConstInteger(Constant):
  def __init__(self, value):
    self.intval = value
    self.type = TYPE_INTEGER

  def add(self, other):
    if other.type == TYPE_INTEGER:
      return ConstInteger(self.intval + other.intval)
    elif other.type == TYPE_REAL:
      return ConstDouble(self.intval + other.doubleval)
    else:
      binary_typeerror(self.type, other.type, u"더하기")

  def subtract(self, other):
    if other.type == TYPE_INTEGER:
      return ConstInteger(self.intval - other.intval)
    elif other.type == TYPE_REAL:
      return ConstDouble(self.intval - other.doubleval)
    else:
      binary_typeerror(self.type, other.type, u"빼기")

  def multiply(self, other):
    if other.type == TYPE_INTEGER:
      return ConstInteger(self.intval * other.intval)
    elif other.type == TYPE_REAL:
      return ConstDouble(self.intval * other.doubleval)
    else:
      binary_typeerror(self.type, other.type, u"곱하기")

  def divide(self, other):
    if other.type == TYPE_INTEGER:
      return ConstInteger(self.intval / other.intval)
    elif other.type == TYPE_REAL:
      return ConstDouble(self.intval / other.doubleval)
    else:
      binary_typeerror(self.type, other.type, u"나누기")

  def mod(self, other):
    if other.type == TYPE_INTEGER:
      return ConstInteger(self.intval % other.intval)
    else:
      binary_typeerror(self.type, other.type, u"나머지")

  def equal(self, other):
    if other.type == TYPE_INTEGER:
      return ConstBoolean(self.intval == other.intval)
    else:
      return ConstBoolean(False)

  def less_than(self, other):
    if other.type == TYPE_INTEGER:
      return ConstBoolean(self.intval < other.intval)
    elif other.type == TYPE_REAL:
      return ConstBoolean(self.intval < other.doubleval)
    else:
      binary_typeerror(self.type, other.type, u"대소 비교")

  def greater_than(self, other):
    if other.type == TYPE_INTEGER:
      return ConstBoolean(self.intval > other.intval)
    elif other.type == TYPE_REAL:
      return ConstBoolean(self.intval > other.doubleval)
    else:
      binary_typeerror(self.type, other.type, u"대소 비교")

  def negate(self):
    return ConstInteger(-self.intval)


class ConstDouble(Constant):
  def __init__(self, value):
    self.doubleval = value
    self.type = TYPE_REAL

  def add(self, other):
    if other.type == TYPE_INTEGER:
      return ConstDouble(self.doubleval + other.intval)
    elif other.type == TYPE_REAL:
      return ConstDouble(self.doubleval + other.doubleval)
    else:
      binary_typeerror(self.type, other.type, u"더하기")

  def subtract(self, other):
    if other.type == TYPE_INTEGER:
      return ConstDouble(self.doubleval - other.intval)
    elif other.type == TYPE_REAL:
      return ConstDouble(self.doubleval - other.doubleval)
    else:
      binary_typeerror(self.type, other.type, u"빼기")

  def multiply(self, other):
    if other.type == TYPE_INTEGER:
      return ConstDouble(self.doubleval * other.intval)
    elif other.type == TYPE_REAL:
      return ConstDouble(self.doubleval * other.doubleval)
    else:
      binary_typeerror(self.type, other.type, u"곱하기")

  def divide(self, other):
    if other.type == TYPE_INTEGER:
      return ConstDouble(self.doubleval / other.intval)
    elif other.type == TYPE_REAL:
      return ConstDouble(self.doubleval / other.doubleval)
    else:
      binary_typeerror(self.type, other.type, u"나누기")

  def equal(self, other):
    if other.type == TYPE_REAL:
      return ConstBoolean(self.doubleval == other.doubleval)
    else:
      return ConstBoolean(False)

  def less_than(self, other):
    if other.type == TYPE_INTEGER:
      return ConstBoolean(self.doubleval < other.intval)
    elif other.type == TYPE_REAL:
      return ConstBoolean(self.doubleval < other.doubleval)
    else:
      binary_typeerror(self.type, other.type, u"대소 비교")

  def greater_than(self, other):
    if other.type == TYPE_INTEGER:
      return ConstBoolean(self.doubleval > other.intval)
    elif other.type == TYPE_REAL:
      return ConstBoolean(self.doubleval > other.doubleval)
    else:
      binary_typeerror(self.type, other.type, u"대소 비교")


class ConstBoolean(Constant):
  def __init__(self, value):
    self.boolval = value
    self.type = TYPE_BOOLEAN

  def equal(self, other):
    if other.type == TYPE_BOOLEAN:
      return ConstBoolean(self.boolval == other.boolval)
    else:
      return ConstBoolean(False)

  def negate(self):
    return ConstBoolean(not self.boolval)


class ConstString(Constant):
  def __init__(self, value):
    self.stringval = value
    self.type = TYPE_STRING

  def equal(self, other):
    if other.type == TYPE_STRING:
      return ConstBoolean(self.stringval == other.stringval)
    else:
      return ConstBoolean(False)


class ConstFunc(Constant):
  def __init__(self, value):
    self.funcval = value
    self.type = TYPE_FUNC


class FuncObject:
  def __init__(self, arity, code, const_table, var_names):
    self.arity = arity
    self.code = code
    self.const_table = const_table
    self.var_names = var_names
