import os

from QCRMut import *

def main(mutants_path:str, oracle_path:str, res_path:str):

    inputs = input_generator(6,100)
    
    results_path = res_path + "/Results_100Rep"
    os.mkdir(results_path)
    num_proc = os.cpu_count()
    
    parallelExecution(num_proc,mutants_path, inputs, 100, oracle_path, results_path, 6, 0.05)
    
    if "IQFT" in mutants_path:
    
        results_path = res_path + "/Results_1024Rep"
        os.mkdir(results_path)

        parallelExecution(num_proc,mutants_path, inputs, 1024, oracle_path, results_path, 6, 0.05)



if __name__=="__main__":
    
    QAlg=["CE","IQFT","BV"] 
    
    path = os.getcwd()
    
    for name in QAlg:
        
        aux_path = f"{path}/{name}/{name}MutantsPGZ"
        oracle_path = f"{path}/{name}/{name}_test_oracle.txt"
        res_path = f"{path}/Results/{name}"
        
        main(aux_path,oracle_path,res_path)

    
