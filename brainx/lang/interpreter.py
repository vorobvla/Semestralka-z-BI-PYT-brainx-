#!/usr/bin/env python3
from maintainance import logger

class InvalidCodeException(Exception):
    pass

class InterpreterSettingsException(Exception):
    pass

class Interpreter:
    memory = bytearray(1)
    tape_len = 1
    memory_ptr = 0
    input = ''
    input_ptr = 0
    output = bytearray()
    debug_file_num = 1
    rgb_input = None
    o128 = False

    # get the memory cell on the position of the 'head' (aka memory pointer)
    read_cell = lambda: Interpreter.memory[Interpreter.memory_ptr]

    # move pointer to 1 cell to the left
    @staticmethod
    def move_head_lt():
        Interpreter.memory_ptr = 0 if Interpreter.memory_ptr == 0 else Interpreter.memory_ptr - 1

    # move pointer to 1 cell to the right
    @staticmethod
    def move_head_rt():
        # add memory cell if it's not enougth memory
        if Interpreter.memory_ptr == Interpreter.tape_len - 1:
            Interpreter.memory.append(0)
            Interpreter.tape_len += 1
        Interpreter.memory_ptr += 1

    @staticmethod
    def jump_head(to):
        if 0 <= to < Interpreter.tape_len:
            Interpreter.tape_len = to

    # increase the value, stored in the memoty cell,  pointered by pointer
    @staticmethod
    def increase_cell():
        Interpreter.memory[Interpreter.memory_ptr] = 0 if Interpreter.memory[Interpreter.memory_ptr] == 255 else \
            Interpreter.memory[Interpreter.memory_ptr] + 1

    # decrease the value, stored in the memoty cell,  pointered by pointer
    @staticmethod
    def decrease_cell():
        Interpreter.memory[Interpreter.memory_ptr] = 255 if Interpreter.memory[Interpreter.memory_ptr] == 0 else \
            Interpreter.memory[Interpreter.memory_ptr] - 1

    # print conent of actual mem cell to ascii char
    @staticmethod
    def print_cell():
        write = Interpreter.memory[Interpreter.memory_ptr] if Interpreter.o128 == False else \
                Interpreter.memory[Interpreter.memory_ptr] % 128
        Interpreter.output.append(write)

    # read from input and write to actual cell
    @staticmethod
    def read_from_input_head():
        if Interpreter.input_ptr < len(Interpreter.input):
            Interpreter.memory[Interpreter.memory_ptr] = ord(Interpreter.input[Interpreter.input_ptr]) % 256
            Interpreter.input_ptr += 1
        else:
            pass

    # flush test info to debug file
    @staticmethod
    def log_state_to_file(sourcecode):
        logger.Logger.log_to_file(program_data=sourcecode, memory=str(bytes(Interpreter.memory)),
                           memory_pointer = str(Interpreter.memory_ptr), output=str(bytes(Interpreter.output)),
                           rgb_input=Interpreter.rgb_input )


# Sets input to interpreter and returns dictionaties of cykles (start->end and end->start)
# surcecode must not contain input. only program data
def analyze_code(sourcecode):
    stack = []
    cykles_list_start_end = []
    cykles_list_end_start = []

    # create list of cykles (format:  'from:to')
    for idx, token in enumerate(sourcecode):
        if token == '[':
            stack.append(idx)
        elif token == ']':
            if len(stack) == 0:
                raise InvalidCodeException('Interpreter found illegal end of cykle instruction (\']\') at position {}'
                                           .format(idx))
            else:
                start = stack.pop()
                cykles_list_start_end.append('{}:{}'.format(start, idx))
                cykles_list_end_start.append('{}:{}'.format(idx, start))

    if len(stack) != 0:
        raise InvalidCodeException('Interpreter found illegal start of cykle instruction (\'[\') at position {}'
                                   .format(stack.pop()))


    # create dictionaties of start and end of cykles

    d_start_to_end = eval('{{{}}}'.format(','.join(cykles_list_start_end)))
    d_end_to_start = eval('{{{}}}'.format(','.join(cykles_list_end_start)))
    return d_start_to_end, d_end_to_start

def interpret_bf(sourcecode_in, in_memory=b'\x00', in_memory_ptr=0, test_opt=False, rgb_input = None, program_input=None,
                 o128 = False):
    Interpreter.o128 = o128
    # control serrings
    if in_memory_ptr >= len(in_memory):
        raise InterpreterSettingsException('Attempt to set memory pointer out of memory.')
    # reset interpreter
    Interpreter.memory = bytearray(in_memory)
    Interpreter.memory_ptr = in_memory_ptr
    Interpreter.tape_len = len(Interpreter.memory)
    Interpreter.output = bytearray()
    Interpreter.rgb_input = rgb_input

    # contains positions of pointer in the beginning of cykle
    cykle_stack = []
    Interpreter.debug_file_num = 1
    # remove blanks (beacuse of tests, actually interpreter tolerates them)
    sourcecode = ''.join(sourcecode_in.split())

    # setup input and get dictionaties for cykles
    try:
        sourcecode, Interpreter.input = sourcecode.split('!', 1)
    except ValueError:
        Interpreter.input = ''
    Interpreter.input = Interpreter.input if program_input is None else program_input

    #coun len after all manipulations with sourcecode
    sourcecode_len = len(sourcecode)

    # set logging if not set and ends with #
    if sourcecode.endswith('#'):
        logger.turn_logging(True)

    cykle_jump_from_start, cykle_jump_from_end = analyze_code(sourcecode)

    idx = 0

    while idx < sourcecode_len:
        if sourcecode[idx].isspace():
            pass
        elif sourcecode[idx] == '+':
            Interpreter.increase_cell()
        elif sourcecode[idx] == '-':
            Interpreter.decrease_cell()
        elif sourcecode[idx] == '<':
            Interpreter.move_head_lt()
        elif sourcecode[idx] == '>':
            Interpreter.move_head_rt()
        elif sourcecode[idx] == '.':
            Interpreter.print_cell()
        elif sourcecode[idx] == ',':
            Interpreter.read_from_input_head()
        elif sourcecode[idx] == '[':
            cykle_stack.append(idx)
            if Interpreter.read_cell() == 0:
                # skip to ]
                idx = cykle_jump_from_start[idx]
            else:
                pass
        elif sourcecode[idx] == ']':
            if Interpreter.read_cell() != 0:
                # skip to [
                idx = cykle_jump_from_end[idx]
                continue
            else:
                cykle_stack.pop()
        elif sourcecode[idx] == '!':
            # end of progrm
            break
        elif sourcecode[idx] == '#':
            # print test
            Interpreter.log_state_to_file(sourcecode)
        else:
            raise InvalidCodeException('Interpreter found unknown instruction \'{}\' at position {}'
                                       .format(sourcecode[idx], idx))
        idx += 1

    if test_opt:
        Interpreter.log_state_to_file(sourcecode)
    return Interpreter.output




