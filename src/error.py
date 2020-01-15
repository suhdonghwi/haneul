class HaneulError(Exception):
  def __init__(self, message):
    self.message = message
    self.error_line = 0


class InvalidType(HaneulError):
  def __init__(self, message):
    HaneulError.__init__(self, message)


class ArgNumberMismatch(HaneulError):
  def __init__(self, message):
    HaneulError.__init__(self, message)


class UnboundVariable(HaneulError):
  def __init__(self, message):
    HaneulError.__init__(self, message)


class CannotReturn(HaneulError):
  def __init__(self, message):
    HaneulError.__init__(self, message)


class NotCallable(HaneulError):
  def __init__(self, message):
    HaneulError.__init__(self, message)
