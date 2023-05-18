from collections import defaultdict
import numpy as np

__all__ = ["finite_differences"]


def finite_differences(positive_roots):
    """
    Expand the finite difference formula in the form
      sum coeff[i] * translate(shift[i])
    and return the list of (coeff,shift)'s.
    """
    # recursively compute multiset of weighted shifts
    zero = np.zeros(len(positive_roots[0]), dtype=object)
    l = [(1, zero)]
    for root in positive_roots:
        l += [(-x[0], x[1] + root) for x in l]

    # optimize
    d = defaultdict(int)
    for coeff, shift in l:
        d[tuple(shift)] += coeff

    return [
        (coeff, np.array(shift, dtype=object))
        for shift, coeff in d.items()
        if coeff != 0
    ]
