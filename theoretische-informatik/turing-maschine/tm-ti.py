"""Turing Machine Emulator and Quadrant Simulator.

    The following script allows you to run a Turing Machine emulator in several different modes and ways.
    You can define a Turing Machine with a word using a binary string (the definition must be unary), 
    you can also define a Turing Machine with a word using an unsigend integer or you can read a Turing Machine from a file.
    You can also run a Quadrant Simulator by giving it a number as a command line argument.

    Args:
      -tmb:
        Turing machine with tape in binary code (0,1).
      -tmd:
        Turing machine with tape in decimal code.
      -tmf:
        Turing machine from file.
      -ex:
        Example number.
      -q:
        Quadrant Simulator by giving it a number as a command line argument.
      -s:
        Stepmode.

    Returns:
      When running in Quad Simulator mode the application returns the Quadrant of the given Number.
      When running in Turing Machine emulator mode the application returns the result of the simulation
      which is either ACCEPTED or REJECTED.
"""

import argparse
from enum import Enum
from io import TextIOWrapper
import time
from typing import List

class CONSOLE_COLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class Symbol:
    def __init__(self, binary: str, value: str) -> None:
        self.binary_code = binary
        self.symbol_value = value
        
    def __str__(self) -> str:
        return "Symbol = {binary_code=" + self.binary_code + " value=" + self.symbol_value + "}"

class Symbols(Enum):
    ZERO = Symbol('0', '0')
    ONE = Symbol('00', '1')
    BLANK = Symbol('000', '_')
    A = Symbol('0000', 'A')
    B = Symbol('00000', 'B')
    C = Symbol('000000', 'C')
    D = Symbol('0000000', 'D')
    E = Symbol('00000000', 'E')
    F = Symbol('000000000', 'F')
    
    @classmethod
    def get_all_symbols(cls) -> List[Symbol]:
        return list(map(lambda c: c.value, cls))
    
    @classmethod
    def get_symbol_from_binary(cls, binary_code) -> Symbol | None:
        symbol_list: List[Symbols] = list(filter(lambda x: x.value.binary_code == binary_code, list(cls)))
        return symbol_list[0].value if len(symbol_list) > 0 else None
        
    def get_value(self) -> Symbol:
        return self.value
    
   
    
class State:
    def __init__(self, binary) -> None:
        self.name = "q" + str(len(binary))
        self.is_accepted = len(binary) == 2
        self.is_start = len(binary) == 1
    
    def __str__(self) -> str:
        return "State = {name=" + self.name + " is_accepted=" + str(self.is_accepted) + " is_start=" + str(self.is_start) + "}"
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, State):
            return False
        return self.name == value.name and self.is_accepted == value.is_accepted and self.is_start == value.is_start
    
    def __hash__(self) -> int:
        return hash(self.name, self.is_accepted, self.is_start)

    
    
class Direction:
    def __init__(self, binary) -> None:
        self.binary_code = binary
        
    def __str__(self) -> str:
        return "Direction = {binary_code=" + self.binary_code + "}"

class Directions(Enum):
    LEFT = Direction("0")
    RIGHT = Direction("00")
    
    @classmethod
    def get_all_directions(cls) -> List[Direction]:
        return list(map(lambda c: c.value, cls))
    
    @classmethod
    def get_direction_from_binary(cls, binary_code) -> Direction | None:
        direction_list = list(filter(lambda x: x.value.binary_code == binary_code, cls))
        return direction_list[0] if len(direction_list) > 0 else None



class Transition:
    def __init__(self, from_state: State, read_symbol: Symbol, to_state: State, write_symbol: Symbol, direction: Direction) -> None:
        self.from_state = from_state
        self.read_symbol = read_symbol
        self.to_state = to_state
        self.write_symbol = write_symbol
        self.direction = direction
    
    def __str__(self) -> str:
        return "Transition = {from_state=" + str(self.from_state.name) + " read_symbol=" + str(self.read_symbol.symbol_value) + " to_state=" + str(self.to_state.name) + " write_symbol=" + str(self.write_symbol.symbol_value) + " direction=" + str(self.direction) + "}"



