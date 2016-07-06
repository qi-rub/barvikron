from __future__ import absolute_import, print_function
import click
from .. import BarvinokEvaluator, LatteEvaluator, kronecker_weight_multiplicity, kronecker
from . import WeightParamType, enable_logging


@click.command()
@click.argument('partitions',
                metavar=u'\u03BB \u03BC \u03BD ...',
                nargs=-1,
                required=True,
                type=WeightParamType())
@click.option(
    '--barvinok',
    metavar='PATH',
    help='Path to barvinok_count tool (see http://barvinok.gforge.inria.fr/).')
@click.option(
    '--latte',
    metavar='PATH',
    help='Path to LattE\'s count tool (see https://www.math.ucdavis.edu/~latte/).'
)
@click.option(
    '--weight-multiplicity',
    is_flag=True,
    help='Compute weight multiplicity instead of Kronecker coefficient.')
@click.option('-v', '--verbose', is_flag=True)
def main(partitions, weight_multiplicity, barvinok, latte, verbose):
    u"""
    Compute (generalized) Kronecker coefficient g(\u03BB,\u03BC,\u03BD,...).
    """
    # enable verbose mode?
    if verbose:
        enable_logging()

    # instantiate evaluator
    assert bool(barvinok) != bool(
        latte), 'Specify either --barvinok or --latte.'
    evaluator = BarvinokEvaluator(barvinok) if barvinok else LatteEvaluator(
        latte)

    # compute Kronecker coefficient
    if weight_multiplicity:
        g = kronecker_weight_multiplicity(partitions, evaluator)
    else:
        g = kronecker(partitions, evaluator)
    click.echo(g)
