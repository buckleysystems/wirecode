from wirecode import geometry


def test_midpoint():
    assert geometry.midpoint(0, 2) == 1
    assert geometry.midpoint(0, 2j) == 1j
    assert geometry.midpoint(1 - 2j, -1 + 2j) == 0
