Paltenghi, M., & Pradel, M. (2023, May). MorphQ: Metamorphic testing of the qiskit quantum computing platform. In 2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE) (pp. 2413-2424). IEEE

##Bullet points
1. Presents MorphQ as a tester for Qiskit's platform.

1. It uses 10 Qiskit metamorphic relations to approach testing, all of them in 3 big groups:
  * Circuit transformation
    * Change of qubit order (non-semantic-preserving)
    * Inject null-effect operation (gate and gate.inverse(), no measurement)
    * Add quantum register (if coupling map not fixed)
    * Parameter injections (new within quantum computing)
    * Partitioned execution (if non-interacting subset of qubits)(non-semantic-preserving)

  * Representation transformation, conversion via QSAM

  * Execution transformation (adapting the environment)
    * Change of coupling map (if no added register)
    * Change of gate set
    * Change of opt level
    * Change of backend


1. What does MorphQ bring new to the table?
   * Quantum program generator, with an specific grammar proposal
   * New approach through metamorphic testing, to test quantum platforms,in particular Qiskit,  influenced by the classical idea of compiler testing.

1. QDiff as probably the only option before MorphQ on testing quantum platforms, Qdiff uses manually written programs and is based on differential testing

1. MorphQ steps:

   * Generating programs
     * A random approach won't be ideal as it will highly likely generate invalid programs
     * Creating programs  with template and grammar (Fig 4 and 5). Limiting to 30 gates due to complexity of operations (execution time).

   * Applying metamorphic transformations

   * Comparing behaviour in 2 levels:
     * Crash difference, if the transform program crashes, as it has been seen that none of the automatically generated programs crashes. The transformation could trigger some faults that manifest through crash.
     * Compares measured output bits of 2 non-crashing programs. Due to the probabilistic nature of measuring, it compares the distribution  with Kolmogorov-Smirnov test (p-value < 5%)

1. Warning management:
   * Semi-automatically clustering based on their crash message, abstracting the particulars of each message.

   * Randomly select few programs from each cluster and manually inspected.
     * Manually reverse every transformation until the one responsible for the crash is found.


##Outcome:
* Generating automatically over 8k non-crashing quantum programs
* Metamorphic transformations leads to a 23% follow-up crash programs. Only 56 of non-crashing programs doesn't fulfil the KS test. 
* Reports 13 bugs in Qiskit platform, 9 of them confirmed by Qiskit [Table III]
* Analysis of MR effectiveness, analysing all 13 bugs and the MR who helped detect them. Roundtrip via QASM and inject null-effect operations, but composing more than 1 transformation exposed 8 out of 13 bugs.
* There is no bugs found on the non-crash programs, there is differences but it's just due to randomness and it falls within the expect it for a 5% significance.
* Improvement vs previous work: Higher code coverage and diversity within follow-up programs


##Future work / Aplications / Lacks:
* Automating the crash cluster and minimization as there is manual inspection of a subset of each cluster
* It may be adapted to other quantum platforms, circuit-based model
* Only used in simulators to avoid false positives

##Data:
https://github.com/sola-st/ MorphQ-Quantum-Qiskit-Testing-ICSE-23

##Unfamiliar items:
* Differential testing
* Delta debugging


##Articles ([Ref] and abstraction) :

* [1] Quantum platforms(Qiskit) full of bugs, unrelated to classical bugs.
* [2] Oracle problem in quantum
* [3][4] metamorphic testing
* [7] QDiff | Estimation of right number of shots
* [9][10][11] Studies of Qiskit platform
* [12] Parametrization of quantum circuits
* [16] Universal gates
* [18][19] KS test
* [20] Delta debugging for minimal sequence
* Testing and manipulating quantum programs VII.Related work (b)
  * Coverage-based methods [30]





