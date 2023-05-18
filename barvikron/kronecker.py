import itertools, logging
import numpy as np
from . import VectorPartitionFunction, finite_differences

__all__ = [
    "kronecker_weight_vpn",
    "flatten_weight",
    "kronecker_weight_multiplicity",
    "positive_roots",
    "kronecker",
]


def kronecker_weight_vpn(dims):
    """
    Return VectorPartitionFunction for computing weight multiplicities in
    the symmetric algebra Sym(C^prod(dims)) with respect to the maximal torus
    of GL(dims[1]) x ... x GL(dims[n]).
    """
    # build list of multi-indices
    multi_indices = list(itertools.product(*map(range, dims)))

    # build matrix such that the r-th row corresponds to the r-th entries of all weights
    As = []
    for i, dim in enumerate(dims):
        A = np.zeros(shape=(dim, len(multi_indices)), dtype=object)
        for j, midx in enumerate(multi_indices):
            A[midx[i], j] = 1
        As.append(A)
    A = np.row_stack(As)

    return VectorPartitionFunction(A)


def flatten_weight(omega):
    """
    Flatten a product weight omega, given as list of weights of each GL(d), into a single vector.
    """
    num_boxes = set(map(sum, omega))
    assert (
        len(num_boxes) == 1
    ), "All components should have the same number of degree (number of boxes)."

    return np.hstack(omega)


def kronecker_weight_multiplicity(omega, evaluator):
    """
    Compute weight multiplicity in Sym(C^prod(dims)) for given weight.
    """
    dims = list(map(len, omega))
    weight = flatten_weight(omega)
    return kronecker_weight_vpn(dims).eval(weight, evaluator)


def positive_roots(dims):
    """
    Return list of positive roots for of GL(dims[1]) x ... x GL(dims[n]).
    """
    roots = []
    for k, dim in enumerate(dims):
        for i in range(dim):
            for j in range(i + 1, dim):
                root = np.zeros(sum(dims), dtype=object)
                root[sum(dims[:k]) + i] = 1
                root[sum(dims[:k]) + j] = -1
                roots.append(root)
    return roots


def kronecker(partitions, evaluator):
    """
    Compute Kronecker coefficient for given highest weight.
    """
    # create partition function
    dims = list(map(len, partitions))
    vpn = kronecker_weight_vpn(dims)

    # compute highest weight and finite-difference formula
    highest_weight = flatten_weight(partitions)
    proots = positive_roots(dims)
    assert all(
        highest_weight.dot(pr) >= 0 for pr in proots
    ), "Highest weight should be dominant."
    findiff = finite_differences(proots)

    # compute finite-difference formula coefficients
    total = len(findiff)
    logging.info(
        "About to compute %d weight multiplicities using a partition function of size %s.",
        total,
        vpn.A.shape,
    )

    g = 0
    for i, (coeff, shift) in enumerate(findiff):
        # compute next weight multiplicity
        weight = highest_weight + shift
        logging.info(
            "(%3d/%3d)   About to compute the weight multiplicity of %s...",
            i + 1,
            total,
            weight,
        )
        weight_mul = vpn.eval(weight, evaluator)
        logging.info(
            "(%3d/%3d)   => weight multiplicity = %d (coeff = %d).",
            i + 1,
            total,
            weight_mul,
            coeff,
        )

        # and add appropriately
        g += coeff * weight_mul

    return g
