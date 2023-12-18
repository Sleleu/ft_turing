#!/usr/bin/python3

from srcs.display import print_banner, print_machine_attributes
from srcs.parsing import create_machine, create_tape, parse_data
from srcs.actions import rec_process
from types import MappingProxyType as mpt
import json
import sys

def load_json(path: str) -> json:
    with open(path, "r") as file:
        return json.load(file)

def print_help():
    return print("""usage: ft_turing [-h] jsonfile input

positional arguments:
  jsonfile            json description of the machine

  input               input of the machine

optional arguments:
  -h, --help          show this help message and exit
""", end=""), exit(0)

def parse_arguments():
    if len(sys.argv) == 2 and sys.argv[1] in ("-h", "--help"):
        print_help()
    if len(sys.argv) != 3:
        return print("ft_turing [-h] jsonfile input"), exit(1)
    if len(sys.argv[2]) <= 0:
        raise ValueError("Input can't be empty")

if __name__ == "__main__":
    HANDLED_ERRORS = (FileNotFoundError, PermissionError, ValueError, IsADirectoryError, 
                      KeyError, TypeError, AttributeError, RecursionError, KeyboardInterrupt)
    try:
        parse_arguments()
        data = mpt(load_json(sys.argv[1]))
        parse_data(data)
        machine = create_machine(data)
        tape = create_tape(sys.argv[2], machine)
        print_banner()
        print_machine_attributes(machine)
        rec_process(machine, tape, 0, machine.initial)
    except HANDLED_ERRORS as error:
        print(f"{__name__}: {type(error).__name__}: {error}")
        exit(1)