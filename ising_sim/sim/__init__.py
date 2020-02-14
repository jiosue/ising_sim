"""``ising_sim.sim`` contains the Ising simulation functionality.

To simulate, we iterate randomly through the spins at each update step and flip
the spin (1) if it is energetically favorable or (2) with probability
exp(-dE / T) if dE > 0, where dE is the change in energy from flipping the
spin.

"""

from ._isingsimulation import *
