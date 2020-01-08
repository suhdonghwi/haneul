instructions = ['PUSH', 'POP', 'STORE', 'STORE_GLOBAL', 'LOAD', 'LOAD_GLOBAL', 'CALL', 'JMP_FORWARD', 'POP_JMP_IF_FALSE',
                'RETURN', 'ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', 'MOD', 'EQUAL', 'LESS_THAN', 'GREATER_THAN', 'NEGATE']
for (i, inst) in enumerate(instructions):
  globals()['INST_' + inst] = i


class Instruction:
  def __init__(self, line_number, opcode):
    self.line_number = line_number
    self.opcode = opcode
    self.operand_int = 0
    self.operand_str = u''
