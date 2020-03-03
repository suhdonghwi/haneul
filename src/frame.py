from rpython.rlib import jit

from constant_type import *
from constant import ConstNone


class Frame:
  _immutable_fields_ = ['locals', 'stack']
  _virtualizable_ = ['local_list[*]', 'stack[*]', 'stack_top']

  def __init__(self, local_number, local_list, max_stack_depth=8):
    self = jit.hint(self, access_directly=True, fresh_virtualizable=True)

    self.local_list = local_list + [None] * (local_number - len(local_list))

    self.stack = [None] * max_stack_depth
    self.stack_top = 0

  def push(self, value):
    index = self.stack_top
    assert index >= 0
    self.stack[index] = value
    self.stack_top += 1

  def pop(self):
    index = self.stack_top - 1
    assert index >= 0
    value = self.stack[index]
    self.stack[index] = None
    self.stack_top = index
    return value

  def load(self, index):
    assert index >= 0

    return self.local_list[index]

  def load_reserve(self, index):
    assert(index >= 0)

    value = self.local_list[index]
    if value is None:
      self.local_list[index] = ConstNone()
      return self.local_list[index]
    else:
      return value

  def store(self, value, index):
    assert(index >= 0)

    dest = self.local_list[index]
    if dest.type == TYPE_NONE:
      dest.type = TYPE_FUNC
      dest.funcval = value.funcval
      dest.builtinval = value.builtinval
      dest.josa_map = value.josa_map
    else:
      self.local_list[index] = value
