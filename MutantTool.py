import random
import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import CircuitInstruction, Instruction, Qubit, Clbit
from qiskit.tools.visualization import circuit_drawer
from qiskit.circuit.gate import Gate

# Gate equivalence classes

mutableGateSet={'x','h','z','y','tdg','t','sx','sdg','s','id','u1','r','rz','ry','rx','p','u2','u3','u',
                'swap','iswap', 'dcx', 'cz', 'cy','cx', 'csx','ch','rzz','rzx','ryy','rxx','cu1','crz','cry',
                'crx','cp','cswap','ccx'} #'i','gms'

gateEquivalenceDict = {"1q0p" : ['x','h','z','y','t','sx','sdg','s','tdg','id'], #'i'
                       "1q1p" : ['p','u1','r','rz','ry','rx'], 
                       "1q2p" : ['u2'],
                       "1q3p" : ['u','u3'], 
                       "2q0p" : ['swap','iswap', 'dcx', 'cz', 'cy','cx', 'csx','ch'],
                       "2q1p" : ['rzz','rzx','ryy','rxx','cu1','crz','cry','crx','cp'],
                       "3q0p" : ['cswap','ccx'] #'gms'
                      }


num_elem=[[len(gateEquivalenceDict[str(i)+"q"+str(j)+"p"]) for j in range(4) 
           if (str(i)+"q"+str(j)+"p" in gateEquivalenceDict.keys())] for i in range(1,4)]

"""
QiskitError: "Cannot unroll the circuit to the given basis, ['ccx', 'cp', 'cswap', 'csx', 'cu', 'cu1', 'cu2', 'cu3', 'cx', 'cy', 'cz', 'delay', 'diagonal', 'h', 'id', 'initialize', 'mcp', 'mcphase', 'mcr', 'mcrx', 'mcry', 'mcrz', 'mcswap', 'mcsx', 'mcu', 'mcu1', 'mcu2', 'mcu3', 'mcx', 'mcx_gray', 'mcy', 'mcz', 'multiplexer', 'p', 'pauli', 'r', 'roerror', 'rx', 'rxx', 'ry', 'ryy', 'rz', 'rzx', 'rzz', 's', 'sdg', 'swap', 'sx', 'sxdg', 't', 'tdg', 'u', 'u1', 'u2', 'u3', 'unitary', 'x', 'y', 'z', 'for_loop', 'if_else', 'kraus', 'qerror_loc', 'quantum_channel', 'roerror', 'save_amplitudes', 'save_amplitudes_sq', 'save_clifford', 'save_density_matrix', 'save_expval', 'save_expval_var', 'save_matrix_product_state', 'save_probabilities', 'save_probabilities_dict', 'save_stabilizer', 'save_state', 'save_statevector', 'save_statevector_dict', 'save_superop', 'save_unitary', 'set_density_matrix', 'set_matrix_product_state', 'set_stabilizer', 'set_statevector', 'set_superop', 'set_unitary', 'superop', 'while_loop']. Instruction gms not found in equivalence library and no rule found to expand."
"""

class Placeholder(CircuitInstruction):
    def __init__(self,  num_qubits, qubits, name = "Input", num_clbit=0, clbits=[], param=[], label="  Input  "):
        self.name = name
        super().__init__(Instruction(name, num_qubits, num_clbit, param, label),
                         qubits=qubits,clbits=clbits)


