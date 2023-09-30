"""
PauliDecomposer class definition.

See: https://arxiv.org/abs/2301.00560
"""

import warnings
import numpy as np
import itertools as it

from utils import PAULI_LABELS
from pauli_composer import PauliComposer, PauliDiagComposer


# Ignore ComplexWarning
warnings.simplefilter('ignore', np.ComplexWarning)


class PauliDecomposer:
    """PauliDecomposer class definition."""

    def __init__(self, H: np.ndarray):
        """Initialize PauliDecomposer class."""
        # Check if all the given hamiltonian elements are real
        self.real_H = np.any(np.isreal(H))
        self.sym = self.real_H and np.all(H == H.T)

        # Number of rows and columns of the given hamiltonian
        row, col = H.shape[0], H.shape[1]

        # The hamiltonian must be a squared-one with 2**n x 2**n entries
        n_row, n_col = np.log2(row), np.log2(col)
        n = int(np.ceil(max(n_row, n_col)))
        size = 1<<n
        if row != col or not n_row.is_integer() or not n_col.is_integer():
            # Matrix with 2**n x 2**n zeros
            if self.real_H:
                square_H = np.zeros((size, size))
            else:
                square_H = np.zeros((size, size), dtype=complex)
            # Overlap the original hamiltonian in the top-left corner
            square_H[:row, :col] = H
            H = square_H
        self.H = H

        # Compute rows
        rows = np.arange(1<<n)

        # If the matrix is diagonal, only sigma_0=I and sigma_3=sigma_z are
        # relevant
        flag_diag = False
        if (self.H == np.diag(np.diagonal(self.H))).all():
            iterable = [PAULI_LABELS[0], PAULI_LABELS[3]]
            flag_diag = True
        else:
            iterable = PAULI_LABELS

        # Compute possible combinations
        combs = it.product(iterable, repeat=n)
        # If all entries are real, avoid an odd number of sigma_2=sigma_y
        if self.sym:
            combs = filter(lambda x: x.count('Y') % 2 == 0, combs)

        # Store coefficients in a dictionary where the keys will be the labels
        # of the compositions and the values will be the associated constants
        coefficients = {}
        if flag_diag:
            H_diag = np.diag(H)
            for comb in combs:
                # Compute the diagonal terms and add them iteratively. Since
                # only one term of each Pauli composition is not zero row by
                # row, we can avoid handling zeros just pointing out to the only
                # non-zero term. Of course, we can avoid multiply by 1 also
                value = 0
                # Return the Kronecker product of the Pauli matrices and the
                # positions of the non-zero entries
                entry = ''.join(comb)
                pauli_comp = PauliDiagComposer(entry)
                ent = pauli_comp.mat
                for r in rows:
                    coef = ent[r]
                    if coef == 1:
                        value += H_diag[r]
                    elif coef == -1:
                        value -= H_diag[r]
                    else:
                        value += coef * H_diag[r]
                # Store only non-zero values
                if value != 0:
                    # Transform non-complex values into float
                    if not np.iscomplex(value):
                        value = float(value)
                    # Divide by 2**n
                    coefficients[entry] = value / size
        else:
            for comb in combs:
                value = 0
                # Return the Kronecker product of the Pauli matrices and the
                # positions of the non-zero entries
                entry = ''.join(comb)
                if all({comb}) in {'I', 'Z'}:
                    pauli_comp = PauliDiagComposer(entry)
                else:
                    pauli_comp = PauliComposer(entry)
                cols, ent = pauli_comp.col, pauli_comp.mat
                for r in rows:
                    coef = ent[r]
                    if coef == 1:
                        value += H[cols[r], r]
                    elif coef == -1:
                        value -= H[cols[r], r]
                    else:
                        value += coef * H[cols[r], r]
                # Store only non-zero values
                if value != 0:
                    # Transform non-complex values into float
                    if not np.iscomplex(value):
                        value = float(value)
                    # Divide by 2**n
                    coefficients[entry] = value / size

        self.coefficients = coefficients


if __name__ == '__main__':
    # Hamiltonian source: https://arxiv.org/abs/2111.00627v1
    hamiltonian = np.array([[-0.43658111, -4.28660705, 0],
                            [-4.28660705, 12.15, -7.82623792],
                            [0, -7.82623792, 19.25]])
    # hamiltonian = np.array([
    #     [1,1-1j],
    #     [1-1j,1]
    # ])
    print('----- Decomposition coefficients -----')
    print(PauliDecomposer(hamiltonian).coefficients)
