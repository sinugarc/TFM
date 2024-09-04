import random
import numpy as np

from typing import Union

from math import comb
from itertools import combinations

from QCRMut import *
from shareFunctions import xor

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

def DJ_Alg_MT(n:int) -> QuantumCircuit:
    
    qs=QuantumRegister(n, 's')
    anc=QuantumRegister(1, 'anc')
    qc = QuantumCircuit(qs, anc)
    
    qc.x(n)
    qc.h(n)

    for i in range(n): qc.h(i)
        
    qc.append(PlaceHolder(qc.num_qubits, qc.qubits))
    
    for i in range(n): qc.h(i) 
    
    qc.name = f"{n} qubit DJ"
    
    return qc

def DJ_oracle(num_qubits:int, flip_outp: int, constant: int, on_states:list[int]) -> QuantumCircuit:
    """
    Create a random Deutsch-Jozsa function.
    https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/
                            quantum-query-algorithms#the-deutsch-jozsa-algorithm
    """

    qc = QuantumCircuit(num_qubits + 1)
    
    """
    if np.random.randint(0, 2):
        # Flip output qubit with 50% chance
        qc.x(num_qubits)
    """
    
    if flip_outp:
        qc.x(num_qubits)
        
    """
    if np.random.randint(0, 2):
        # return constant circuit with 50% chance
        return qc
    """
    
    if constant:
        return qc
    
    """
    # next, choose half the possible input states
    on_states = np.random.choice(
        range(2**num_qubits),  # numbers to sample from
        2**num_qubits // 2,  # number of samples
        replace=False,  # makes sure states are only sampled once
    )
    """

    def add_cx(qc, bit_string):
        for qubit, bit in enumerate(reversed(bit_string)):
            if bit == "1":
                qc.x(qubit)
        return qc

    for state in on_states:
        #qc.barrier()  # Barriers are added to help visualize how the functions are created. They can safely be removed.
        qc = add_cx(qc, f"{state:0b}")
        qc.mcx(list(range(num_qubits)), num_qubits)
        qc = add_cx(qc, f"{state:0b}")

    #qc.barrier()

    return qc

def DJ_input_generator(num_qubits:int, num_inputs:int = 64) -> list[tuple[int, # flip output bit
                                                                          int, # constant or balance
                                                                          tuple[int, ...] # define the oracle when balance
                                                                          ]]:
    
    assert num_inputs > 3 # We would like to cover all possibilities at least once. 
    
    possible_inputs = comb(2**num_qubits, 2**(num_qubits-1)) + 2
    
    if num_inputs >= possible_inputs:
        input_list = [(0,1,()),(1,1,())] + list(map(lambda x: (random.randint(0,1),0,x),list(combinations(range(2**num_qubits),2**(num_qubits-1)))))
    
    else:
        input_set=set()
        
        while len(input_set) < (num_inputs - 2):
            f_input = tuple(sorted(random.sample(range(2**num_qubits), 2**(num_qubits-1))))
            input_set.add(f_input)
        
        input_list = list(map(lambda x: (random.randint(0,1),0,x),list(input_set))) + [(0,1,()),(1,1,())]
    random.shuffle(input_list)
    return input_list
                                                                  
def perm(num_qubits:int) -> list[int]:
    p = list(range(num_qubits))
    random.shuffle(p)
    return tuple(p)

def DJ_input_generator_MR1(num_qubits:int, num_inputs:int = 32) -> list[tuple[tuple[int,int, tuple[int, ...]], # DJ_input_generator
                                                                              tuple[int, ...] # permutation
                                                                              ]]:
    
    half_input_list = DJ_input_generator(num_qubits, num_inputs)
    input_list = list(map(lambda x: (x,perm(num_qubits)),half_input_list))
    
    return input_list

def DJ_MR1(mutant:QuantumCircuit, inp: tuple[tuple[int,int,tuple[int, ...]],tuple[int, ...]]) -> list[QuantumCircuit]:

    # Do we need to undo permutation? We have swap qubits to perfrom the calculation, shouldnt we bring the result back to eh original position?
    # No need as the order of qubits in result does not affect analysis, the only value important on analysis states is 0*
    
    n = mutant.num_qubits-1
    
    qc_list=[]
    
    for i in [0,1]:
        
        qs=QuantumRegister(n, 's')
        anc=QuantumRegister(1, 'anc1')
        c_test=ClassicalRegister(n, 'c_test')
        qc = QuantumCircuit(qs, anc, c_test)
    
        # Inputs added to mutated circuits
        f_s = DJ_oracle(n,*(inp[0]))
    
        aux=mutant.copy()
        
        if i:
            placeHolderSwap(aux,f_s)
            gate_s = aux.to_instruction()
            gate_s.name=f'  DJ_oracle  \n \nInput\n{inp[0]}'
            
        else:
            permutation = Permutation(n, pattern=inp[1])
            perm_f_s=f_s.compose(permutation,range(n),front=True)
            placeHolderSwap(aux,perm_f_s)
            gate_s = aux.to_instruction()
            gate_s.name=f'  DJ_oracle  \n \nInput\n{inp[0]}\n\nPerm\n{inp[1]}'
        
        qc.append(gate_s,qs[:]+anc[:])
        
        qc.measure(qs, c_test)
        
        qc_list.append(qc)
    
    return qc_list

