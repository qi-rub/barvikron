from __future__ import absolute_import, print_function
import click
import logging
from . import BarvinokEvaluator, LatteEvaluator, kronecker_weight_multiplicity, kronecker


class WeightParamType(click.ParamType):
    name = 'weight'

    def convert(self, value, param, ctx):
        value = eval(value)
        if not isinstance(value, (tuple, list)):
            self.fail('%s is not a valid weight' % value, param, ctx)
        return value


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
def cli(partitions, weight_multiplicity, barvinok, latte, verbose):
    # enable verbose mode?
    if verbose:
        logging.basicConfig(format='%(asctime)-25s %(message)s',
                            level=logging.INFO)

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
