import itertools as it


def iter_with_lookahead(i, fillvalue=None):
    """Iterate over adjacent pairs [A,B,C] -> (A,B), (B,C), (C,fillvalue)"""
    i1, i2 = it.tee(i)
    _ = next(i2)
    return it.zip_longest(i1, i2, fillvalue=fillvalue)