"""_isingsimulation.py.

This file contains the main class for simulating the 1D Ising chain.

"""

from qubovert import spin_var
from numpy import exp
import random


__all__ = 'IsingSimulation',


class IsingSimulation:
    """IsingSimulation.

    A class to manage the simulation of the 1D Ising chain.

    Example
    -------
    >>> length = 10
    >>> T = 4  # temperature
    >>> ising = IsingSimulation(length)
    >>> for time in range(100):
    >>>     print(ising.state)
    >>>     ising.update(T)
    >>> T = 2
    >>> for time in range(100):
    >>>     print(ising.state)
    >>>     ising.update(T)

    """

    def __init__(self, length, J=-1, initial_state=None):
        """__init__.

        Parameters
        ----------
        length : int.
            The length of the 1D Ising chain.
        J : numeric (optional, defaults to -1).
            The coupling value of the Ising model. If ``J < 0``, then it is
            favorable for the spins to align; if ``J > 0``, then it is
            favorable for the spins to antialign.
        initial_state : dict or iterable (optional, defaults to None).
            The initial state of the chain. Ie spin ``i`` will be initialized
            to value ``initial_state[i]``, which should be in {1, -1}. If
            ``initial_state is None``, then it will be initialized to all 1s.

        """
        self._length, self._J = length, J
        if initial_state is None:
            self._state = {i: 1 for i in range(length)}
        else:
            self._state = {i: initial_state[i] for i in range(length)}
            if set(self._state.values()) != {1, -1}:
                raise ValueError("Spins must be either 1 or -1")
        self._initial_state = self._state.copy()

        self._past_states = []

        z = {i: spin_var(i) for i in range(length)}
        z[-1] = 0
        z[length] = 0
        self._subgraphs = {
            i: J * z[i] * (z[i-1] + z[i+1])
            for i in range(length)
        }
        # self._ham = sum(J * z[i] * z[i+1] for i in range(length))

    @property
    def state(self):
        """state.

        The current state of the spins.

        Returns
        -------
        state : dict.
            Dictionary that maps spin locations to their values.

        """
        return self._state.copy()

    def get_past_states(self, num_states=1000):
        """get_past_states.

        Return the previous ``num_states`` states of the system (if that many
        exist; ``self`` only stores up the previous 1000 states).

        Parameters
        ----------
        num_states : int (optional, defaults to 1000).
            The number of previous update steps to include.

        Returns
        -------
        states : list of dicts.
            Each dict maps spin labels to their values.

        """
        return [
            s.copy() for s in self._past_states[-num_states+1:]
        ] + [self.state]

    @property
    def length(self):
        """length.

        Return the length of the spin chain.

        Returns
        -------
        length : int.

        """
        return self._length

    @property
    def J(self):
        """J.

        The coupling value of the Ising model. If ``J == -1``, then it is
        favorable for the spins to align; if ``J == 1``, then it is
        favorable for the spins to antialign.

        Returns
        -------
        J : int in {-1, 1}.

        """
        return self._J

    def _add_past_state(self, state):
        """_add_past_state.

        Add ``state`` to the ``past_states`` memory.

        Parameters
        ----------
        state : dict.
            Maps spin labels to their values.

        """
        self._past_states.append(state)
        if len(self._past_states) > 1000:
            self._past_states.pop(0)

    def reset(self):
        """reset.

        Reset the simulation back to its original state.

        """
        self._state = self._initial_state.copy()
        self._past_states = []

    def update(self, T, num_updates=1):
        """update.

        Update the simulation at temperature ``T``. Updates the internal state,
        and returns a set of the spins that were flipped.

        Parameters
        ----------
        T : number >= 0.
            Temperature.
        num_updates : int >= 1 (optional, defaults to 1).
            The number of times to update.

        Returns
        -------
        flipped : set.
            A set of the spins that were flipped.

        """
        flipped = set()
        if num_updates < 0:
            raise ValueError("Cannot update a negative number of times")
        elif num_updates > 1:
            for _ in range(num_updates):
                f = self.update(T)
                for spin in f:
                    if spin in flipped:
                        flipped.remove(spin)
                    else:
                        flipped.add(spin)
        elif num_updates == 1:
            self._add_past_state(self.state)
            for _ in range(self._length):
                i = random.randint(0, self._length-1)
                E = self._subgraphs[i].value(self._state)
                self._state[i] *= -1  # flip the spin
                E_flip = self._subgraphs[i].value(self._state)

                dE = E_flip - E
                if dE < 0 or (T and random.random() < exp(-dE / T)):
                    flipped.add(i)
                else:  # flip the spin back
                    self._state[i] *= -1

        return flipped

    def schedule_update(self, schedule):
        """schedule_update.

        Update the simulation with a schedule.

        Parameters
        ----------
        schedule : tuple of tuples.
            Each element in ``schedule`` is a pair ``(T, n)`` which designates
            a temperature and a number of updates. See `Notes` below.

        Returns
        -------
        flipped : set.
            A set of the spins that were flipped after updating.

        Notes
        -----
        The following two code blocks perform exactly the same thing (except
        that the final ``flipped`` will be different).

        >>> sim = IsingSimulation(10)
        >>> for T in (3, 2):
        >>>     sim.update(T, 100)
        >>> sim.update(1, 50)

        >>> sim = IsingSimulation(10)
        >>> schedule = (3, 100), (2, 100), (1, 50)
        >>> sim.schedule_update(schedule)

        """
        flipped = set()
        for T, n in schedule:
            f = self.update(T, n)
            for spin in f:
                if spin in flipped:
                    flipped.remove(spin)
                else:
                    flipped.add(spin)

        return flipped


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    N = 100
    sim = IsingSimulation(N)
    for T in range(5, 0, -1):
        sim.update(T, num_updates=N)

    past_states = sim.get_past_states(100)

    spins = list(range(1, N))
    correlations = [
        sum(s[0] * s[i] for s in past_states) / len(past_states)
        for i in spins
    ]

    plt.plot(spins, correlations, 'o-')
    plt.xlabel('distance')
    plt.ylabel('correlation')
    plt.show()