class Tape:
    def __init__(self, tape: List[str]) -> None:
        self.tape = tape if len(tape) > 0 else [Symbols.BLANK.get_value().symbol_value]
        self.position: int = 0
        self.position_offset: int = 0
    
    def __str__(self) -> str:
        tape_margin_left_content = Symbols.BLANK.get_value().symbol_value * (max(15 - self.get_index(), 0))
        tape_margin_right_content = Symbols.BLANK.get_value().symbol_value * (max(15 + self.get_index(), 0))
        tape_content = "".join(self.tape)
        head_index_string = " " * (max(15 - self.get_index(), 0) + self.get_index()) + CONSOLE_COLORS.BOLD + "↓" + CONSOLE_COLORS.ENDC
        return CONSOLE_COLORS.BOLD + "Tape" + CONSOLE_COLORS.ENDC + " (position=" + str(self.position) + " position_offset=" + str(self.position_offset) + "):\n" + str(head_index_string) + "\n" + "".join([tape_margin_left_content, tape_content, tape_margin_right_content])
    
    def move_left(self) -> None:
        self.position -= 1
        if self.position + self.position_offset < 0:
            self.position_offset += 1
            self.tape.insert(0, Symbols.BLANK.get_value().symbol_value)
            
    def move_right(self) -> None:
        self.position += 1
        if self.position + self.position_offset >= len(self.tape):
            self.tape.append(Symbols.BLANK.get_value().symbol_value)
    
    def write(self, symbol: str) -> None:
        self.tape[self.position + self.position_offset] = symbol
    
    def get_index(self) -> int:
        return self.position + self.position_offset
    
    def get_symbol(self) -> str:
        return self.tape[self.position + self.position_offset]
    
    def get_tape_list(self) -> List[str]:
        return self.tape



class Turingmachine:
    def __init__(self, transitions: List[Transition], input_string: str, is_step_mode: bool = False, is_mulitplication_mode: bool = False) -> None:
        self.transitions = transitions
        self.tape = Tape(list(map(lambda x: x, input_string)))
        self.is_step_mode = is_step_mode
        self.is_mulitplication_mode = is_mulitplication_mode
        self.calculation_count: int = 0
        self.current_state: State = None
        
    def __str__(self) -> str:
        return "Turingmachine = {num of transitions=" + str(len(self.transitions)) + ", is_step_mode=" + str(self.is_step_mode) + ", is_mulitplication_mode=" + str(self.is_mulitplication_mode) + ", calculation_count=" + str(self.calculation_count) + ", current_state=" + str(self.current_state) + "}"

    def calculate(self, CUTOFF: int = 1_000_000) -> None:
        start_transition_list: Transition = list(filter(lambda x: x.from_state.is_start, self.transitions))
        if len(start_transition_list) == 0:
            raise Exception("No start state found")
        start_transition: Transition = start_transition_list[0]
        self.current_state = start_transition.from_state
        
        for iteration_num in range(0, CUTOFF+1):
            if iteration_num == CUTOFF:
                raise RuntimeWarning("Turing machine calculation stopped due to CUTOFF (" + str(CUTOFF) + ")")
            
            self.print_step()
            
            has_next_transition = False
            for next_transition in self.transitions:
                if next_transition.from_state == self.current_state and next_transition.read_symbol.symbol_value == self.tape.get_symbol():
                    self.tape.write(next_transition.write_symbol.symbol_value)
                    if next_transition.direction == Directions.LEFT:
                        self.tape.move_left()
                    elif next_transition.direction == Directions.RIGHT:
                        self.tape.move_right()
                    else:
                        raise Exception("Unknown direction: " + str(next_transition.direction))
                    
                    self.current_state = next_transition.to_state
                    has_next_transition = True
                    self.calculation_count += 1
                    break
                
            if not has_next_transition:
                print(CONSOLE_COLORS.OKCYAN + "------------------------------------------------------------------------" + CONSOLE_COLORS.ENDC)
                if self.is_mulitplication_mode:
                    print("Caluculation count: " + CONSOLE_COLORS.OKBLUE + str(self.calculation_count) + CONSOLE_COLORS.ENDC)
                    print(CONSOLE_COLORS.OKGREEN + "Result: " + str(self.get_result_from_tape()) + CONSOLE_COLORS.ENDC)
                elif self.current_state.is_accepted:
                    print(CONSOLE_COLORS.OKGREEN + "ACCEPTED: " + str(self.current_state) + CONSOLE_COLORS.ENDC)
                else:
                    raise Exception("REJECTED: No next transition found for current state: " + str(self.current_state) + " and tape symbol: " + self.tape.get_symbol())
                break
            
    def get_result_from_tape(self):
        result_tape_list = self.tape.get_tape_list()
        result = 0
        for index in range(0, len(result_tape_list)):
            result += 1 if result_tape_list[index] == Symbols.ZERO.value.symbol_value else 0
        return result

    def print_step(self, SLEEP_TIME: float = 0.25):
        if self.is_step_mode:
            print(CONSOLE_COLORS.OKCYAN + "------------------------------------------------------------------------" + CONSOLE_COLORS.ENDC)
            print("Current state: " + CONSOLE_COLORS.OKBLUE + str(self.current_state) + CONSOLE_COLORS.ENDC)
            print(self.tape)
            print("Caluculation count: " + CONSOLE_COLORS.OKBLUE + str(self.calculation_count) + CONSOLE_COLORS.ENDC)
            time.sleep(SLEEP_TIME)
                


