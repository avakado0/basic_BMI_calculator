import unittest
from modules.solution import Engine, BMIFunctions, Validation
class TestBMICalculation(unittest.TestCase):
    def test_valid_value(self):
        bmi = BMIFunctions()
        self.assertEqual(bmi.calculate_bmi(60, 172), 20.28, "Incorrect BMI calculated")
class TestValidator(unittest.TestCase):
    def test_validate_BMI_inputs(self):
        validate = Validation()
        self.assertEqual(validate.validate_BMI_inputs('value', 172), False, "Incorrect BMI calculated")

unittest.main()        