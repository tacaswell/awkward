# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE


import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

# https://github.com/scikit-hep/awkward-1.0/issues/459#issuecomment-694941328
#
# So the rules would be,
#    * if arrays have different `__array__` or `__record__` parameters, they are not equal;
#    * if they otherwise have different parameters, the types can be equal, but merging
#      (concatenation, option-simplify, or union-simplify) removes parameters other than
#      `__array__` and `__record__`.


@pytest.mark.skip(reason="FIXME: ak.type not merged yet")
def test_0459_types():
    plain_plain = ak._v2.highlevel.Array(
        ak._v2.contents.NumpyArray(np.array([0.0, 1.1, 2.2, 3.3, 4.4]), parameters={})
    )
    array_plain = ak._v2.highlevel.Array(
        ak._v2.contents.NumpyArray(
            np.array([0.0, 1.1, 2.2, 3.3, 4.4]), parameters={"__array__": "zoinks"}
        )
    )
    plain_isdoc = ak._v2.highlevel.Array(
        ak._v2.contents.NumpyArray(
            np.array([0.0, 1.1, 2.2, 3.3, 4.4]),
            parameters={"__doc__": "This is a zoink."},
        )
    )
    array_isdoc = ak._v2.highlevel.Array(
        ak._v2.contents.NumpyArray(
            np.array([0.0, 1.1, 2.2, 3.3, 4.4]),
            parameters={"__doc__": "This is a zoink.", "__array__": "zoinks"},
        )
    )

    assert ak._v2.operations.describe.parameters(plain_plain) == {}
    assert ak._v2.operations.describe.parameters(array_plain) == {"__array__": "zoinks"}
    assert ak._v2.operations.describe.parameters(plain_isdoc) == {
        "__doc__": "This is a zoink."
    }
    assert ak._v2.operations.describe.parameters(array_isdoc) == {
        "__array__": "zoinks",
        "__doc__": "This is a zoink.",
    }

    assert ak._v2.operations.describe.type(
        plain_plain
    ) == ak._v2.operations.describe.type(plain_plain)
    assert ak._v2.operations.describe.type(
        array_plain
    ) == ak._v2.operations.describe.type(array_plain)
    assert ak._v2.operations.describe.type(
        plain_isdoc
    ) == ak._v2.operations.describe.type(plain_isdoc)
    assert ak._v2.operations.describe.type(
        array_isdoc
    ) == ak._v2.operations.describe.type(array_isdoc)

    assert ak._v2.operations.describe.type(
        plain_plain
    ) != ak._v2.operations.describe.type(array_plain)
    assert ak._v2.operations.describe.type(
        array_plain
    ) != ak._v2.operations.describe.type(plain_plain)

    assert ak._v2.operations.describe.type(
        plain_plain
    ) == ak._v2.operations.describe.type(plain_isdoc)
    assert ak._v2.operations.describe.type(
        plain_isdoc
    ) == ak._v2.operations.describe.type(plain_plain)

    assert ak._v2.operations.describe.type(
        array_plain
    ) == ak._v2.operations.describe.type(array_isdoc)
    assert ak._v2.operations.describe.type(
        array_isdoc
    ) == ak._v2.operations.describe.type(array_plain)

    assert ak._v2.operations.describe.type(
        plain_isdoc
    ) != ak._v2.operations.describe.type(array_isdoc)
    assert ak._v2.operations.describe.type(
        array_isdoc
    ) != ak._v2.operations.describe.type(plain_isdoc)