class Parser:
    def get_transition_from_binary(transition_binary) -> Transition:
        transition_binary = transition_binary[1:] if transition_binary.startswith("1") else transition_binary
        tuple_of_five = transition_binary.split("1")
        if tuple_of_five is None or len(tuple_of_five)!= 5:
            print(CONSOLE_COLORS.FAIL + "Invalid transition input" + CONSOLE_COLORS.ENDC)
            exit(1)
        from_state = State(tuple_of_five[0])
        read_symbol = Symbols.get_symbol_from_binary(tuple_of_five[1])
        to_state = State(tuple_of_five[2])
        write_symbol = Symbols.get_symbol_from_binary(tuple_of_five[3])
        direction = Directions.get_direction_from_binary(tuple_of_five[4])
        newTransistion = Transition(from_state, read_symbol, to_state, write_symbol, direction)
        return newTransistion
    
    def parse_transitions_from_file(file: TextIOWrapper) -> str:
        binary_string = ""
        for line in file:
            binary_string += Parser._parse_transition(line)
            binary_string += "11"
        binary_string += "1"
        return binary_string
    
    def _parse_transition(transition_string: str) -> str:
        binary_string = ""
        transition_string = transition_string.replace(") = (q", ",").replace("(q", "").replace(")", "").split(",")
        binary_string += "0" * int(transition_string[0])
        binary_string += "1"
        binary_string += Parser._parse_symbol(transition_string[1])
        binary_string += "1"
        binary_string += "0" * int(transition_string[2])
        binary_string += "1"
        binary_string += Parser._parse_symbol(transition_string[3])
        binary_string += "1"
        binary_string += Parser._parse_direction(transition_string[4].strip("\n"))
        return binary_string
    
    def _parse_symbol(symbol_string: str) -> str:
        all_symbols = Symbols.get_all_symbols()
        for symbol in all_symbols:
            if symbol_string == symbol.symbol_value:
                return symbol.binary_code
        raise Exception("Unknown symbol: " + symbol_string)
    
    def _parse_direction(direction_string: str) -> str:
        if direction_string == "L":
            return Directions.LEFT.value.binary_code
        elif direction_string == "R":
            return Directions.RIGHT.value.binary_code
        else:
            raise Exception("Unknown direction: " + direction_string)



