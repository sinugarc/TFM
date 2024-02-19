import random
from itertools import product

def xor(a:str,b:str) -> str:
    return "".join(str(int(x)) for x in map(lambda s, t : bool(int(s))^bool(int(t)),a,b))

def s_generator(n: int) -> str:
    return "".join(str(random.randint(0,1)) for _ in range(n))

def input_generator (n_qubits: int , n_inputs: int) -> [str] :
    if 2**n_qubits <= n_inputs:
        input_list = list(map(lambda x : "".join(str(x[i]) for i in range(len(x))), product([0,1],repeat=n_qubits)))
    else:
        input_set = set([s_generator(n_qubits) for _ in range(n_inputs)])
        while len(input_set) < n_inputs:
            new_input=s_generator(n_qubits)
            if new_input not in input_set:
                input_set.add(new_input)
        input_list=list(input_set)
    return input_list