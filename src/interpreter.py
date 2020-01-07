from instruction import *
from constant import *
from variable import Variable


class BytecodeInterpreter:
  def __init__(self, const_table, var_names, code, parent=None):
    self.const_table = const_table
    self.local_vars = [Variable(name) for name in var_names]
    self.code = code
    self.parent = parent

    self.stack = []

  def find_index(self, index):
    var = self.local_vars[index]
    if var.value is None:
      if self.parent is None:
        return None
      else:
        return self.parent.find_name(var.name)
    return var.value

  def find_name(self, name):
    for (i, var) in enumerate(self.local_vars):
      if var.name == name:
        return self.find_index(i)

    return self.parent.find_name(name)

  def run(self):
    code_iter = iter(self.code)
    for inst in code_iter:
      if inst.opcode == INST_PUSH:
        #print "PUSH"
        self.stack.append(self.const_table[inst.operand])
      elif inst.opcode == INST_POP:
        #print "POP"
        self.stack.pop()
      elif inst.opcode == INST_STORE:
        #print "STORE"
        self.local_vars[inst.operand].value = self.stack.pop()
      elif inst.opcode == INST_LOAD:
        #print "LOAD"
        self.stack.append(self.find_index(inst.operand))
      elif inst.opcode == INST_CALL:
        #print "CALL"
        args = []
        for i in range(inst.operand):
          args.append(self.stack.pop())

        func_object = self.stack.pop().funcval
        func_interpreter = BytecodeInterpreter(
            func_object.const_table, func_object.var_names, func_object.code, self)
        args.reverse()
        for (i, arg) in enumerate(args):
          func_interpreter.local_vars[i].value = arg

        return_value = func_interpreter.run()
        self.stack.append(return_value)
      elif inst.opcode == INST_JMP_FORWARD:
        #print "JMPFORWARD"
        for i in range(inst.operand):
          next(code_iter)
      elif inst.opcode == INST_POP_JMP_IF_FALSE:
        #print "POPJMPIFFALSE"
        value = self.stack.pop().boolval
        if value == False:
          for i in range(inst.operand):
            next(code_iter)
      elif inst.opcode == INST_RETURN:
        #print "RETURN"
        value = self.stack.pop()
        return value
      elif inst.opcode == INST_NEGATE:
        #print "NEGATE"
        value = self.stack.pop()
        self.stack.append(value.negate())
      else:
        rhs, lhs = self.stack.pop(), self.stack.pop()
        if inst.opcode == INST_ADD:
          #print "ADD"
          self.stack.append(lhs.add(rhs))
        elif inst.opcode == INST_SUBTRACT:
          #print "SUBTRACT"
          self.stack.append(lhs.subtract(rhs))
        elif inst.opcode == INST_MULTIPLY:
          #print "MULTIPLY"
          self.stack.append(lhs.multiply(rhs))
        elif inst.opcode == INST_DIVIDE:
          #print "DIVIDE"
          self.stack.append(lhs.divide(rhs))
        elif inst.opcode == INST_MOD:
          #print "MOD"
          self.stack.append(lhs.mod(rhs))
        elif inst.opcode == INST_EQUAL:
          #print "EQUAL"
          self.stack.append(lhs.equal(rhs))
        elif inst.opcode == INST_LESS_THAN:
          #print "LESS_THAN"
          self.stack.append(lhs.less_than(rhs))
        elif inst.opcode == INST_GREATER_THAN:
          #print "GREATER_THAN"
          self.stack.append(lhs.greater_than(rhs))

      """
      print "[",
      for c in self.stack:
        if c.type == TYPE_INT:
          print c.intval,
        if c.type == TYPE_DOUBLE:
          print c.doubleval,
        if c.type == TYPE_CHAR:
          print c.charval,
        if c.type == TYPE_BOOLEAN:
          print c.boolval,
        if c.type == TYPE_FUNC:
          print c.funcval,
          print ", ",
          print "]"
    """
