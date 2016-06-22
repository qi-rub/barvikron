from barvikron import BarvinokEvaluator, LatteEvaluator


def pytest_addoption(parser):
    parser.addoption(
        "--barvinok",
        metavar="PATH",
        action="store",
        default=None,
        help="evaluate partition functions using barvinok (http://barvinok.gforge.inria.fr/)")
    parser.addoption(
        "--latte",
        metavar="PATH",
        action="store",
        default=None,
        help="evaluate partition functions using LaTTe (https://www.math.ucdavis.edu/~latte/)")


def pytest_generate_tests(metafunc):
    if 'evaluator' in metafunc.fixturenames:
        evaluators = []

        # add barvinok?
        barvinok_path = metafunc.config.getoption("--barvinok")
        if barvinok_path:
            evaluators.append(BarvinokEvaluator(barvinok_path))

        # add latte? (XXX)
        latte_path = metafunc.config.getoption("--latte")
        if latte_path:
            evaluators.append(LatteEvaluator(latte_path))

        metafunc.parametrize('evaluator', evaluators)
