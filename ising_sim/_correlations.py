"""_correlations.py.

Compute the correlations.

"""

__all__ = 'compute_correlations',


def compute_correlations(states):
    """compute_correlations.

    Calculate the average correlation of spin 0 and every other spin.

    Parameters
    ----------
    states : list of states.
        ``len(states)`` must be >= 1!

    Returns
    -------
    correlations : list of floats.

    """
    return [
        sum(s[0] * s[i] for s in states) / len(states)
        for i in range(len(states[0]))
    ]
