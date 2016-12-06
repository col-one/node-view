



class AbstractAttr(object):
    def __init__(self, value=None, implementation=None):
        self._value = value
        self.is_dirty = False

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, v):
        if self._value == v:
            self.is_dirty = False
        else:
            self._value = v
            self.is_dirty = True


