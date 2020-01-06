INST_PUSH = 0
INST_POP = 1
INST_STORE = 2
INST_LOAD = 3
INST_CALL = 4
INST_JMP_FORWARD = 5
INST_POP_JMP_IF_FALSE = 6
INST_RETURN = 7
INST_ADD = 8
INST_SUBTRACT = 9
INST_MULTIPLY = 10
INST_DIVIDE = 11
INST_MOD = 12
INST_EQUAL = 13
INST_LESS_THAN = 14
INST_GREATER_THAN = 15
INST_NEGATE = 16


class Instruction:
  def __init__(self, line_number, opcode, operand=0):
    self.line_number = line_number
    self.opcode = opcode
    self.operand = operand
