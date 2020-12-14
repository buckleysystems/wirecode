import itertools as it


def iter_with_lookbehind(i, fillvalue=None):
    """Iterate over adjacent pairs [A,B,C] -> (fill, A), (A,B), (B,C)"""
    i1, i2 = it.tee(i)
    return zip(it.chain([fillvalue], i1), i2)


def iter_with_lookahead(i, fillvalue=None):
    """Iterate over adjacent pairs [A,B,C] -> (A,B), (B,C), (C,fill)"""
    i1, i2 = it.tee(i)
    _ = next(i2)
    return it.zip_longest(i1, i2, fillvalue=fillvalue)


def test(string: str) -> str:
    return string.lower()