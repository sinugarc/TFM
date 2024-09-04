import pickle
import gzip
import os
import time

from multiprocessing import Manager, Pool

from scipy.stats import chisquare

from .specImport import oracleToDict

from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator
from qiskit.circuit import CircuitInstruction, Instruction

Seed = 42

Simulator = AerSimulator(seed_simulator = Seed)

def obtainMutant(file: str) -> QuantumCircuit:
    with gzip.open(file,mode='rb') as f:
        m=pickle.load(f)
    f.close()
    return m

def qc_SetUp(mutant:QuantumCircuit, input:str) -> QuantumCircuit:
    """
    As defined in Muskit for comparation purposes.
    Input will be inserted at the start of the circuit, using Pauli-X gates.
    We will assume if the input has len n then it needs to be applied to the
    first n qubits.
    """
    mut=mutant.copy()
    for i in range(len(input)):
        if input[i] == 1:
            cInst=CircuitInstruction(operation=Instruction(name='x', num_qubits=1, num_clbits=0, params=[]),
                                     qubits=(mutant.qubits[len(input)-1-i],), clbits=())
            mut.data.insert(0,cInst)
    for i in range(max(mut.num_qubits,mut.num_clbits)):
        cInst=CircuitInstruction(operation=Instruction(name='measure', num_qubits=1, num_clbits=1, params=[]),
                           qubits=(mutant.qubits[i],), clbits=(mutant.clbits[i],))
        mut.data.append(cInst)
    return mut

def oracleAnalysis(oracle: dict[str,float], results: dict[str,float], pValue: float) -> bool :
    """
    As defined in Muskit for comparation purposes.
    It will analyse the restuls of the execution. It does follow the same principle of two oracles,
        although we will only register if the mutant has been killed.
    """
    killed = False
    if not results.keys() <= oracle.keys():
        # If there is a non valid result in the results key.
        killed = True
    else:
        # Uses Chi-square to compare distributions.
        oracleL = list(oracle.items())
        theo = [oracleL[i][1] for i in range(len(oracleL))]
        res = [results[x[0]] if x[0] in results.keys() else 0 for x in oracleL]
        _,actual_pValue = chisquare(res)
        if actual_pValue < pValue:
            killed = True
    return killed

def mutantExecution(mutant_path:str, results_path:str, inputs: list[str], rep: int, oracle: dict[str,dict[str,int]], pValue:int):
    """
    Receives a path for a mutant with format PGZ, and a path to save results.
    It will execute the mutant for each input saving the results.
    It will create a file to summarise all results and return a boolean indicating if the mutant has been killed. 
    """

    mutant = obtainMutant(mutant_path)

    r=[0,0]

    for x in inputs:
            
        mut = qc_SetUp(mutant, x)
        results = Simulator.run(transpile(mut,Simulator),shots=rep).result().get_counts()
        killed = oracleAnalysis(oracle[x], results, pValue)

        if killed:
            r[0] += 1
        else:
            r[1] += 1
            
        with open(results_path,mode='a') as f:
            f.write(x + ":" + str(killed) + "\n")
        f.close()

    with open(results_path,mode='a') as f:
        f.write("\n(#Killed, #NotKilled): " + str(r))
    f.close()
        
    return r[0] > 0


def parallelExecution(num_proc:int, path: str, inputs: list[str], rep: int, oracle_path: str, results_path:str, num_qubits: int = 6, pValue: float = 0.05):
    """
    I will collect all mutants in the provided path and execute them using Pool and the function previously defined.
    Once all processes have finished it will collect all information and save it on the correspondant results folder.
    """

    start = time.time()

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and f[-3:]=="pgz"]

    manager = Manager()
    oracle = manager.dict(oracleToDict(oracle_path,num_qubits))
    inp = manager.list(inputs)
    
    proc=[(f"{path}/{fi}", f"{results_path}/results_{fi.split('/')[-1][:-4]}.txt", inp, rep, oracle, pValue) for fi in files]
    time_lap = time.time()

    with Pool(processes=num_proc) as pool:
        results=pool.starmap_async(mutantExecution,proc)
        results.get()

    finish = time.time()

    results_path += "/" + "0_results.txt"

    kills=sum(list(results.get()))
    
    with open(results_path,mode='a') as fi:
        fi.write(f"Results for {path}\n\nUsing ChiSquare from Scipy library with pValue = {str(pValue)} and {str(rep)} repetitions on each execution in AerSimulator with seed: {str(Seed)}\n\n{str(kills)} mutants killed\nMutation Score: {str('{:.2f}'.format(kills/len(files)*100))} %\n\nTotal execution time: {str('{:.3f}'.format(finish-start))} s\nProcess creation time: {str('{:.3f}'.format(time_lap-start))} s\nProcess execution Time: {str('{:.3f}'.format(finish-time_lap))} s\n\nWith inputs:\n{str(inputs)}")
    fi.close()
