import os
import pickle
import gzip
import math
import random

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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

def rule_seed_test(rule: QMutation_TestingStructure, rule_path: str, parameters: P, num_proc: int) -> list[str]:
    
    output=[]
    
    for p in parameters:
        
        test=Q_Test(rule,p[0],p[1],**p[2])
        input_arg = p[3]
        exec_arg = p[4]
        results_path = os.path.join(rule_path,f"test_seed{p[2]['seed']}_{p[1]}_mutants.txt")
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

def rule_plot(data,colmap,path) -> None:
    info = data[0]
    name = info["name"]
    num_qubits = info["qubits"]
    
    plot_title = f"{num_qubits} Qubit {name} Mutation score evolution."
    
    seeds = info["seeds"]
    num_mutants = info["mutants"]
    
    num_mutants_QCRMut = info["mut_desired"]
    
    cmap = mpl.colormaps[colmap]

    colors = cmap(np.linspace(0, 1, len(seeds)))
    
    for i, color in enumerate(colors):
        plt.plot(num_mutants,list(map(lambda x : float(x),data[i+1])),color=color,label=f"Seed {seeds[i]}")
        
    plt.axvline(x=num_mutants_QCRMut,color="red",linestyle="--", label="Number of mutants for QCRMut coverability")
    
    plt.xlabel('Number of mutants')
    plt.ylabel('Mutation score')
    plt.title(plot_title)
    plt.legend()
    plt.legend(loc='center left',bbox_to_anchor=(1.04, 0.5))
    plt.savefig(path, bbox_inches='tight')
    plt.clf()
    
def seed_test(Rules, main_path, Qubits, Mutants, Inp_karg, Exec_karg, seeds, num_proc):
    
    results_path = os.path.join(main_path,"Results")
    os.mkdir(results_path)
    
    figure_path = os.path.join(results_path,"Figures")
    os.mkdir(figure_path)
    
    for k in Rules.keys():
        
        for r in Rules[k]:
            rule_path = os.path.join(main_path,r.__name__)
            os.mkdir(rule_path)
            
            for j in Qubits:
                rqubit_path = os.path.join(rule_path, f"{j}_qubits")
                os.mkdir(rqubit_path)
                
                n = num_mututants_calculator(r.__name__, j) # Mutants desired according to QCRMut 
                
                info={"name":r.__name__,
                      "qubits": j,
                      "seeds":seeds,
                      "mutants":Mutants,
                      "mut_desired":n}
                result = [info]
                
                for seed in seeds:
                    Mut_karg = [{"seed":seed}]
            
                    param = list(product(Mutants,Mut_karg,Inp_karg,Exec_karg))

                    parameters = list(map(lambda p : (j,p[0],p[1],([j],p[2]),([],p[3])),param))
                
                    res = rule_seed_test(r,rqubit_path,parameters,num_proc)
                    result.append(res)
                    
                res_path=os.path.join(results_path,f"{r.__name__}_{j}_qubits.pgz")
                
                with gzip.open(res_path,mode='wb') as f:
                    pickle.dump(result,f)
                    
                
                rule_plot(result,'hsv',os.path.join(figure_path,f"{r.__name__}_{j}_qubits.png"))   
    

if __name__ == "__main__":
    
    Rules = {"DJ_MRules": [DJ_test_MR1,DJ_test_MR2],
             "Simon_MRules": [Simon_test_MR2], 
             "BV_MRules": [BV_test_MR2]}
    
    Qubits = [3,4,5]
    Mutants = [10,20,30,50,70,100,150,200,300,500]
    Inp_karg = [{}]
    Exec_karg = [{}]
    
    num_proc = os.cpu_count() - 2 
    #num_proc = 10
    
    
    test_path = os.path.join(os.getcwd(),"Seed_Test_I")
    os.mkdir(os.path.abspath(test_path))
    
    seeds = [x*0.5 for x in range(1, 2*10+1)]
    
    seed_test(Rules, test_path, Qubits, Mutants, Inp_karg, Exec_karg, seeds, num_proc)
    
    
    Rules = {"BV_MRules": [BV_test_MR2]}
    
    test_path = os.path.join(os.getcwd(),"Seed_Test_II")
    os.mkdir(os.path.abspath(test_path))
    
    seeds = [x*50 for x in range(1, 2*10+1)]
    
    seed_test(Rules, test_path, Qubits, Mutants, Inp_karg, Exec_karg, seeds, num_proc)
    
    
    test_path = os.path.join(os.getcwd(),"Seed_Test_III")
    os.mkdir(os.path.abspath(test_path))
    
    random.seed(1)
    seeds = [random.uniform(0,1) for _ in range(20)]
    
    seed_test(Rules, test_path, Qubits, Mutants, Inp_karg, Exec_karg, seeds, num_proc)