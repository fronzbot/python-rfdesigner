"""Main CLI entry point for RFDesigner."""
import sys
from rfdesigner.cli import RFcli
from rfdesigner.options import entry_arguments
from rfdesigner.netlist import parse_netlist, IMPLEMENTED_BLOCKS


def display_implemented():
    """Display implemented variables."""
    implemented_string = "Available blocks for netlisting:"
    for block in IMPLEMENTED_BLOCKS:
        implemented_string += f"\n  - {block}"
    implemented_string += "\n"
    return implemented_string


def display_properties(props):
    """Display supported properties for a block."""
    prop_string = "Available properties:\n"
    for prop in props:
        prop_string += f"  - <block>.{prop[0]:<14}units={prop[2]:<6}{prop[1]}\n"
    return prop_string


def main():
    """CLI handler."""
    parser = entry_arguments()
    args = parser.parse_args()
    if args.implemented:
        print(display_implemented())
        sys.exit(0)
    if args.properties:
        cls = IMPLEMENTED_BLOCKS[args.properties]()
        print(display_properties(cls.supported))
        sys.exit(0)
    if args.validate:
        netlist = args.validate
        result = parse_netlist(netlist)
        if not result:
            print("Netlist incorrect.")
            sys.exit(1)
        print(result)
        sys.exit(0)
    rfcli = RFcli()
    sys.exit(rfcli.cmdloop())


if __name__ == "__main__":
    main()
