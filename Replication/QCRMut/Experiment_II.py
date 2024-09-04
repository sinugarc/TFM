import sys
import random
import os

from QCRMut import *

from qiskit import QuantumCircuit

def main(num_proc:int, qc: QuantumCircuit, num_mutants:int, seed:int, dir_path:str, num_inputs:int, pValue:float):

    random.seed(seed)
    
    mutants_path = dir_path + "/Mutants"
    os.mkdir(mutants_path)
    
    mutant_generator(qc, num_mutants,seed,True,mutants_path)
    num_qubits = qc.num_qubits

    inputs = input_generator(num_qubits ,num_inputs)
    
    oracle_path = qc.name+"/"+qc.name+"_test_oracle.txt"
    
    results_path = dir_path + "/Results_100Rep"
    os.mkdir(results_path)
    
    parallelExecution(num_proc,mutants_path, inputs, 100, oracle_path, results_path, num_qubits, pValue)
    
    results_path = dir_path + "/Results_1024Rep"
    os.mkdir(results_path)

    parallelExecution(num_proc,mutants_path, inputs, 1024, oracle_path, results_path, num_qubits, pValue)


if __name__=="__main__":
    
    if len(sys.argv)>1 and isinstance(sys.argv[1],int) : 
        num_proc = sys.argv[1]
    else:
        num_proc = os.cpu_count()
    
    QA_SetUp=[("CE",288),("IQFT",500),("BV",160)] #(QuantumAlgorithm, num_mutants)
    seed=1
    num_inputs = 100
    pValue = 0.05
        
    dir_path="Experiment_II"
    os.mkdir(dir_path)
    
    for (x,num_mutants) in QA_SetUp:
        
        module = __import__(x)
        func = getattr(module,x)
        qc=func()
        qc.name=x
        
        aux_path = dir_path + "/" + x
        os.mkdir(aux_path)
        
        main(num_proc,qc,num_mutants,seed,aux_path,num_inputs,pValue)

    
