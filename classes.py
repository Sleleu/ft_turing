class Transition():
    def __init__(self, read: str, to_state: str, write: str, action: str):
        self.read = read
        self.to_state = to_state
        self.write = write
        self.action = action

class TuringMachine:
    def __init__(self, name: str, alphabet: tuple[str], blank: str, states: tuple[str],
                 initial : str, finals : tuple[str], transitions: dict[str, tuple[Transition]]):
        self.name = name
        self.alphabet = alphabet
        self.blank = blank
        self.states = states
        self.initial = initial
        self.finals = finals
        self.transitions = transitions