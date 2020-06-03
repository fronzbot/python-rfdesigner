"""Test for VGA class."""
import unittest
from rfdesigner.components import RFSignal
from rfdesigner.components.vga import VGA


class TestVGA(unittest.TestCase):
    """Representation of VGA test case."""

    def test_vga_parameter_setting(self):
        """Test setting VGA parameters."""
        vga = VGA()
        vga.gain = 10
        self.assertEqual(vga.gain.__class__, RFSignal)
        vga.gain_min = 1
        self.assertEqual(vga.gain_min.__class__, RFSignal)
        vga.gain_max = 5
        self.assertEqual(vga.gain_max.__class__, RFSignal)
        vga.gain_step = 0.1
        self.assertEqual(vga.gain_step.__class__, RFSignal)
        vga.control = 1
        self.assertEqual(vga.control.__class__, RFSignal)

    def test_vga_gain(self):
        """Test VGA gain property."""
        vga = VGA(gain_min=0, gain_max=10, gain_step=1)
        self.assertEqual(round(vga.gain.dBV, 2), 1)
        vga.control = 2
        self.assertEqual(round(vga.gain.dBV, 2), 2)
        vga.control = 11
        self.assertEqual(round(vga.gain.dBV, 2), 10)
