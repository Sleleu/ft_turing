import json
from classes import TuringMachine

def rec_check_type(iterable):
    if not iterable: return
    if not isinstance(iterable[0], str):
        raise TypeError("Values need to be a string type")
    rec_check_type(iterable[1:])

def check_alphabet(alphabet: tuple[str], blank: str) -> tuple[str]:
    rec_check_type(alphabet)
    if not all(map(lambda x: len(x) == 1 , alphabet)):
        raise ValueError("Each character of the alphabet must be a string of length strictly equal to 1")
    if blank not in alphabet:
        raise ValueError("'blank' not in 'alphabet'")

def check_states(states: tuple[str], initial: str, finals: tuple[str]) -> tuple[str]:
    rec_check_type(states)
    rec_check_type(finals)

    def rec_in_states(value, states):
        return states and (value == states[0] or rec_in_states(value, states[1:]))
    
    if not rec_in_states(initial, states):
        raise ValueError("'initial' not in 'states'")
    
    def rec_check_finals_in_states(finals):
        if not finals:
            return
        if not rec_in_states(finals[0], states):
            raise ValueError("'finals' not in 'states'")
        rec_check_finals_in_states(finals[1:])

    rec_check_finals_in_states(finals)

def rec_check_t_lines(t:tuple[dict[str, str]], alphabet, states)-> None:
    if not t: return
    if t[0]["read"] not in alphabet or t[0]["write"] not in alphabet:
        raise ValueError("'read' and 'write' values must be in 'alphabet'")
    if t[0]["to_state"] not in states:
        raise ValueError("'to_state' must be in 'states'")
    if t[0]["action"] not in {"LEFT", "RIGHT"}:
        raise ValueError("'action' must be 'LEFT' or 'RIGHT'")
    rec_check_t_lines(t[1:], alphabet, states)

def rec_check_transitions(state_keys, transitions, alphabet: tuple[str], states: tuple[str])-> dict:
    if not state_keys: return
    key = state_keys[0]
    if key not in states:
        raise ValueError(f"Transition '{key}' not in states list")
    trans_tuple = transitions[key]
    rec_check_t_lines(trans_tuple, alphabet, states)
    rec_check_transitions(state_keys[1:], transitions, alphabet, states)

def check_transitions(transitions: dict[str, tuple[dict[str, str]]], alphabet: tuple[str], states: tuple[str]):
    state_keys = tuple(transitions.keys())
    rec_check_transitions(state_keys, transitions, alphabet, states)

def parse_data(data: json):
    check_alphabet((data["alphabet"]), data["blank"])
    check_states((data["states"]), data["initial"], (data["finals"]))
    check_transitions((data["transitions"]), data["alphabet"], data["states"])

def create_machine(data: json) -> TuringMachine:
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