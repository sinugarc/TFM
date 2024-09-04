from .basicFunctions import intToBin

def oracleToDict(file:str,length:int) -> dict[str,dict[str,float]] :
    """
    This function will transform an oracle, with Muskit's format,
       to a dictionary. The key will be the inputs and their
       values will be a dictionary with all possible outputs as keys
       and their the outcome probabilities as values.
    """
    oracle = {}
    with open(file,'r') as f:
        for line in f:
            l=line.split(': ')
            l1=l[0][1:-1].split(', ')
            k_inp=intToBin(int(l1[0]),length)
            res=intToBin(int(l1[1]),length)
            p=float(l[1])
            if k_inp in oracle.keys():
                oracle[k_inp][res]=p
            else:
                oracle[k_inp]={res:p}
    f.close()
    return oracle
