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
        if self.units == "dBm":
            return self
        return RFSignal(self._convert_to_dBW() + 30.0)

    @property
    def dBW(self):
        """Return value is dBW."""
        if self.units == "dBW":
            return self
        return RFSignal(self._convert_to_dBW())

    @property
    def dBV(self):
        """Return value as dBV."""
        if self.units == "dBV":
            return self
        return RFSignal(2.0 * self._convert_to_dBW())

    @property
    def dBA(self):
        """Return value as dBA."""
        if self.units == "dBA":
            return self
        return RFSignal(2.0 * self._convert_to_dBW())

    @property
    def W(self):
        """Return value as Watts."""
        if self.units == "W":
            return self
        return RFSignal(self._convert_to_W())

    @property
    def V(self):
        """Return value as Volts."""
        if self.units == "V":
            return self
        return RFSignal(math.sqrt(self._convert_to_W() * 50.0))

    @property
    def A(self):
        """Return value as Amps."""
        if self.units == "A":
            return self
        return RFSignal(math.sqrt(self._convert_to_W() / 50.0))

    @property
    def Vgain(self):
        """Return value as V/V."""
        if self.units == "V":
            return self
        return RFSignal(10 ** (self._convert_to_dBW() / 10), units="V")

    def _convert_to_dBW(self):
        """Convert current units to dBW."""
        if self.units == "dBW":
            return self
        if self.units == "dBm":
            return self - 30.0
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
            return power * 50.0
        return power / 50.0

    def _convert_to_W(self):
        """Convert current units to Watts."""
        if self.units == "W":
            return self
        value_dBW = self
        if self.units != "dBW":
            value_dBW = self._convert_to_dBW()
        return 10 ** (value_dBW / 10.0)


class Generic:
    """Class representing a generic RF component."""

    def __init__(self, **kwargs):
        """
        Initialize generic class.

        All of the following inputs are optional.
        :param name: Name of the block (for example, a part name)
        :param power: Power consumption of the block in W
        :param gain: Gain of the block in dBW
        :param nf: Noise figure of the block in dB
        :param p1db: 1dB compression point in dBm
        :param oip3: Output 3rd-order intercept point in dBm
        :param iip3: Input 3rd-order intercept point in dBm
        """
        self.name = kwargs.get("name", "")
        self._power = RFSignal(kwargs.get("power", 0), units="W")
        self._gain = RFSignal(kwargs.get("gain", 0), units="dBW")
        self._nf = RFSignal(kwargs.get("nf", -1 * self.gain), units="dBW")
        self._p1db = RFSignal(kwargs.get("p1db", math.inf), units="dBm")
        self._oip3 = RFSignal(kwargs.get("oip3", math.inf), units="dBm")
        self._iip3 = RFSignal(kwargs.get("iip3", math.inf), units="dBm")

        self._total_gain = RFSignal(0, units="dBW")
        self._total_nf = RFSignal(0, units="dBW")
        self._total_iip3 = RFSignal(0, units="dBm")
        self._total_p1db = RFSignal(0, units="dBm")
        self._estimate_nonlinearities()

        self.is_compressed = False
        self._pout = RFSignal(0, units="dBm")

    def _estimate_nonlinearities(self):
        """Estimate non-linearities based on inputs."""
        if self.p1db == math.inf and self.oip3 == math.inf:
            self.oip3 = self.iip3 + self.gain
        if self.oip3 == math.inf and self.iip3 == math.inf:
            self.oip3 = self.p1db + 9.6
        if self.iip3 == math.inf:
            self.iip3 = self.oip3 - self.gain
        if self.p1db == math.inf:
            self.p1db = self.oip3 - 9.6
        if self.oip3 == math.inf:
            self.oip3 = self.iip3 + self.gain

    @property
    def power(self):
        """Get power value."""
        return self._power

    @power.setter
    def power(self, value):
        """Set power value."""
        self._power = RFSignal(value, units="W")

    @property
    def gain(self):
        """Get gain value."""
        return self._gain

    @gain.setter
    def gain(self, value):
        """Set gain value."""
        self._gain = RFSignal(value, units="dBW")

    @property
    def nf(self):
        """Get noise figure value."""
        return self._nf

    @nf.setter
    def nf(self, value):
        """Set noise figure value."""
        self._nf = RFSignal(value, units="dBW")

    @property
    def p1db(self):
        """Get p1db value."""
        return self._p1db

    @p1db.setter
    def p1db(self, value):
        """Set p1db value."""
        self._p1db = RFSignal(value, units="dBm")

    @property
    def oip3(self):
        """Get oip3 value."""
        return self._oip3

    @oip3.setter
    def oip3(self, value):
        """Set oip3 value."""
        self._oip3 = RFSignal(value, units="dBm")

    @property
    def iip3(self):
        """Get iip3 value."""
        return self._iip3

    @iip3.setter
    def iip3(self, value):
        """Set iip3 value."""
        self._iip3 = RFSignal(value, units="dBm")

    @property
    def total_gain(self):
        """Get total gain value."""
        return self._total_gain

    @total_gain.setter
    def total_gain(self, value):
        """Set total gain value."""
        self._total_gain = RFSignal(value, units="dBW")

    @property
    def total_nf(self):
        """Get total noise figure."""
        return self._total_nf

    @total_nf.setter
    def total_nf(self, value):
        """Set total noise figure."""
        self._total_nf = RFSignal(value, units="dBW")

    @property
    def total_iip3(self):
        """Get total iip3 value."""
        return self._total_iip3

    @total_iip3.setter
    def total_iip3(self, value):
        """Set total iip3 value."""
        self._total_iip3 = RFSignal(value, units="dBm")

    @property
    def total_p1db(self):
        """Get total p1db value."""
        return self._total_p1db

    @total_p1db.setter
    def total_p1db(self, value):
        """Set total p1db value."""
        self._total_p1db = RFSignal(value, units="dBm")

    @property
    def pout(self):
        """Get output power value."""
        return self._pout

    @pout.setter
    def pout(self, value):
        """Set output power value."""
        self._pout = RFSignal(value, units="dBm")

    def output(self, pin=0):
        """Generate output given input power."""
        _pin = pin
        if not isinstance(_pin, RFSignal):
            # Assume input power is dBm
            _pin = RFSignal(pin, units="dBm")
        self._pout = _pin.dBm + self.gain
        if _pin.dBm >= self.p1db - 1:
            self.is_compressed = True
            self._pout = self.gain + self.p1db - 1
        return self._pout


class Passive(Generic):
    """Class representing a generic passive."""
