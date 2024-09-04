import random

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit import Instruction

from itertools import chain

from QCRMut import *
from shareFunctions import xor, sumgate, input_generator

def BV_Alg_MT(n:int) -> QuantumCircuit:
    
    qs=QuantumRegister(n, 's')
    anc1=QuantumRegister(1, 'anc1')
    qc = QuantumCircuit(qs, anc1)

    for i in range(n+1): qc.h(i)
        
    qc.z(anc1)

    qc.barrier()
    qc.append(PlaceHolder(qc.num_qubits, qc.qubits))
    qc.barrier()
    
    for i in range(n): qc.h(i)
    
    qc.name = f"{n} qubit BV"
    
    return qc

def BV_Oracle_Generator(s:str) -> QuantumCircuit:
    n=len(s)
    qc=QuantumCircuit(n+1)
    s = s[::-1]
    for q in range(n):
        if s[q] != '0':
            qc.cx(q, n)
    return qc

def BV_input_generator_pairs(num_qubits: int, num_max_inputs: int = 64) -> list[list[str]]:
    
    input_list = input_generator(num_qubits, num_max_inputs)
    
    input_pairs = [(input_list[i],input_list[random.randint(0,len(input_list)-1)])for i in range(len(input_list))]
    
    return input_pairs


def BV_input_generator_xor(num_qubits: int, num_max_inputs: int = 64) -> list[list[str]]:
    
    input_list = input_generator(num_qubits, num_max_inputs)
    
    aux = "1" * num_qubits
    input_pairs = [(input_list[i],xor(input_list[i],aux))for i in range(len(input_list))]
    
    return input_pairs

def BV_TestMT_Input(s : str) -> Instruction:
    auxqc=QuantumCircuit(len(s))
    for i in range(len(s)):
        if s[i]=="1":
            auxqc.x(i)
    return auxqc.to_instruction(label='  BV Inputs \n\n Relation ')

def BV_TestMT12_Output(n: int) -> Instruction:
    
    outputTest = QuantumCircuit(3*n)
    
    outputTest.append(sumgate(n),chain(range(n),range(2*n,3*n))) #Adds BV s result to q_test
    outputTest.append(sumgate(n),chain(range(n,2*n),range(2*n,3*n))) #Adds BV r result to q_test
    
    # q_test will be xor(s,r) + BV_s + BV_r, where + is the binary addition
    
    return outputTest.to_instruction(label='  Metamorphic \n\n Relation \n\n BV MR 1&2')

def BV_MR12(mutant:QuantumCircuit, inputs: tuple[str,str]) -> list[QuantumCircuit]:
    
    n = mutant.num_qubits-1
    
    # Testing circuit generation
           
    qs=QuantumRegister(n, 's')
    anc1=QuantumRegister(1, 'anc1')
    qr=QuantumRegister(n, 'r')
    anc2=QuantumRegister(1, 'anc2')
    q_test=QuantumRegister(n, 'q_test')
    c_test=ClassicalRegister(n, 'c_test')
    qc = QuantumCircuit(qs, anc1, qr, anc2, q_test, c_test)
    
    # Inputs relation for BV MR1/2
    
    input_relation=BV_TestMT_Input(xor(inputs[0],inputs[1])) 
    qc.append(input_relation,q_test)
    
    qc.barrier()
    
    # Mutated circuits added to Testing circuit
    
    for i in [0,1]:
        f=BV_Oracle_Generator(inputs[i]) # Oracle creation for input i
        aux=mutant.copy() 
        placeHolderSwap(aux,f) # Replace placeHolder by input i oracle
        gate = aux.to_instruction() # Reduce to instruction
        gate.name=f'  BV_{qc.qregs[2*i].name}  \n\n{qc.qregs[2*i].name} = {inputs[i]}'
        qc.append(gate, qc.qregs[2*i][:]+qc.qregs[2*i+1][:]) # Add BV mutated circuit with input i to test circuit

    qc.barrier()
    
    # Outputs relation for BV MR1/2
    
    output_relation=BV_TestMT12_Output(n)
    qc.append(output_relation,qs[:]+qr[:]+q_test[:])
    
    # Measurement
    
    qc.measure(q_test, c_test)
    
    return [qc]

def BV_MR3(mutant:QuantumCircuit, inputs: [str]) -> list[QuantumCircuit]:

    assert len(inputs)==2
    
    n = mutant.num_qubits-1
    
    # Testing circuit generation
           
    q=QuantumRegister(n, 's+r')
    anc1=QuantumRegister(1, 'anc1')
    q_test=QuantumRegister(n, 'q_test')
    c_test=ClassicalRegister(n, 'c_test')
    qc = QuantumCircuit(q, anc1, q_test, c_test)
    
    # Inputs relation for BV MR1/2
    
    input_relation = BV_TestMT_Input(xor(inputs[0],inputs[1]))
    qc.append(input_relation,q_test)
    
    qc.barrier()
    
    # Mutated circuit added to Testing circuit
    
    auxInp = QuantumCircuit(q, anc1)
    
    for i in [0,1]:
        f=BV_Oracle_Generator(inputs[i])
        auxInp.append(f, q[:]+anc1[:])
    
    aux=mutant.copy()
    placeHolderSwap(aux,auxInp)
    gate = aux.to_instruction()
    gate.name=f'  BV_s+r  \n\ns={inputs[0]}\n\nr={inputs[1]}'
    qc.append(gate, q[:]+anc1[:])
    
    qc.barrier()
    
    # Outputs relation for BV MR3
    
    output_relation = sumgate(n).to_instruction(label='BV \n\n Metamorphic \n\n Relation 3')
    qc.append(output_relation,q[:]+q_test[:])
    
    # Measurement
    
    qc.measure(q_test, c_test)
    
    return [qc]

def BV_analysis (results: list[dict[str,int]]) -> bool:
    
    assert len(results) > 0
    
    num_qubits = len(list(results[0].keys())[0])
    expected_result = "0" * num_qubits
    killed = False
    
    if expected_result not in results[0].keys() or len(results[0].keys())>1:
        killed = True
    
    return killed