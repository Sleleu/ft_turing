#!/usr/bin/python3

from srcs.display import print_banner, print_machine_attributes
from srcs.parsing import create_machine, create_tape
from srcs.actions import rec_process
from types import MappingProxyType as mpt
import json
import argparse

def load_json(path: str) -> json:
    HANDLED_ERRORS = (FileNotFoundError, PermissionError,
                      ValueError, IsADirectoryError)
    try:
        with open(path, "r") as file:
            data = json.load(file)
        return data
    except HANDLED_ERRORS as error:
        print(f"{__name__}: {type(error).__name__}: {error}")
        exit(1)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.usage = "ft_turing [-h] jsonfile input"
    parser.add_argument("jsonfile", help="json description of the machine")
    parser.add_argument("input", help="input of the machine")
    if len(parser.parse_args().input) <= 0:
        raise ValueError("Input can't be empty")
    return (parser.parse_args())

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