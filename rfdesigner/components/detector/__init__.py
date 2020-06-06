"""Initialize the detector class."""
from rfdesigner import const
from rfdesigner.components import RFSignal
from rfdesigner.components.amplifier import Amplifier, AMP_SUPPORTED


LAW_UNIT_MAP = {
    "log": "dBm",
    "square": "W",
    "rms": "V",
}

DETECTOR_SUPPORTED = [const.ATTR_LAW, const.ATTR_MDS, const.ATTR_SMAX] + AMP_SUPPORTED


class Detector(Amplifier):
    """Representation of a detector object."""

    def __init__(self, **kwargs):
        """
        Initialize a Detector object.

        Creates a detection block with the following inputs.
        :param law: Detector law type. log/square/rms.  Defaul log.
        :param mds: Minimium detecable signal. Units derived from law type.
        :param smax: Maximum detectable input signal. Units derived from law type.
        """
        super().__init__(**kwargs)
        self._law = kwargs.get("law", "log").lower()
        self._mds = RFSignal(kwargs.get("mds", 0), units=LAW_UNIT_MAP[self.law])
        self._smax = RFSignal(kwargs.get("smax", 1), units=LAW_UNIT_MAP[self.law])

    @property
    def law(self):
        """Get law value."""
        if self._law not in LAW_UNIT_MAP:
            self._law = "log"
        return self._law

    @law.setter
    def law(self, value):
        """Set law value."""
        self._law = value.lower()

    @property
    def mds(self):
        """Get mds value."""
        self._mds.units = LAW_UNIT_MAP[self.law]
        return self._mds

    @mds.setter
    def mds(self, value):
        """Set mds value."""
        self._mds = RFSignal(value, units=LAW_UNIT_MAP[self.law])

    @property
    def smax(self):
        """Get smax value."""
        self._smax.units = LAW_UNIT_MAP[self.law]
        return self._smax

    @smax.setter
    def smax(self, value):
        """Set smax value."""
        self._smax = RFSignal(value, units=LAW_UNIT_MAP[self.law])

    def output(self, pin=0):
        """Get output power values."""
        self._pout = super().output(pin=pin)
        self._pout = max(self._pout.dBm, self.mds.dBm + self.gain)
        self._pout = min(self._pout.dBm, self.smax.dBm + self.gain)
        return self._pout

    @property
    def supported(self):
        """Return supported features."""
        return DETECTOR_SUPPORTED
