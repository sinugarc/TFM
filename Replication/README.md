# Experiment replication

These are the instructions to replicate our experiments. The execution time may vary across different machines. Some experiments may take up to one day to execute on our machine.

We have divided this section into two folders, one corresponding to each chapter in the document.

## Set up

Download this folder and set up a Python environment. In our case, we used Pyenv with the following: Python 3.9.13 and Qiskit 0.38.0.

## QCRMut

### Experiment I and II

These experiments involve QCRMut mutants. Experiment I creates the desired mutants and records the time taken for their creation. Experiment II executes the mutants and calculates the mutant score. To reproduce these results, you can execute executeAll.sh to run all experiments, or run execute_I.sh and execute_II.sh separately. Both options should not be mixed, as this may cause issues with pre-existing folders.

*executeAll.sh* and *execute_II.sh* can accept an argument representing the number of processors you want to use. If no argument is provided, the system will automatically determine the number of processors.

### muskitTest

This experiment aims to reproduce Muskit's results. You need to execute *muskitTest.sh*.

### MemoryExp

This experiment observes the difference in memory usage between .py and .pgz files based on the number of LOC/Gates in the circuit. To execute, run *memoryExp.sh*.

## MetTesting

These experiments are configured to use two fewer CPUs than are available on your system. This can be changed in each test file.

### Metamorphic experiment

These experiments replicate Experiments I, II, and III of metamorphic testing. To reproduce these results, execute the Python file *matemorphicTest.py*.

### Seed experiment

These experiments reproduce Experiment I, II and III of the seed tests. To reproduce these results, execute the Python file *seedTest.py*.
