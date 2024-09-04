import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MutTest import QMutation_TestingStructure
from QCRMut import mutant_generator
from shareFunctions import execution

from .DJ_MR import DJ_Alg_MT, DJ_input_generator, DJ_input_generator_MR1, DJ_MR1, DJ_MR2, DJ_analysis

DJ_test_MR1 = QMutation_TestingStructure("DJ_MR1",DJ_Alg_MT, mutant_generator, DJ_input_generator_MR1, DJ_MR1, execution, DJ_analysis)

DJ_test_MR2 = QMutation_TestingStructure("DJ_MR2",DJ_Alg_MT, mutant_generator, DJ_input_generator, DJ_MR2, execution, DJ_analysis)