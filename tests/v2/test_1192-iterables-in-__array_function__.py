# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE


import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

to_list = ak._v2.operations.convert.to_list


def test():
    first = ak._v2.operations.convert.from_numpy(np.array([1, 2, 3]))
    deltas = ak._v2.highlevel.Array([[1, 2], [1, 2], [1, 2, 3]])
    assert np.hstack(
        (
            first[:, np.newaxis],
            ak._v2.operations.structure.fill_none(
                ak.operations.structure.pad_none(deltas, 3, axis=-1), 999
            ),
        )
    ).tolist() == [[1, 1, 2, 999], [2, 1, 2, 999], [3, 1, 2, 3]]
