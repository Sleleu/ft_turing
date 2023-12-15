from srcs.classes import TuringMachine

def read_char_in_tape(tape, head, blank):
    return tape[head] if head in tape else blank

def rec_extract_action(read_char, transition: dict):
    match transition:
        case []: raise ValueError(f"character '{read_char}' is not in actual transition")
        case _ :
            return transition[0] if read_char in transition[0]["read"] else rec_extract_action(read_char, transition[1:]) 

def write_char_in_tape(tape_keys, tape, head, write_char):
    def return_pair(i):
        if head != i:
            return (i, tape[i])
        else:
            return (i, write_char)
    new_tape = dict(map(return_pair, range(len(tape_keys))))
    return new_tape

def print_tape(tape, head):
    return "".join((map(lambda i: tape[i] if head != i else '<' + tape[i] + '>', range(len(tape))))).ljust(20, '.')

def rec_process(machine, tape, head: int, state: str):
    def display_actual_stat():
        func = print_tape(tape, head)
        print(f'[{func}] ({state}, {read_char}) -> ({new_state}, {action["write"]}, {action["action"]})')
    read_char: str = read_char_in_tape(tape, head, machine.blank)
    action: dict = rec_extract_action(read_char, machine.transitions[state])
    new_state: str = action["to_state"]
    tape_keys = tuple(tape.keys()) if head in tuple(tape.keys()) else tuple(tape.keys()) + (head,)
    new_tape: dict = write_char_in_tape(tape_keys, tape, head, action["write"])
    new_head = head + 1 if action["action"] == "RIGHT" else head - 1
    display_actual_stat()
    return rec_process(machine, new_tape, new_head, new_state) if new_state not in machine.finals else exit()

def run_machine(machine : TuringMachine, tape: dict):
    head: int = 0
    state: str = machine.initial
    rec_process(machine, tape, head, state)