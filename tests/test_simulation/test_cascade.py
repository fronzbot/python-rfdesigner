"""Test module for core simulation methods."""
import unittest
import rfdesigner.simulation.cascade as sim
from rfdesigner.components import Generic


class TestCascade(unittest.TestCase):
    """Object to test cascade methods."""

    def setUp(self):
        """Set up cascade testing."""
        self.system = [
            Generic(gain=15, nf=3, p1db=10, iip3=20),
            Generic(gain=10, nf=6, p1db=12, iip3=30),
        ]
        self.expected_gain = 25
        self.expected_nf = 3.20
        self.expected_iip3 = 13.81
        self.expected_p1db = -3.21

    def test_exit_on_empty_system(self):
        """Test that sim returns empty dict on empty system."""
        result = sim.run()
        self.assertDictEqual(result, {})
        result = sim.run(system=[])
        self.assertDictEqual(result, {})

    def test_cascade_gain(self):
        """Test that gain is correctly cascaded."""
        result = sim.cascade_gain(self.system, [15, 10])
        self.assertEqual(result, self.expected_gain)
        self.assertEqual(self.system[0].total_gain, 15)
        self.assertEqual(self.system[1].total_gain, self.expected_gain)

    def test_cascade_nf(self):
        """Test that the nosie figure is correctly cascaded."""
        sim.cascade_gain(self.system, [15, 10])
        result = sim.cascade_property(
            self.system, [10 ** (3 / 10), 10 ** (6 / 10)], prop="nf"
        )
        self.assertEqual(result, self.expected_nf)
        self.assertEqual(self.system[0].total_nf, 3)
        self.assertEqual(self.system[1].total_nf, self.expected_nf)

    def test_cascade_iip3(self):
        """Test that the iip3 values are correctly cascaded."""
        sim.cascade_gain(self.system, [15, 10])
        result = sim.cascade_property(
            self.system, [10 ** ((20 - 30) / 10), 10 ** ((30 - 30) / 10)], prop="iip3"
        )
        self.assertEqual(result, self.expected_iip3)
        self.assertEqual(self.system[0].total_iip3, 20)
        self.assertEqual(self.system[1].total_iip3, self.expected_iip3)

    def test_cascade_p1db(self):
        """Test that the p1db values are correctly cascaded."""
        sim.cascade_gain(self.system, [15, 10])
        result = sim.cascade_property(
            self.system, [10 ** ((10 - 30) / 10), 10 ** ((12 - 30) / 10)], prop="p1db"
        )
        self.assertEqual(result, self.expected_p1db, msg=self.system[0].total_p1db)
        self.assertEqual(self.system[0].total_p1db, 10)
        self.assertEqual(self.system[1].total_p1db, self.expected_p1db)

    def test_cascade_full(self):
        """Test the full cascade method."""
        results = sim.run(self.system, pin=-60)
        self.assertEqual(results["pout"], -60 + self.expected_gain)
        self.assertEqual(results["gain"], self.expected_gain)
        self.assertEqual(results["nf"], self.expected_nf)
        self.assertEqual(results["iip3"], self.expected_iip3)
        self.assertEqual(results["oip3"], self.expected_iip3 + self.expected_gain)