def test_0459():
    plain_plain = ak._v2.highlevel.Array(
        ak._v2.contents.NumpyArray(np.array([0.0, 1.1, 2.2, 3.3, 4.4]), parameters={})
    )
    array_plain = ak._v2.highlevel.Array(
        ak._v2.contents.NumpyArray(
            np.array([0.0, 1.1, 2.2, 3.3, 4.4]), parameters={"__array__": "zoinks"}
        )
    )
    plain_isdoc = ak._v2.highlevel.Array(
        ak._v2.contents.NumpyArray(
            np.array([0.0, 1.1, 2.2, 3.3, 4.4]),
            parameters={"__doc__": "This is a zoink."},
        )
    )
    array_isdoc = ak._v2.highlevel.Array(
        ak._v2.contents.NumpyArray(
            np.array([0.0, 1.1, 2.2, 3.3, 4.4]),
            parameters={"__doc__": "This is a zoink.", "__array__": "zoinks"},
        )
    )

    assert ak._v2.operations.describe.parameters(plain_plain) == {}
    assert ak._v2.operations.describe.parameters(array_plain) == {"__array__": "zoinks"}
    assert ak._v2.operations.describe.parameters(plain_isdoc) == {
        "__doc__": "This is a zoink."
    }
    assert ak._v2.operations.describe.parameters(array_isdoc) == {
        "__array__": "zoinks",
        "__doc__": "This is a zoink.",
    }

    assert (
        ak._v2.operations.describe.parameters(
            ak._v2.operations.structure.concatenate([plain_plain, plain_plain])
        )
        == {}
    )
    assert ak._v2.operations.describe.parameters(
        ak._v2.operations.structure.concatenate([array_plain, array_plain])
    ) == {"__array__": "zoinks"}
    assert ak._v2.operations.describe.parameters(
        ak._v2.operations.structure.concatenate([plain_isdoc, plain_isdoc])
    ) == {"__doc__": "This is a zoink."}
    assert ak._v2.operations.describe.parameters(
        ak._v2.operations.structure.concatenate([array_isdoc, array_isdoc])
    ) == {
        "__array__": "zoinks",
        "__doc__": "This is a zoink.",
    }

    assert isinstance(
        ak._v2.operations.structure.concatenate([plain_plain, plain_plain]).layout,
        ak._v2.contents.NumpyArray,
    )
    assert isinstance(
        ak._v2.operations.structure.concatenate([array_plain, array_plain]).layout,
        ak._v2.contents.NumpyArray,
    )
    assert isinstance(
        ak._v2.operations.structure.concatenate([plain_isdoc, plain_isdoc]).layout,
        ak._v2.contents.NumpyArray,
    )
    assert isinstance(
        ak._v2.operations.structure.concatenate([array_isdoc, array_isdoc]).layout,
        ak._v2.contents.NumpyArray,
    )

    assert (
        ak._v2.operations.describe.parameters(
            ak._v2.operations.structure.concatenate([plain_plain, array_plain])
        )
        == {}
    )
    assert (
        ak._v2.operations.describe.parameters(
            ak._v2.operations.structure.concatenate([plain_isdoc, array_isdoc])
        )
        == {}
    )
    assert (
        ak._v2.operations.describe.parameters(
            ak._v2.operations.structure.concatenate([array_plain, plain_plain])
        )
        == {}
    )
    assert (
        ak._v2.operations.describe.parameters(
            ak._v2.operations.structure.concatenate([array_isdoc, plain_isdoc])
        )
        == {}
    )

    assert isinstance(
        ak._v2.operations.structure.concatenate([plain_plain, array_plain]).layout,
        ak._v2.contents.UnionArray,
    )
    assert isinstance(
        ak._v2.operations.structure.concatenate([plain_isdoc, array_isdoc]).layout,
        ak._v2.contents.UnionArray,
    )
    assert isinstance(
        ak._v2.operations.structure.concatenate([array_plain, plain_plain]).layout,
        ak._v2.contents.UnionArray,
    )
    assert isinstance(
        ak._v2.operations.structure.concatenate([array_isdoc, plain_isdoc]).layout,
        ak._v2.contents.UnionArray,
    )

    assert (
        ak._v2.operations.describe.parameters(
            ak._v2.operations.structure.concatenate([plain_plain, plain_isdoc])
        )
        == {}
    )
    assert ak._v2.operations.describe.parameters(
        ak._v2.operations.structure.concatenate([array_plain, array_isdoc])
    ) == {"__array__": "zoinks"}
    assert (
        ak._v2.operations.describe.parameters(
            ak._v2.operations.structure.concatenate([plain_isdoc, plain_plain])
        )
        == {}
    )
    assert ak._v2.operations.describe.parameters(
        ak._v2.operations.structure.concatenate([array_isdoc, array_plain])
    ) == {"__array__": "zoinks"}

    assert isinstance(
        ak._v2.operations.structure.concatenate([plain_plain, plain_isdoc]).layout,
        ak._v2.contents.NumpyArray,
    )
    assert isinstance(
        ak._v2.operations.structure.concatenate([array_plain, array_isdoc]).layout,
        ak._v2.contents.NumpyArray,
    )
    assert isinstance(
        ak._v2.operations.structure.concatenate([plain_isdoc, plain_plain]).layout,
        ak._v2.contents.NumpyArray,
    )
    assert isinstance(
        ak._v2.operations.structure.concatenate([array_isdoc, array_plain]).layout,
        ak._v2.contents.NumpyArray,
    )


