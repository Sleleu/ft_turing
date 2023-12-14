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
    return (parser.parse_args())

if __name__ == "__main__":
    try:
        args = parse_arguments()
        jsonfile : str = args.jsonfile
        data = load_json(jsonfile)
        machine : TuringMachine = create_machine(data)
        print_banner()
        print_machine_attributes(machine)
    except (ValueError, KeyError, TypeError) as error:
        print(f"{__name__}: {type(error).__name__}: {error}")
