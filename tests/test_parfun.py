import itertools
import pytest
from barvikron import *


def sturmfels_expected(b):
    """
    Closed formula from Sturmfels (1995).
    """
    u, v, w = sorted(b, reverse=True)

    if (u + v + w) % 2 == 1:
        return 0

    if u >= v + w:
        psi = v * w / 2 + v * w**2 / 8 - w**3 / 24

        if u % 2 == 0 and v % 2 == 0:
            psi += 1 + v / 2 + 2 * w / 3
        elif u % 2 == 1 and v % 2 == 1:
            psi += 1 / 2 + v / 2 + 5 * w / 12
        else:
            psi += 1 / 2 + 3 * v / 8 + 13 * w / 24
    else:
        psi = (
            -(u**2) / 8
            - v**2 / 8
            - w**2 / 8
            + u * v / 4
            + u * w / 4
            + v * w / 4
            + u**3 / 48
            - u**2 * v / 16
            - u**2 * w / 16
            + u * v**2 / 16
            + u * v * w / 8
            + u * w**2 / 16
            - v**3 / 48
            - v**2 * w / 16
            + v * w**2 / 16
            - w**3 / 16
        )
        if u % 2 == 0 and v % 2 == 0:
            psi += 1 + u / 6 + v / 3 + w / 2
        elif u % 2 == 1 and v % 2 == 1:
            psi += 1 / 2 + u / 6 + v / 3 + w / 4
        else:
            psi += 1 / 2 + u / 6 + 5 * v / 24 + 3 * w / 8
    return int(round(psi))


def test_construction():
    vpn = VectorPartitionFunction([[1, 0], [0, 1], [1, 1]])
    assert vpn.A.shape == (3, 2)


@pytest.mark.parametrize("b", itertools.product(range(1, 5), repeat=3))
def test_sturmfels_evaluation(b, evaluator):
    sturmfels_vpn = VectorPartitionFunction(
        [[2, 1, 1, 0, 0, 0], [0, 1, 0, 2, 1, 0], [0, 0, 1, 0, 1, 2]]
    )

    # compare evaluation for all b in {1,...,4}^3
    got = sturmfels_vpn.eval(b, evaluator)
    expected = sturmfels_expected(b)
    assert got == expected
