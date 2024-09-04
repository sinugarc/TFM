import os
import random
from typing import Callable, TypeVar, Generic, Any
from collections.abc import Iterable

from qiskit import QuantumCircuit

from multiprocessing import Manager, Pool

import time

T = TypeVar('T')

class QMutation_TestingStructure:
    
    def __init__(self, name: str,
                 original_algorithm : Callable[int,QuantumCircuit],
                 mutant_generator: Callable[[QuantumCircuit, int, Any],Iterable[QuantumCircuit]],
                 input_generator : Callable[ [int, Any], list[Generic[T]]],
                 testCircuit_generator : Callable[ [QuantumCircuit, Generic[T]], list[QuantumCircuit]],
                 execution : Callable[ [list[QuantumCircuit],Any], list[dict[str,int]]],
                 analysis : Callable[ list[dict[str,int]], bool]):
        
        self.__name__= name
        
        self._algorithm = original_algorithm
        self._mutation = mutant_generator
        self._input = input_generator
        self._testCircuit = testCircuit_generator
        self._execution = execution
        self._analysis = analysis
        
    @property
    def algorithm(self):
        return self._algorithm
    
    @property
    def mutant_generator(self):
        return self._mutation
    
    @property
    def input_generator(self):
        return self._input
    
    @property
    def testCircuit_generator(self):
        return self._testCircuit
    
    @property
    def execution(self):
        return self._execution
    
    @property
    def analysis(self):
        return self._analysis
    
class Q_Test():
    
    def __init__(self,
                 test_structure: QMutation_TestingStructure,
                 num_qubits: int,
                 num_mutants: int,
                 *mutantGeneration_arg: list[Any],
                 **mutantGeneration_kwarg: dict[str,Any]):
        
        self.test_structure = test_structure
        
        self.test_algorithm = test_structure.algorithm(num_qubits)
        self.num_qubits = num_qubits
        
        self.num_mutants = num_mutants
        self.mut_arguments = (mutantGeneration_arg,mutantGeneration_kwarg)
        self.mutants = test_structure.mutant_generator(self.test_algorithm, num_mutants, *mutantGeneration_arg, **mutantGeneration_kwarg)
    
    def execPar(self,
                mutant: QuantumCircuit,
                index: int,
                inputs: Manager,
                execution_arguments: tuple[list[Any],dict[str,Any]]
               ) -> tuple[bool,int] : # (killed, max_input_index)
        
        killed = False
            
        i = 0

        while not killed and i < len(inputs):

            testCircuits = self.test_structure.testCircuit_generator(mutant,inputs[i])
            result_x_i = self.test_structure.execution(testCircuits,*execution_arguments[0],**execution_arguments[1])
            killed = self.test_structure.analysis(result_x_i)
            
            i += 1
            
        return (killed, i)
    
    def execution(self,
                  results_path: str,
                  num_proc: int,
                  inpGeneration_arguments: tuple[list[Any],dict[str,Any]],
                  execution_arguments: tuple[list[Any],dict[str,Any]]
                 ) -> tuple[Iterable[tuple[QuantumCircuit,int]],str]:
        
        # Need it for reproducibility 
        if 'seed' in self.mut_arguments[1].keys():
            random.seed(self.mut_arguments[1]['seed'])
        else:
            random.seed(1)
        self.mutants = list(self.mutants)

        inputs = self.test_structure.input_generator(*inpGeneration_arguments[0],**inpGeneration_arguments[1])
        
        manager = Manager()
        
        inp = manager.list(inputs)
        
        proc=[(self.mutants[i], i, inp, execution_arguments) for i in range(len(self.mutants))]
            
        start = time.time()

        with Pool(processes=num_proc) as pool:
            results=pool.starmap(self.execPar,proc)

        finish = time.time()
        
        kills = list(map(lambda x : x[0],results))
        input_indexes = list(map(lambda x : x[1],results))
        
        successful_inputs = set([inputs[x[1]-1] for x in results if x[0]])
        
        max_input_index = max(input_indexes)
        totalExecutions = sum(input_indexes)
        inputsUsed = inputs[:(max_input_index)]
        
        mutants_killed = sum(kills)
        mutation_score = str("{:.2f}".format(mutants_killed/self.num_mutants*100))
        survived_mutantsIndex = [i for i in range(len(kills)) if not kills[i]]
        
        self.__results(results_path, finish-start, kills, successful_inputs, inputsUsed, totalExecutions,
                      inpGeneration_arguments, execution_arguments)

        return ([(self.mutants[i],i) for i in range(len(self.mutants)) if not kills[i]],mutation_score)
    
    def __results(self,
                  path: str,
                  execution_time: float,
                  results: list[bool],
                  successful_inputs: set[Generic[T]],
                  inputsUsed: list[Generic[T]],
                  totalExecutions: int,
                  inpGeneration_arguments: list[Any],
                  execution_arguments: list[Any]) -> None :

        exec_time = str("{:.2f}".format(execution_time))+" s"
        mutants_killed = sum(results)
        mutation_score = str("{:.2f}".format(mutants_killed/self.num_mutants*100))
        survived_mutantsIndex = [i for i in range(len(results)) if not results[i]]
        
        with open(path,mode='w') as g:
            g.write(f'''Results for {self.test_algorithm.name} with {self.num_mutants} mutants and
                        Mutant generation arguments: {self.mut_arguments}
                        Input generation arguments: {inpGeneration_arguments}
                        Execution arguments: {execution_arguments}\n
                        Execution time: {exec_time}\n
                        Results:
                        Mutants killed: {mutants_killed}
                        Mutation Score: {mutation_score}%
                        Total QP executed: {totalExecutions}
                        Survived mutants indexes: {survived_mutantsIndex}
                        Successful inputs: {successful_inputs}
                        Inputs used: {inputsUsed}''')
            g.close()
