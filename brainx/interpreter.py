#!/usr/bin/env python3


class InvalidCodeException(Exception):
    pass


class Interpreter:
    memory = bytearray()
    tape_len = 1
    memory_ptr = 0
    input = ''
    input_ptr = 0
    db_file_number = 0
    output = ''

    # get the memory cell on the position of the 'head' (aka memory pointer)
    get_head = lambda: Interpreter.memory[Interpreter.memory_ptr]

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
    def increase_head():
        Interpreter.memory[Interpreter.memory_ptr] = 0 if Interpreter.memory[Interpreter.memory_ptr] == 255 else \
            Interpreter.memory[Interpreter.memory_ptr] + 1

    # decrease the value, stored in the memoty cell,  pointered by pointer
    @staticmethod
    def decrease_head():
        Interpreter.memory[Interpreter.memory_ptr] = 255 if Interpreter.memory[Interpreter.memory_ptr] == 0 else \
            Interpreter.memory[Interpreter.memory_ptr] - 1

    # print conent of actual mem cell to ascii char
    @staticmethod
    def print_head():
        Interpreter.output += chr(Interpreter.memory[Interpreter.memory_ptr])

    # read from input and write to actual cell
    @staticmethod
    def write_from_input_head():
        if Interpreter.input_ptr < len(Interpreter.input):
            Interpreter.memory[Interpreter.memory_ptr] = ord(Interpreter.input[Interpreter.input_ptr]) % 256
            Interpreter.input_ptr += 1
        else:
            pass

def interpret_bf(sourcecode, in_memory=b'\000', in_memory_ptr=0, test=False):
    # setup interpreter
    Interpreter.memory = bytearray(in_memory)
    Interpreter.memory_ptr = in_memory_ptr
    Interpreter.tape_len = len(Interpreter.memory)
    Interpreter.output = ''
    #contains positions of pointer in the beginning of cykle
    cykle_stack = []
    sourcecode_len = len(sourcecode)

    # find input
    input_idx = sourcecode.find('!')
    Interpreter.input = sourcecode[input_idx + 1:] if input_idx != -1 else ''

    idx = 0

    while idx < sourcecode_len:
        if sourcecode[idx].isspace():
            pass
        elif sourcecode[idx] == '+':
            Interpreter.increase_head()
        elif sourcecode[idx] == '-':
            Interpreter.decrease_head()
        elif sourcecode[idx] == '<':
            Interpreter.move_head_lt()
        elif sourcecode[idx] == '>':
            Interpreter.move_head_rt()
        elif sourcecode[idx] == '.':
            Interpreter.print_head()
        elif sourcecode[idx] == ',':
            Interpreter.write_from_input_head()
        elif sourcecode[idx] == '[':
            if Interpreter.get_head() == 0:
                # skip to ]
                while sourcecode[idx] != ']':
                    idx += 1
            else:
                cykle_stack.append(idx)
        elif sourcecode[idx] == ']':
            if len(cykle_stack) == 0:
                raise InvalidCodeException('Interpreter found illegal end of cykle instruction(\']\') at position {}'
                                           .format(idx))
            if Interpreter.get_head() != 0:
                # skip to [
                idx = cykle_stack.pop()
                continue
            else:
                cykle_stack.pop()
        elif sourcecode[idx] == '!':
            # end of progrm
            break
        elif sourcecode[idx] == '#':
            # print test
            pass
        else:
            raise InvalidCodeException('Interpreter found unknown instruction \'{}\' at position {}'
                                       .format(sourcecode[idx], idx))
        idx += 1
    if len(cykle_stack) != 0:
        raise InvalidCodeException('Interpreter found illegal start of cykle instruction(\'[\') at position {}'
                                   .format(cykle_stack.pop()))
    print('INPUT: ')
    print(Interpreter.input)
    return Interpreter.output




