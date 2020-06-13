# -*- coding: utf-8 -*-

from rpython.rlib import jit

from constant import ConstFunc


class Frame:
  _immutable_fields_ = ['locals', 'stack']
  _virtualizable_ = ['local_list[*]', 'stack[*]', 'stack_top']

  def __init__(self, local_number, local_list, max_stack_size):
    self = jit.hint(self, access_directly=True, fresh_virtualizable=True)

    self.local_list = local_list + [None] * (local_number - len(local_list))

    self.stack = [None] * max_stack_size
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
    """
    Free variable 등록이 아직 정의되지 않은 상수에 대해 적용되었을 때,
    해당 위치에 비어있는 ConstFunc를 넣어주고 반환하는 함수입니다.
    """
    assert(index >= 0)

    value = self.local_list[index]
    if value is None:
      self.local_list[index] = ConstFunc(None, None, None)
      return self.local_list[index]
    else:
      return value

  def store(self, value, index):
    """
    로컬 인덱스를 받고 해당 위치에 값을 넣어주는 함수입니다.
    해당 위치에 (`load_reserve`를 통해 저장된) ConstNone이 들어있으면
    ConstNone 객체를 value로 바꿉니다.
    """
    assert(index >= 0)

    dest = self.local_list[index]
    if isinstance(dest, ConstFunc) and isinstance(value, ConstFunc):
      dest.funcval = value.funcval
      dest.builtinval = value.builtinval
      dest.josa_map = value.josa_map
    else:
      self.local_list[index] = value
