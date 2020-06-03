"""Test class for the amplifier."""

import math
import unittest
from rfdesigner.components.amplifier import Amplifier


class TestAmplifier(unittest.TestCase):
    """Test the Amplifier class."""

    def test_bandwidth_default(self):
        """Test the default bandwidth properties."""
        amp = Amplifier()
        self.assertEqual(amp.f3db, math.inf)
        self.assertEqual(amp.fbw, math.inf)
