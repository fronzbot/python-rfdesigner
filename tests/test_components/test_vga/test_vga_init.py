"""Test for VGA class."""
import unittest
from rfdesigner.components.vga import VGA


class TestVGA(unittest.TestCase):
    """Representation of VGA test case."""

    def test_vga_gain(self):
        """Test VGA gain property."""
        vga = VGA(gain_min=0, gain_max=10, gain_step=1)
        self.assertEqual(round(vga.gain.dBV, 2), 1)
        vga.control = 2
        self.assertEqual(round(vga.gain.dBV, 2), 2)
        vga.control = 11
        self.assertEqual(round(vga.gain.dBV, 2), 10)
