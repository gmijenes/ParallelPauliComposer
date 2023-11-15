"""
Pauli(Diag)Composer class definition.

See: https://arxiv.org/abs/2301.00560
"""

import warnings
import numpy as np
import scipy.sparse as ss
from numbers import Number
# from mask import ComplexNumber, RealNumber
from  solution.py.parallel_solution.utils import BINARY
from  solution.py.parallel_solution.mask import ComplexNumber, RealNumber


# Ignore ComplexWarning
warnings.simplefilter('ignore', np.ComplexWarning)


class ParallelDiagPauliComposer:
    """Class that computes the tensor product of Pauli Matrices"""

    def __init__(self, entry: str, weight: Number = 1):
        """
        entry (str)     = string that defines the Pauli matrix, i.e: XXXX
        weight (Number) = coefficient that multiplies the matrix
        """
        # Compute the length of the string
        n = len(entry)
        self.n = n

        # Compute helpful powers (using bitshift because it's faster)
        self.dim = 1<<n #self.dim = 1 *2^n

        # Store the entry (Pauli word) converting the Pauli labels into uppercase
        self.entry = entry.upper()
        self.paulis = list(set(self.entry))

        import ctypes

        self.lib_pauli_composer = ctypes.CDLL('solution/c/.so/pauli_composer_diag.so')
        
        col = (ctypes.c_int * self.dim)()
        real = (ctypes.c_float * self.dim)()

        entry_lwr = self.entry.lower().encode()

        result = self.lib_pauli_composer.pauli_composer(entry_lwr, 
            ctypes.c_int(self.n), ctypes.c_float(1), real) 

        
        self.__val__= real
        self.mat=RealNumber(self.__val__, weight)




