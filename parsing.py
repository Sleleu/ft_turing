import json
from classes import TuringMachine

def rec_check_type(iterable)-> None:
    """
    Recursively checks if all elements in an iterable are str.
    """
    if not iterable: return
    if not isinstance(iterable[0], str):
        raise TypeError("Values need to be a string type")
    rec_check_type(iterable[1:])

def check_alphabet(alphabet: tuple, blank: str)-> tuple:
    """
    Checks if an alphabet is valid and contains the 'blank' character.
    """
    rec_check_type(alphabet)
    if not all(map(lambda x: len(x) == 1 , alphabet)):
        raise ValueError("Each character of the alphabet must be a string of length strictly equal to 1")
    if blank not in alphabet:
        raise ValueError("'blank' not in 'alphabet'")

def check_states(states: tuple, initial: str, finals: tuple)-> tuple:
    """
    Checks if states are valid, including the initial state and final states.
    """
    rec_check_type(states)
    rec_check_type(finals)

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

        :param finals: A list (or tuple) of final states to be checked.
        :param states: A list (or tuple) of all states for comparison.
        :raises ValueError: If any final state is not found in the list of all states.
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