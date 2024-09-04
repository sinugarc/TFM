import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MutTest import QMutation_TestingStructure
from QCRMut import mutant_generator
from shareFunctions import execution

from .BV_MR import BV_Alg_MT, BV_MR12, BV_MR3, BV_analysis, BV_input_generator_pairs, BV_input_generator_xor

BV_test_MR1 = QMutation_TestingStructure("BV_MR1",BV_Alg_MT, mutant_generator, BV_input_generator_pairs, BV_MR12, execution, BV_analysis)

BV_test_MR2 = QMutation_TestingStructure("BV_MR2",BV_Alg_MT, mutant_generator, BV_input_generator_xor, BV_MR12, execution, BV_analysis)

BV_test_MR3 = QMutation_TestingStructure("BV_MR3",BV_Alg_MT, mutant_generator, BV_input_generator_pairs, BV_MR3, execution, BV_analysis)