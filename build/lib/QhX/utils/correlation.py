"""
This module provides functions for calculating correlations between n-dimensional arrays.
"""

import numpy as np

def correlation_nd(A, B):
    """
    Computes the correlation between two n-dimensional arrays, A and B.

    Parameters:
        A (ndarray): First input array with shape (n, m).
        B (ndarray): Second input array with shape (n, m).

    Returns:
        ndarray: The correlation matrix between A and B.
    """

    # Row-wise mean of input arrays & subtract from input arrays themselves
    A_mA = A - A.mean(1)[:, None]
    B_mB = B - B.mean(1)[:, None]

    # Compute and return the correlation matrix
    return np.dot(A_mA, B_mB.T)
