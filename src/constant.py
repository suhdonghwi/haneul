# -*- coding: utf-8 -*-
from rpython.rlib import jit

from error import *


class Constant:
  _attrs_ = []

  def add(self, other):
    raise BinaryTypeError(self, other, u"더하기")

  def subtract(self, other):
    raise BinaryTypeError(self, other, u"빼기")

  def multiply(self, other):
    raise BinaryTypeError(self, other, u"곱하기")

  def divide(self, other):
    raise BinaryTypeError(self, other, u"나누기")

  def mod(self, other):
    raise BinaryTypeError(self, other, u"나머지")

  def equal(self, other):
    raise BinaryTypeError(self, other, u"비교")

  def less_than(self, other):
    raise BinaryTypeError(self, other, u"대소 비교")

  def greater_than(self, other):
    raise BinaryTypeError(self, other, u"대소 비교")

  def negate(self):
    raise UnaryTypeError(self, u"부호 반전")

  def logic_not(self):
    raise UnaryTypeError(self, u"논리 부정")

  def logic_and(self, other):
    raise BinaryTypeError(self, other, u"그리고")

  def logic_or(self, other):
    raise BinaryTypeError(self, other, u"또는")

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
      raise BinaryTypeError(self, other, u"더하기")

  def subtract(self, other):
    if isinstance(other, ConstInteger):
      return ConstInteger(self.intval - other.intval)
    elif isinstance(other, ConstReal):
      return ConstReal(self.intval - other.doubleval)
    else:
      raise BinaryTypeError(self, other, u"빼기")

  def multiply(self, other):
    if isinstance(other, ConstInteger):
      return ConstInteger(self.intval * other.intval)
    elif isinstance(other, ConstReal):
      return ConstReal(self.intval * other.doubleval)
    else:
      raise BinaryTypeError(self, other, u"곱하기")

  def divide(self, other):
    if isinstance(other, ConstInteger):
      if other.intval == 0:
        raise DivideByZero()
      return ConstInteger(self.intval / other.intval)
    elif isinstance(other, ConstReal):
      if other.doubleval == 0:
        raise DivideByZero()
      return ConstReal(self.intval / other.doubleval)
    else:
      raise BinaryTypeError(self, other, u"나누기")

  def mod(self, other):
    if isinstance(other, ConstInteger):
      if other.intval == 0:
        raise DivideByZero()
      return ConstInteger(self.intval % other.intval)
    else:
      raise BinaryTypeError(self, other, u"나머지")

  def equal(self, other):
    if isinstance(other, ConstInteger):
      return ConstBoolean(self.intval == other.intval)
    elif isinstance(other, ConstReal):
      return ConstBoolean(self.intval == other.doubleval)
    else:
      return ConstBoolean(False)

  def less_than(self, other):
    if isinstance(other, ConstInteger):
      return ConstBoolean(self.intval < other.intval)
    elif isinstance(other, ConstReal):
      return ConstBoolean(self.intval < other.doubleval)
    else:
      raise BinaryTypeError(self, other, u"대소 비교")

  def greater_than(self, other):
    if isinstance(other, ConstInteger):
      return ConstBoolean(self.intval > other.intval)
    elif isinstance(other, ConstReal):
      return ConstBoolean(self.intval > other.doubleval)
    else:
      raise BinaryTypeError(self, other, u"대소 비교")

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
      raise BinaryTypeError(self, other, u"더하기")

  def subtract(self, other):
    if isinstance(other, ConstInteger):
      return ConstReal(self.doubleval - other.intval)
    elif isinstance(other, ConstReal):
      return ConstReal(self.doubleval - other.doubleval)
    else:
      raise BinaryTypeError(self, other, u"빼기")

  def multiply(self, other):
    if isinstance(other, ConstInteger):
      return ConstReal(self.doubleval * other.intval)
    elif isinstance(other, ConstReal):
      return ConstReal(self.doubleval * other.doubleval)
    else:
      raise BinaryTypeError(self, other, u"곱하기")

  def divide(self, other):
    if isinstance(other, ConstInteger):
      if other.intval == 0:
        raise DivideByZero()
      return ConstReal(self.doubleval / other.intval)
    elif isinstance(other, ConstReal):
      if other.doubleval == 0:
        raise DivideByZero()
      return ConstReal(self.doubleval / other.doubleval)
    else:
      raise BinaryTypeError(self, other, u"나누기")

  def equal(self, other):
    if isinstance(other, ConstReal):
      return ConstBoolean(self.doubleval == other.doubleval)
    elif isinstance(other, ConstInteger):
      return ConstBoolean(self.doubleval == other.intval)
    else:
      return ConstBoolean(False)

  def less_than(self, other):
    if isinstance(other, ConstInteger):
      return ConstBoolean(self.doubleval < other.intval)
    elif isinstance(other, ConstReal):
      return ConstBoolean(self.doubleval < other.doubleval)
    else:
      raise BinaryTypeError(self, other, u"대소 비교")

  def greater_than(self, other):
    if isinstance(other, ConstInteger):
      return ConstBoolean(self.doubleval > other.intval)
    elif isinstance(other, ConstReal):
      return ConstBoolean(self.doubleval > other.doubleval)
    else:
      raise BinaryTypeError(self, other, u"대소 비교")

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
      raise BinaryTypeError(self, other, u"그리고")

  def logic_or(self, other):
    if isinstance(other, ConstBoolean):
      return ConstBoolean(self.boolval or other.boolval)
    else:
        raise BinaryTypeError(self, other, u"또는")

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
    return u"'" + self.charval + u"'"

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

