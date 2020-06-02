"""Test components.__init__ file."""

import math
import unittest
from rfdesigner.components import RFSignal, Generic


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


class TestGeneric(unittest.TestCase):
    """Test the generic RF class."""

    def test_minimal_setup(self):
        """Test setup with minimal arguments."""
        rf = Generic()
        self.assertEqual(rf.gain, 0)
        self.assertEqual(rf.nf, 0)
        self.assertEqual(rf.gain.__class__, RFSignal)
        self.assertEqual(rf.nf.__class__, RFSignal)

    def test_nf_from_gain(self):
        """Test that noise figure is correctly calculated from gain."""
        rf = Generic(gain=1)
        self.assertEqual(rf.nf, -1)

    def test_only_oip3_given(self):
        """Test that p1db and iip3 are calculated from oip3."""
        rf = Generic(gain=10, oip3=10)
        self.assertEqual(rf.iip3, 0)
        self.assertEqual(rf.p1db, 10 - 9.6)

    def test_only_iip3_given(self):
        """Test that p1db and oip3 are calculated from iip3."""
        rf = Generic(gain=10, iip3=10)
        self.assertEqual(rf.oip3, 20)
        self.assertEqual(rf.p1db, 20 - 9.6)

    def test_only_p1db_given(self):
        """Test that oip3 and iip3 are calculated from p1db."""
        rf = Generic(gain=10, p1db=10)
        self.assertEqual(rf.oip3, 10 + 9.6)
        self.assertEqual(round(rf.iip3, 1), 9.6)

    def test_full_config(self):
        """Test generic class with all arguments."""
        rf = Generic(name="foobar", power=1, gain=2, nf=3, p1db=4, oip3=5, iip3=6)
        self.assertEqual(rf.name, "foobar")
        self.assertEqual(rf.power, 1)
        self.assertEqual(rf.gain, 2)
        self.assertEqual(rf.nf, 3)
        self.assertEqual(rf.p1db, 4)
        self.assertEqual(rf.oip3, 5)
        self.assertEqual(rf.iip3, 6)

    def test_cascade(self):
        """Test cascade function."""
        rf = Generic(gain=10, p1db=10)
        self.assertEqual(rf.cascade(pin=1), 11)
        self.assertEqual(rf.cascade(pin=1).__class__, RFSignal)
        self.assertFalse(rf.is_compressed)
        self.assertEqual(rf.cascade(pin=20), 19)
        self.assertTrue(rf.is_compressed)
