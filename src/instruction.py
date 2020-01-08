INST_PUSH = 0
INST_POP = 1
INST_STORE = 2
INST_STORE_GLOBAL = 3
INST_LOAD = 4
INST_LOAD_GLOBAL = 5
INST_CALL = 6
INST_JMP_FORWARD = 7
INST_POP_JMP_IF_FALSE = 8
INST_RETURN = 9
INST_ADD = 10
INST_SUBTRACT = 11
INST_MULTIPLY = 12
INST_DIVIDE = 13
INST_MOD = 14
INST_EQUAL = 15
INST_LESS_THAN = 16
INST_GREATER_THAN = 17
INST_NEGATE = 18


class Instruction:
  def __init__(self, line_number, opcode):
    self.line_number = line_number
    self.opcode = opcode
    self.operand_int = 0
    self.operand_str = u''
