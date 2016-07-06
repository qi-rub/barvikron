from __future__ import absolute_import
import numpy as np

__all__ = ['VectorPartitionFunction', 'EvaluatorBase']


class VectorPartitionFunction(object):
    """
    Vector partition function

      phi_A(b) = #{ x >= 0 : A * x = b }

    for given list of integer matrix A.
    """

    def __init__(self, A):
        self.A = np.array(A)

    def __repr__(self):
        return '<VectorPartitionFunction(%s)>' % self.A

    def eval(self, b, evaluator):
        assert len(b) == self.A.shape[0]
        return evaluator.eval(self, b)


class EvaluatorBase(object):
    """
    Interface for evaluating vector partition functions at a given value.
    """

    def eval(self, vpn, b):
        raise NotImplementedError
