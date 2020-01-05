from constant import FuncObject

nest_level = 0


def nprint(p):
  print " " * nest_level * 2,
  print p


def dump_constant(constant):
  global nest_level

  if isinstance(constant, FuncObject):
    nprint("FuncObject:")
    nest_level += 1
    nprint("[arity] " + str(constant.arity))

    nprint("[const table]")
    nest_level += 1
    for c in constant.const_table:
      dump_constant(c)
    nest_level -= 1

    nprint("[var names]")
    nest_level += 1
    for name in constant.var_names:
      nprint(name)
    nest_level -= 1

    nprint("[code] ")
    nest_level += 1
    for inst in constant.code:
      dump_inst(inst)
    nest_level -= 1
    nest_level -= 1
  else:
    nprint(constant)


def dump_inst(inst):
  nprint(str(inst.line_number) + " " +
         str(inst.opcode) + " " + str(inst.operand))