def mutant_gen_change_gate_name (testQC:QuantumCircuit, index:int, equivalenceGroup_name:str) -> QuantumCircuit:
    """
    testQC : QuantumCircuit, QC under test
    index : int, index in testQC.data to be mutated
    equivalenceGroup_name : str, name of the equivalence group of testQC.data[index].operator
    
    This function returns a copy the QC under test, obtains randomly a gate name from the equivalence 
        group, ensures it is no the same one and substitues the new gate name in the returning copy. 
    
    assert 0 <= index < len(testQC.data)
    assert testQC.data[index].operator.name in gateEquivalenceDict[equivalenceGroup_name]
    assert len(gateEquivalenceDict[equivalenceGroup_name]) > 1
    """
    
    assert len(gateEquivalenceDict[equivalenceGroup_name]) > 1
    mutant = testQC.copy()

    new_name = random.choice(gateEquivalenceDict[equivalenceGroup_name])
    
    while new_name == mutant.data[index].operation.name:
        new_name = random.choice(gateEquivalenceDict[equivalenceGroup_name])
        
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
    assert: testQC.data[index].operator.name not in gateEquivalenceDict["1q0p"]
    """
    mutant = testQC.copy()
    
    gate_num_qubits = mutant.data[index].operation.num_qubits
    gate_num_params = len(mutant.data[index].operation.params)
    
    new_qubits = tuple(random.sample(mutant.qubits, gate_num_qubits))
    if mutant.num_qubits > 1:
        # Only force different combination of qubits if circuit has more than 1 qubit.
        while new_qubits == mutant.data[index].qubits:
            new_qubits = tuple(random.sample(mutant.qubits, gate_num_qubits))
    
    new_params = [random.uniform(-math.pi/2,math.pi/2) for _ in range(gate_num_params)]
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
    gate_num_qubits = random.choices(range(1,max_num_qubits), weights = [sum(num_elem[i]) for i in range(max_num_qubits-1)])[0]
        
    gate_qubits = tuple(random.sample(mutant.qubits, gate_num_qubits))
    
    if gate_num_qubits == 1:
        
        gate_num_parameters = random.choices(range(len(num_elem[0])), weights = list(map(lambda x: x/(sum(num_elem[0])),num_elem[0])))[0]
        gate_parameters = [random.uniform(-math.pi/2,math.pi/2) for _ in range(gate_num_parameters)]
        
        gate_name = random.choice(gateEquivalenceDict["1q"+str(gate_num_parameters)+"p"])
        
    elif gate_num_qubits == 2:
            
        gate_num_parameters = random.choices(range(len(num_elem[1])), weights = list(map(lambda x: x/(sum(num_elem[1])),num_elem[1])))[0]
        gate_parameters = [random.uniform(-math.pi/2,math.pi/2) for _ in range(gate_num_parameters)]
        
        gate_name = random.choice(gateEquivalenceDict["2q"+str(gate_num_parameters)+"p"])
        
    else:
        
        gate_parameters = []
        gate_name = random.choice(gateEquivalenceDict["3q0p"])
    
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
    assert: len(mutableGateSetIndex) > 0
    """
    
    mut_type=random.randint(0,3)
    # Select randomly the mutation operator
    
    if mut_type == 0:
        # Gate change within its equivalence class keeping same qubits and parameters
        
        # Exception: There is only one equivalent gate
        gate_name = testQC.data[mutableIndex].operation.name
        equivalenceGroup_name = str(testQC.data[mutableIndex].operation.num_qubits) + 'q' + str(len(testQC.data[mutableIndex].operation.params))+ 'p'
    
        exception = (len(gateEquivalenceDict[equivalenceGroup_name]) == 1)
        if exception:
            mutant = mutant_generator_aux(testQC, mutableIndex) 
        
        mutant = mutant_gen_change_gate_name(testQC, mutableIndex, equivalenceGroup_name)
        
    elif mut_type == 1 :
        # Gate changes in control/target qubit or parameters
        
        # Exception: Trying to mutate a 1 qubit operator with no parameters in 1 qubit QC
        exception = (testQC.num_qubits == 1 and (testQC.data[mutableIndex].operation.name in gateEquivalenceDict["1q0p"]))
        if exception:
            mutant = mutant_generator_aux(testQC, mutableIndex) 
        else:
            mutant = mutant_gen_change_gate_properties(testQC, mutableIndex)
        
    elif mut_type == 2:
        # Gate insertion 
        mutant = mutant_gen_insert_gate(testQC)
        
    else:
        # Gate deletion
        mutant = testQC.copy()
        del mutant.data[mutableIndex]
        
    return mutant


def mutant_generator(testQC:QuantumCircuit, num_mutants:int) -> [QuantumCircuit]:
    """
    testQC : QuantumCircuit, QC under test
    num_mutants : int, number of randomly generated mutants desired
    
    This function returns a list of num_mutants mutated QuantumCircuits. It makes a 
        difference with two extreme cases: No QuantumInstructions in the circuit and 
        No mutable gates in the circuit. In this cases, only gate insertion operator 
        is available.
            
    """
    assert num_mutants > 0
    
    if len(testQC.data) == 0:
        # Avoid extreme case of an empty QC.
        mutants = [mutant_gen_insert_gate(testQC) for _ in range(num_mutants)]
        
    else:
        mutableGateSetIndex=[i for i in range(len(testQC.data)) if testQC.data[i].operation.name in mutableGateSet]

        if len(mutableGateSetIndex) == 0:
            # Avoid the possibility of having only non mutable gates (out of our scope of mutability)
            mutants = [mutant_gen_insert_gate(testQC) for _ in range(num_mutants)]

        else:
            mutants = [mutant_generator_aux(testQC, mutableGateSetIndex[random.randint(0,len(mutableGateSetIndex)-1)]) 
                       for _ in range(num_mutants)]
    
    return mutants


def QCSetUp (mutant: QuantumCircuit, inp: QuantumCircuit) -> Instruction:
    """
    mutant: QuantumCircuit, basic mutant with barriers and without input.
    inp: QuantumCircuit, it represents the input.
    
    This function takes the mutant and the input. Creates a copy of the mutant,
    inserts the input in the Placeholder and removes all barriers from the circuits.
    The idea is to convert all into an Instruction for posterior use in MT circuit.
    We are unable to convert it into a gate if there is non-basic gates.
    """
    mutRes = mutant.copy_empty_like()
    
    mutRes.data=[mutant.data[i] for i in range(len(mutant.data)) if mutant.data[i].operation.name != "barrier"]
    swap=False
    i=0
    while not swap and i < len(mutRes.data):
        
        if mutRes.data[i].operation.name == "Input":
            gate = inp.to_instruction(label=" Input ")
            mutRes.data[i].operation = gate
        i += 1
    
    return mutRes.to_instruction()