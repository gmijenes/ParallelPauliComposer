"""
Pauli(Diag)Composer class definition.

See: https://arxiv.org/abs/2301.00560
"""

import warnings
import numpy as np
import scipy.sparse as ss
from numbers import Number

from utils import BINARY


# Ignore ComplexWarning
warnings.simplefilter('ignore', np.ComplexWarning)

class ComplexNumber:
    def __init__(self, imag):
        self.imag = imag
    def __getitem__(self, i):
        return np.complex(0, self.imag[i])

class ParallelPauliComposer:
    """Class that computes the tensor product of Pauli Matrices"""

    def __init__(self, entry: str, weight: Number = None):
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
        
        # Define a dictionary with the possible values of the first element precomputed
        # (-i)**(0+4m)=1, (-i)**(1+4m)=-i, (-i)**(2+4m)=-1, (-i)**(3+4m)=i
        mat_ent = {0: 1, 1: -1j, 2: -1, 3: 1j}

        # Count the number of ny mod 4
        self.ny = self.entry.count('Y') & 3
        init_ent = mat_ent[self.ny]
        # If weight is not none, multiply it
        if weight is not None:
            # first non-zero entry
            init_ent *= weight
        self.init_entry = init_ent
        self.iscomplex = np.iscomplex(init_ent)

        

        import ctypes

        # Cargamos la libreria 
        self.lib_pauli_composer = ctypes.CDLL('./pauli_composer.so')

        # Definimos los tipos de los argumentos de la función 
        #lib_pauli_composer.pauli_composer.argtypes = (ctypes.c_char_p, ctypes.c_float, ctypes.c_float, ctypes.c_bool, ctypes.c_float,ctypes.c_float,)

        # Definimos el tipo del retorno de la función 
        # lib_pauli_composer.pauli_composer.restype = ctypes.POINTER(ctypes.c_void_p)

        # Creamos nuestra función en Python
        # hace de Wrapper para llamar a la función de C
        
        col = (ctypes.c_int * self.dim)()
        real = (ctypes.c_float * self.dim)()
        img = (ctypes.c_float * self.dim)()

        entry_lwr = self.entry.lower().encode()

        result = self.lib_pauli_composer.pauli_composer(entry_lwr, 
            ctypes.c_int(self.n), ctypes.c_bool(self.iscomplex), ctypes.c_float(init_ent.real),
            ctypes.c_float(init_ent.imag), col, real, img) 
        
            #result_py = ctypes.cast(result_c, ctypes.py_object).value

        # self.col = ctypes.cast(result[0], ctypes.POINTER(ctypes.c_float))
        # if (self.iscomplex):
        #     self.__real__ = ctypes.cast(result[1], ctypes.POINTER(ctypes.c_float))
        #     self.__imag__ = ctypes.cast(result[2], ctypes.POINTER(ctypes.c_float))
        #     self.mat=np.vectorize(self.complex_element)

        # else:
        #     self.mat=ctypes.cast(result[1], ctypes.POINTER(ctypes.c_float))

        self.col = col
        if (self.iscomplex):
            self.__imag__ = img
            self.mat=ComplexNumber(self.__imag__)
        else:
            self.mat=real


    def to_sparse(self):
        """Convert to scipy csr matrix"""
        self.row = np.arange(self.dim)
        return ss.csr_matrix((self.mat, (self.row, self.col)),
                             shape=(self.dim, self.dim))

    def to_matrix(self):
        """Convert to numpy array"""
        return self.to_sparse().toarray()



