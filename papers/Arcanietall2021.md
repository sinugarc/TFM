S. Ali, P. Arcaini, X. Wang, and T. Yue, “Assessing the effectiveness of input and output coverage criteria for testing quantum programs,” in Proc. 14th IEEE Conf. Softw. Testing Verif. Validation, 2021, pp. 13–23, doi: 10.1109/ICST49551.2021.00014.

### Bullet points
* Quito -> QUantum InpuT Output coverage, 3 coverage criteria

* It's going to follow a comparation between Quito and QSharpCheck

* Statistical assessment: Wilcoxon test, 99% confidence interval

* Formal definition of QP, input, output, program specification (set of all outcomes towards their probability, including 0 probability), valid output values (p greater than 0), test input, test outcome and test suite.
  * Is it practical?

* Test suit outcomes:
  * Definitely fail: outcome returns a not valid output (I guess they are only using simulators).
  * Likely fail: tested probability significantly deviates from expected probability by W-test.
  * Inconclusive: nothing wrong has been detected.

* Creation of 2 different oracles:
  * Wrong Output Oracle, WOO: Checks if QP only produces valid output values.
  * Output Probability Oracle, OPO: Checks if the QP returns an expected output with their assoc probability.

* Defines the input criteria, requires that all valid inputs get tested. Includes a parameter K in the criteria, that represents the number of executions for each valid input.

* Algorithm for test suite generation within input coverage, it just runs the algorithm executing K time each input, it will stop if it detects a non-valid output.

* Defines Output coverage, requires all possible outputs to be observed.

* Algorithm for test suite generation within output criteria. Need for a budget limit, in case we are unable to find one of the possible outcomes.

* Creates and algorithm combining both criteria.

* Coverage criteria assessment by mutation analysis:
  * As result may be different from each execution, every test suit will be executed K times for each criteria
  * Mutation operators:
    * AG, add gate
    * DG, delete gate
    * RG, replace gate
    * RMO, replace mathematical operator
    * Not going into classical mutation operators
  * Mutant will be considered killed if at least one of the oracles proposed fails. (Due to mutation score definition, I suppose that test suites killed by WOO won't be executed in OPO)
  * Mutation scored defined taking equivalent mutants(known) off the total number of mutants. As the number of eq mutants is unknown, authors take 0 to start with and analyse after test.
  * Equivalent mutants studied manually step by step, comparing states from original process and a mutated one, using QCEngine execution facility


### Outcome:
* 3 coverage criteria independent from specific language, with their own algorithm to create test suites to obtain full coverage

* Mutation scores tends to stay within the same range indp. of coverage criteria. Although there is some significances but with a real computational cost. ie, RCR reaches 80% mutation score with (8000 test cases in input coverage and over 15000 in output coverage) but it reaches a 95% on input-output coverage but using 160k test cases

* All non killed mutants were equivalent mutants and some of them had a phase difference. 


### Future work / Applications / Lacks:
* They want to work on: Testing QP phases, reduction of test cases through boundary values and equivalence partitioning.
* Need to have all possible values registered beforehand, called program specification and only uses programs with 2 or 3 qubits
* There is no knowledge/approach about equivalent mutants in QP
* There is no knowledge/guide of the right set up for parameters to be used in these criteria.

### Data:
https://simula- complex.github.io/Quantum- Software- Engineering/ICST21. html

### Unknown concepts:
* QSharpCheck
* Circle notation for QP states, is it worth it for more than 2 or 3 qubits? As it identifies each possible state with a circle.


### Papers ([Ref] and abstraction) :
- [ ] [2] Challenges in testing QP
- [ ] [3] QP testing methods survey
- [ ] [4] QSharpCheck, testing approach for Q#
- [ ] [7] Testing focused on  Markov chains
- [ ] [8] QuanFuzz, test input generator for QS
- [ ] [9] Definition of bugs in QC
- [ ] [10][11] Definition and assertion in QP as invariants, pre or post-conditions
- [ ] [13] Programming quantum computers book. Shows circle notation for QP states
- [ ] [15] Guidelines for Threats to Validity


### Obs

* This paper was a reference by 2 or more studied papers. It does need a citation evaluation.