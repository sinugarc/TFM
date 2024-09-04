from QCRMut import *
from shareFunctions import xor, sumgate

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

def Simon_Alg_MT(n:int) -> QuantumCircuit:
    
    qs=QuantumRegister(n, 's')
    anc=QuantumRegister(n, 'anc')
    qc = QuantumCircuit(qs, anc)

    qc.h(qs)

    qc.barrier()
    qc.append(PlaceHolder(qc.num_qubits, qc.qubits))
    qc.barrier()
    
    qc.h(qs) 
    
    qc.name = f"{n} qubit Simon"
    
    return qc

def simon_oracle(b:str) -> QuantumCircuit:
    """
    Returns a Simon oracle for bitstring b
    
    Ref: @book{qiskitextbook2023,   
        author = {various authors},   
        year = {2023},   
        title = {Qiskit Textbook},   
        publisher = {Github},   
        url = {https://github.com/Qiskit/textbook}, 
    }
    """
    b = b[::-1] # reverse b for easy iteration
    n = len(b)
    qc = QuantumCircuit(n*2)
    # Do copy; |x>|0> -> |x>|x>
    for q in range(n):
        qc.cx(q, q+n)
    if '1' not in b: 
        return qc  # 1:1 mapping, so just exit
    i = b.find('1') # index of first non-zero bit in b
    # Do |x> -> |s.x> on condition that q_i is 1
    for q in range(n):
        if b[q] == '1':
            qc.cx(i, (q)+n)
    return qc

def Simon_QC2(mutant:QuantumCircuit, inp: str) -> QuantumCircuit:

    assert mutant.num_qubits % 2 == 0
    
    n = mutant.num_qubits//2
    
    # Testing circuit generation
           
    qs1=QuantumRegister(n, 's1')
    anc1=QuantumRegister(n, 'anc1')
    qs2=QuantumRegister(n, 's2')
    anc2=QuantumRegister(n, 'anc2')
    c_test=ClassicalRegister(n, 'c_test')
    qc = QuantumCircuit(qs1, anc1, qs2, anc2, c_test)
    
    # Mutated circuits added to Testing circuit
    
    f_s=simon_oracle(inp)
    aux=mutant.copy()
    placeHolderSwap(aux,f_s)
    gate_s = aux.to_instruction()
    gate_s.name=f'  Simon_oracle  \n \ns={inp}'
    qc.append(gate_s, qs1[:]+anc1[:])
    qc.append(gate_s, qs2[:]+anc2[:])
    
    qc.barrier()
    
    # Outputs relation for Simon MR1
    
    output_relation = sumgate(n).to_instruction(label=' Simon \n\n Metamorphic \n\n Relation 1')
    qc.append(output_relation, qs1[:]+qs2[:])
    
    # Measurement
    qc.measure(qs2, c_test)
    
    return qc

def Simon_QC(mutant:QuantumCircuit, inp: str, inverse: bool = False) -> QuantumCircuit:

    assert mutant.num_qubits % 2 == 0
    
    n = mutant.num_qubits//2
    
    # Testing circuit generation
           
    qs=QuantumRegister(n, 's')
    anc=QuantumRegister(n, 'anc1')
    c_test=ClassicalRegister(n, 'c_test')
    qc = QuantumCircuit(qs, anc, c_test)
    
    # Oracle added to Testing circuit
    
    f_s=simon_oracle(inp)
    aux=mutant.copy()
    placeHolderSwap(aux,f_s)
    gate_s = aux.to_instruction()
    gate_s.name=f'  Simon_oracle  \n \ns={inp}'
    qc.append(gate_s, qs[:]+anc[:])
    
    qc.barrier()
    
    # Outputs relation for Simon MR (key-checks, Post-Measurement)
    
    # Measurement
    if inverse:
        qc.measure(qs, c_test[::-1])
    else:
        qc.measure(qs, c_test)
    
    return qc

def Simon_MR1 (mutant: QuantumCircuit, inp: str) -> list[QuantumCircuit]:
    QC1 = Simon_QC(mutant, inp)
    QC2 = Simon_QC2(mutant, inp)
    return [QC1,QC2]

def Simon_MR2 (mutant: QuantumCircuit, inp: str) -> list[QuantumCircuit]:
    QC1 = Simon_QC(mutant, inp)
    QC2 = Simon_QC(mutant, inp, inverse = True)
    return [QC1,QC2]

def Simon_analysis (results: list[dict[str,int]]) -> bool:
    
    return (results[0].keys() != results[1].keys())