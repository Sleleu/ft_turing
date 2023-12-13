#!/usr/bin/python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: sleleu <sleleu@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/13 16:07:57 by sleleu            #+#    #+#              #
#    Updated: 2023/12/13 16:40:35 by sleleu           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import json
import argparse
from display import print_banner, print_machine_attributes
from classes import Transition, TransitionList, TuringMachine

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

def get_string(key: str, json: json) -> str:
    print("get_string")

def create_machine(data: json) -> TuringMachine:
    machine = TuringMachine()
    machine.name = data["name"]
    machine.alphabet = data["alphabet"]
    machine.blank = data["blank"]
    machine.states = data["states"]
    machine.initial = data["initial"]
    machine.finals = data["finals"]
    machine.transitions = data["transitions"]
    return machine

if __name__ == "__main__":
    args = parse_arguments()
    jsonfile : str = args.jsonfile
    data = load_json(jsonfile)
    machine : TuringMachine = create_machine(data)
    print_banner()
    print_machine_attributes(machine)

