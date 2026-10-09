import math
import unittest
from calculator import calculate, summarize, convert, number_properties

class CalculatorTests(unittest.TestCase):
    def test_original_bug_regressions(self):
        self.assertEqual(summarize([1,2,3,4])['median'],2.5)
        self.assertAlmostEqual(calculate('cbrt',[-27]),-3)
        self.assertEqual(calculate('lcm',[0,0]),0)
        self.assertEqual(set(summarize([1,1,2,2])['modes']),{1,2})
    def test_real_domains(self):
        for op,values in [('divide',[1,0]),('sqrt',[-1]),('ln',[0]),('log',[4,1]),('asin',[2]),('power',[-1,.5]),('factorial',[-1]),('combination',[3,-1])]:
            with self.subTest(op=op),self.assertRaises((ValueError,ZeroDivisionError)):
                calculate(op,values)
    def test_inputs_and_overflow(self):
        for values in ([float('nan')],[float('inf')]):
            with self.assertRaises(ValueError): summarize(values)
        with self.assertRaises(ValueError): calculate('add',[1])
        with self.assertRaises(ValueError): calculate('add',[1e308,1e308])
        self.assertGreater(calculate('factorial',[1000]),10**100)
    def test_conversion(self):
        self.assertEqual(convert(-40,'celsius','fahrenheit'),-40)
        self.assertAlmostEqual(convert(1,'mile','m'),1609.344)
        self.assertAlmostEqual(convert(0,'kelvin','celsius'),-273.15)
        for args in [(1,'kg','m'),(-1,'kg','g'),(-1,'kelvin','celsius')]:
            with self.assertRaises(ValueError):convert(*args)
    def test_properties(self):
        self.assertTrue(number_properties(17)['prime'])
        self.assertFalse(number_properties(25)['prime'])
        self.assertTrue(number_properties(153)['armstrong'])
        self.assertFalse(number_properties(-153)['armstrong'])
        self.assertTrue(number_properties(0)['perfect_square'])

if __name__=='__main__':unittest.main()
