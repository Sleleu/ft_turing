from srcs.classes import TuringMachine, Tape
from srcs.display import print_stat
from tail_recursive import tail_recursive
from types import MappingProxyType as mpt

def get_char(tape: mpt, head: int, blank: str):
    return tape.get(head, blank)

def rec_extract_action(read_char: str, transition: mpt)-> mpt:
    match transition:
        case []: raise ValueError(f"character '{read_char}' is not in actual transition")
        case _ :
            return transition[0] if read_char in transition[0]["read"] else rec_extract_action(read_char, transition[1:]) 

def write_char_in_tape(tape: mpt, head: int, write_char: str)-> mpt:
    return mpt({**tape, head: write_char})

def refresh_head(head: int, action_str: str)-> int:
    return head + 1 if action_str == "RIGHT" else head - 1

def get_new_values(machine: TuringMachine, tape: mpt, head: int, state: str)-> Tape:
    def get_action():
        return rec_extract_action(get_char(tape, head, machine.blank), machine.transitions[state])
    return Tape(read_char = get_char(tape, head, machine.blank),
                tape = write_char_in_tape(tape, head, get_action()["write"]),
                head = refresh_head(head, get_action()["action"]),
                state = get_action()["to_state"],
                action = get_action())

@tail_recursive
def rec_process(machine: TuringMachine, tape: mpt, head: int, state: str):
    t = get_new_values(machine, tape, head, state)
    print_stat(tape, head, state, t)
    return rec_process.tail_call(machine, t.tape, t.head, t.state) if t.state not in machine.finals else exit()
