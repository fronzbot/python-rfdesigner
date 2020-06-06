"""CLI definitions for RFDesigner."""
import sys
import os.path
import json
import cmd2
from rfdesigner import options
from rfdesigner.netlist import parse_netlist
from rfdesigner.simulation import cascade


def validate_cascade_args(args, systems):
    """Validate cascade arguments."""
    errors = []
    if args.name not in systems:
        errors.append(f"{args.name} not found in system list.")

    if args.pin is None:
        try:
            args.pin = systems["sim"]["pin"]
        except KeyError:
            args.pin = 0
    if args.bw is None:
        try:
            args.bw = systems["sim"]["bw"]
        except KeyError:
            args.bw = 1
    if args.temp is None:
        try:
            args.temp = systems["sim"]["temp"]
        except KeyError:
            args.temp = 290

    if args.save is not None:
        if os.path.isdir(args.save):
            args.save = os.path.join(args.save, f"rf_cascade_results_{args.name}.json")
        elif not os.path.isfile(args.save):
            errors.append(f"{args.save} not a valid file or directory.")

    if errors:
        return (False, errors)
    return (True, args)


class RFcli(cmd2.Cmd):
    """Command processer for RFDesigner."""

    prompt = "%rf> "
    systems = None

    def do_netlist(self, netlist_file):
        """Netlist a file."""
        self.systems = parse_netlist(netlist_file)

    def do_show_systems(self, line):
        """Show netlisted systems."""
        system_string = ""
        try:
            for name, chain in self.systems.items():
                if name == "sim":
                    continue
                system_string += f"{name}:\n"
                count = 1
                for block in chain.system:
                    system_string += f"{count}: {block.__class__}\n"
                    count += 1
            self.poutput(system_string)
        except TypeError:
            self.poutput("Please run netlister first.")

    @cmd2.with_argparser(options.cascade_arguments())
    def do_cascade(self, args):
        """Run cascade analysis."""
        result, args = validate_cascade_args(args, self.systems)
        if not result:
            for error in args:
                self.poutput(error)
            return

        result = cascade.run(
            system=self.systems[args.name].system,
            pin=args.pin,
            bandwidth=args.bw,
            noise_temp=args.temp,
        )
        if not args.no_output:
            self.poutput(json.dumps(result))
        if args.save:
            with open(args.save, "w") as json_file:
                json.dump(result, json_file, indent=4)
            self.poutput(f"Results saved to {args.save}")

    def do_exit(self, line):
        """Exit command line interface."""
        sys.exit(0)
