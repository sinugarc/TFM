import os
import time

import random
import pickle
import gzip

from typing import TypeVar
from collections.abc import Iterable

from math import pi
from qiskit import QuantumCircuit
from qiskit.circuit import CircuitInstruction, Instruction, Qubit, Clbit

MutableGateSet = {'x','h','z','y','tdg','t','sx','sdg','s','id','u1','r','rz','ry','rx','p','u2','u3','u',
                'swap','iswap', 'dcx', 'cz', 'cy','cx', 'csx','ch','rzz','rzx','ryy','rxx','cu1','crz','cry',
                'crx','cp','cswap','ccx'}

# Gate equivalence classes

GateEquivalenceDict = {"1q0p" : ['x','h','z','y','t','sx','sdg','s','tdg','id'], 
                       "1q1p" : ['p','u1','r','rz','ry','rx'], 
                       "1q2p" : ['u2'],
                       "1q3p" : ['u','u3'], 
                       "2q0p" : ['swap','iswap', 'dcx', 'cz', 'cy','cx', 'csx','ch'],
                       "2q1p" : ['rzz','rzx','ryy','rxx','cu1','crz','cry','crx','cp'],
                       "3q0p" : ['cswap','ccx']
                      }

Num_Elem = [[len(GateEquivalenceDict[str(i)+"q"+str(j)+"p"]) for j in range(4) 
             if (str(i)+"q"+str(j)+"p" in GateEquivalenceDict.keys())] for i in range(1,4)]

# Num_Elem will support us with the weights on random.choice used on insertion operator

Num_Elem[0][0] -= 1 # 'id' gate will not be inserted in a QC.

AnyNum = TypeVar('AnyNum', int, float)

class PlaceHolder(CircuitInstruction):
    def __init__(self,  num_qubits:int, qubits:list[Qubit], name:str = "Input", num_clbits:int = 0, clbits:list[Clbit] = [], param:list[AnyNum] = [], label:str = "  Input  "):
        assert num_qubits == len(qubits)
        assert num_clbits == len(clbits)
        self.name = name
        super().__init__(Instruction(name, num_qubits, num_clbits, param, label),
                         qubits=qubits,clbits=clbits)

def mutant_gen_change_gate_name (testQC:QuantumCircuit, index:int, equivalenceGroup_name:str) -> QuantumCircuit:
    """
    testQC : QuantumCircuit, QC under test
    index : int, index in testQC.data to be mutated
    equivalenceGroup_name : str, name of the equivalence group of testQC.data[index].operator
    
    This function returns a copy the QC under test, obtains randomly a gate name from the equivalence 
        group, ensures it is no the same one and substitues the new gate name in the returning copy. 
    
    assert: 0 <= index < len(testQC.data)
    assert: testQC.data[index].operator.name in GateEquivalenceDict[equivalenceGroup_name]
    assert: len(GateEquivalenceDict[equivalenceGroup_name]) > 1
    """
    
    assert len(GateEquivalenceDict[equivalenceGroup_name]) > 1
    mutant = testQC.copy()
    
    new_name = random.choice(GateEquivalenceDict[equivalenceGroup_name])
    
    while new_name == mutant.data[index].operation.name:
        new_name = random.choice(GateEquivalenceDict[equivalenceGroup_name])
        
    mutant.data[index].operation.name = new_name
    
    return mutant

def mutant_gen_change_gate_properties (testQC:QuantumCircuit, index:int) -> QuantumCircuit:
    """
    testQC : QuantumCircuit, QC under test
    index : int, index in testQC.data to be mutated
    
    This function returns a copy the QC under test changing the qubits and parameters
        on the CircuitInstruction in correspondent index. It obtains randomly a different
        qubit tuple and different parameters according to the gate needs if necessary.
    
    assert: 0 <= index < len(testQC.data)
    assert: testQC.data[index].operator.name not in GateEquivalenceDict["1q0p"]
    """
    mutant = testQC.copy()
    
    gate_num_qubits = mutant.data[index].operation.num_qubits
    gate_num_params = len(mutant.data[index].operation.params)
    
    new_qubits = tuple(random.sample(mutant.qubits, gate_num_qubits))
    if mutant.num_qubits > 1:
        # Only force different combination of qubits if circuit has more than 1 qubit.
        while new_qubits == mutant.data[index].qubits:
            new_qubits = tuple(random.sample(mutant.qubits, gate_num_qubits))
    
    new_params = [random.uniform(-pi/2,pi/2) for _ in range(gate_num_params)]
    if gate_num_params!=0:
        # Only force different parameters if there is parameters.
        while new_qubits == mutant.data[index].qubits:
            new_qubits = tuple(random.sample(mutant.qubits, gate_num_qubits))
    
    mutant.data[index].qubits = new_qubits
    mutant.data[index].operation.params = new_params
    
    return mutant

