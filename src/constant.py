# -*- coding: utf-8 -*-

from error import TypeError

types = ['NONE', 'INT', 'DOUBLE', 'BOOLEAN', 'CHAR', 'FUNC']
for (i, typename) in enumerate(types):
  globals()['TYPE_' + typename] = i


def get_type_name(t):
  if t == TYPE_INT:
    return "정수"
  elif t == TYPE_DOUBLE:
    return "실수"
  elif t == TYPE_BOOLEAN:
    return "참 또는 거짓"
  elif t == TYPE_CHAR:
    return "문자"
  elif t == TYPE_FUNC:
    return "함수"
  else:
    return "(타입 없음)"


def binary_typeerror(type1, type2, operation):
  raise TypeError(get_type_name(type1) + " 타입의 값과 " + get_type_name(type2) + " 타입의 값은 " +
                  operation + " 연산을 지원하지 않습니다.")


def unary_typeerror(type1, operation):
  raise TypeError(get_type_name(type1) + " 타입의 값은 " +
                  operation + " 연산을 지원하지 않습니다.")


class Constant:
  def add(self, other):
    binary_typeerror(self.type, other.type, "더하기")

  def subtract(self, other):
    binary_typeerror(self.type, other.type, "빼기")

  def multiply(self, other):
    binary_typeerror(self.type, other.type, "곱하기")

  def divide(self, other):
    binary_typeerror(self.type, other.type, "나누기")

  def mod(self, other):
    binary_typeerror(self.type, other.type, "나머지")

  def equal(self, other):
    binary_typeerror(self.type, other.type, "비교")

  def less_than(self, other):
    binary_typeerror(self.type, other.type, "대소 비교")

  def greater_than(self, other):
    binary_typeerror(self.type, other.type, "대소 비교")

  def negate(self):
    unary_typeerror(self.type, "반전")


class ConstInteger(Constant):
  def __init__(self, value):
    self.intval = value
    self.type = TYPE_INT

  def add(self, other):
    if other.type == TYPE_INT:
      return ConstInteger(self.intval + other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.intval + other.doubleval)
    else:
      binary_typeerror(self.type, other.type, "더하기")

  def subtract(self, other):
    if other.type == TYPE_INT:
      return ConstInteger(self.intval - other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.intval - other.doubleval)
    else:
      binary_typeerror(self.type, other.type, "빼기")

  def multiply(self, other):
    if other.type == TYPE_INT:
      return ConstInteger(self.intval * other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.intval * other.doubleval)
    else:
      binary_typeerror(self.type, other.type, "곱하기")

  def divide(self, other):
    if other.type == TYPE_INT:
      return ConstInteger(self.intval / other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.intval / other.doubleval)
    else:
      binary_typeerror(self.type, other.type, "나누기")

  def mod(self, other):
    if other.type == TYPE_INT:
      return ConstInteger(self.intval % other.intval)
    else:
      binary_typeerror(self.type, other.type, "나머지")

  def equal(self, other):
    if other.type == TYPE_INT:
      return ConstBoolean(self.intval == other.intval)
    else:
      return ConstBoolean(False)

  def less_than(self, other):
    if other.type == TYPE_INT:
      return ConstBoolean(self.intval < other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstBoolean(self.intval < other.doubleval)
    else:
      binary_typeerror(self.type, other.type, "대소 비교")

  def greater_than(self, other):
    if other.type == TYPE_INT:
      return ConstBoolean(self.intval > other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstBoolean(self.intval > other.doubleval)
    else:
      binary_typeerror(self.type, other.type, "대소 비교")

  def negate(self):
    return ConstInteger(-self.intval)


class ConstDouble(Constant):
  def __init__(self, value):
    self.doubleval = value
    self.type = TYPE_DOUBLE

  def add(self, other):
    if other.type == TYPE_INT:
      return ConstDouble(self.doubleval + other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.doubleval + other.doubleval)
    else:
      binary_typeerror(self.type, other.type, "더하기")

  def subtract(self, other):
    if other.type == TYPE_INT:
      return ConstDouble(self.doubleval - other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.doubleval - other.doubleval)
    else:
      binary_typeerror(self.type, other.type, "빼기")

  def multiply(self, other):
    if other.type == TYPE_INT:
      return ConstDouble(self.doubleval * other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.doubleval * other.doubleval)
    else:
      binary_typeerror(self.type, other.type, "곱하기")

  def divide(self, other):
    if other.type == TYPE_INT:
      return ConstDouble(self.doubleval / other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.doubleval / other.doubleval)
    else:
      binary_typeerror(self.type, other.type, "나누기")

  def equal(self, other):
    if other.type == TYPE_DOUBLE:
      return ConstBoolean(self.doubleval == other.doubleval)
    else:
      return ConstBoolean(False)

  def less_than(self, other):
    if other.type == TYPE_INT:
      return ConstBoolean(self.doubleval < other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstBoolean(self.doubleval < other.doubleval)
    else:
      binary_typeerror(self.type, other.type, "대소 비교")

  def greater_than(self, other):
    if other.type == TYPE_INT:
      return ConstBoolean(self.doubleval > other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstBoolean(self.doubleval > other.doubleval)
    else:
      binary_typeerror(self.type, other.type, "대소 비교")


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


class ConstChar(Constant):
  def __init__(self, value):
    self.charval = value
    self.type = TYPE_CHAR

  def equal(self, other):
    if other.type == TYPE_CHAR:
      return ConstBoolean(self.charval == other.charval)
    else:
      return ConstBoolean(False)

  def less_than(self, other):
    if other.type == TYPE_CHAR:
      return ConstBoolean(self.charval < other.charval)
    else:
      binary_typeerror(self.type, other.type, "대소 비교")

  def greater_than(self, other):
    if other.type == TYPE_CHAR:
      return ConstBoolean(self.charval > other.charval)
    else:
      binary_typeerror(self.type, other.type, "대소 비교")


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
