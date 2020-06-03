"""Initialize the filter classes."""
from rfdesigner.components import Passive


class LPF(Passive):
    """Representation of a low pass filter."""


class HPF(Passive):
    """Representation of a high pass filter."""


class BPF(Passive):
    """Representation of a band pass filter."""
