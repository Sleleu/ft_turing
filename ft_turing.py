#!/usr/bin/python3

from srcs.display import print_banner, print_machine_attributes
from srcs.parsing import load_json, create_machine, create_tape, parse_arguments
from srcs.actions import rec_process
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
        rec_process(machine, tape, 0, machine.initial)
    except (ValueError, KeyError, TypeError, RecursionError) as error:
        print(f"{__name__}: {type(error).__name__}: {error}")