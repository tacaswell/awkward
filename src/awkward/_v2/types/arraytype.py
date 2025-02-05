# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE


import awkward as ak
import awkward._v2.types.type


class ArrayType:
    def __init__(self, content, length):
        if not isinstance(content, awkward._v2.types.type.Type):
            raise TypeError(
                "{} all 'contents' must be Type subclasses, not {}".format(
                    type(self).__name__, repr(content)
                )
            )
        if not ak._util.isint(length) or length < 0:
            raise ValueError(
                "{} 'length' must be of a positive integer, not {}".format(
                    type(self).__name__, repr(length)
                )
            )
        self._content = content
        self._length = length

    @property
    def content(self):
        return self._content

    @property
    def length(self):
        return self._length

    def __str__(self):
        return str(self._length) + " * " + str(self._content)

    def __repr__(self):
        args = [repr(self._content), repr(self._length)]
        return "{}({})".format(type(self).__name__, ", ".join(args))

    def __eq__(self, other):
        if isinstance(other, ArrayType):
            return self._length == other._length and self._content == other._content
        else:
            return False
