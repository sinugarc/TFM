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
qc.rz(1.5707963267948966,q[3])
qc.cu1(pi/2**(1), q[3], q[4])
qc.cu1(pi/2**(2), q[3], q[5])
qc.h(q[4])
qc.cu1(pi/2**(1), q[4], q[5])
qc.h(q[5])
