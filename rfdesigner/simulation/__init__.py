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


def cascade_property(system, values, prop="nf"):
    """Perform cascade analysis for given property."""
    running_sum = 0
    for index, val in enumerate(values):
        if index == 0:
            running_sum = 1 / val
            if prop == "nf":
                running_sum = val
        else:
            gains = system[index].total_gain - system[index].gain
            if prop == "nf":
                running_sum += (val - 1) / 10 ** (gains / 10)
            else:
                running_sum += 1 / val * 10 ** (gains / 10)
        if prop == "nf":
            save_val = round(10 * math.log10(running_sum), 2)
            system[index].total_nf = save_val
        else:
            try:
                save_val = round(10 * math.log10(1 / running_sum) + 30, 2)
            except ZeroDivisionError:
                save_val = math.inf
            if prop == "iip3":
                system[index].total_iip3 = save_val
            elif prop == "p1db":
                system[index].total_p1db = save_val
    return save_val


def cascade_gain(system, gain_vals):
    """Cascade system gains."""
    total_gain = sum(gain_vals)
    running_sum = 0
    for index, gain in enumerate(gain_vals):
        running_sum += gain
        system[index].total_gain = running_sum
    return round(total_gain, 2)


def cascade(system=None, pin=0, bandwidth=1, noise_temp=290):
    """
    Perform cascade analysis on signal chain.

    :param system: Sequential list of RF objects where position in list indicates position in signal chain. Currently mutli-branch networks not supported.
    :param pin: Input power of the system in dBm.
    :param bandwidth: Bandwidth of input signal in Hz.
    :param noise_temp: Noise temperature in Kelvin.
    """
    if not system:
        return {}

    gain_array = []
    nf_array = []
    iip3_array = []
    p1db_array = []

    for block in system:
        gain_array.append(block.gain.dBW)
        nf_array.append(block.nf.W)
        iip3_array.append(block.iip3.W)
        p1db_array.append(block.p1db.W)

    total_gain = cascade_gain(system, gain_array)
    total_nf = cascade_property(system, nf_array, prop="nf")
    total_iip3 = cascade_property(system, iip3_array, prop="iip3")
    total_p1db = cascade_property(system, p1db_array, prop="p1db")
    total_oip3 = total_iip3 + total_gain
    mds = noise_floor(nf=total_nf, bandwidth=bandwidth, noise_temp=noise_temp)
    snr = pin - mds - total_nf
    sfdr = 2 / 3 * (total_iip3 - mds)

    results = {
        "pin": pin,
        "pout": pin + total_gain,
        "gain": total_gain,
        "nf": total_nf,
        "iip3": total_iip3,
        "oip3": total_oip3,
        "p1db": total_p1db,
        "snr": snr,
        "sfdr": sfdr,
        "mds": mds,
    }
    return results
