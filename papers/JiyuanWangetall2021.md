Wang, J., Zhang, Q., Xu, G. H., & Kim, M. (2021, November). Qdiff: Differential testing of quantum software stacks. In 2021 36th IEEE/ACM International Conference on Automated Software Engineering (ASE) (pp. 692-704).

### Bullet points:
* QDiff workflow:
  * Input program generation, preserving semantics
  * Speed differential testing by filtering QP not worth to execute by analysing static characteristics
  * Equivalence mechanism. KS test and cross entropy

* 3 technical challenges that make difficult to test Quantum Software Stacks (QSS)
  * Generating semantically equivalent programs to test Q compilers
  * Compilers not the only source of bugs in QSS
  * How to interpretate measurements from QP

* Base for QDiff program variant generator: SWAP equivalent to 3 CNOT

* Motivation for the paper: Collection of issues reported for each QSS to show incoherence between user answers and beliefs to show that it's unknow the bug source and even it may be confused with QIndeterminacy.

*QDiff aims to generate semantically equivalent but syntactically different circuits and speed up by filtering circuits

* [Table III] Equivalent gates, it just transforms one gate to an equivalent one. Equivalent gate transformation, EGT. Their target is to diversify the pool of input programs.

* Uses mutation-based fuzz testing to calculate and compared equivalent programs using K-S distance from the reference distribution. Applying after a mutation operator

* Quantum simulation and execution
  * Compiler Configuration exploration, focus on optimization level. Qiskit, decides the type of optimization if it's just the collapse of adjacent gates (level 1) to resynthesize two-qubit blocks (level 3).

  * Backend exploration, runs same input programs using different backends

  * Filtering programs, as QDiff wants to focus on software defects, it does filter the problem to avoid any QP that may invoke errors due to hardware limitations.
    * Filters unnecessary circuits, comparing identical physical circuits after optimizations and logical-to-physical mappings.
    *Static analysis to remove possible unreliable executions and leaving meaningful divergences. This gets satisfied if the deepness of a QP is lower than a threshold defined by T1 (qubit degradation time)/(Avg gate execution time) and if the accumulative of gate errors is less than a hardware-depending threshold

* Equivalence checking: KS Test (t=0.1)  or Cross Entropy

* Reporting divergences: Depending on conditions it will categorize the divergences between backend, frontend and API gat implementation.

* Use of small QP due to reliability in quantum hardware and the restriction on IBM quantum systems use.

### Outcome:
* QDiff evaluated in Qiskit, Corq and Pyquil
* From six QP, QDiff generated 730 variant algorithms though mutations and then it created near 15000 variants by semantic-preserving transformations. QDiff filtering reduced testing time but 66%.
* 6 instability sources, 4 software crash bugs in Pyquil and Cirq and 2 root causes that may explain 25 out of 29 cases of divergence beyond expected noise on IBM hardware, due to unreliable connections between 2 qubits. All manually checked.


### Future work / Applications / Lacks:
* Use of QDiff to verify new QSS versions

### Data:
* https://github.com/wjy99-c/QDiff

### Unknown concepts:
* Fuzz mutation testing


### Papers ([Ref] and abstraction) :
- [ ] [8][9] Challenge generating semantically equivalent QP
- [ ] [10] Efficiency of testing compilers with equivalent programs
- [ ] [13]-[15] Possible backend bugs in QSS
- [ ] [32] Mutation-based fuzz testing
- [ ] [34][35] Quantum mutant generation
  - [x][35] input-output coverage {Under review}
- [ ] [47][48] Randomize compilation
- [ ] [58] Quantum software life cycle- Challenges and opportunities
- [ ] [59] Formally reasoning due to a representation of qubits and gates as matrix-valued boolean expressions
- [ ] [60] Quantum program assertions
- [ ] [61] Proq as runtime assertion framework for testing and debugging quantum programs
- [ ] [62] Classical model checking on quantum programs based on Quantum Markov chain.





