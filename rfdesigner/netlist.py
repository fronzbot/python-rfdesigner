"""Netlist utility for RFDesigner."""
from os.path import isfile
import toml
from rfdesigner.components import Generic, Passive
from rfdesigner.components.amplifier import Amplifier, LNA, PowerAmp
from rfdesigner.components.detector import Detector
from rfdesigner.components.filter import LPF, BPF, HPF
from rfdesigner.components.mixer import Mixer
from rfdesigner.components.vga import VGA


IMPLEMENTED_BLOCKS = {
    "generic": Generic,
    "passive": Passive,
    "amplifier": Amplifier,
    "amp": Amplifier,
    "lna": LNA,
    "poweramp": PowerAmp,
    "pa": PowerAmp,
    "power_amp": PowerAmp,
    "detector": Detector,
    "lpf": LPF,
    "lowpass": LPF,
    "bpf": BPF,
    "bandpass": BPF,
    "hpf": HPF,
    "highpass": HPF,
    "mixer": Mixer,
    "demod": Mixer,
    "demodulator": Mixer,
    "modulator": Mixer,
    "vga": VGA,
}


def parse_netlist(file_name):
    """Parse a TOML formatted netlist file."""
    if not isfile(file_name):
        print(f"Netlist file {file_name} not found!")
        return None
    netlist = toml.load(file_name)
    system_list = {}
    for name, system in netlist.items():
        if name in ["sim", "simulator", "simulation"]:
            system_list["sim"] = system
            continue
        if validate_signal_chain(name, system):
            system_list[name] = SignalChain(name, system)
    return system_list


def validate_signal_chain(name, system):
    """Validate signal chain netlist."""
    if "1" not in system.keys():
        print("Cannot find first block in signal chain (missing key: 1)")
        return False
    for entry, value in system.items():
        try:
            if value["type"].lower() not in IMPLEMENTED_BLOCKS:
                print(f"{value['type']} is not a valid block entry.")
                return False
        except KeyError:
            print(f"'type' not defined for block #{entry} in {name}")
            return False
    return True


class SignalChain:
    """Object representing a signal chain."""

    def __init__(self, name, system):
        """Initialize the signal chain object."""
        self.name = name
        self.system = self.generate_system_list(system)

    def generate_system_list(self, system):
        """Create a list from netlisted system."""
        system_list = []
        for block_number in sorted(system):
            block_args = system[block_number]
            system_list.append(
                IMPLEMENTED_BLOCKS[block_args["type"].lower()](**block_args)
            )
        return system_list
