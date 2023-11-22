"""
Collection of different tests for PauliComposer and PauliDecomposer classes.

See: https://arxiv.org/abs/2301.00560
"""
import ctypes
import numpy as np
from time import time
from numpy.random import rand
#from qiskit.quantum_info import SparsePauliOp
#from pennylane import pauli_decompose
import datetime

from solution.py.base_solution.utils import PAULI_LABELS
from solution.py.parallel_solution.pauli_composer import  ParallelPauliComposer
from solution.py.parallel_solution.pauli_composer_diag import  ParallelDiagPauliComposer

from solution.py.base_solution.pauli_composer_py import PauliComposer, PauliDiagComposer
from solution.py.pauli_decomposer import PauliDecomposer



##### PC/PDC #####
def pc_pdc_test(reps: int, n0=2, nf=31) -> None:
    '''
    Check times for the Pauli composer from n=n0 to n=nf repeating reps times
    '''

    for n in range(n0, nf, 1):
        # comp = ''.join(np.random.choice(['I',  'X', 'Z'], n))  # PC
        comp = ''.join(np.random.choice(['I',   'Z'], n))  # PDC
        t = time()
        for _ in range(reps):
            m2 = ParallelDiagPauliComposer(comp)
            # m1 = PauliDiagComposer(comp)
            # for i in range (0, m1.dim):
                # if (m1.col[i] != m2.col[i]):
                #     print(f"ColError: En la posicion {i} parallelPauliComposer calculo  {m2.col[i] } pero deberia ser  {m1.col[i]}")
                # if (m1.mat[i] != m2.mat[i]):
                #     print(f"RealError: En la posicion {i} parallelPauliComposer calculo  {m2.mat[i]}  pero deberia ser  {m1.mat[i]}")
        print('n=%i %.10f s' % (n, (time() - t)/reps))

pc_pdc_test(10, 1, 31) 


##### DECOMPOSER #####
def ham_decompose_test(
    form: str, init: int = 2, end: int = 11, reps: int = 3
    ) -> None:
    """Check times for the Pauli Decomposer. Take into account that for n=9 it takes quite some time for Qiskit and Pennylane
    form (str) = Whether the matrices to be generated are non hermitian ('N'), hermitian ('H'), symmetric ('S') or diagonal ('D')"""
    form = form.capitalize()

    # Build random hamiltonians
    nh = lambda n, a=5: 2*a*rand(1<<n, 1<<n)+2*a*1j*rand(1<<n, 1<<n)-a-a*1j
    ns = lambda n, a=5: 2*a*rand(1<<n, 1<<n)-a
    h = lambda H: np.array(np.matrix(H)+np.matrix(H).H)
    s = lambda H: np.array(np.matrix(H)+np.matrix(H).T)
    d = lambda H, a=10: np.diag(2*a*H-a)

    flag = False
    for n in range(init, end):
        print()
        if form == 'N':
            H = nh(n,a=10)
            flag = True  # PennyLane only works with hermitian hamiltonians
        elif form == 'H':
            aux_H = nh(n)
            H = h(aux_H)
        elif form == 'S':
            aux_H = ns(n)
            H = s(aux_H)
        else:
            H = d(rand(1<<n))
        t=time()
        for _ in range(reps):
            dec = PauliDecomposer(H)
        # print('PC (n=%i): %i min %i s' % (n, *divmod(time()-t, 60)))
        print('PC (n=%i): %.5f s' % (n, (time()-t)/reps))
        t=time()
        for _ in range(reps):
            dec = SparsePauliOp.from_operator(H)
        print('Qiskit (n=%i): %.5f s' % (n, (time()-t)/reps))
        if not flag:
            t=time()
            for _ in range(reps):
                dec = decompose_hamiltonian(H)
            print('PennyLane (n=%i): %.5f s' % (n, (time()-t)/reps))


##### DIAGONAL HAMILTONIAN #####
def strings(n: int, w_ones, w_twos):
    """."""
    base = ['I']*n
    hp_terms = 0
    for i in range(n):
        base_one = list(base)
        base_one[i] = 'Z'
        hp_terms += PauliDiagComposer(''.join(base_one), w_ones[i]).mat
        for j in range(i+1, n):
            base_two = list(base_one)
            base_two[j] = 'Z'
            hp_terms += PauliDiagComposer(''.join(base_two), w_twos[i, j]).mat
    return hp_terms

def strings_2(n: int, w_ones, w_twos):
    """."""
    base = ['I']*n
    hp_terms = 0
    for i in range(n):
        base_one = list(base)
        base_one[i] = 'Z'
        hp_terms += w_ones[i] * PauliDiagComposer(''.join(base_one)).mat
        for j in range(i+1, n):
            base_two = list(base_one)
            base_two[j] = 'Z'
            hp_terms += w_twos[i, j] * PauliDiagComposer(''.join(base_two)).mat
    return hp_terms




