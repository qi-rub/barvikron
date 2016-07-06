from setuptools import setup
from setuptools.command.test import test as TestCommand
import ast, io, re, os.path, sys

# determine __version__ from pw.py source (adapted from mitsuhiko)
VERSION_RE = re.compile(r'__version__\s+=\s+(.*)')
with io.open('barvikron/__init__.py', encoding='utf-8') as fp:
    version_code = VERSION_RE.search(fp.read()).group(1)
    version = str(ast.literal_eval(version_code))

# read long description and convert to RST
long_description = io.open(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'README.md'),
    encoding='utf-8').read()
try:
    import pypandoc
    long_description = pypandoc.convert(long_description, 'rst', format='md')
except ImportError:
    pass

setup(
    name='barvikron',
    version=version,
    description='Efficiently compute Kronecker coefficients of bounded height (using the technique of arXiv:1204.4379).',
    long_description=long_description,
    author='Michael Walter',
    author_email='michael.walter@gmail.com',
    url='https://github.com/catch22/barvikron',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
    ],
    install_requires=['Click', 'numpy', 'six', 'whichcraft'],
    packages=['barvikron'],
    tests_require=['pytest'],
    entry_points='''
    [console_scripts]
    barvikron=barvikron.scripts.serial:main
    barvikron-master=barvikron.scripts.parallel:master
    barvikron-worker=barvikron.scripts.parallel:worker
    ''')
