# -*- coding: utf-8 -*-
from rpython.rlib import jit

from error import InvalidType
from constant_type import *


class Constant:
  _attrs_ = _immutable_fields_ = [
      'intval', 'doubleval', 'boolval', 'charval', 'funcval', 'builtinval', 'josa_map', 'type']

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
  _attrs_ = _immutable_fields_ = ['type']

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
  _attrs_ = _immutable_fields_ = ['intval', 'type']

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
  _attrs_ = _immutable_fields_ = ['doubleval', 'type']

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
  _attrs_ = _immutable_fields_ = ['boolval', 'type']

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
  _attrs_ = _immutable_fields_ = ['charval', 'type']

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
  _attrs_ = _immutable_fields_ = ['funcval', 'builtinval', 'josa_map', 'type']

  def __init__(self, josa_map, value, builtin_func=None):
    self.josa_map = josa_map
    self.funcval = value
    self.builtinval = builtin_func
    self.type = TYPE_FUNC

  def show(self):
    return u"(함수)"

  def copy(self):
    func = ConstFunc(self.josa_map, self.funcval.copy(), self.builtinval)
    return func


class CodeObject:
  _attrs_ = _immutable_fields_ = [
      'const_table', 'code', 'local_number', 'free_vars']

  def __init__(self, const_table, code, local_number, free_vars=[]):
    self.const_table = const_table
    self.code = code
    self.local_number = local_number
    self.free_vars = free_vars

  @jit.elidable
  def get_constant(self, index):
    return self.const_table[index]

  def copy(self):
    return CodeObject(self.const_table, self.code, self.local_number, list(self.free_vars))


class BuiltinObject:
  _attrs_ = _immutable_fields_ = ['func']

  def __init__(self, arity, func):
    self.func = func
