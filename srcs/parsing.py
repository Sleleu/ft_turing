import json
import argparse
from srcs.classes import TuringMachine

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
    if len(parser.parse_args().input) >= 0:
        raise ValueError("Input can't be empty")
    return (parser.parse_args())


def rec_is_duplicate(iterable: tuple)-> bool:
    match iterable :
        case []:
            return False
        case [hd, *tl]:
            return hd in tl or rec_is_duplicate(tl)

def rec_is_not_str(iterable)-> bool:
    match iterable :
        case []:
            return False
        case [hd, *tl]:
            if not isinstance(hd, str):
                return True
            return rec_is_not_str(tl)

def check_alphabet(alphabet: tuple, blank: str)-> tuple:
    """
    Checks if an alphabet is valid and contains the 'blank' character.
    """
    if rec_is_not_str(alphabet):
        raise TypeError("Values need to be a string type")
    if rec_is_duplicate(alphabet):
        raise ValueError("'alphabet' contain duplicates")
    if not all(map(lambda x: len(x) == 1 , alphabet)):
        raise ValueError("Each character of the alphabet must be a string of length strictly equal to 1")
    if blank not in alphabet:
        raise ValueError("'blank' not in 'alphabet'")

def check_states(states: tuple, initial: str, finals: tuple)-> tuple:
    """
    Checks if states are valid, including the initial state and final states.
    """
    if rec_is_not_str(states) or rec_is_not_str(finals):
        raise TypeError("Values need to be a string type")
    if rec_is_duplicate(states) or rec_is_duplicate(finals):
        raise ValueError("'states' or 'finals' contain duplicates")

    def rec_in_states(value, states)-> bool:
        """
        Recursively checks if a given value is present in a list of states.
        """
        if not states: return False
        return value == states[0] or rec_in_states(value, states[1:])
    
    if not rec_in_states(initial, states):
        raise ValueError("'initial' not in 'states'")
    
    def rec_check_finals_in_states(finals)-> None:
        """
        Recursively checks if each final state is in the tuple 'states'.
        
        This function is typically used to verify that all final states of a Turing machine are valid.
        """
        if not finals:
            return
        if not rec_in_states(finals[0], states):
            raise ValueError("'finals' not in 'states'")
        rec_check_finals_in_states(finals[1:])

    rec_check_finals_in_states(finals)

def rec_check_t_lines(t:tuple[dict[str, str]], alphabet, states)-> None:
    """
    Recursively check if each key is present, and if each value is present :
    - in 'states' for 'to_action' key
    - in 'alphabet' for 'read' and 'write' key
    - if 'action' contain only 'LEFT' or 'RIGHT'
    """
    if not t: return
    if t[0]["read"] not in alphabet or t[0]["write"] not in alphabet:
        raise ValueError("'read' and 'write' values must be in 'alphabet'")
    if t[0]["to_state"] not in states:
        raise ValueError("'to_state' must be in 'states'")
    if t[0]["action"] not in {"LEFT", "RIGHT"}:
        raise ValueError("'action' must be 'LEFT' or 'RIGHT'")
    rec_check_t_lines(t[1:], alphabet, states)

def rec_check_transitions(state_keys: tuple, transitions, alphabet: tuple, states: tuple)-> dict:
    """
    Recursively checks all transitions for each state.
    - check if each key is in the 'states' list
    - create a tuple ({"read": '1', ...}, {...}, ...) to recursively iterate 
      on all possibilities in a transition
    """
    if not state_keys: return
    key = state_keys[0]
    if key not in states:
        raise ValueError(f"Transition '{key}' not in states list")
    trans_tuple = tuple(transitions[key])
    if rec_is_duplicate(tuple(map(lambda i: trans_tuple[i]["read"], range(len(trans_tuple))))):
        raise ValueError(f"state '{key}' contain duplicates")
    rec_check_t_lines(trans_tuple, alphabet, states)
    rec_check_transitions(state_keys[1:], transitions, alphabet, states)

def check_transitions(transitions: dict[str, tuple[dict[str, str]]], alphabet: tuple, states: tuple):
    """
    Create a tuple of keys containing each transitions ("scanright", "eraseone", ...),
    to recursively iterate on them
    """
    state_keys : tuple = tuple(transitions.keys())
    rec_check_transitions(state_keys, transitions, alphabet, states)

def parse_data(data: json):
    """
    Parse and validate JSON data for the TuringMachine
    """
    check_alphabet((data["alphabet"]), data["blank"])
    check_states((data["states"]), data["initial"], (data["finals"]))
    check_transitions((data["transitions"]), data["alphabet"], data["states"])

def create_machine(data: json) -> TuringMachine:
    """
    Creates an instance of the Turing Machine from validated JSON data.
    """
    parse_data(data)
    return TuringMachine(
        name=data["name"],
        alphabet=tuple(data["alphabet"]),
        blank=data["blank"],
        states=tuple(data["states"]),
        initial=data["initial"],
        finals=tuple(data["finals"]),
        transitions=data["transitions"]
    )

def create_tape(input: str, machine: TuringMachine) -> dict:
    def check_input_char(i):
        char = input[i]
        if char not in machine.alphabet:
            raise ValueError(f"Character '{char}' must be in 'alphabet'")
        if char == machine.blank:
            raise ValueError(f"Character '{char}' is 'blank' and must not be in input")
        return (i, char)
    return dict(map(check_input_char, range(len(input))))
