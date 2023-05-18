import logging, multiprocessing, multiprocessing.managers, os, queue
import click
from .. import (
    BarvinokEvaluator,
    LatteEvaluator,
    flatten_weight,
    finite_differences,
    positive_roots,
    kronecker_weight_vpn,
)
from . import WeightParamType, enable_logging


class WorkManager(multiprocessing.managers.BaseManager):
    pass


DEFAULT_PORT = 12345


@click.group()
def main():
    pass


@main.command()
@click.argument(
    "partitions",
    metavar="\u03BB \u03BC \u03BD ...",
    nargs=-1,
    required=True,
    type=WeightParamType(),
)
@click.option(
    "-P",
    "--port",
    type=int,
    default=DEFAULT_PORT,
    help="Port to listen at for communication with workers.",
)
@click.option(
    "-K",
    "--authkey",
    required=True,
    help="Secret authentication key for communication with workers.",
)
@click.option("-v", "--verbose", is_flag=True)
def master(partitions, port, authkey, verbose):
    """
    Compute (generalized) Kronecker coefficient g(\u03BB,\u03BC,\u03BD,...)
    using parallel processing. See README for instructions.
    """
    if verbose:
        enable_logging()

    # create queues and register with work manager
    work_queue = multiprocessing.JoinableQueue()
    result_queue = multiprocessing.Queue()
    WorkManager.register("work_queue", callable=lambda: work_queue)
    WorkManager.register("result_queue", callable=lambda: result_queue)

    # compute highest weight and finite-difference formula
    logging.info("Preparing work items...")
    dims = list(map(len, partitions))
    highest_weight = flatten_weight(partitions)
    findiff = finite_differences(positive_roots(dims))
    total = len(findiff)
    for i, (coeff, shift) in enumerate(findiff):
        work_queue.put((i, total, coeff, highest_weight + shift))

    # setup work manager
    manager = WorkManager(address=("", port), authkey=authkey.encode("ascii"))
    manager.start()
    logging.info("Serving %d weight multiplicities on port %d...", total, port)

    # wait until all work items have been processed...
    work_queue.join()

    # accumulate weight multiplicities
    logging.info("All work items have been processed. Now accumulating...")
    g = 0
    for _ in findiff:
        g += result_queue.get()
    click.echo(g)


@main.command()
@click.argument(
    "partitions",
    metavar="\u03BB \u03BC \u03BD ...",
    nargs=-1,
    required=True,
    type=WeightParamType(),
)
@click.option("-H", "--host", required=True, help="Hostname of master.")
@click.option(
    "-P",
    "--port",
    type=int,
    default=DEFAULT_PORT,
    help="Port to connect to for communication with master.",
)
@click.option(
    "-K",
    "--authkey",
    required=True,
    help="Secret authentication key for communication with workers.",
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
@click.option("-v", "--verbose", is_flag=True)
def worker(partitions, host, port, authkey, barvinok, latte, verbose):
    """
    Compute (generalized) Kronecker coefficient g(\u03BB,\u03BC,\u03BD,...)
    using parallel processing. See README for instructions.
    """
    if verbose:
        enable_logging()

    # instantiate evaluator
    assert bool(barvinok) != bool(latte), "Specify either --barvinok or --latte."
    evaluator = BarvinokEvaluator(barvinok) if barvinok else LatteEvaluator(latte)

    # create partition function
    dims = list(map(len, partitions))
    vpn = kronecker_weight_vpn(dims)

    # connect work manager, and retrieve queues
    WorkManager.register("work_queue")
    WorkManager.register("result_queue")
    logging.info("Connecting to %s:%d...", host, port)
    manager = WorkManager(address=(host, port), authkey=authkey.encode("ascii"))
    manager.connect()
    work_queue = manager.work_queue()
    result_queue = manager.result_queue()

    while True:
        try:
            # get next work item
            index, total, coeff, weight = work_queue.get_nowait()

            # compute weight multiplicity
            logging.info(
                "(%3d/%3d)   [%6s]   Computing the multiplicity of %s...",
                index + 1,
                total,
                os.getpid(),
                weight,
            )
            weight_mul = vpn.eval(weight, evaluator)
            logging.info(
                "(%3d/%3d)   [%6s]   => weight multiplicity = %d (coeff = %d).",
                index + 1,
                total,
                os.getpid(),
                weight_mul,
                coeff,
            )

            # post result
            result_queue.put(coeff * weight_mul)
            work_queue.task_done()
        except queue.Empty:
            break


if __name__ == "__main__":
    main()
