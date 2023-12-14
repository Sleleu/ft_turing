# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    display.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: sleleu <sleleu@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/13 18:00:36 by sleleu            #+#    #+#              #
#    Updated: 2023/12/14 01:01:03 by sleleu           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from classes import TuringMachine

LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
END = "\033[0m"

def print_banner()-> None:
    print(f"{LIGHT_CYAN}╔════════════════════════════════════════════════════════════════════════════╗{END}")
    print(f"{LIGHT_CYAN}║{LIGHT_RED}  ███████ ████████         ████████ ██    ██ ██████  ██ ███    ██  ██████   {LIGHT_CYAN}║{END}")
    print(f"{LIGHT_CYAN}║{LIGHT_GREEN}  ██         ██               ██    ██    ██ ██   ██ ██ ████   ██ ██        {LIGHT_CYAN}║{END}")
    print(f"{LIGHT_CYAN}║{LIGHT_PURPLE}  █████      ██               ██    ██    ██ ██████  ██ ██ ██  ██ ██   ███  {LIGHT_CYAN}║{END}")
    print(f"{LIGHT_CYAN}║{YELLOW}  ██         ██               ██    ██    ██ ██   ██ ██ ██  ██ ██ ██    ██  {LIGHT_CYAN}║{END}")
    print(f"{LIGHT_CYAN}║{LIGHT_BLUE}  ██         ██    ███████    ██     ██████  ██   ██ ██ ██   ████  ██████   {LIGHT_CYAN}║{END}")
    print(f"{LIGHT_CYAN}╚════════════════════════════════════════════════════════════════════════════╝{END}")

def print_machine_attributes(machine: TuringMachine)-> None:
    print(f"Name: '{machine.name}'")
    print(f"Alphabet: {machine.alphabet}")
    print(f"Blank: '{machine.blank}'")
    print(f"States: {machine.states}")
    print(f"Initial: '{machine.initial}'")
    print(f"Finals: {machine.finals}")