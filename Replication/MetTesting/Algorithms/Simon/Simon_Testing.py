import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MutTest import QMutation_TestingStructure
from QCRMut import mutant_generator
from shareFunctions import execution, input_generator

from .Simon_MR import Simon_Alg_MT, Simon_MR1, Simon_MR2, Simon_analysis

Simon_test_MR1 = QMutation_TestingStructure("Simon_MR1",Simon_Alg_MT, mutant_generator, input_generator, Simon_MR1, execution, Simon_analysis)

Simon_test_MR2 = QMutation_TestingStructure("Simon_MR2",Simon_Alg_MT, mutant_generator, input_generator, Simon_MR2, execution, Simon_analysis)