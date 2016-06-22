from __future__ import absolute_import
import sys

__version__ = '0.3'
LONG_INTEGER = int if sys.version_info > (3, ) else long

from .parfun import *
from .barvinok import *
from .latte import *
from .findiff import *
from .kronecker import *