def test_0522():
    content1 = ak._v2.highlevel.Array([0.0, 1.1, 2.2, 3.3, 4.4]).layout
    content2 = ak._v2.highlevel.Array([0, 100, 200, 300, 400]).layout
    tags = ak._v2.index.Index8(np.array([0, 0, 0, 1, 1, 0, 0, 1, 1, 1], np.int8))
    index = ak._v2.index.Index64(np.array([0, 1, 2, 0, 1, 3, 4, 2, 3, 4], np.int64))
    unionarray = ak._v2.highlevel.Array(
        ak._v2.contents.UnionArray(tags, index, [content1, content2])
    )
    assert unionarray.tolist() == [0.0, 1.1, 2.2, 0, 100, 3.3, 4.4, 200, 300, 400]

    assert (unionarray + 10).tolist() == [
        10.0,
        11.1,
        12.2,
        10,
        110,
        13.3,
        14.4,
        210,
        310,
        410,
    ]
    assert (10 + unionarray).tolist() == [
        10.0,
        11.1,
        12.2,
        10,
        110,
        13.3,
        14.4,
        210,
        310,
        410,
    ]

    assert (unionarray + range(0, 100, 10)).tolist() == [
        0.0,
        11.1,
        22.2,
        30,
        140,
        53.3,
        64.4,
        270,
        380,
        490,
    ]
    assert (range(0, 100, 10) + unionarray).tolist() == [
        0.0,
        11.1,
        22.2,
        30,
        140,
        53.3,
        64.4,
        270,
        380,
        490,
    ]

    assert (unionarray + np.arange(0, 100, 10)).tolist() == [
        0.0,
        11.1,
        22.2,
        30,
        140,
        53.3,
        64.4,
        270,
        380,
        490,
    ]
    assert (np.arange(0, 100, 10) + unionarray).tolist() == [
        0.0,
        11.1,
        22.2,
        30,
        140,
        53.3,
        64.4,
        270,
        380,
        490,
    ]

    assert (unionarray + ak._v2.highlevel.Array(np.arange(0, 100, 10))).tolist() == [
        0.0,
        11.1,
        22.2,
        30,
        140,
        53.3,
        64.4,
        270,
        380,
        490,
    ]
    assert (ak._v2.highlevel.Array(np.arange(0, 100, 10)) + unionarray).tolist() == [
        0.0,
        11.1,
        22.2,
        30,
        140,
        53.3,
        64.4,
        270,
        380,
        490,
    ]

    assert (unionarray + unionarray).tolist() == [
        0.0,
        2.2,
        4.4,
        0,
        200,
        6.6,
        8.8,
        400,
        600,
        800,
    ]
