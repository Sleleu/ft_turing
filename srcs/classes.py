from types import MappingProxyType as mpt
from dataclasses import dataclass

@dataclass(frozen=True)
class TuringMachine:
    name: str
    alphabet: tuple[str]
    blank: str
    states: tuple[str]
    initial : str
    finals : tuple[str]
    transitions: mpt[str, tuple[mpt[str, str]]]
    
@dataclass(frozen=True)
class Tape:
    tape : mpt
    head : int
    state : str
    read_char : str
    action: mpt[str, str]