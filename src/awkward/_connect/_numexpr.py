# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

# v2: replace with src/awkward/_v2/_connect/numexpr.py


import warnings
import sys
import types

import awkward as ak

checked_version = False


def import_numexpr():
    global checked_version
    try:
        import numexpr
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            """install the 'numexpr' package with:

    pip install numexpr --upgrade

or

    conda install numexpr"""
        ) from None
    else:
        if not checked_version and ak._v2._util.parse_version(
            numexpr.__version__
        ) < ak._v2._util.parse_version("2.7.1"):
            warnings.warn(
                "Awkward Array is only known to work with numexpr 2.7.1 or later"
                "(you have version {})".format(numexpr.__version__),
                RuntimeWarning,
            )
        checked_version = True
        return numexpr


def getArguments(names, local_dict=None, global_dict=None):
    call_frame = sys._getframe(2)

    clear_local_dict = False
    if local_dict is None:
        local_dict = call_frame.f_locals
        clear_local_dict = True
    try:
        frame_globals = call_frame.f_globals
        if global_dict is None:
            global_dict = frame_globals

        clear_local_dict = clear_local_dict and frame_globals is not local_dict

        arguments = []
        for name in names:
            try:
                a = local_dict[name]
            except KeyError:
                a = global_dict[name]
            arguments.append(a)  # <--- different from NumExpr
    finally:
        if clear_local_dict:
            local_dict.clear()

    return arguments


def evaluate(
    expression, local_dict=None, global_dict=None, order="K", casting="safe", **kwargs
):
    numexpr = import_numexpr()

    context = numexpr.necompiler.getContext(kwargs, frame_depth=1)
    expr_key = (expression, tuple(sorted(context.items())))
    if expr_key not in numexpr.necompiler._names_cache:
        numexpr.necompiler._names_cache[expr_key] = numexpr.necompiler.getExprNames(
            expression, context
        )
    names, ex_uses_vml = numexpr.necompiler._names_cache[expr_key]
    arguments = getArguments(names, local_dict, global_dict)

    arrays = [
        ak.operations.convert.to_layout(x, allow_record=True, allow_other=True)
        for x in arguments
    ]

    def getfunction(inputs):
        if all(
            isinstance(x, ak.layout.NumpyArray) or not isinstance(x, ak.layout.Content)
            for x in inputs
        ):
            return lambda: (
                ak.layout.NumpyArray(
                    numexpr.evaluate(
                        expression,
                        dict(zip(names, inputs)),
                        {},
                        order=order,
                        casting=casting,
                        **kwargs
                    )
                ),
            )
        else:
            return None

    behavior = ak._util.behaviorof(*arrays)
    out = ak._util.broadcast_and_apply(
        arrays, getfunction, behavior, allow_records=False, pass_depth=False
    )
    assert isinstance(out, tuple) and len(out) == 1
    return ak._util.wrap(out[0], behavior)


evaluate.evaluate = evaluate


def re_evaluate(local_dict=None):
    numexpr = import_numexpr()

    try:
        compiled_ex = numexpr.necompiler._numexpr_last["ex"]  # noqa: F841
    except KeyError:
        raise RuntimeError(
            "not a previous evaluate() execution found"
            + ak._util.exception_suffix(__file__)
        )
    names = numexpr.necompiler._numexpr_last["argnames"]
    arguments = getArguments(names, local_dict)

    arrays = [
        ak.operations.convert.to_layout(x, allow_record=True, allow_other=True)
        for x in arguments
    ]

    def getfunction(inputs):
        if all(
            isinstance(x, ak.layout.NumpyArray) or not isinstance(x, ak.layout.Content)
            for x in inputs
        ):
            return lambda: (
                ak.layout.NumpyArray(numexpr.re_evaluate(dict(zip(names, inputs)))),
            )
        else:
            return None

    behavior = ak._util.behaviorof(*arrays)
    out = ak._util.broadcast_and_apply(
        arrays, getfunction, behavior, allow_records=False, pass_depth=False
    )
    assert isinstance(out, tuple) and len(out) == 1
    return ak._util.wrap(out[0], behavior)


ak.numexpr = types.ModuleType("numexpr")
ak.numexpr.evaluate = evaluate
ak.numexpr.re_evaluate = re_evaluate
