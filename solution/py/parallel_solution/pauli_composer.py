"""
Parallel Pauli(Diag)Composer class definition.

See: https://arxiv.org/abs/2301.00560
"""

import ctypes
import warnings
import numpy as np
import scipy.sparse as ss
# from mask import ComplexNumber, RealNumber
from numbers import Number
from solution.py.parallel_solution.utils import BINARY
from solution.py.parallel_solution.mask import ComplexNumber, RealNumber

warnings.simplefilter('ignore', np.ComplexWarning)

class ParallelPauliComposer:
    """Class that computes the tensor product of Pauli Matrices"""

    def __init__(self, entry: str, weight: Number = 1):
        """
        entry (str)     = string that defines the Pauli matrix, i.e: XXXX
        weight (Number) = coefficient that multiplies the matrix
        """
        
        n = len(entry)
        self.n = n
        self.dim = 1<<n 

        self.entry = entry.upper()
        self.paulis = list(set(self.entry))

        mat_ent = {0: 1, 1: -1j, 2: -1, 3: 1j}
        c_ent = {0: '1', 1: '0', 2: '0', 3: '1'}

        self.ny = self.entry.count('Y') & 3
        init_ent = mat_ent[self.ny]
        c_init_ent = c_ent[self.ny]

        self.init_entry = init_ent
        self.iscomplex = np.iscomplex(init_ent)

        self.lib_pauli_composer = ctypes.CDLL('solution/c/pauli_composer.so')

        col = (ctypes.c_uint * self.dim)()
        real = (ctypes.c_char * self.dim)()

        entry_lwr = self.entry.lower().encode()
        result = self.lib_pauli_composer.pauli_composer(entry_lwr, 
            ctypes.c_int(self.n), ctypes.c_bool(self.iscomplex),
            ctypes.c_char(c_init_ent.encode()), 
            col, real) 

        self.col = col
        if (self.iscomplex):
            self.__val__ = real
            self.mat=ComplexNumber(self.__val__, weight)
        else:
            self.__val__= real
            self.mat=RealNumber(self.__val__, weight)


    def to_sparse(self):
        """Convert to scipy csr matrix"""
        self.row = np.arange(self.dim)
        return ss.csr_matrix((self.mat, (self.row, self.col)),
                             shape=(self.dim, self.dim))

    def to_matrix(self):
        """Convert to numpy array"""
        return self.to_sparse().toarray()



