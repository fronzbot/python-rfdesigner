"""Test components.__init__ file."""

import math
import unittest
from rfdesigner.components import RFSignal


class TestRFSignalClass(unittest.TestCase):
    """Test the RFSignal type."""

    def test_correct_type(self):
        """Test to check if class is immutable."""
        my_var = RFSignal(1)
        my_var += 1
        self.assertEqual(my_var.__class__, RFSignal)
        my_var -= 1
        self.assertEqual(my_var.__class__, RFSignal)
        my_var *= 1
        self.assertEqual(my_var.__class__, RFSignal)
        my_var /= 1
        self.assertEqual(my_var.__class__, RFSignal)
        my_var = my_var ** 2
        self.assertEqual(my_var.__class__, RFSignal)

    def test_assign(self):
        """Test to check basic assignment."""
        my_var = RFSignal(2)
        self.assertEqual(my_var, 2)

    def test_default_units(self):
        """Test to check correct default units."""
        my_var = RFSignal(1)
        self.assertEqual(my_var.units, "dBm")
        my_var = RFSignal(1, units="bad-option")
        self.assertEqual(my_var.units, "dBm")

    def test_no_unit_change(self):
        """Test to check that units don't change with math operands."""
        my_var = RFSignal(1)
        self.assertEqual(my_var.units, "dBm")
        my_var += 1
        self.assertEqual(my_var.units, "dBm")
        new_var = my_var - 4
        self.assertEqual(new_var.__class__, RFSignal)
        self.assertEqual(new_var.units, "dBm")

    def test_basic_math(self):
        """Test to check basic math operations."""
        my_var = RFSignal(2)
        self.assertEqual(my_var + 1, 3)
        self.assertEqual(my_var - 2, 0)
        self.assertEqual(my_var - 3, -1)
        self.assertEqual(my_var * 2, 4)
        self.assertEqual(my_var / -2, -1)

    def test_units_as_dBm(self):
        """Test to check correct unit conversions."""
        my_var = RFSignal(0, units="dBm")
        self.assertEqual(my_var.dBm, 0)
        self.assertEqual(my_var.dBW, -30)
        self.assertEqual(my_var.dBV, -60)
        self.assertEqual(my_var.dBA, -60)
        self.assertEqual(my_var.W, 0.001)
        self.assertEqual(my_var.V, math.sqrt(0.05))
        self.assertEqual(my_var.A, math.sqrt(0.00002))
