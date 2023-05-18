import sys
import click
from .. import (
    BarvinokEvaluator,
    LatteEvaluator,
    kronecker_weight_multiplicity,
    kronecker,
    default_evaluator,
    NoEvaluatorFound,
)
from . import WeightParamType, enable_logging


@click.command()
@click.argument(
    "partitions",
    metavar="\u03BB \u03BC \u03BD ...",
    nargs=-1,
    required=True,
    type=WeightParamType(),
)
@click.option(
    "--barvinok",
    metavar="PATH",
    help="Path to barvinok_count tool (see http://barvinok.gforge.inria.fr/).",
)
@click.option(
    "--latte",
    metavar="PATH",
    help="Path to LattE's count tool (see https://www.math.ucdavis.edu/~latte/).",
)
@click.option(
    "--weight-multiplicity",
    is_flag=True,
    help="Compute weight multiplicity instead of Kronecker coefficient.",
)
@click.option("-v", "--verbose", is_flag=True)
def main(partitions, weight_multiplicity, barvinok, latte, verbose):
    """
    Compute (generalized) Kronecker coefficient g(\u03BB,\u03BC,\u03BD,...).
    """
    # enable verbose mode?
    if verbose:
        enable_logging()

    # instantiate evaluator
    if barvinok and latte:
        click.echo("Specify either --barvinok or --latte (but not both).", err=True)
        sys.exit(1)

    if barvinok:
        evaluator = BarvinokEvaluator(barvinok)
    elif latte:
        evaluator = LatteEvaluator(latte)
    else:
        try:
            evaluator = default_evaluator()
        except NoEvaluatorFound:
            click.echo(
                "No partition function evaluator found. Specify --barvinok or --latte option.",
                err=True,
            )
            sys.exit(1)

    # compute Kronecker coefficient
    if weight_multiplicity:
        g = kronecker_weight_multiplicity(partitions, evaluator)
    else:
        g = kronecker(partitions, evaluator)
    click.echo(g)


if __name__ == "__main__":
    main()