def mutant_gen_insert_gate(testQC:QuantumCircuit) -> QuantumCircuit:
    """
    testQC : QuantumCircuit, QC under test
    
    This function returns a copy the QC under test adding a new CircuitInstruction in 
        a random index. The new CircuitInstruction is obtained randomly within the 
        possibilities of the number of qubits in testQC.
    """
    
    mutant = testQC.copy()
    
    #It may take len(mutant.data) as index, due to being an insertion
    index = random.randint(0,len(mutant.data)) 
    max_num_qubits = min(3,mutant.num_qubits)
    gate_num_qubits = random.choices(range(1,max_num_qubits), weights = [sum(Num_Elem[i]) for i in range(max_num_qubits-1)])[0]
        
    gate_qubits = tuple(random.sample(mutant.qubits, gate_num_qubits))
    
    if gate_num_qubits == 1:
        
        gate_num_parameters = random.choices(range(len(Num_Elem[0])), weights = list(map(lambda x: x/(sum(Num_Elem[0])),Num_Elem[0])))[0]
        
        gate_parameters = [random.uniform(-pi,pi) for _ in range(gate_num_parameters)]
        
        gate_name = random.choice(GateEquivalenceDict["1q"+str(gate_num_parameters)+"p"])
        
        if gate_num_parameters > 0:
            while ([0]*gate_num_parameters) == gate_parameters: # We want to avoid equivalent mutants.
                gate_parameters = [random.uniform(-pi,pi) for _ in range(gate_num_parameters)]
        
        else:
            while gate_name == 'id':
                gate_name = random.choice(GateEquivalenceDict["1q"+str(gate_num_parameters)+"p"])

    elif gate_num_qubits == 2:
            
        gate_num_parameters = random.choices(range(len(Num_Elem[1])), weights = list(map(lambda x: x/(sum(Num_Elem[1])),Num_Elem[1])))[0]
        gate_parameters = [random.uniform(-pi,pi) for _ in range(gate_num_parameters)]
        
        gate_name = random.choice(GateEquivalenceDict["2q"+str(gate_num_parameters)+"p"])
        
    else:
        
        gate_parameters = []
        gate_name = random.choice(GateEquivalenceDict["3q0p"])
    
    inst = Instruction(name=gate_name, num_qubits=gate_num_qubits, num_clbits=0, params=gate_parameters)
    cInt = CircuitInstruction(inst,gate_qubits)
    
    mutant.data.insert(index,cInt)
    
    return mutant


def mutant_generator_aux(testQC:QuantumCircuit, mutableIndex:int) -> QuantumCircuit:
    """
    testQC : QuantumCircuit, QC under test
    mutableIndex : int, index in testQC.data to be mutated
    
    This function returns a mutated QC. It randomly selects between the correct type 
        of mutation for the required circuit. The mutation operators are:
        
            - 0) Gate name change
            - 1) Gate qubits/parameters change
            - 2) Gate insertion
            - 3) Gate deletion
            
    assert: len(testQC.data) > 0
    assert: len(MutableGateSetIndex) > 0
    """
    
    mut_type=random.randint(0,3)
    # Select randomly the mutation operator
    
    if mut_type == 0:
        # Gate change within its equivalence class keeping same qubits and parameters
        # Exception: There is only one equivalent gate
        
        equivalenceGroup_name = str(testQC.data[mutableIndex].operation.num_qubits) + 'q' + str(len(testQC.data[mutableIndex].operation.params))+ 'p'
    
        exception = (len(GateEquivalenceDict[equivalenceGroup_name]) == 1)
        if exception:
            mutant = mutant_generator_aux(testQC, mutableIndex) 
        
        mutant = mutant_gen_change_gate_name(testQC, mutableIndex, equivalenceGroup_name)
        
    elif mut_type == 1 :
        # Gate changes in control/target qubit or parameters
        # Exception: Trying to mutate a 1 qubit operator with no parameters in 1 qubit QC

        exception = (testQC.num_qubits == 1 and (testQC.data[mutableIndex].operation.name in GateEquivalenceDict["1q0p"]))
        if exception:
            mutant = mutant_generator_aux(testQC, mutableIndex) 
        else:
            mutant = mutant_gen_change_gate_properties(testQC, mutableIndex)
        
    elif mut_type == 2: # Gate insertion
         
        mutant = mutant_gen_insert_gate(testQC)
        
    else: # Gate deletion
        
        exception = testQC.data[mutableIndex].operation.name == "id" #Delete the identity produce an equivalent mutant
        
        if exception:
            mutant = mutant_generator_aux(testQC, mutableIndex)

        else:
            mutant = testQC.copy()
            del mutant.data[mutableIndex]
        
    return mutant

