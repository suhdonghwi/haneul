# -*- coding: utf-8 -*-
from rpython.rlib import jit

from error import InvalidType, DivideByZero, binary_typeerror, unary_typeerror


class Constant:
  _attrs_ = []

  def add(self, other):
    binary_typeerror(self, other, u"더하기")

  def subtract(self, other):
    binary_typeerror(self, other, u"빼기")

  def multiply(self, other):
    binary_typeerror(self, other, u"곱하기")

  def divide(self, other):
    binary_typeerror(self, other, u"나누기")

  def mod(self, other):
    binary_typeerror(self, other, u"나머지")

  def equal(self, other):
    binary_typeerror(self, other, u"비교")

  def less_than(self, other):
    binary_typeerror(self, other, u"대소 비교")

  def greater_than(self, other):
    binary_typeerror(self, other, u"대소 비교")

  def negate(self):
    unary_typeerror(self, u"부호 반전")

  def logic_not(self):
    unary_typeerror(self, u"논리 부정")

  def logic_and(self, other):
    binary_typeerror(self, other, u"그리고")

  def logic_or(self, other):
    binary_typeerror(self, other, u"또는")

  def show(self):
    raise NotImplementedError()

  def type_name(self):
    raise NotImplementedError()


class ConstNone(Constant):
  def equal(self, other):
    if isinstance(other, ConstNone):
      return ConstBoolean(True)
    else:
      return ConstBoolean(False)

  def show(self):
    return u"(없음)"

  def type_name(self):
    return u"(없음)"


class ConstInteger(Constant):
  _attrs_ = _immutable_fields_ = ['intval']

  def __init__(self, value):
    self.intval = value

  def add(self, other):
    if isinstance(other, ConstInteger):
      return ConstInteger(self.intval + other.intval)
    elif isinstance(other, ConstReal):
      return ConstReal(self.intval + other.doubleval)
    else:
      binary_typeerror(self, other, u"더하기")

  def subtract(self, other):
    if isinstance(other, ConstInteger):
      return ConstInteger(self.intval - other.intval)
    elif isinstance(other, ConstReal):
      return ConstReal(self.intval - other.doubleval)
    else:
      binary_typeerror(self, other, u"빼기")

  def multiply(self, other):
    if isinstance(other, ConstInteger):
      return ConstInteger(self.intval * other.intval)
    elif isinstance(other, ConstReal):
      return ConstReal(self.intval * other.doubleval)
    else:
      binary_typeerror(self, other, u"곱하기")

  def divide(self, other):
    if isinstance(other, ConstInteger):
      if other.intval == 0:
        raise DivideByZero(u"0으로 나눌 수 없습니다.")
      return ConstInteger(self.intval / other.intval)
    elif isinstance(other, ConstReal):
      if other.doubleval == 0:
        raise DivideByZero(u"0으로 나눌 수 없습니다.")
      return ConstReal(self.intval / other.doubleval)
    else:
      binary_typeerror(self, other, u"나누기")

  def mod(self, other):
    if isinstance(other, ConstInteger):
      if other.intval == 0:
        raise DivideByZero(u"0으로 나눌 수 없습니다.")
      return ConstInteger(self.intval % other.intval)
    else:
      binary_typeerror(self, other, u"나머지")

  def equal(self, other):
    if isinstance(other, ConstInteger):
      return ConstBoolean(self.intval == other.intval)
    else:
      return ConstBoolean(False)

  def less_than(self, other):
    if isinstance(other, ConstInteger):
      return ConstBoolean(self.intval < other.intval)
    elif isinstance(other, ConstReal):
      return ConstBoolean(self.intval < other.doubleval)
    else:
      binary_typeerror(self, other, u"대소 비교")

  def greater_than(self, other):
    if isinstance(other, ConstInteger):
      return ConstBoolean(self.intval > other.intval)
    elif isinstance(other, ConstReal):
      return ConstBoolean(self.intval > other.doubleval)
    else:
      binary_typeerror(self, other, u"대소 비교")

  def negate(self):
    return ConstInteger(-self.intval)

  def show(self):
    return str(self.intval).decode('utf-8')

  def type_name(self):
    return u"정수"


