import json
from srcs.classes import TuringMachine
from types import MappingProxyType as mpt

def rec_is_duplicate(iterable: tuple)-> bool:
    """ Pattern matching to check if there is a duplicate in an iterable """
    match iterable :
        case []:
            return False
        case [hd, *tl]:
            return hd in tl or rec_is_duplicate(tl)

def rec_is_not_str(iterable)-> bool:
    """ Pattern matching to check if all items in an iterable are string type """
    match iterable :
        case []:
            return False
        case [hd, *tl]:
            if not isinstance(hd, str):
                return True
            return rec_is_not_str(tl)

def check_alphabet(alphabet: tuple, blank: str)-> tuple:
    """ Checks if an alphabet is valid and contains the 'blank' character. """
    if rec_is_not_str(alphabet):
        raise TypeError("Values need to be a string type")
    if rec_is_duplicate(alphabet):
        raise ValueError("'alphabet' contain duplicates")
    if not all(map(lambda x: len(x) == 1 , alphabet)):
        raise ValueError("Each character of the alphabet must be a string of length strictly equal to 1")
    if blank not in alphabet:
        raise ValueError("'blank' not in 'alphabet'")

def check_states(states: tuple, initial: str, finals: tuple)-> tuple:
    """ Checks if states are valid, including the initial state and final states. """
    if rec_is_not_str(states) or rec_is_not_str(finals):
        raise TypeError("Values need to be a string type")
    if rec_is_duplicate(states) or rec_is_duplicate(finals):
        raise ValueError("'states' or 'finals' contain duplicates")

    def rec_in_states(value, states)-> bool:
        """ Recursively checks if a given value is present in a list of states. """
        if not states: return False
        return value == states[0] or rec_in_states(value, states[1:])
    
    if not rec_in_states(initial, states):
        raise ValueError("'initial' not in 'states'")
    
    def rec_check_finals_in_states(finals)-> None:
        """ Recursively checks if each final state is in the tuple 'states'. """
        if not finals:
            return
        if not rec_in_states(finals[0], states):
            raise ValueError("'finals' not in 'states'")
        rec_check_finals_in_states(finals[1:])

    rec_check_finals_in_states(finals)

def rec_check_t_lines(t:tuple[mpt[str, str]], alphabet, states)-> None:
    """ Recursively check if each key is present, and if each value is present """
    if not t: return
    if t[0]["read"] not in alphabet or t[0]["write"] not in alphabet:
        raise ValueError(f"'read' | 'write': '{t[0]['read']}' must be in 'alphabet'")
    if t[0]["to_state"] not in states:
        raise ValueError(f"'{t[0]['to_state']}' must be in 'states'")
    if t[0]["action"] not in {"LEFT", "RIGHT"}:
        raise ValueError("'action' must be 'LEFT' or 'RIGHT'")
    rec_check_t_lines(t[1:], alphabet, states)

def rec_check_transitions(state_keys: tuple, transitions: mpt, alphabet: tuple, states: tuple)-> mpt:
    """
    Recursively checks all transitions for each state.
    - check if each key is in 'states' and duplicates of read
    """
    def get_trans():
        return transitions[state_keys[0]]
 
    if not state_keys: return
    if state_keys[0] not in states:
        raise ValueError(f"Transition '{state_keys[0]}' not in states list")
    if rec_is_duplicate(tuple(map(lambda i: get_trans()[i]["read"], range(len(get_trans()))))):
        raise ValueError(f"state '{state_keys[0]}' contain duplicates")
    rec_check_t_lines(get_trans(), alphabet, states)
    rec_check_transitions(state_keys[1:], transitions, alphabet, states)

def parse_data(data: json):
    """ Parse and validate JSON data for the TuringMachine """
    check_alphabet((data["alphabet"]), data["blank"])
    check_states((data["states"]), data["initial"], (data["finals"]))
    rec_check_transitions((tuple(data["transitions"].keys())), data["transitions"], data["alphabet"], data["states"])

def create_machine(data: json) -> TuringMachine:
    """ Creates an instance of the Turing Machine from validated JSON data. """
    return TuringMachine(
        name=data["name"],
        alphabet=tuple(data["alphabet"]),
        blank=data["blank"],
        states=tuple(data["states"]),
        initial=data["initial"],
        finals=tuple(data["finals"]),
        transitions=data["transitions"]
    )

def create_tape(input: str, machine: TuringMachine) -> mpt:
    """ iter with map with the function check_input_char, return a dict """
    def check_input_char(i):
        """ return a pair of key/values """
        if input[i] not in machine.alphabet:
            raise ValueError(f"Character '{input[i]}' must be in 'alphabet'")
        if input[i] == machine.blank:
            raise ValueError(f"Character '{input[i]}' is 'blank' and must not be in input")
        return (i, input[i])
    return mpt(dict(map(check_input_char, range(len(input)))))
