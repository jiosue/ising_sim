"""__init__.py.

Define the version number of ``ising_sim``.

"""

from ._version import __version__

from . import sim
from . import gui

from ._correlations import *
from ._graphical_simulation import *

__version__ = '0.0.0'
name = "ising_sim"
