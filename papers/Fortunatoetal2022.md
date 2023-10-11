Fortunato, D., Campos, J., & Abreu, R. (2022). Mutation testing of quantum programs: A case study with qiskit. IEEE Transactions on Quantum Engineering, 3, 1-17.

### Bullet points/ideas:
* Creation of QMutPy, as an extension of MutPy
* Case study on 24 real quantum programs from IBM's qiskit library
* QP are much harder to develop, so it's easier to make mistakes in the counterintuitive quantum programming world
* QP measurements are probabilistic and impossible to examine without disrupting execution
* Bugs represent realistic mistakes that programmers often make.
* Mutants included:
  * QGR, Quantum gate replacement
  * QGD, Quantum gate deletion
  * QGI, Quantum gate insertion
  * QMI, Quantum measurement insertion
  * QMD, Quantum measurement deletion

* Needs for a QP toolset, chosen MutPy as it fulfils all of them
  * Supports python programs and testing frameworks
  * Supports mutation operators
  * Supports creation of reports

* MutPy workflow:
  * Load source code and test suite
  * Executes the original source code
  * Applies mutation operators and generates all mutant versions of P
  * Executes the test suite on each mutant and provides a summary of results

  * MutPy uses python AST

* Experiment baseline, QMutPy vs MutPy

* Experiment requirements: (Qiskit-Aqua provides all)
  * Real QP in qiskit and written in python
  * Open-source implementation of each QP
  * Test suite of each QP

* Experimental metrics:
  * Mutation score
  * Mutation score without non executed mutants (maximum score d be achievable

* Where needed the statistical test is Kruskal-Wallis non-parametric test with 0.01 significance

* It takes more time for the creation of quantum mutants than classical ones, although the creation time for the mutated version is similar for both.
  * QMut based on function calls instead of constant or logical operators
  * Search for quantum gates

* [Table III] & [Table IV] Mutant summary and scores. Big difference, as expected, between gate mutations and measurements.


### Outcome:
* Novel set of mutation operators for quantum programs
* Gate equivalence depending on number and type or arguments [Figure 1]
* Empirical evaluation of QMutPy effectiveness and efficiency
* Test suits may focus only in the quantum part of the program, as seen per difference of mutation score between classical and quantum mutations and the killing type (error vs test assertion)
* Increase of test suites to improve coverage in only 2 QP to prove that LOC coverage was directly impacting mutation score
* Asserting number of measurements to avoid false negatives. Directly affecting mutation score as we avoid false positives (shor's alg)

### Future work / Applications / Lacks:
* Extend to different platforms and increase of mutation operators (they are working on)
* Too many requirements for the experiment?
* Adapt/Create a new operation in Python AST for quantum gates (The idea is to reduce mutant creating runtime)
* Only 11 QP out of 24 had QMut introduced by QMutPy
* Better approaches to reduce number of design errors of QMI mutation
* Automatic test generation for QP, as now manually produced test achieved a higher mutation score.

### Data:
* MutPy: https://github.com/danielfobooss/mutpy
* QMutPy: https://github.com/jose/qmutpy-experiments

### Unknown concepts:
* MutPy
* unittest/pytest
* Abstract syntax tree within Python

### Papers ([Ref] and abstraction) :
- [ ] [4] Challenges in computer science
- [ ] [5][6] Software quality through testing
- [ ] [7]-[12] Classical testing approaches
- [ ] [13]-[15] Quantum testing approaches
- [ ] [16] Counterintuitive QW
- [ ] [18] Correct implementation of QP is harder
- [ ] [19]-[23] Mutation testing as improvement to testing practices
- [ ] [24] Effectiveness of mutation testing
- [ ] [25] Previous study 
- [x] [30] Previous article about mutation in QP {Introduction to this article}{No review needed}
- [ ] [32] Described quantum mutation to assess the correct behaviour of QP
- [ ] [33] Bug patterns in Qiskit programs
- [ ] [35] MutPy
- [ ] [40]-[43] preliminary work in quantum mutation
  - [ ] [40] Analysis in automatic generated test with 4 mutation operators
  - [ ] [41] Muskit, mutation tool without equivalence gates implemented
  - [x] [42] QDiff {Under review}
  - [ ] [43] MTQC, Java quantum mutation tool for Qiskit and Q#
- [ ] [46] Best practices for code coverage
- [ ] [47] GNU parallel tool
- [ ] [49] guidelines for threats to validity
- [ ] [50] Lack of real world QP







