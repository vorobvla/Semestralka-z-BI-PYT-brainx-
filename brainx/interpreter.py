#!/usr/bin/env python3


class UnknownInstructionException(Exception):
    pass


class Interpreter:
    memory = bytearray()
    tape_len = 1
    memory_ptr = 0
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

    



def interpret_bf(sourcecode, in_memory=b'\000', in_memory_ptr=0, test=False):
    # setup interpreter
    Interpreter.memory = bytearray(in_memory)
    Interpreter.memory_ptr = in_memory_ptr
    Interpreter.tape_len = len(Interpreter.memory)
    Interpreter.output = ''
    #contains positions of pointer in the beginning of cykle
    cykle_stack = []
    sourcecode_len = len(sourcecode)

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
            print('FOUND .')
            Interpreter.print_head()
        elif sourcecode[idx] == ',':
            pass
        elif sourcecode[idx] == '[':
            if Interpreter.get_head() == 0:
                # skip to ]
                while sourcecode[idx] != ']':
                    idx += 1
            else:
                cykle_stack.append(idx)
        elif sourcecode[idx] == ']':
            if Interpreter.get_head() != 0:
                # skip to [
                idx = cykle_stack.pop()
                continue
            else:
                pass
        elif sourcecode[idx] == '!':
            # distinguish input
            pass
        elif sourcecode[idx] == '#':
            # print test
            pass
        else:
            raise UnknownInstructionException('Interpreter found unknown instruction \'{}\''.format(sourcecode[idx]))
        idx += 1
    return Interpreter.output




