from srcs.classes import TuringMachine, Tape
from srcs.display import print_tape
from tail_recursive import tail_recursive
from types import MappingProxyType as mpt

def read_char_in_tape(tape, head, blank):
    return tape[head] if head in tape else blank

def rec_extract_action(read_char: str, transition: mpt)-> mpt:
    match transition:
        case []: raise ValueError(f"character '{read_char}' is not in actual transition")
        case _ :
            return transition[0] if read_char in transition[0]["read"] else rec_extract_action(read_char, transition[1:]) 

def write_char_in_tape(tape_keys: tuple, tape: mpt, head: int, write_char: str)-> mpt:
    return (mpt(dict(map(lambda key: (key, write_char if key == head else tape.get(key, '.')), tape_keys))))

def refresh_head(head: int, action_str: str)-> int:
    match action_str:
        case "RIGHT": return head + 1
        case "LEFT": return head - 1

def refresh_tape_keys(tape, head)-> tuple:
    return tuple(tape.keys()) if head in tuple(tape.keys()) else tuple(tape.keys()) + (head,)

def get_new_values(machine, tape, head, state)-> Tape:
    read_char = read_char_in_tape(tape, head, machine.blank)
    action = rec_extract_action(read_char, machine.transitions[state])
    new_state = action["to_state"]
    tape_keys = refresh_tape_keys(tape, head)
    new_tape = write_char_in_tape(tape_keys, tape, head, action["write"])
    new_head = refresh_head(head, action["action"])
    return Tape(read_char=read_char, tape=new_tape, tape_keys=tape_keys,
                head=new_head, state=new_state, action=action)

@tail_recursive
def rec_process(machine, tape, head: int, state: str):
    def display_actual_stat():
        func = print_tape(tape, head)
        print(f'[{func}] ({state}, {t.read_char}) -> ({t.state}, {t.action["write"]}, {t.action["action"]})')
    t = get_new_values(machine, tape, head, state)
    display_actual_stat()
    return rec_process.tail_call(machine, t.tape, t.head, t.state) if t.state not in machine.finals else exit()

def run_machine(machine : TuringMachine, tape: mpt):
    head = 0
    state = machine.initial
    rec_process(machine, tape, head, state)