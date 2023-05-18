from barvikron import *


def sorted_list(coeffs):
    return sorted([(coeff, shift.tolist()) for coeff, shift in coeffs])


def test_1dimensional():
    findiff = finite_differences([[1], [1], [1]])
    assert sorted_list(findiff) == [(-3, [1]), (-1, [3]), (+1, [0]), (+3, [2])]


def test_kronecker_findiff():
    expected = [
        (-1, [0, 0, 0, 0, 1, -1]),
        (-1, [0, 0, 1, -1, 0, 0]),
        (-1, [1, -1, 0, 0, 0, 0]),
        (-1, [1, -1, 1, -1, 1, -1]),
        (+1, [0, 0, 0, 0, 0, 0]),
        (+1, [0, 0, 1, -1, 1, -1]),
        (+1, [1, -1, 0, 0, 1, -1]),
        (+1, [1, -1, 1, -1, 0, 0]),
    ]
    coeffs = finite_differences(positive_roots([2, 2, 2]))
    assert sorted_list(coeffs) == expected
