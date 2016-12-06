



class AbstractAttr(object):
    _value = None
    is_dirty = False

    def __init__(self, value=None, implementation=None):
        if not value is None:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if self.sanity(v):
            if self._value == v:
                self.is_dirty = False
            else:
                self._value = v
                self.is_dirty = True

    def sanity(self, v):
        return True

class StringAttr(AbstractAttr):
    def sanity(self, v):
        if not isinstance(v, str):
            raise TypeError("Wrong value type, must be str")
        return True
