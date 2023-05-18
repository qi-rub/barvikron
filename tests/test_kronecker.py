import pytest
from barvikron import *


def stretch(N, partitions):
    return [[N * x for x in partition] for partition in partitions]


def test_kronecker_weight_vpn():
    assert kronecker_weight_vpn([2, 2, 2]).A.tolist() == [
        # [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
    ]

    assert kronecker_weight_vpn([2, 3]).A.tolist() == [
        # [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1],
        [1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1],
    ]


def test_flatten_weight():
    v = flatten_weight([[3, 8], [5, 6], [6, 5]])
    assert v.tolist() == [3, 8, 5, 6, 6, 5]


def test_positive_roots():
    roots = positive_roots([2, 2, 2])
    assert list(map(list, roots)) == [
        [1, -1, 0, 0, 0, 0],
        [0, 0, 1, -1, 0, 0],
        [0, 0, 0, 0, 1, -1],
    ]


@pytest.mark.parametrize(
    "partitions,expected",
    [
        ([[1, 0], [1, 0], [1, 0]], 1),
        ([[1, 0], [0, 1], [1, 0]], 1),
        ([[1, 0], [0, 1], [2, -1]], 0),
    ],
)
def test_kronecker_weight_multiplicity(partitions, expected, evaluator):
    assert kronecker_weight_multiplicity(partitions, evaluator) == expected


@pytest.mark.parametrize("N", [1, 2, 3, 4, 5, 10**20, 10**20 + 5])
def test_two_row_boxes(N, evaluator):
    partitions = stretch(N, [[1, 1], [1, 1], [1, 1]])
    assert kronecker(partitions, evaluator) == (N + 1) % 2


@pytest.mark.parametrize("j", [1, 2])
@pytest.mark.parametrize("N", [1, 2, 3, 4, 100, 10**20])
def test_briand_orellana_rosas_2_4(j, N, evaluator):
    """
    Compare with formula by Briand-Orellana-Rosas (Theorem 2.4 of arXiv:0810.3163).
    """
    # choose numbers such that i > j > 0 and k > 2i + j
    i = j + 5
    k = 2 * i + j + 23

    alpha = [k, k]
    beta = [k + 1, k - 1]
    gamma = [2 * k - 2 * i - 2 * j, 2 * i, 2 * j]

    got = kronecker(stretch(N, [alpha, beta, gamma]), evaluator)
    # expected = N / 2 + 1 - (N % 2) * 3 / 2
    expected = (N + 2 - (N % 2) * 3) // 2
    assert got == expected


@pytest.mark.parametrize("N", [1, 2, 3, 4, 5, 100, 10**20])
def test_briand_orellana_rosas_p8(N, evaluator):
    """
    Compare with formula by Briand-Orellana-Rosas (page 8 of arXiv:0810.3163).
    """
    alpha = [10, 6, 2]
    beta = [10, 8]
    gamma = [11, 7]

    got = kronecker(stretch(N, [alpha, beta, gamma]), evaluator)
    # expected = 7 / 4 * N**2 + 3 / 2 * N + 1 - (N % 2) * 5 / 4
    expected = (7 * N**2 + 6 * N + 4 - (N % 2) * 5) // 4
    assert got == expected
