import os, subprocess
from . import EvaluatorBase

__all__ = ["BarvinokEvaluator"]


def prepare_input(A, b):
    """
    Prepare vector partition function query in the format expected by barvinok_count.
    """
    nrows, ncols = A.shape
    s = "%d %d\n" % (ncols + nrows, 1 + ncols + 1)

    # x[i] >= 0
    for i in range(ncols):
        delta_i = [int(i == j) for j in range(ncols)]
        s += "1   %s   0\n" % " ".join(map(str, delta_i))

    # A[i] * x - b[i] >= 0
    for i, row in enumerate(A):
        s += "0   %s   %s\n" % (" ".join(map(str, row)), -b[i])
    return s


class BarvinokEvaluator(EvaluatorBase):
    """
    Evaluate vector partition functions at given point using barvinok (http://barvinok.gforge.inria.fr/).
    """

    def __init__(self, path):
        assert os.path.isfile(path), (
            '"%s" not found (should be path to barvinok_count binary)' % path
        )
        self.path = path

    def eval(self, vpn, b):
        # prepare input
        stdin = prepare_input(vpn.A, b).encode("ascii")

        # run barvinok_count
        popen = subprocess.Popen(
            self.path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        stdout, _ = popen.communicate(stdin)
        assert popen.returncode == 0

        # parse output
        return int(stdout.splitlines()[-1])

    def __str__(self):
        return "barvinok[%s]" % self.path
