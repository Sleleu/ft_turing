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

def create_tape(input: str, machine: TuringMachine) -> dict:
    def check_input_char(i):
        char = input[i]
        if char not in machine.alphabet:
            raise ValueError(f"Character '{char}' must be in 'alphabet'")
        if char == machine.blank:
            raise ValueError(f"Character '{char}' is 'blank' and must not be in input")
        return (i, char)
    return dict(map(check_input_char, range(len(input))))

def exec_final_state(machine, tape, state):
    print("FINAL STATE")

def read_char_in_tape(tape, head, blank):
    return tape[head] if head in tape else blank

def rec_extract_action(read_char, transition: dict):
    match transition:
        case []: raise ValueError(f"character '{read_char}' is not in actual transition")
        case _ :
            return transition[0] if read_char in transition[0]["read"] else rec_extract_action(read_char, transition[1:]) 

def write_char_in_tape(tape, head, read_char):
    return dict()

def rec_process_read_write(machine, tape, head: int, state: str):
    # display_actual_state()
    if state in machine.finals:
        return exec_final_state(machine, tape, state)
    read_char: str = read_char_in_tape(tape, head, machine.blank)
    action: dict = rec_extract_action(read_char, machine.transitions[state])
    new_state = action["to_state"]
    new_tape = write_char_in_tape()
    print(new_tape)
    # new_head = head + 1 if action["action"] is "RIGHT" else head - 1
    # rec_process_read_write(machine, new_tape, new_head, new_state)

def run_machine(machine : TuringMachine, tape: dict):
    head: int = 0
    state: str = machine.initial
    rec_process_read_write(machine, tape, head, state)

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
        run_machine(machine, tape)
    except (ValueError, KeyError, TypeError) as error:
        print(f"{__name__}: {type(error).__name__}: {error}")
