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
qc.t(q[0])
qc.h(q[0])
qc.cu1(pi/2**(1), q[0], q[1])
qc.cu1(pi/2**(2), q[0], q[2])
qc.cu1(pi/2**(3), q[0], q[3])
qc.cu1(pi/2**(4), q[0], q[4])
qc.cu1(pi/2**(5), q[0], q[5])
qc.h(q[1])
qc.cu1(pi/2**(1), q[1], q[2])
qc.cu1(pi/2**(2), q[1], q[3])
qc.cu1(pi/2**(3), q[1], q[4])
qc.cu1(pi/2**(4), q[1], q[5])
qc.h(q[2])
qc.cu1(pi/2**(1), q[2], q[3])
qc.cu1(pi/2**(2), q[2], q[4])
qc.cu1(pi/2**(3), q[2], q[5])
qc.h(q[3])
qc.cu1(pi/2**(1), q[3], q[4])
qc.cu1(pi/2**(2), q[3], q[5])
qc.h(q[4])
qc.cu1(pi/2**(1), q[4], q[5])
qc.h(q[5])


with gzip.open('/srv/home/sinugarc/TFM/Repl/QCRMutExp/muskitTest/IQFT/IQFTMutantsPGZ/61AddGate_t_inGap_4_.pgz',mode='wb') as f:
    pickle.dump(qc,f)
f.close()