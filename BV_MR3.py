from MutantTool import Placeholder, QCSetUp
from basicFunctions import xor

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit import Instruction
from qiskit.circuit.gate import Gate

def BV_Alg_MT(n):
    
    qs=QuantumRegister(n, 's')
    anc1=QuantumRegister(1, 'anc1')
    qc = QuantumCircuit(qs, anc1)

    for i in range(n+1):
        qc.h(i)
    qc.z(n)

    qc.barrier()
    qc.append(Placeholder(qc.num_qubits, qc.qubits))
    qc.barrier()
    
    for i in range(n):
        qc.h(i)
    
    return qc

def BV_Oracle_Generator(s:str) -> QuantumCircuit:
    n=len(s)
    qc=QuantumCircuit(n+1)
    s = s[::-1]
    for q in range(n):
        if s[q] == '0':
            qc.i(q)
        else:
            qc.cx(q, n)
    return qc

def sumgate(n: int) -> QuantumCircuit:
    qubits=3*n+2
    qc = QuantumCircuit(qubits)
    for i in range(n):
        qc.cx(i,2*(n+1)+i)
        qc.cx(n+1+i,2*(n+1)+i)
    return qc

def BV_TestMT3_Output(qc: QuantumCircuit, n: int):
    suma = sumgate(n)
    sgate = suma.to_instruction(label='  Metamorphic \n\n Relation \n\n Outputs')
    qc.append(sgate, range(3*n+2))
    for i in range(n):
        qc.measure(2*(n+1)+i, i)
        
def BV_TestMT3_Input(s : str) -> Instruction:
    auxqc=QuantumCircuit(len(s))
    for i in range(len(s)):
        if s[i]=="1":
            auxqc.x(i)
    inp = auxqc.to_instruction(label='  Metamorphic \n\n Relation \n\n Inputs')
    return inp

def BV_MT3(mutant:QuantumCircuit, inputs: [str]) -> QuantumCircuit:

    assert len(inputs)==2
    
    n = mutant.num_qubits-1
           
    qs=QuantumRegister(n, 's')
    anc1=QuantumRegister(1, 'anc1')
    qs1=QuantumRegister(n, 's1')
    anc2=QuantumRegister(1, 'anc2')
    q_test=QuantumRegister(n, 'q_test')
    c_test=ClassicalRegister(n, 'c_test')
    qc = QuantumCircuit(qs, anc1, qs1, anc2, q_test, c_test)
    
    f_s=BV_Oracle_Generator(inputs[0])
    gate_s = QCSetUp(mutant,f_s)
    gate_s.name='  BV_s  \n \ns='+ inputs[0]
    qc.append(gate_s, range(n+1))
    
    f_s1=BV_Oracle_Generator(inputs[1])
    gate_s1 = QCSetUp(mutant,f_s1)
    gate_s1.name='  BV_s1  \n \ns1=' + inputs[1]
    qc.append(gate_s1, range(n+1,2*n+2))

    inp=BV_TestMT3_Input(xor(inputs[0],inputs[1]))
    qc.append(inp,q_test)
    
    qc.barrier()
    
    BV_TestMT3_Output(qc,n)
    
    qc.draw(output='mpl')
    
    return qc