def main():
    EXAMPLES = [
        ("T1 with VALID input", "010010001010011000101010010110001001001010011000100010001010", "11"),
        ("T1 with INVALID input", "010010001010011000101010010110001001001010011000100010001010", "101"),
        ("T2 with VALID input", "1010010100100110101000101001100010010100100110001010010100", "00"),
        ("T2 with INVALID input", "1010010100100110101000101001100010010100100110001010010100", "010")
    ]
    TM_QUAD = "10101010100110100010000000000000100010110010010010100110010000010010100110001010001010110001000100001000100110000101000001000010011000010010000000010010110000010100000101001100000100100000100100110000010001000000101001100000010001000000010101100000001010000000101011000000010010000000100101100000001000010000100001001100000001000001000010000010011000000001000100100010011000000001000010000000001000010110000000010000010000000000001000001011000000000100010000000000100010011000000000100001000000000100001011000000000100000100000000001000001001100000000001000010000000000010000010011000000000001010000000000010100110000000000010010000000000010010011000000000001000010000000000010100110000000000010001000000010001011000000000000100000100000000000010000010110000000000001000100100010011000000000000010100010010"
    print("A maximum of " + str(len(Symbols.get_all_symbols())) + " different symbols is supported.")
    
    parser = argparse.ArgumentParser()

    # -tmb TURINGMACHINE_BINARY
    # -tmd TURINGMACHINE_DECIAML
    # -tmf TURINGMACHINE_FILE_PATH and TURINGMACHINE_INPUT_IN_BINARY
    # -ex EXAMPLE_NUMBER
    # -q QUAD_MODE_WITH_NUMBER
    # -s STEPMODE
    parser.add_argument("-tmb", "--turingmachinebinary", help="Turing machine with tape in binary code (0,1)", type=str)
    parser.add_argument("-tmd", "--turingmachinedecimal", help="Turing machine with tape in decimal code", type=int)
    parser.add_argument("-tmf", "--turingmachinefile", help="Turing machine from file using file path", type=list, nargs="+")
    parser.add_argument("-ex", "--example", help="Example number from {} to {}".format(1, len(EXAMPLES)), type=int)
    parser.add_argument("-q", "--quad", help="Use quad mode to quadrate given number", type=int)
    parser.add_argument("-s", "--stepmode", help="Stepmode", type=bool, action=argparse.BooleanOptionalAction, default=False)

    args = parser.parse_args()

    multiplication_mode = False
    if args.turingmachinebinary != None:
        transitions_and_input = args.turingmachinebinary.split("111")
    elif args.turingmachinedecimal != None:
        transitions_and_input = str(bin(args.turingmachinedecimal))[2:].split("111")
    elif args.turingmachinefile != None and len(args.turingmachinefile) == 2:
        file = open("".join(args.turingmachinefile[0]), "r")
        if not set(args.turingmachinefile[1]).issubset(set('01')):
            print(CONSOLE_COLORS.FAIL + "Invalid input string" + CONSOLE_COLORS.ENDC)
            exit(1)
        transitions_and_input = (Parser.parse_transitions_from_file(file) + "".join(args.turingmachinefile[1])).split("111")
    elif args.example != None:
        transitions_and_input = [EXAMPLES[args.example - 1][1],EXAMPLES[args.example - 1][2]]
        print(CONSOLE_COLORS.OKCYAN + "Example: {}".format(EXAMPLES[args.example - 1]) + CONSOLE_COLORS.ENDC)
    elif args.quad != None:
        transitions_and_input = [TM_QUAD, "0" * args.quad]
        multiplication_mode = True
    else:
        print(CONSOLE_COLORS.FAIL + "Invalid arguments" + CONSOLE_COLORS.ENDC)
        exit(1)
        
    if len(transitions_and_input) != 2:
        print(CONSOLE_COLORS.FAIL + "Invalid binary string (You may have forgotten to add the tape at the end)" + CONSOLE_COLORS.ENDC)
        exit(1)

    transitions_binary = transitions_and_input[0].split("11")
    
    try:
        transitions = list(map(Parser.get_transition_from_binary, transitions_binary))
        print(CONSOLE_COLORS.BOLD + "All Transitions:" + CONSOLE_COLORS.ENDC)
        for transition in transitions:
            print(transition)
    except Exception as e:
        print(CONSOLE_COLORS.OKBLUE + str(e) + CONSOLE_COLORS.ENDC)
        exit(1)

    turingmachine = Turingmachine(transitions, transitions_and_input[1], args.stepmode, multiplication_mode)
    print(CONSOLE_COLORS.OKCYAN + str(turingmachine) + CONSOLE_COLORS.ENDC)
    
    try:
        turingmachine.calculate()
    except RuntimeWarning as e:
        print(CONSOLE_COLORS.WARNING + str(e) + CONSOLE_COLORS.ENDC)
        exit(1)
    except Exception as e:
        print(CONSOLE_COLORS.FAIL + str(e) + CONSOLE_COLORS.ENDC)
        exit(1)

if __name__ == "__main__":
    # COMMANDS:
    # (1), (2), (3) and (4) are all the same Turing machine with the same input
    # (1) python3 tm-ti.py -tmb 01001000101001100010101001011000100100101001100010001000101011111 -s
    # (2) python3 tm-ti.py -tmd 47363324500958581087 -s
    # (3) python3 tm-ti.py -tmf tm-converter-data.txt 11 -s
    # (4) python3 tm-ti.py -ex 1 -s
    # (5) python3 tm-ti.py -ex 4
    # (6) python3 tm-ti.py -q 7
    # (7) python3 tm-ti.py -q 2 -s
    main()
