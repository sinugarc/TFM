import sys
import random
import os

from QCRMut import *

from qiskit import QuantumCircuit

def main(qc:QuantumCircuit, num_mutants:int, seed:int, dir_path:str):

    random.seed(seed)
    
    mutants_path = mutant_generator(qc, num_mutants,seed,True,dir_path)


if __name__=="__main__":
    
    QuantumAlgorithms=["CE", "IQFT", "BV"]
    NumberMutants=[100,1000,10000] #,100000
    
    dir_path="Experiment_I"
    os.mkdir(dir_path)
    
    for x in QuantumAlgorithms:
        
        module = __import__(x)
        func = getattr(module,x)
        qc=func()
        qc.name=x
        
        aux_path = dir_path + "/" + x
        os.mkdir(aux_path)
        
        aux_path = aux_path + "/" + x + "_"
        
        for num in NumberMutants:
            
            os.mkdir(aux_path+str(num))
            main(qc,num,1,aux_path+str(num))
        

    
