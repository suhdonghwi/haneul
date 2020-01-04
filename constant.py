class FuncObject:
  def __init__(self, arity, insts, const_table, var_names):
    self.arity = arity
    self.insts = insts
    self.const_table = const_table
    self.var_names = var_names
