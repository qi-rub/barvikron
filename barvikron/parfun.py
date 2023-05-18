import os
import numpy as np
import whichcraft

__all__ = [
    "VectorPartitionFunction",
    "EvaluatorBase",
    "default_evaluator",
    "NoEvaluatorFound",
]


class VectorPartitionFunction(object):
    """
    Vector partition function

      phi_A(b) = #{ x >= 0 : A * x = b }

    for given list of integer matrix A.
    """

    def __init__(self, A):
        self.A = np.array(A)

    def __repr__(self):
        return "<VectorPartitionFunction(%s)>" % self.A

    def eval(self, b, evaluator):
        assert len(b) == self.A.shape[0]
        return evaluator.eval(self, b)


class EvaluatorBase(object):
    """
    Interface for evaluating vector partition functions at a given value.
    """

    def eval(self, vpn, b):
        raise NotImplementedError


class NoEvaluatorFound(Exception):
    pass


def default_evaluator():
    """
    Find and instantiate best available evaluator.
    """
    from .barvinok import BarvinokEvaluator
    from .latte import LatteEvaluator

    # first try environment variables
    if "BARVIKRON_BARVINOK" in os.environ:
        return BarvinokEvaluator(os.environ["BARVIKRON_BARVINOK"])
    if "BARVIKRON_LATTE" in os.environ:
        return LatteEvaluator(os.environ["BARVIKRON_LATTE"])

    # then try to find executables
    path = whichcraft.which("barvinok_count")
    if path:
        return BarvinokEvaluator(path)

    path = whichcraft.which("count")
    if path:
        return LatteEvaluator(path)

    raise NoEvaluatorFound("Cannot find 'barvinok_count' nor LattE's 'count' in path.")
