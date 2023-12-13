class Transition:
    read : str
    to_state : str
    write : str
    action : str

class TransitionList:
    dict[tuple[Transition]]

class TuringMachine:
    name : str
    alphabet : tuple[str]
    blank : str
    states : tuple[str]
    initial : str
    finals : tuple[str]
    transitions : TransitionList