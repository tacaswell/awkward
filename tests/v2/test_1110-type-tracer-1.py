# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE


import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

from awkward._v2._typetracer import UnknownLength

typetracer = ak._v2._typetracer.TypeTracer.instance()


def test_getitem_at():
    concrete = ak._v2.contents.NumpyArray(np.arange(2 * 3 * 5).reshape(2, 3, 5) * 0.1)
    abstract = ak._v2.contents.NumpyArray(concrete.to(typetracer))

    assert concrete.shape == (2, 3, 5)
    assert abstract.shape == (UnknownLength, 3, 5)
    assert abstract[0].shape == (UnknownLength, 5)
    assert abstract[0][0].shape == (UnknownLength,)

    assert abstract.form == concrete.form
    assert abstract.form.type == concrete.form.type

    assert abstract[0].form == concrete[0].form
    assert abstract[0].form.type == concrete[0].form.type
