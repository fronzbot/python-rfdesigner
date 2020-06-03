"""Test for VGA class."""
import unittest
from rfdesigner.components import RFSignal
from rfdesigner.components.detector import Detector


class TestDetector(unittest.TestCase):
    """Representation of Detector test case."""

    def test_detector_setting(self):
        """Test setting detector values."""
        det = Detector()
        det.mds = 10
        self.assertEqual(det.mds.__class__, RFSignal)
        det.smax = 10
        self.assertEqual(det.mds.__class__, RFSignal)

    def test_detector_law_units(self):
        """Test detector units properly setup depending on law."""
        det = Detector()
        # Default is log
        self.assertEqual(det.law, "log")
        self.assertEqual(det.mds.units, "dBm")
        self.assertEqual(det.smax.units, "dBm")

        det.law = "square"
        self.assertEqual(det.mds.units, "W")
        self.assertEqual(det.smax.units, "W")

        det.law = "rms"
        self.assertEqual(det.mds.units, "V")
        self.assertEqual(det.smax.units, "V")

    def test_bad_detector_law(self):
        """Test that detector defaults to 'log'."""
        det = Detector(law="foobar")
        self.assertEqual(det.law, "log")
        det.law = "test"
        self.assertEqual(det.law, "log")

    def test_law_capitalization(self):
        """Check that law capitalization is ignored."""
        det = Detector()
        det.law = "sQuArE"
        self.assertEqual(det.law, "square")

    def test_detector_log_output(self):
        """Check that correct output given for log detector."""
        det = Detector(gain=10, mds=-10, smax=10, law="log")
        pin = 5  # in dBm
        self.assertEqual(det.output(pin=pin), 15)

        # Power < MDS
        pin = -11
        self.assertEqual(det.output(pin=pin), 0)

        # Power > Drange
        pin = 11
        self.assertEqual(det.output(pin=pin), 20)

    def test_detector_square_output(self):
        """Check that correct output given for log detector."""
        det = Detector(gain=10, mds=1e-6, smax=1, law="square")
        pin = RFSignal(0.001, units="W")
        self.assertEqual(det.output(pin=pin).W, 0.01)

        # Power < MDS
        pin = RFSignal(1e-9, units="W")
        self.assertEqual(det.output(pin=pin).W, 1e-5)

        # Power > Drange
        pin = RFSignal(10, units="W")
        self.assertEqual(det.output(pin=pin).W, 10)

    def test_detector_rms_output(self):
        """Check that correct output given for rms detector."""
        det = Detector(gain=20, mds=0.1, smax=10, law="rms")
        pin = RFSignal(0.5, units="V")
        self.assertEqual(det.output(pin=pin).V, 5)

        # Power < MDS
        pin = RFSignal(0.01, units="V")
        self.assertEqual(det.output(pin=pin).V, 1)

        # Power > Drange
        pin = RFSignal(20, units="V")
        self.assertEqual(round(det.output(pin=pin).V, 2), 100)
