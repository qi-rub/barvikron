import pytest
from barvikron import BarvinokEvaluator, LatteEvaluator, default_evaluator


def pytest_addoption(parser):
    parser.addoption(
        "--barvinok",
        metavar="PATH",
        action="store",
        default=None,
        help="evaluate partition functions using barvinok (http://barvinok.gforge.inria.fr/)",
    )
    parser.addoption(
        "--latte",
        metavar="PATH",
        action="store",
        default=None,
        help="evaluate partition functions using LaTTe (https://www.math.ucdavis.edu/~latte/)",
    )


def pytest_configure(config):
    pytest.evaluators = []

    # add barvinok?
    barvinok_path = config.getoption("--barvinok")
    if barvinok_path:
        pytest.evaluators.append(BarvinokEvaluator(barvinok_path))

    # add latte?
    latte_path = config.getoption("--latte")
    if latte_path:
        pytest.evaluators.append(LatteEvaluator(latte_path))

    # no evaluator specified? add default
    if not pytest.evaluators:
        pytest.evaluators.append(default_evaluator())


def pytest_report_header(config):
    return "evaluators: %s" % ", ".join(str(e) for e in pytest.evaluators)


def pytest_generate_tests(metafunc):
    if "evaluator" in metafunc.fixturenames:
        metafunc.parametrize("evaluator", pytest.evaluators)
