#!/usr/bin/python3

from srcs.display import print_banner, print_machine_attributes
from srcs.parsing import load_json, create_machine, create_tape, parse_arguments
from srcs.actions import run_machine
from types import MappingProxyType as mpt

if __name__ == "__main__":
    try:
        args = parse_arguments()
        jsonfile = str(args.jsonfile)
        input = str(args.input)
        data = mpt(load_json(jsonfile))
        machine = create_machine(data)
        tape = create_tape(input, machine)
        print_banner()
        print_machine_attributes(machine)
        run_machine(machine, tape)
    except (ValueError, KeyError, TypeError) as error:
        print(f"{__name__}: {type(error).__name__}: {error}")
    except RecursionError as error:
        print(f"The machine cannot find a solution")