def DJ_MR2(mutant:QuantumCircuit, inp: tuple[int,int,tuple[int, ...]]) -> list[QuantumCircuit]:
    
    n = mutant.num_qubits-1
    
    associated_input = (xor(str(inp[0]),"1"),inp[1],inp[2])
    
    inputs = [inp,associated_input]
    
    qc_list=[]
    
    for i in [0,1]:
           
        qs=QuantumRegister(n, 's')
        anc=QuantumRegister(1, 'anc1')
        c_test=ClassicalRegister(n, 'c_test')
        qc = QuantumCircuit(qs, anc, c_test)
        
        aux=mutant.copy()
        f_s = DJ_oracle(n,*(inputs[i]))
        placeHolderSwap(aux,f_s)
        gate_s = aux.to_instruction()
        gate_s.name=f'  DJ_oracle  \n \nInput\n{inputs[i]}'
        qc.append(gate_s,qs[:]+anc[:])
        
        qc.measure(qs, c_test)
        
        qc_list.append(qc)
    
    return qc_list

def DJ_analysis(results: list[dict[str,int]]) -> bool:
    
    assert len(results) > 0
    
    num_qubits = len(list(results[0].keys())[0])
    expected_result = "0" * num_qubits
    
    if expected_result not in results[0].keys(): # Circuit 1 is balance
        killed = expected_result in results[1].keys()
        # Circuit 2 is cte or non-valid
        
    elif len(results[0].keys()) == 1: # Circuit 1 is constant
        killed = len(results[1].keys()) > 1 or expected_result not in results[1].keys()
        # Circuit 2 is non-valid or balance
        
    else: # Circuit 1 issues a non-valid result
        killed = True
    
    return killed


# Function and class obtained from Qiskit, not implement it in the current version used.

from qiskit.circuit.quantumcircuit import Gate
from qiskit.circuit.exceptions import CircuitError

"""
https://github.com/Qiskit/qiskit/blob/stable/1.1/qiskit/synthesis/permutation/permutation_utils.py
"""
    
def _get_ordered_swap(permutation_in):
    """Sorts the input permutation by iterating through the permutation list
    and putting each element to its correct position via a SWAP (if it's not
    at the correct position already). If ``n`` is the length of the input
    permutation, this requires at most ``n`` SWAPs.

    More precisely, if the input permutation is a cycle of length ``m``,
    then this creates a quantum circuit with ``m-1`` SWAPs (and of depth ``m-1``);
    if the input  permutation consists of several disjoint cycles, then each cycle
    is essentially treated independently.
    """
    permutation = list(permutation_in[:])
    swap_list = []
    index_map = _inverse_pattern(permutation_in)
    for i, val in enumerate(permutation):
        if val != i:
            j = index_map[i]
            swap_list.append((i, j))
            permutation[i], permutation[j] = permutation[j], permutation[i]
            index_map[val] = j
            index_map[i] = i
    swap_list.reverse()
    return swap_list


def _inverse_pattern(pattern):
    """Finds inverse of a permutation pattern."""
    b_map = {pos: idx for idx, pos in enumerate(pattern)}
    return [b_map[pos] for pos in range(len(pattern))]


"""
https://github.com/Qiskit/qiskit/blob/stable/1.1/qiskit/circuit/library/generalized_gates/permutation.py#L27-L94
"""

class Permutation(QuantumCircuit):
    """An n_qubit circuit that permutes qubits."""

    def __init__(
        self,
        num_qubits: int,
        pattern: Union[list[int], np.ndarray, None] = None,
        seed: Union[int, None] = None,
    ) -> None:
        """Return an n_qubit permutation circuit implemented using SWAPs.

        Args:
            num_qubits: circuit width.
            pattern: permutation pattern, describing which qubits occupy the
                positions 0, 1, 2, etc. after applying the permutation, that
                is ``pattern[k] = m`` when the permutation maps qubit ``m``
                to position ``k``. As an example, the pattern ``[2, 4, 3, 0, 1]``
                means that qubit ``2`` goes to position ``0``, qubit ``4``
                goes to the position ``1``, etc. The pattern can also be ``None``,
                in which case a random permutation over ``num_qubits`` is
                created.
            seed: random seed in case a random permutation is requested.

        Raises:
            CircuitError: if permutation pattern is malformed.

        Reference Circuit:
            .. plot::

               from qiskit.circuit.library import Permutation
               A = [2,4,3,0,1]
               circuit = Permutation(5, A)
               circuit.draw('mpl')

        Expanded Circuit:
            .. plot::

               from qiskit.circuit.library import Permutation
               from qiskit.visualization.library import _generate_circuit_library_visualization
               A = [2,4,3,0,1]
               circuit = Permutation(5, A)
               _generate_circuit_library_visualization(circuit.decompose())
        """
        if pattern is not None:
            if sorted(pattern) != list(range(num_qubits)):
                raise CircuitError(
                    "Permutation pattern must be some ordering of 0..num_qubits-1 in a list."
                )
            pattern = np.array(pattern)
        else:
            rng = np.random.default_rng(seed)
            pattern = np.arange(num_qubits)
            rng.shuffle(pattern)

        name = "permutation_" + np.array_str(pattern).replace(" ", ",")

        circuit = QuantumCircuit(num_qubits, name=name)

        super().__init__(num_qubits, name=name)

        # pylint: disable=cyclic-import

        for i, j in _get_ordered_swap(pattern):
            circuit.swap(i, j)

        all_qubits = self.qubits
        self.append(circuit.to_gate(), all_qubits)