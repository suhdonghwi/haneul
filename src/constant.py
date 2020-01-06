TYPE_NONE = 0
TYPE_INT = 1
TYPE_DOUBLE = 2
TYPE_BOOLEAN = 3
TYPE_CHAR = 4
TYPE_FUNC = 5


class Constant:
  def add(self, other):
    raise Exception("wrong type")

  def subtract(self, other):
    raise Exception("wrong type")

  def multiply(self, other):
    raise Exception("wrong type")

  def divide(self, other):
    raise Exception("wrong type")

  def mod(self, other):
    raise Exception("wrong type")

  def equal(self, other):
    raise Exception("wrong type")

  def less_than(self, other):
    raise Exception("wrong type")

  def negate(self):
    raise Exception("wrong type")


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
      raise Exception("wrong type")

  def subtract(self, other):
    if other.type == TYPE_INT:
      return ConstInteger(self.intval - other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.intval - other.doubleval)
    else:
      raise Exception("wrong type")

  def multiply(self, other):
    if other.type == TYPE_INT:
      return ConstInteger(self.intval * other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.intval * other.doubleval)
    else:
      raise Exception("wrong type")

  def divide(self, other):
    if other.type == TYPE_INT:
      return ConstInteger(self.intval / other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.intval / other.doubleval)
    else:
      raise Exception("wrong type")

  def mod(self, other):
    if other.type == TYPE_INT:
      return ConstInteger(self.intval % other.intval)
    else:
      raise Exception("wrong type")

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
      raise Exception("wrong type")

  def greater_than(self, other):
    if other.type == TYPE_INT:
      return ConstBoolean(self.intval > other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstBoolean(self.intval > other.doubleval)
    else:
      raise Exception("wrong type")

  def negate(self):
    raise Exception("wrong type")


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
      raise Exception("wrong type")

  def subtract(self, other):
    if other.type == TYPE_INT:
      return ConstDouble(self.doubleval - other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.doubleval - other.doubleval)
    else:
      raise Exception("wrong type")

  def multiply(self, other):
    if other.type == TYPE_INT:
      return ConstDouble(self.doubleval * other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.doubleval * other.doubleval)
    else:
      raise Exception("wrong type")

  def divide(self, other):
    if other.type == TYPE_INT:
      return ConstDouble(self.doubleval / other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstDouble(self.doubleval / other.doubleval)
    else:
      raise Exception("wrong type")

  def mod(self, other):
    raise Exception("wrong type")

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
      raise Exception("wrong type")

  def greater_than(self, other):
    if other.type == TYPE_INT:
      return ConstBoolean(self.doubleval > other.intval)
    elif other.type == TYPE_DOUBLE:
      return ConstBoolean(self.doubleval > other.doubleval)
    else:
      raise Exception("wrong type")

  def negate(self):
    raise Exception("wrong type")


class ConstBoolean(Constant):
  def __init__(self, value):
    self.boolval = value
    self.type = TYPE_BOOLEAN

  def add(self, other):
    raise Exception("wrong type")

  def subtract(self, other):
    raise Exception("wrong type")

  def multiply(self, other):
    raise Exception("wrong type")

  def divide(self, other):
    raise Exception("wrong type")

  def mod(self, other):
    raise Exception("wrong type")

  def equal(self, other):
    if other.type == TYPE_BOOLEAN:
      return ConstBoolean(self.boolval == other.boolval)
    else:
      return ConstBoolean(False)

  def less_than(self, other):
    raise Exception("wrong type")

  def greater_than(self, other):
    raise Exception("wrong type")

  def negate(self):
    return ConstBoolean(not self.boolval)


class ConstChar(Constant):
  def __init__(self, value):
    self.charval = value
    self.type = TYPE_CHAR

  def add(self, other):
    raise Exception("wrong type")

  def subtract(self, other):
    raise Exception("wrong type")

  def multiply(self, other):
    raise Exception("wrong type")

  def divide(self, other):
    raise Exception("wrong type")

  def mod(self, other):
    raise Exception("wrong type")

  def equal(self, other):
    if other.type == TYPE_CHAR:
      return ConstBoolean(self.charval == other.charval)
    else:
      return ConstBoolean(False)

  def less_than(self, other):
    raise Exception("wrong type")

  def greater_than(self, other):
    raise Exception("wrong type")

  def negate(self):
    raise Exception("wrong type")


class ConstFunc(Constant):
  def __init__(self, value):
    self.funcval = value
    self.type = TYPE_FUNC

  def add(self, other):
    raise Exception("wrong type")

  def subtract(self, other):
    raise Exception("wrong type")

  def multiply(self, other):
    raise Exception("wrong type")

  def divide(self, other):
    raise Exception("wrong type")

  def mod(self, other):
    raise Exception("wrong type")

  def equal(self, other):
    raise Exception("wrong type")

  def less_than(self, other):
    raise Exception("wrong type")

  def greater_than(self, other):
    raise Exception("wrong type")

  def negate(self):
    raise Exception("wrong type")


class FuncObject:
  def __init__(self, arity, code, const_table, var_names):
    self.arity = arity
    self.code = code
    self.const_table = const_table
    self.var_names = var_names
