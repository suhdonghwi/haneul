class FuncObject:
  def __init__(self, arity, code, const_table, var_names):
    self.arity = arity
    self.code = code
    self.const_table = const_table
    self.var_names = var_names
