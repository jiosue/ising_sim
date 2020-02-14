"""_gui.py.

This file contains the class GUI which contains the graphics functionality
for the Ising simulation.

"""

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


__all__ = 'GUI',


COLORS = {1: "yellow", -1: "green"}
HELP = "Yellow is a positive spin, green is a negative spin."


class GUI(tk.Tk):
    """GUI.

    The main class for the graphics. It inherits from tk.Tk.

    """

    def __init__(self, length, *args, **kwargs):
        """__init__.

        args and kwargs are sent into tk.Tk.__init__.

        Parameters
        ----------
        length : int > 0.
            Length of the 1D Ising chain.

        """
        self._length = length
        super().__init__(*args, **kwargs)
        width = kwargs.get("width", 600)
        height = kwargs.get("height", 25)
        self.title("Ising Simulation")

        tk.Label(self, text=HELP).pack()

        # canvas and spins
        self._can = tk.Canvas(self, width=width, height=height)
        self._can.pack()

        w = int(round(width / length))
        self._spins = {
            i: self._can.create_rectangle(2+w*i, 2, 2+w*(i+1), height)
            for i in range(length)
        }

        # correlation plot
        fig = plt.figure()
        self._plot = FigureCanvasTkAgg(fig, master=self)
        self._plot.get_tk_widget().pack()
        self._corr = fig.add_subplot(111)

        # Temperature widget
        self._temp = tk.Scale(
            self, label='temperature', from_=0, to=5, orient=tk.HORIZONTAL,
            length=200, resolution=0.1
        )
        self._temp.pack()

    @property
    def length(self):
        """length.

        Return
        ------
        length : int.
            The length of the chain.

        """
        return self._length

    def update_correlation(self, correlation):
        """update_correlation.

        Update the plot of the correlation as a function of distance.

        Parameters
        ----------
        correlation : list.
            A list of correlations. ``len(correlation) = self.length``.

        """
        self._corr.clear()
        self._corr.plot(range(self._length), correlation)
        self._corr.set_xlabel("distance")
        self._corr.set_ylabel("avg correlation to spin 0")
        self._corr.set_xlim([-1, self._length])
        self._corr.set_ylim([-1.1, 1.1])
        self._plot.draw()

    def set_state(self, state):
        """set_state.

        Draw the state.

        Parameters
        ----------
        state : dict.
            ``state`` maps a spin label to its value in {1, -1}.

        """
        for i in range(self._length):
            self._can.itemconfig(self._spins[i], fill=COLORS[state[i]])

    def get_temperature(self):
        """get_temperature.

        Get the temperature that the user has set with the slider.

        Returns
        -------
        T : float.

        """
        return self._temp.get()

    def destroy(self):
        """destroy.

        Override the existing ``destroy`` function to include ``quit``. There
        is a weird bug upon closing sometimes if you don't do this.

        """
        self.quit()
        super().destroy()


if __name__ == "__main__":
    root = GUI(100)
    root.update_correlation([1]*50 + [-1]*50)
    state = {i: 1 for i in range(90)}
    state.update({i: -1 for i in range(90, 100)})
    root.set_state(state)
    print(root.get_temperature())
    root.mainloop()