class ConstReal(Constant):
  _attrs_ = _immutable_fields_ = ['doubleval']

  def __init__(self, value):
    self.doubleval = value

  def add(self, other):
    if isinstance(other, ConstInteger):
      return ConstReal(self.doubleval + other.intval)
    elif isinstance(other, ConstReal):
      return ConstReal(self.doubleval + other.doubleval)
    else:
      binary_typeerror(self, other, u"더하기")

  def subtract(self, other):
    if isinstance(other, ConstInteger):
      return ConstReal(self.doubleval - other.intval)
    elif isinstance(other, ConstReal):
      return ConstReal(self.doubleval - other.doubleval)
    else:
      binary_typeerror(self, other, u"빼기")

  def multiply(self, other):
    if isinstance(other, ConstInteger):
      return ConstReal(self.doubleval * other.intval)
    elif isinstance(other, ConstReal):
      return ConstReal(self.doubleval * other.doubleval)
    else:
      binary_typeerror(self, other, u"곱하기")

  def divide(self, other):
    if isinstance(other, ConstInteger):
      if other.intval == 0:
        raise DivideByZero(u"0으로 나눌 수 없습니다.")
      return ConstReal(self.doubleval / other.intval)
    elif isinstance(other, ConstReal):
      if other.doubleval == 0:
        raise DivideByZero(u"0으로 나눌 수 없습니다.")
      return ConstReal(self.doubleval / other.doubleval)
    else:
      binary_typeerror(self, other, u"나누기")

  def equal(self, other):
    if isinstance(other, ConstReal):
      return ConstBoolean(self.doubleval == other.doubleval)
    else:
      return ConstBoolean(False)

  def less_than(self, other):
    if isinstance(other, ConstInteger):
      return ConstBoolean(self.doubleval < other.intval)
    elif isinstance(other, ConstReal):
      return ConstBoolean(self.doubleval < other.doubleval)
    else:
      binary_typeerror(self, other, u"대소 비교")

  def greater_than(self, other):
    if isinstance(other, ConstInteger):
      return ConstBoolean(self.doubleval > other.intval)
    elif isinstance(other, ConstReal):
      return ConstBoolean(self.doubleval > other.doubleval)
    else:
      binary_typeerror(self, other, u"대소 비교")

  def show(self):
    return str(self.doubleval).decode('utf-8')

  def type_name(self):
    return u"실수"


class ConstBoolean(Constant):
  _attrs_ = _immutable_fields_ = ['boolval']

  def __init__(self, value):
    self.boolval = value

  def equal(self, other):
    if isinstance(other, ConstBoolean):
      return ConstBoolean(self.boolval == other.boolval)
    else:
      return ConstBoolean(False)

  def logic_not(self):
    return ConstBoolean(not self.boolval)

  def logic_and(self, other):
    if isinstance(other, ConstBoolean):
      return ConstBoolean(self.boolval and other.boolval)
    else:
      binary_typeerror(self, other, u"그리고")

  def logic_or(self, other):
    if isinstance(other, ConstBoolean):
      return ConstBoolean(self.boolval or other.boolval)
    else:
      binary_typeerror(self, other, u"그리고")

  def show(self):
    return u"참" if self.boolval else u"거짓"

  def type_name(self):
    return u"부울"


class ConstChar(Constant):
  _attrs_ = _immutable_fields_ = ['charval']

  def __init__(self, value):
    self.charval = value

  def equal(self, other):
    if isinstance(other, ConstChar):
      return ConstBoolean(self.charval == other.charval)
    else:
      return ConstBoolean(False)

  def show(self):
    return self.charval

  def type_name(self):
    return u"문자"


class ConstFunc(Constant):
  _attrs_ = _immutable_fields_ = ['funcval', 'builtinval', 'josa_map']

  def __init__(self, josa_map, value, builtin_func=None):
    self.josa_map = josa_map
    self.funcval = value
    self.builtinval = builtin_func

  def show(self):
    return u"(함수)"

  def type_name(self):
    return u"함수"

  def copy(self):
    func = ConstFunc(self.josa_map, self.funcval.copy(), self.builtinval)
    return func


class CodeObject:
  _attrs_ = _immutable_fields_ = [
      'var_names', 'const_table', 'code', 'local_number', 'stack_size', 'free_vars']

  def __init__(self, var_names, const_table, code, local_number, stack_size, free_vars=[]):
    self.var_names = var_names
    self.const_table = const_table
    self.code = code
    self.local_number = local_number
    self.stack_size = stack_size
    self.free_vars = free_vars

  @jit.elidable
  def get_constant(self, index):
    return self.const_table[index]

  def copy(self):
    return CodeObject(self.var_names,
                      self.const_table,
                      self.code,
                      self.local_number,
                      self.stack_size,
                      list(self.free_vars))


class BuiltinObject:
  _attrs_ = _immutable_fields_ = ['func']

  def __init__(self, func):
    self.func = func
