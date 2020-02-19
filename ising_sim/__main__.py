"""``ising_sim`` is for simulation of the 1-dim classical Ising model.

Here we define the module functionality for ``ising_sim``. For usage, run
    ``python -m ising_sim length [J] [num_past_states] [coarse]``,
where ``[]`` denotes that the argument is optional. ``length`` is the number
of spins in the chain. ``J`` is the coupling value. ``num_past_states`` is the
number of previous states to use to calculate the average correlation.
``coarse`` is the number of times to update before updating the graphics.

"""

from sys import argv
from . import start_graphical_simulation


if __name__ == "__main__":
    if not argv[1:]:
        print(
            "Please run ``python -m ising_sim length [J] "
            "[num_past_states] [coarse]``"
        )
    else:
        length = int(argv[1])
        J = float(argv[2]) if argv[2:] else -1
        num_past_states = int(argv[3]) if argv[3:] else 100
        coarse = int(argv[4]) if argv[4:] else 5
        start_graphical_simulation(length, J, num_past_states, coarse)