def mutant_generator(testQC: QuantumCircuit, num_mutants: int, seed: int = 1, save: bool = False, dir_name: str = "") -> Iterable[QuantumCircuit]:
    """
    testQC : QuantumCircuit, QC under test
    num_mutants : int, number of randomly generated mutants desired
    dir_name: path to mutant saving directory from working directory
    
    This function generates mutated QuantumCircuits. If save option is chosen then,
        it is saved using pickle and gzip libraries. 
        
    It makes a difference with two extreme cases: No QuantumInstructions in the circuit 
        and no mutable gates in the circuit. In this cases, only gate insertion operator 
        is available.     
    """
    
    assert num_mutants > 0
    assert (dir_name != "") or not save
    
    random.seed(seed)

    MutableGateSetIndex=[i for i in range(len(testQC.data)) if testQC.data[i].operation.name in MutableGateSet]

    start=time.time()
    
    if len(testQC.data) == 0 or len(MutableGateSetIndex) == 0:
        # Avoid extreme case of an empty QC.
        # Avoid the possibility of having only non mutable gates (out of our scope of mutability)
        if save:
            path = os.path.join(os.getcwd(),dir_name)
            for i in range(num_mutants):
                mutant = mutant_gen_insert_gate(testQC)
                saveMutant(mutant,f"{path}/mutant_{str(i)}.pgz")
                
            finish=time.time()
            with open(f"{path}/0infoMutants.txt",mode='w') as f:
                f.write(f"Number of mutants generated: {num_mutants}\nSeed used: {seed}\nExecution time: " + str("{:.3f}".format(finish-start)) + " s")

        return (mutant_gen_insert_gate(testQC) for _ in range(num_mutants))
        
    elif save:
        path = os.path.join(os.getcwd(),dir_name)
        for i in range(num_mutants):
            mutant = mutant_generator_aux(testQC, MutableGateSetIndex[random.randint(0,len(MutableGateSetIndex)-1)])
            saveMutant(mutant,f"{path}/mutant_{str(i)}.pgz")
            
        finish=time.time()
        with open(f"{path}/0infoMutants.txt",mode='w') as f:
            f.write(f"Number of mutants generated: {num_mutants}\nSeed used: {seed}\nExecution time: " + str("{:.3f}".format(finish-start)) + " s")

    return (mutant_generator_aux(testQC, MutableGateSetIndex[random.randint(0,len(MutableGateSetIndex)-1)]) for _ in range (num_mutants))
    
def saveMutant(qc: QuantumCircuit, path: str) -> None :
    with gzip.open(path,mode='wb') as f:
        pickle.dump(qc,f)
    f.close()
    
def loadMutant(path: str) -> QuantumCircuit:
    with gzip.open(path,mode='rb') as f:
        m=pickle.load(f)
    f.close()
    return m

newOpType = TypeVar('newOpType', QuantumCircuit, CircuitInstruction) 

def placeHolderSwap (mutant: QuantumCircuit, newOp: newOpType, newOpLabel:str = " Input ", holderName:str = "Input"):
    """
    This function takes the mutant and the new operator.
    It inserts the newOp in the Placeholder called holderName.
    It will include the new label 
    """
    
    swap=False
    
    for i  in range(len(mutant.data)):
        
        if mutant.data[i].operation.name == holderName:
            
            if isinstance(newOp,QuantumCircuit):
                gate = newOp.to_instruction(label=newOpLabel)
                mutant.data[i].operation = gate
                
            else:
                mutant.data[i].operation = newOp
                mutant.data[i].label = newOpLabel
            
            swap = True
    
    if not swap: print('PlaceHolder not found')