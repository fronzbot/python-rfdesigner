"""Init file for simulation."""
import math
from rfdesigner.const import KBOLTZMAN


def noise_floor(nf=1, bandwidth=1, noise_temp=290):
    """
    Calculate noise floor of a receiver.

    :param nf: Noise figure in dB
    :param bandwidth: bandwidth in Hz
    :param noise_temp: noise temperature in Kelvin
    """
    return (
        10 * math.log10(KBOLTZMAN * noise_temp * 1000) + nf + 10 * math.log10(bandwidth)
    )


def snr(pin=0, mds=0, nf=0):
    """
    Calculate SNR from Pin, mds, and Noise Figure.

    :param pin: Input power in dBm.
    :param mds: Minimum detectable signal in dBm.
    :param nf: Noise Figure in dB.
    """
    return pin - mds - nf


def sfdr(iip3=0, mds=0):
    """
    Calculate SFDR from IIP3 and mds.

    :param iip3: Input-referred 3rd-order intercept point in dBm.
    :param mds: Minimum detectable signal in dBm.
    """
    return 2 / 3 * (iip3 - mds)
