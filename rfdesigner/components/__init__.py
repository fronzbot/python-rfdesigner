"""Generic component definitions."""
import math


VALID_UNITS = ["dBm", "dBA", "dBV", "dBW", "V", "A", "W"]


class RFSignal(float):
    """Class representing an RF signal."""

    def __new__(cls, value, *args, **kwargs):
        """Overload the new function for float class."""
        return super(cls, cls).__new__(cls, value)

    def __init__(self, *args, **kwargs):
        """Initialize the RFSignal data type."""
        self.units = kwargs.get("units", "dBm")
        if self.units not in VALID_UNITS:
            self.units = "dBm"
        if self.units == "dB":
            self.units = "dBV"

        super().__init__()

    def __add__(self, other):
        """Return class after add."""
        result = super(RFSignal, self).__add__(other)
        return self.__class__(result, units=self.units)

    def __sub__(self, other):
        """Return class after subtraction."""
        result = super(RFSignal, self).__sub__(other)
        return self.__class__(result, units=self.units)

    def __mul__(self, other):
        """Return class after multiplication."""
        result = super(RFSignal, self).__mul__(other)
        return self.__class__(result, units=self.units)

    def __truediv__(self, other):
        """Return class after div."""
        result = super(RFSignal, self).__truediv__(other)
        return self.__class__(result, units=self.units)

    def __pow__(self, other):
        """Return class after raised to power."""
        result = super(RFSignal, self).__pow__(other)
        return self.__class__(result, units=self.units)

    @property
    def dBm(self):
        """Return value as dBm."""
        return self._convert_to_dBW() + 30

    @property
    def dBW(self):
        """Return value is dBW."""
        return self._convert_to_dBW()

    @property
    def dBV(self):
        """Return value as dBV."""
        return 2 * self._convert_to_dBW()

    @property
    def dBA(self):
        """Return value as dBA."""
        return 2 * self._convert_to_dBW()

    @property
    def W(self):
        """Return value as Watts."""
        return self._convert_to_W()

    @property
    def V(self):
        """Return value as Volts."""
        return math.sqrt(self._convert_to_W() * 50)

    @property
    def A(self):
        """Return value as Amps."""
        return math.sqrt(self._convert_to_W() / 50)

    def _convert_to_dBW(self):
        """Convert current units to dBW."""
        if self.units == "dBm":
            return self - 30
        if self.units in ["dBV", "dBA"]:
            return 0.5 * self
        power = self
        if self.units in ["V", "A"]:
            power = self._convert_VA_to_W()
        return 10 * math.log10(power)

    def _convert_VA_to_W(self):
        """Convert Volts of Amps to Watts with 50Ohm reference."""
        power = self ** 2
        if self.units == "A":
            return power * 50
        return power / 50

    def _convert_to_W(self):
        """Convert current units to Watts."""
        value_dBW = self._convert_to_dBW()
        return 10 ** (value_dBW / 10)


class Generic:
    """Class representing a generic RF component."""

    def __init__(self, **kwargs):
        """
        Initialize generic class.

        All of the following inputs are optional.
        :param name: Name of the block (for example, a part name)
        :param power: Power consumption of the block in W
        :param gain: Gain of the block in dB
        :param nf: Noise figure of the block in dB
        :param p1db: 1dB compression point in dBm
        :param oip3: Output 3rd-order intercept point in dBm
        :param iip3: Input 3rd-order intercept point in dBm
        """
        self.name = kwargs.get("name", "")
        self.power = RFSignal(kwargs.get("power", 0), units="W")
        self.gain = RFSignal(kwargs.get("gain", 0), units="dBV")
        self.nf = RFSignal(kwargs.get("nf", -1 * self.gain), units="dBV")
        self.p1db = RFSignal(kwargs.get("p1db", math.inf), units="dBm")
        self.oip3 = RFSignal(kwargs.get("oip3", math.inf), units="dBm")
        self.iip3 = RFSignal(kwargs.get("iip3", math.inf), units="dBm")

        self.total_gain = RFSignal(0, units="dBV")
        self.total_nf = RFSignal(0, units="dBV")
        self.total_iip3 = RFSignal(0, units="dBm")
        self._estimate_nonlinearities()

        self.is_compressed = False
        self.pout = RFSignal(0, units="dBm")

    def _estimate_nonlinearities(self):
        """Estimate non-linearities based on inputs."""
        if self.p1db == math.inf and self.oip3 == math.inf:
            self.p1db = self.iip3 + self.gain
        if self.oip3 == math.inf and self.iip3 == math.inf:
            self.oip3 = self.p1db.dBm + 9.6
        if self.iip3 == math.inf:
            self.iip3 = self.oip3.dBm - self.gain.dBV
        if self.p1db == math.inf:
            self.p1db = self.oip3.dBm - 9.6
        if self.oip3 == math.inf:
            self.oip3 = self.iip3.dBm + self.gain.dBV

    def cascade(self, pin=0):
        """Generate output after cascading."""
        _pin = RFSignal(pin, "dBm")
        self.pout = _pin.dBm + self.gain.dBV
        if _pin.dBm >= self.p1db.dBm - 1:
            self.is_compressed = True
            self.pout = self.gain.dBV + self.p1db.dBm - 1
        return self.pout.dBm
