#!/usr/bin/python3

import json
import argparse
from display import print_banner, print_machine_attributes
from classes import TuringMachine
from parsing import create_machine

def load_json(path: str) -> json:
    HANDLED_ERRORS = (FileNotFoundError, PermissionError,
                      ValueError, IsADirectoryError)
    try:
        with open(path, "r") as file:
            data = json.load(file)
        return data
    except HANDLED_ERRORS as error:
        print(f"{__name__}: {type(error).__name__}: {error}")
        return None

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.usage = "ft_turing [-h] jsonfile input"
    parser.add_argument("jsonfile", help="json description of the machine")
    parser.add_argument("input", help="input of the machine")
    return (parser.parse_args())

def get_pair_from_input(i: int, machine: TuringMachine)-> tuple:
    char = input[i]
    if char not in machine.alphabet:
        raise ValueError(f"Character '{char}' must be in 'alphabet'")
    if char == machine.blank:
        raise ValueError(f"Character '{char}' is 'blank' and must not be in input")
    return (i, char)

def create_tape(input: str, machine: TuringMachine) -> dict:
    return dict(map(lambda i : get_pair_from_input(i, machine), range(len(input))))

if __name__ == "__main__":
    try:
        args = parse_arguments()
        jsonfile : str = args.jsonfile
        input : str = args.input
        data = load_json(jsonfile)
        machine : TuringMachine = create_machine(data)
        tape : dict = create_tape(input, machine)
        print_banner()
        print_machine_attributes(machine)
        print(tape)
        # rec_run_machine(machine, tape)
    except (ValueError, KeyError, TypeError) as error:
        print(f"{__name__}: {type(error).__name__}: {error}")
