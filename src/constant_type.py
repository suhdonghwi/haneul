# -*- coding: utf-8 -*-
types = ['NONE', 'INTEGER', 'REAL', 'STRING', 'BOOLEAN', 'FUNC', 'BUILTIN']
for (i, typename) in enumerate(types):
  globals()['TYPE_' + typename] = i


def get_type_name(t):
  if t == TYPE_INTEGER:
    return u"정수"
  elif t == TYPE_REAL:
    return u"실수"
  elif t == TYPE_STRING:
    return u"문자열"
  elif t == TYPE_BOOLEAN:
    return u"참 또는 거짓"
  elif t == TYPE_FUNC:
    return u"함수"
  elif t == TYPE_BUILTIN:
    return u"미리 만들어진 값"
  else:
    return u"(없음)"


def binary_typeerror(type1, type2, operation):
  raise TypeError(u"%s 타입의 값과 %s 타입의 값은 %s 연산을 지원하지 않습니다." %
                  (get_type_name(type1), get_type_name(type2), operation))


def unary_typeerror(type1, operation):
  raise TypeError(u"%s 타입의 값은 %s 연산을 지원하지 않습니다." %
                  (get_type_name(type1), operation))
