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
    return alphabet

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
    return states

# changer transition en fonctionnel 
# + séparer les check et assignation des variables en plus 
# de fonctions découpées
# peut-être faire les duplicats

def check_transitions(transitions: dict, alphabet: list[str], states: list[str])-> dict:
    for state, trans_list in transitions.items():
        if state not in states:
            raise ValueError(f"Transition '{state}' is not in the states list")
        for trans in trans_list:
            if trans["read"] not in alphabet or trans["write"] not in alphabet:
                raise ValueError("'read' and 'write' values must be in 'alphabet'")
            if trans["to_state"] not in states:
                raise ValueError("'to_state' must be in 'states'")
            if trans["action"] not in {"LEFT", "RIGHT"}:
                raise ValueError("'action' must be 'LEFT' or 'RIGHT'")
    return transitions

def create_machine(data: json) -> TuringMachine:
    alphabet = check_alphabet(tuple[str](data["alphabet"]), data["blank"])
    states = check_states(tuple[str](data["states"]), data["initial"], tuple[str](data["finals"]))
    transitions = check_transitions(dict[str, tuple[str]](data["transitions"]), alphabet, states)

    return TuringMachine(
        name=data["name"],
        alphabet=alphabet,
        blank=data["blank"],
        states=states,
        initial=data["initial"],
        finals=data["finals"],
        transitions=transitions
    )