class ConstStruct(Constant):
  _attrs_ = _immutable_fields_ = ['struct_data']

  def __init__(self, struct_data):
    self.struct_data = struct_data

  def equal(self, other):
    if isinstance(other, ConstStruct):
      if len(self.struct_data) == len(other.struct_data):
        for k in self.struct_data.keys():
          try:
            if not self.struct_data[k].equal(other.struct_data[k]).boolval:
              return ConstBoolean(False)
          except:
            return ConstBoolean(False)
        
        return ConstBoolean(True)
    else:
      return ConstBoolean(False)

  def show(self):
    result = u"{"
    items = self.struct_data.items()
    for (k, v) in items[:-1]:
      result += k + u": " + v.show() + u", "
    (k, v) = items[-1]
    result += k + u": " + v.show() + u"}"

    return result

  def type_name(self):
    return u"구조체"

  def copy(self):
    return ConstStruct(self.struct_data)
  
  def get_field(self, field):
    try:
      return self.struct_data[field]
    except KeyError:
      raise UnknownField(field)

class CodeObject:
  _attrs_ = _immutable_fields_ = [
      'var_names', 'const_table', 'name', 'file_path', 'code', 'local_number', 'stack_size', 'line_no', 'line_no_table', 'free_vars'
  ]

  def __init__(self, var_names, const_table, name, file_path, code, local_number, stack_size, line_no, line_no_table, free_vars=[]):
    self.var_names = var_names
    self.const_table = const_table
    self.name = name
    self.file_path = file_path
    self.code = code
    self.local_number = local_number
    self.stack_size = stack_size
    self.line_no = line_no
    self.line_no_table = line_no_table
    self.free_vars = free_vars

  @jit.elidable
  def get_constant(self, index):
    return self.const_table[index]
  
  def calculate_pos(self, pc):
    line = self.line_no
    path = self.file_path

    for (inst_offset, line_info) in self.line_no_table:
      if pc >= inst_offset:
        if line_info.file_path is None:
          line = line_info.line
        else:
          path = line_info.file_path

      else:
        break
    
    assert path is not None
    return (line, path)

  def copy(self):
    return CodeObject(self.var_names,
                      self.const_table,
                      self.name,
                      self.file_path,
                      self.code,
                      self.local_number,
                      self.stack_size,
                      self.line_no,
                      self.line_no_table,
                      list(self.free_vars))


class BuiltinObject:
  _attrs_ = _immutable_fields_ = ['func']

  def __init__(self, func):
    self.func = func

def list_to_struct(lst):
  if len(lst) == 0:
    return ConstNone()
  else:
    return ConstStruct({u'첫번째': lst[0], u'나머지': list_to_struct(lst[1:])})

def collect_string(lst):
  if isinstance(lst, ConstNone):
    return u''
  elif isinstance(lst, ConstStruct):
    fst = lst.get_field(u'첫번째')
    if isinstance(fst, ConstChar):
      return fst.charval + collect_string(lst.get_field(u'나머지'))
    else:
      raise InvalidType(u'문자', fst.type_name())
  else:
    raise InvalidType(u'구조체', lst.type_name())
