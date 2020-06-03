"""Initialize the variable gain amplifier class."""
from rfdesigner.components import RFSignal
from rfdesigner.components.amplifier import Amplifier


class VGA(Amplifier):
    """Representation of a variable gain amplifier."""

    def __init__(self, **kwargs):
        """
        Initialize a VGA object.

        Extends the amplifier class with the following optional inputs.
        :param gain_min: Minimum amplifier gain in dB
        :param gain_max: Maximum amplifier gain in dB
        :param gain_step: Amplifier gain step in dB/mV or dB/step
        :param control: Control voltage in mV or in steps for digital control
        """
        self._gain_min = RFSignal(kwargs.get("gain_min", 0), units="dBV")
        self._gain_max = RFSignal(kwargs.get("gain_max", 1), units="dBV")
        self._gain_step = RFSignal(kwargs.get("gain_step", 1), units="dBV")
        self._control = RFSignal(kwargs.get("control", 1), units="V")
        self._gain = RFSignal(1, "dBV")
        super().__init__(**kwargs)

    @property
    def gain(self):
        """Get the current gain."""
        value = self.control.V * self.gain_step.dBV + self.gain_min.dBV
        self._gain = RFSignal(value, units="dBV")
        self._gain = min(self._gain, self.gain_max)
        self._gain = max(self._gain, self.gain_min)
        return self._gain

    @gain.setter
    def gain(self, value):
        """Set the gain value."""
        self._gain = RFSignal(value, units="dBV")

    @property
    def gain_min(self):
        """Get the gain_min value."""
        return self._gain_min

    @gain_min.setter
    def gain_min(self, value):
        """Set the gain_min value."""
        self._gain_min = RFSignal(value, units="dBV")

    @property
    def gain_max(self):
        """Get the gain_max value."""
        return self._gain_max

    @gain_max.setter
    def gain_max(self, value):
        """Set the gain_max value."""
        self._gain_max = RFSignal(value, units="dBV")

    @property
    def gain_step(self):
        """Get the gain_step value."""
        return self._gain_step

    @gain_step.setter
    def gain_step(self, value):
        """Set the gain_step value."""
        self._gain_step = RFSignal(value, units="dBV")

    @property
    def control(self):
        """Get the vga control voltage."""
        return self._control

    @control.setter
    def control(self, value):
        """Set the vga control voltage."""
        self._control = RFSignal(value, units="V")
