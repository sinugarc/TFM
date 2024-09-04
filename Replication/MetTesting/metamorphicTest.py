import os
import pickle
import gzip
import math
import random

import numpy as np

from typing import Union, Any
from itertools import product

from Algorithms import *
from MutTest import *

#Parameter type
P = list[tuple[int, #Qubits
               int, #Mutants
               dict[str,Union[int,bool,str]], # Mutation kargs
               tuple[list[int],dict[str,int]], # Input args & kargs
               tuple[list[int],dict[str,Any]], # Execution args & kargs
              ]]

def rule_met_test(rule: QMutation_TestingStructure, rule_path: str, parameters: P, num_proc: int) -> list[str]:
    
    output=[]
    
    for p in parameters:
        
        test=Q_Test(rule,p[0],p[1],**p[2])
        input_arg = p[3]
        exec_arg = p[4]
        results_path = os.path.join(rule_path,f"test_{p[0]}Qubits_{p[1]}_mutants.txt")
        r=test.execution(results_path,num_proc,input_arg,exec_arg)
          
        output.append(r[1])
        
    return output

def num_mututants_calculator(name, num_qubits):
    
    if name[0] == "S":
        gates = 2*num_qubits + 1
    else:
        gates = 2*num_qubits + 3
        
    n = 4*(gates + 1)*math.ceil(math.log(gates + 1) + 1)
    
    return n
    
def met_test(Rules, main_path, Qubits, Mut_karg, Inp_karg, Exec_karg, num_proc):
    
    results_path = os.path.join(main_path,"Results")
    os.mkdir(results_path)
    
    for k in Rules.keys():
        
        for r in Rules[k]:
            rule_path = os.path.join(main_path,r.__name__)
            os.mkdir(rule_path)
            
            for j in Qubits:
                
                n = num_mututants_calculator(r.__name__, j) # Mutants desired according to QCRMut 
                
                info={"name":r.__name__,
                      "qubits": j,
                      "mutants": n}
                result = [info]
            
                param = list(product(Mut_karg,Inp_karg,Exec_karg))

                parameters = list(map(lambda p : (j,n,p[0],([j],p[1]),([],p[2])),param))
                
                res = rule_met_test(r,rule_path,parameters,num_proc)
                result.append(res)
                    
                res_path=os.path.join(results_path,f"{r.__name__}_{j}_qubits.pgz")
                
                with gzip.open(res_path,mode='wb') as f:
                    pickle.dump(result,f) 
    

if __name__ == "__main__":
    
    Rules = {"DJ_MRules": [DJ_test_MR1,DJ_test_MR2],
             "BV_MRules": [BV_test_MR1,BV_test_MR2,BV_test_MR3],
             "Simon_MRules": [Simon_test_MR2,Simon_test_MR1]}
    
    
    Mut_karg = [{"seed":1}]
    Inp_karg = [{}]
    Exec_karg = [{}]
    
    num_proc = os.cpu_count() - 2
    #num_proc = 10
    
    test_path = os.path.join(os.getcwd(),"Metamorphic_Test_I")
    os.mkdir(os.path.abspath(test_path))
    
    Qubits = [3,4,5,6,7]
    
    met_test(Rules, test_path, Qubits, Mut_karg, Inp_karg, Exec_karg, num_proc)
    
    
    Rules = {"DJ_MRules": [DJ_test_MR1,DJ_test_MR2],
             "BV_MRules": [BV_test_MR1,BV_test_MR2,BV_test_MR3],
             "Simon_MRules": [Simon_test_MR2]}
    
    Qubits = [8,9]
    
    
    test_path = os.path.join(os.getcwd(),"Metamorphic_Test_II")
    os.mkdir(os.path.abspath(test_path))
    
    met_test(Rules, test_path, Qubits, Mut_karg, Inp_karg, Exec_karg, num_proc)
    
    
    test_path = os.path.join(os.getcwd(),"Metamorphic_Test_III")
    os.mkdir(os.path.abspath(test_path))
    
    Inp_karg = [{"num_inputs":10}]
    
    met_test(Rules, test_path, Qubits, Mut_karg, Inp_karg, Exec_karg, num_proc)
