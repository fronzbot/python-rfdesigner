"""Initialize the Amplifier objects."""
import math
from rfdesigner.components import Generic


class Amplifier(Generic):
    """Representation of a generic amplifier."""

    def __init__(self, **kwargs):
        """
        Initialize a generic amplifier object.

        Extends the Generic class with the following options inputs.
        :param f3db: 3dB bandwidth of the amplifier in MHz
        :param fbw: cutoff frequency of the amplifier in MHz
        """
        super().__init__(**kwargs)
        self.f3db = kwargs.get("f3db", math.inf)
        self.fbw = kwargs.get("fbw", math.inf)


class LNA(Amplifier):
    """Representation of an LNA."""


class PowerAmp(Amplifier):
    """Representation of a Power Amplifier."""
