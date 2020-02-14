"""_graphical_simulation.py.

Contains the function that brings together the gui and the simulation.

"""

from .sim import IsingSimulation
from .gui import GUI
from . import compute_correlations
import tkinter as tk

__all__ = 'start_graphical_simulation',


class _Run:
    """_Run.

    An internal class to handle the combination of the spin chain simulation
    and the graphics.

    """

    def __init__(self, root, sim, num_past_states, coarse):
        """__init__.

        Parameters
        ----------
        root : GUI object.
        sim : IsingSimulation object.
        num_past_states : int.
            Number of past states to use to compute the average correlation.
        coarse : int.
            Number of simulation updates before updating the graphics.

        """
        self._root, self._sim, self._coarse = root, sim, coarse
        self._num_past_states = num_past_states
        self._update_state()
        self._paused = True

        self._update_state()

        self._button = tk.Button(
            self._root, text="Play", command=self._pause_play
        )
        self._button.pack()

        tk.Label(
            root,
            text="""
            Chain length: N = %d
            Coupling constant: J = %g
            Number of past states to use to compute the average correlation: %d
            Number of simulation updates before updating the graphics: %d

            To adjust any of these, rerun the simulation with
                python -m ising_sim [N] [J] [num_past_states] [coarse]
            """ % (sim.length, sim.J, num_past_states, coarse)
        ).pack()

    def _pause_play(self):
        """_pause_play.

        Pause or resume the simulation whenever the button is clicked.

        """
        if self._paused:
            self._button.config(text="Pause")
            self._paused = False
            self._update()
        else:
            self._button.config(text="Play")
            self._paused = True

    def _update_state(self):
        """_update_state.

        Update the GUI with the state and the correlations.

        """
        self._root.set_state(self._sim.state)
        self._root.update_correlation(compute_correlations(
            self._sim.get_past_states(self._num_past_states)
        ))

    def _update(self):
        """_update.

        Update the simulation, update the GUI, the repeat after 50
        milliseconds.

        """
        if self._paused:
            return
        self._sim.update(self._root.get_temperature(), self._coarse)
        self._update_state()
        self._root.after(50, self._update)


def start_graphical_simulation(length, J=-1, num_past_states=50, coarse=10):
    """start_graphical_simulation.

    Make the GUI and start running the simulation.

    Parameters
    ----------
    length : int.
        The length of the 1D ising chain.
    J : float (optional, defaults to -1).
        The coupling constant for the spin chain. ``J < 0`` is a ferromagnetic
        chain; ``J > 0`` is an antiferromagnetic chain.
    num_past_states : int (optional, defaults to 50).
        The number of recent states to use to calculate the average correlation
        function.
    coarse : int (optional, defaults to 10).
        The number of simulation updates before updating the graphics.

    Notes
    -----
    - The initial state is all 1's.
    - If you are running ``ising_sim`` as a module and you want to adjust
    these, run ``python -m ising_sim [N] [J] [num_past_states] [coarse]``.

    """
    sim = IsingSimulation(length, J)
    root = GUI(length)
    _Run(root, sim, num_past_states, coarse)
    root.mainloop()
