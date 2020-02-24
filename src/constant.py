# -*- coding: utf-8 -*-
from rpython.rlib import jit

from error import InvalidType
from constant_type import *


class Constant:
  _immutable_fields_ = ['intval', 'doubleval', 'boolval',
                        'charval', 'funcval', 'type']

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

  def show(self):
    raise NotImplementedError()


class ConstNone(Constant):
  _immutable_fields_ = ['type']

  def __init__(self):
    self.type = TYPE_NONE

  def equal(self, other):
    if other.type == TYPE_NONE:
      return ConstBoolean(True)
    else:
      return ConstBoolean(False)

  def show(self):
    return u"(없음)"


class ConstInteger(Constant):
  _immutable_fields_ = ['intval', 'type']

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

  def show(self):
    return str(self.intval).decode('utf-8')


class ConstDouble(Constant):
  _immutable_fields_ = ['doubleval', 'type']

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

  def show(self):
    return str(self.doubleval).decode('utf-8')


class ConstBoolean(Constant):
  _immutable_fields_ = ['boolval', 'type']

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

  def show(self):
    return u"참" if self.boolval else u"거짓"


class ConstChar(Constant):
  _immutable_fields_ = ['charval', 'type']

  def __init__(self, value):
    self.charval = value
    self.type = TYPE_CHAR

  def equal(self, other):
    if other.type == TYPE_CHAR:
      return ConstBoolean(self.charval == other.charval)
    else:
      return ConstBoolean(False)

  def show(self):
    return self.charval


class ConstFunc(Constant):
  _immutable_fields_ = ['funcval', 'type']

  def __init__(self, josa_list, value, builtin_func=None):
    self.josa_map = {}
    for josa in josa_list:
      self.josa_map[josa] = None

    self.funcval = value
    self.builtinval = builtin_func
    self.type = TYPE_FUNC

  def show(self):
    return u"(함수)"


class FuncObject:
  _immutable_fields_ = ['code', 'const_table']

  def __init__(self, code, const_table):
    self.code = code
    self.const_table = const_table
    self.free_vars = []  # 실행 시점에 수정될 값이므로 immutable fields에 추가하지 않습니다.


class BuiltinObject:
  _immutable_fields_ = ['func']

  def __init__(self, arity, func):
    self.func = func
