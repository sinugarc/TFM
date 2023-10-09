Fortunato, D., Campos, J., & Abreu, R. (2022). Mutation testing of quantum programs: A case study with qiskit. IEEE Transactions on Quantum Engineering, 3, 1-17.

### Bullet points/ideas:
* Creation of QMutPy, as an extension of MutPy
* Case study on 24 real quantum programs from IBM's qiskit library
* QP are much harder to develop, so it's easier to make mistakes in the counterintuitive quantum programming world
* QP measssaurement are probabilistic and impossible to exmine without disrupting execution
* Bugs represent realistic mistakes that programmers often make.
* Mutants included:
  * QGR, Quantum gate replacement
  * QGD, Quantum gate deletion
  * QGI, Quantum gate insertion
  * QMI, Quantum measurement insertion
  * QMD, Quantum measurement delition

* Needs for a QP toolset, chosen MutPy as it fulfills all of them
  * Supports python programs and testing frameworks
  * Supports mutation operators
  * supports creation of reports

* MutPy workflow:
  * Load source code and test suite
  * Executes the original source code
  * applies mutation operators and generates all mutant versions of P
  * executes the test suite on each mutant and provides a summary of results

  * MutPy uses python AST

* Experiment baseline, QMutPy vs MutPy

* Experiment requirements: (Qiskit-Aqua provides all)
  * Real QP in qiskit and written in python
  * Open-souce implementation of each QP
  * Test suite of each QP

* Experimental metrics:
  * Mutation score
  * Mutation score without non executed mutants (maximun score d be achievable

* Where needed the statistical test is Kruskal-Wallis non parametric test with 0.01 significance

* It takes more time for the creation of quantum mutants than classical ones, although the creation time for the mutated version is similar for both.
  * QMut based on function calls instead of consntant or logical operators
  * Search for quantum gates

* [Table III] & [Table IV] Mutant summary and scores


### Outcome:
* Novel set of mutation operators for quantum programs
* Gate equivalence depending on number and type or arguments [Figure 1]
* Empericial evaluation of QMutPy effectiveness and efficiency

### Future work / Aplications / Lacks:
* Extend to different platforms
* Too many requirements for the experiment?
* Adapt/Create a new operation in Python AST for quantum gates (The idea is to reduce mutant creating runtime)

### Data:
* MutPy: https://github.com/danielfobooss/mutpy
* QMutPy: https://github.com/jose/qmutpy-experiments

### Unfamiliar items:
* MutPy
* unittest/pytest
* Abstract syntax tree within Python

### Articles ([Ref] and abstraction) :
* [4] Challenges in computer science
* [5][6] Software quality through testing
* [7]-[12] Classical testing approaches
* [13]-[15] Quantum testing approaches
* [16] Counterintuitive QW
* [18] Correct implementation of QP is harder
* [19]-[23] Mutation testing as improvement to testing practices
* [24] Effectiveness of mutation testing
* [25] Previous study
* [30] Previous article about mutation in QP
* [32] Described quantum mutation to asses the correct behavior of QP
* [33] Bug patterns in Qiskit programs
* [35] MutPy
* [40]-[43] preliminary work in quantum mutation
* [46] Best practices for code coverage
* [47] GNU parallel tool
* [49] guidelines for threats to validity
* [50] Lack of real world QP







