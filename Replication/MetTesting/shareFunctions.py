import random
from itertools import product
from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator

def intToBin(n:int,length:int = None) -> str:
    bn=bin(n)[2:]
    if length != None :
        assert len(bn)<= length
        bn = '0'*(length-len(bn))+bn
    return bn

def xor(a:str,b:str) -> str:
    return "".join(str(int(x)) for x in map(lambda s, t : bool(int(s))^bool(int(t)),a,b))

def s_generator(n: int) -> str:
    return "".join(str(random.randint(0,1)) for _ in range(n))

def input_generator (n_qubits: int , num_inputs: int = 64) -> list[str] :
    if 2**n_qubits <= num_inputs:
        input_list = list(map(lambda x : "".join(str(x[i]) for i in range(len(x))), product([0,1],repeat=n_qubits)))
    else:
        input_set = set([s_generator(n_qubits) for _ in range(num_inputs)])
        while len(input_set) < num_inputs:
            new_input=s_generator(n_qubits)
            if new_input not in input_set:
                input_set.add(new_input)
        input_list=list(input_set)
    return input_list  

def sumgate(n: int) -> QuantumCircuit:
    qubits=2*n
    qc = QuantumCircuit(qubits)
    qc.cx(qc.qubits[:n],qc.qubits[n:])
    return qc

def execution(qCircuits: list[QuantumCircuit], rep: int = 1024, backend = AerSimulator, seed: int = 42 , simulation: bool = True ) -> list[dict[str,int]] :
    
    if simulation:
        sim = backend(seed_simulator = seed)
    else:
        sim = backend()
        
    res=[]
    
    for qCirc in qCircuits:
        r_qCirc = sim.run(transpile(qCirc,sim),shots=rep).result().get_counts()
        res.append(r_qCirc)
    
    return res
