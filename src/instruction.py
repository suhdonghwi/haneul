INSTRUCTION_NAMES = ['PUSH', 'POP', 'LOAD_LOCAL', 'STORE_LOCAL', 'LOAD_DEREF', 'STORE_GLOBAL', 'LOAD_GLOBAL',
                     'CALL', 'MAKE_STRUCT', 'GET_FIELD', 'JMP', 'POP_JMP_IF_FALSE', 'FREE_VAR', 
                     'ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', 'MOD', 
                     'EQUAL', 'LESS_THAN', 'GREATER_THAN', 'NEGATE', "LOGIC_NOT", "LOGIC_AND", "LOGIC_OR"]
for (i, inst) in enumerate(INSTRUCTION_NAMES):
  globals()['INST_' + inst] = i


class Instruction:
  _immutable_fields_ = ['opcode', 'operand_int', 'operand_josa_list[*]', 'operand_free_var_list[*]', 'operand_str']

  def __init__(self, opcode):
    self.opcode = opcode
    self.operand_int = 0
    self.operand_josa_list = None
    self.operand_free_var_list = None
    self.operand_str = None
