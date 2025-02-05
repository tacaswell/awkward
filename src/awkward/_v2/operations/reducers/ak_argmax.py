# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE


import awkward as ak

np = ak.nplike.NumpyMetadata.instance()


# @ak._v2._connect.numpy.implements("argmax")
def argmax(array, axis=None, keepdims=False, mask_identity=True, flatten_records=False):
    """
    Args:
        array: Array-like data (anything #ak.to_layout recognizes).
        axis (None or int): If None, combine all values from the array into
            a single scalar result; if an int, group by that axis: `0` is the
            outermost, `1` is the first level of nested lists, etc., and
            negative `axis` counts from the innermost: `-1` is the innermost,
            `-2` is the next level up, etc.
        keepdims (bool): If False, this reducer decreases the number of
            dimensions by 1; if True, the reduced values are wrapped in a new
            length-1 dimension so that the result of this operation may be
            broadcasted with the original array.
        mask_identity (bool): If True, reducing over empty lists results in
            None (an option type); otherwise, reducing over empty lists
            results in the operation's identity.
        flatten_records (bool): If True, axis=None combines fields from different
            records; otherwise, records raise an error.

    Returns the index position of the maximum value in each group of elements
    from `array` (many types supported, including all Awkward Arrays and
    Records). The identity of maximization would be negative infinity, but
    argmax must return the position of the maximum element, which has no value
    for empty lists. Therefore, the identity should be masked: the argmax of
    an empty list is None. If `mask_identity=False`, the result would be `-1`,
    which is distinct from all valid index positions, but care should be taken
    that it is not misinterpreted as "the last element of the list."

    This operation is the same as NumPy's
    [argmax](https://docs.scipy.org/doc/numpy/reference/generated/numpy.argmax.html)
    if all lists at a given dimension have the same length and no None values,
    but it generalizes to cases where they do not.

    See #ak.sum for a more complete description of nested list and missing
    value (None) handling in reducers.
    """
    layout = ak._v2.operations.convert.to_layout(
        array, allow_record=False, allow_other=False
    )

    if axis is None:
        layout = ak._v2.operations.structure.fill_none(
            layout, -np.inf, axis=-1, highlevel=False
        )

        best_index = None
        best_value = None
        for tmp in layout.completely_flatten(
            function_name="ak.argmax", flatten_records=flatten_records
        ):
            # FIXME: this isn't going to survive a type-tracer!
            out = layout.nplike.argmax(tmp, axis=None)
            if best_index is None or tmp[out] > best_value:
                best_index = out
                best_value = tmp[out]
        return best_index

    else:
        behavior = ak._v2._util.behavior_of(array)
        out = layout.argmax(axis=axis, mask=mask_identity, keepdims=keepdims)
        if isinstance(out, (ak._v2.contents.Content, ak._v2.record.Record)):
            return ak._v2._util.wrap(out, behavior)
        else:
            return out
