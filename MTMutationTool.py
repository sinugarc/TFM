import random
from typing import Callable

from MutantTool import mutant_generator
from basicFunctions import xor, input_generator

from qiskit import QuantumCircuit, transpile, Aer
from qiskit.providers.aer import QasmSimulator

svsim = Aer.get_backend('aer_simulator')
simulator = QasmSimulator()

def mutation_MT(original_algorithm : Callable[[int],QuantumCircuit], MR_algorithm : Callable[[QuantumCircuit, list[str]],QuantumCircuit],
                num_qubits: int, num_mutants : int, rep : int, num_max_inputs=20, input_OnesComplement=False) -> tuple[list[bool],float,set[tuple[str,str]]]: 
    
    originalQC = original_algorithm(num_qubits)
    mutants = mutant_generator(originalQC, num_mutants)

    input_list = input_generator(num_qubits, num_max_inputs)
    if input_OnesComplement :
        aux = "1" * num_qubits
        input_pairs = [[input_list[i],xor(input_list[i],aux)]for i in range(len(input_list))]
    else:
        input_pairs = [[input_list[i],input_list[random.randint(0,len(input_list)-1)]]for i in range(len(input_list))]

    results=[]
    total=0
    final_inputs=set()
    expected_result = "0" * num_qubits
    for x in mutants:
        killed = False
        i = 0
        
        while not killed and i < len(input_pairs):
            
            result_x_i=svsim.run(transpile(MR_algorithm(x,input_pairs[i]),svsim),shots=rep).result().get_counts()
            
            if expected_result not in result_x_i.keys() or result_x_i[expected_result]!=rep:
                killed = True
                final_inputs.add(tuple(input_pairs[i]))
        
            i += 1
            
        total += i  
        results.append(killed)

    mutants_killed = sum(results)
    mutation_score = mutants_killed/len(results)*100
    print("Mutants Killed: ",mutants_killed)
    
    print("Mutantion Score: ",mutation_score,"%")

    print("Total QP executed: ",total)

    print("Set of inputs used: ", final_inputs)

    return (results, mutation_score, final_inputs)