from srcs.classes import TuringMachine
from tail_recursive import tail_recursive

def read_char_in_tape(tape, head, blank):
    return tape[head] if head in tape else blank

def rec_extract_action(read_char, transition: dict):
    match transition:
        case []: raise ValueError(f"character '{read_char}' is not in actual transition")
        case _ :
            return transition[0] if read_char in transition[0]["read"] else rec_extract_action(read_char, transition[1:]) 

def write_char_in_tape(tape_keys: tuple, tape: dict, head: int, write_char: str)-> dict:
    @tail_recursive
    def construct_tape(keys):
        match keys:
            case []: return {}
            case [hd, *tl]:
                value = write_char if hd == head else tape.get(hd, '.')
                return {hd: value} | construct_tape.tail_call(tl)
    return construct_tape(tape_keys)

def refresh_head(head: int, action_str: str)-> int:
    return head + 1 if action_str == "RIGHT" else head - 1

def refresh_tape_keys(tape, head)-> tuple:
    return tuple(tape.keys()) if head in tuple(tape.keys()) else tuple(tape.keys()) + (head,)

def print_tape(tape, head):
    def generate_keys():
        minimum = min(tape) if min(tape) < head else head
        maximum = max(tape) if max(tape) > head else head
        return range(minimum, maximum + 1)
    return "".join(map(lambda i: tape.get(i, '.') if i != head else '<' + tape.get(i, '.') + '>', generate_keys()))

@tail_recursive
def rec_process(machine, tape, head: int, state: str):
    def display_actual_stat():
        func = print_tape(tape, head)
        print(f'[{func}] ({state}, {read_char}) -> ({new_state}, {action["write"]}, {action["action"]})')
    read_char: str = read_char_in_tape(tape, head, machine.blank)
    action: dict = rec_extract_action(read_char, machine.transitions[state])
    new_state: str = action["to_state"]
    tape_keys: tuple = refresh_tape_keys(tape, head)
    new_tape: dict = write_char_in_tape(tape_keys, tape, head, action["write"])
    new_head = refresh_head(head, action["action"])
    display_actual_stat()
    return rec_process.tail_call(machine, new_tape, new_head, new_state) if new_state not in machine.finals else exit()

def run_machine(machine : TuringMachine, tape: dict):
    head: int = 0
    state: str = machine.initial
    rec_process(machine, tape, head, state)