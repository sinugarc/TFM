import pickle
import gzip
import qiskit
from qiskit import *
from math import pi


q = QuantumRegister(6)
c = ClassicalRegister(6)
qc = QuantumCircuit(q,c)


qc.swap(q[0], q[5])
qc.swap(q[1], q[4])
qc.swap(q[2], q[3])
qc.h(q[0])
qc.h(q[1])
qc.h(q[2])
qc.h(q[3])
qc.h(q[4])
qc.ry(3.141592653589793,q[5])


with gzip.open('/srv/home/sinugarc/TFM/Repl/QCRMutExp/muskitTest/IQFT/IQFTMutantsPGZ/76ReplaceGate.pgz',mode='wb') as f:
    pickle.dump(qc,f)
f.close()