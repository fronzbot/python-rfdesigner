"""Module to handle argument parsing."""
import argparse
from rfdesigner.const import __version__
from rfdesigner.netlist import IMPLEMENTED_BLOCKS


def entry_arguments():
    """Get valid arguments to be used at CLI entry."""
    parser = argparse.ArgumentParser(
        description="RFDesigner: RF system design, simplified."
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--implemented",
        action="store_true",
        help="Display list of implemented blocks usable in a netlist.",
    )
    parser.add_argument(
        "--properties",
        choices=IMPLEMENTED_BLOCKS.keys(),
        help="Dispaly list of properties that can be used for the given block type.",
    )
    parser.add_argument("--validate", type=str, help="Validate provided netlist file.")

    return parser


def cascade_arguments():
    """Get valid arguments for cascade analysis."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name",
        type=str,
        help="Name of system to perform cascade analysis on (from netlist)",
    )
    parser.add_argument("--pin", type=float, help="Input power in dBm")
    parser.add_argument("--bw", type=float, help="Signal bandwidth in MHz")
    parser.add_argument("--temp", type=int, help="Noise temperature in Kelvin")
    parser.add_argument("--save", "-s", type=str, help="Location to store results")
    parser.add_argument(
        "--no-output", action="store_true", help="Supress results outputing to terminal"
    )

    return parser
