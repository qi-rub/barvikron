# barvikron [![CI](https://github.com/qi-rub/barvikron/actions/workflows/ci.yml/badge.svg)](https://github.com/qi-rub/barvikron/actions/workflows/ci.yml) [![arXiv](http://img.shields.io/badge/arXiv-1204.4379-blue.svg?style=flat)](http://arxiv.org/abs/1204.4379)

**Efficiently compute Kronecker coefficients of bounded height**

`barvikron` is a Python implementation of an efficient algorithm for computing Kronecker coefficients proposed by [Christandl-Doran-Walter (2012)](http://arxiv.org/abs/1204.4379). Kronecker coefficients play an important role in combinatorics, quantum physics and geometric complexity theory. Their computation is known to be #P-hard in general. Given partitions with a bounded number of rows, however, our algorithm based on lattice-point counting computes the corresponding Kronecker coefficient in polynomial time.

If you find barvikron useful in your research please consider citing our paper:
```bibtex
@Inproceedings{barvikron,
  Author    = {Christandl, M. and Doran, B. and Walter, M.},
  Title     = {{Computing Multiplicities of Lie Group Representations}},
  Booktitle = {2012 IEEE 53rd Annual Symposium on Foundations of Computer Science (FOCS)},
  Doi       = {10.1109/FOCS.2012.43},
  Pages     = {639--648},
  Year      = {2012},
  Note      = {Software available at \url{https://github.com/qi-rub/barvikron/}.},
}
```

# Installation

To install `barvikron`, simply run:
```bash
pip install git+git://github.com/qi-rub/barvikron.git
```
Then install either [barvinok](https://barvinok.sourceforge.io) or [LattE](https://www.math.ucdavis.edu/~latte/).

# Getting started

To compute a single Kronecker coefficient, call `barvikron` with the partitions and specify either the barvinok or LattE backend:
```bash
$ barvikron [4096,4096] [4096,4096] [4096,4096] --barvinok /opt/barvinok/bin/barvinok_count
1

$ barvikron [4096,4096] [4096,4096] [4096,4096] --latte /opt/latte/bin/count
1
```

`barvikron` can also be used as a Python library:
```python
import barvikron

e = barvikron.BarvinokEvaluator('/opt/barvinok/bin/barvinok_count')
g = barvikron.kronecker([[3,1], [3,1], [2,2]], e)
print(g)  # prints 1
```

# Usage

## Computing on a single processor

```
Usage: barvikron [OPTIONS] λ μ ν ...

  Compute (generalized) Kronecker coefficient g(λ,μ,ν,...).

Options:
  --barvinok PATH        Path to barvinok_count tool (see
                         http://barvinok.gforge.inria.fr/).
  --latte PATH           Path to LattE's count tool (see
                         https://www.math.ucdavis.edu/~latte/).
  --weight-multiplicity  Compute weight multiplicity instead of Kronecker
                         coefficient.
  -v, --verbose
  --help                 Show this message and exit.
```

## Computing on multiple processors and/or machines

There are two parts. First, there is the "master" process, which is run once:
```
Usage: barvikron-parallel master [OPTIONS] λ μ ν ...

  Compute (generalized) Kronecker coefficient g(λ,μ,ν,...) using parallel
  processing. See README for instructions.

Options:
  -P, --port INTEGER  Port to listen at for communication with workers.
  -K, --authkey TEXT  Secret authentication key for communication with
                      workers.  [required]
  -v, --verbose
  --help              Show this message and exit.
```
It hands off the weight multiplicity computations to worker processes that should be run on the computational nodes (optimally, one process per core of each node).
```
Usage: barvikron-parallel worker [OPTIONS] λ μ ν ...

  Compute (generalized) Kronecker coefficient g(λ,μ,ν,...) using parallel
  processing. See README for instructions.

Options:
  -H, --host TEXT     Hostname of master.  [required]
  -P, --port INTEGER  Port to connect to for communication with master.
  -K, --authkey TEXT  Secret authentication key for communication with
                      workers.  [required]
  --barvinok PATH     Path to barvinok_count tool (see
                      http://barvinok.gforge.inria.fr/).
  --latte PATH        Path to LattE's count tool (see
                      https://www.math.ucdavis.edu/~latte/).
  -v, --verbose
  --help              Show this message and exit.
```
In this way, Kronecker coefficients can be computed in a massively parallel fashion.

Here is a sample script for computing Kronecker coefficients using the LSF platform:
```
#!/bin/bash
PARTITIONS="[40000,20000,10000] [50000,10000,10000] [30000,20000,20000]"
barvikron-parallel master $PARTITIONS -K SECRET -v &
blaunch -z "$LSB_HOSTS" barvikron-parallel worker -H "$HOSTNAME" -K SECRET $PARTITIONS --barvinok $PATH_TO_BARVINOK -v
```

# Performance

Barvikron is much faster than codes such as [LiE](http://wwwmathlabo.univ-poitiers.fr/~maavl/LiE/) or [SageMath](https://sagemath.org/)'s symmetric function library for computing Kronecker coefficients with long rows. Here are some preliminary benchmarking results for computing three-row Kronecker coefficients `g_{N * [4,2,1], N * [5,1,1], N * [3,2,2]}` using a varying number of processors (of type Opteron6174).

| N | Processors | Runtime |
| ------- | --- | ---------- |
|  10000  |  24 | 26m42.948s |
|  10000  |	 48	| 14m26.250s |
|  10000	| 128	|  n/a       |
| 100000	|  24	| 31m32.325s |
| 100000	|  48	| 16m41.689s |
| 100000	| 128 |	 7m6.346s  |


We note that evaluating each such Kronecker coefficient amounts to evaluating 216 weight multiplicities for GL(3) x GL(3) x GL(3). Computing a single weight multiplicity takes 3m25.701s and 4m7.178s for N = 10000 and 100000, respectively.

Interestingly, the weight multiplicity of `[400000,200000,100000], [500000,100000,100000], [300000,200000,200000]` in `Sym^700000(C^27)` is equal to `342216835855298841170737708279176303674277186351573308277640173317403784744358278942583775`...

— Michael Walter, 2012–2023
