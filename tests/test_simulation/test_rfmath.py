"""Test module for rfmath methods."""
import unittest
from rfdesigner.simulation import rfmath


class TestRFMath(unittest.TestCase):
    """Class to test rfmath methods."""

    def test_noise_floor(self):
        """Test the noise floor method."""
        result = rfmath.noise_floor(nf=0, bandwidth=1, noise_temp=290)
        self.assertEqual(round(result), -174)

    def test_snr(self):
        """Test the SNR method."""
        result = rfmath.snr(pin=10, mds=4, nf=0.5)
        self.assertEqual(result, 5.5)

    def test_sfdr(self):
        """Test the SFDR method."""
        result = rfmath.sfdr(iip3=20, mds=5)
        self.assertEqual(result, 10)
