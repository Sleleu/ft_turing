class TuringMachine:
    def __init__(self, name: str, alphabet: tuple[str], blank: str, states: tuple[str],
                 initial : str, finals : tuple[str], transitions: dict[str, tuple[dict[str, str]]]):
        self.name = name
        self.alphabet = alphabet
        self.blank = blank
        self.states = states
        self.initial = initial
        self.finals = finals
        self.transitions = transitions