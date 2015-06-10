#!/usr/bin/env python3


class Interpreter:
    memory = None
    memory_ptr = 0
    db_file_number = 0

    # get the memory cell on the position of the 'head' (aka memory pointer)
    get_head = lambda: Interpreter.memory[Interpreter.memory_ptr]


def interpret_bf(sourcecode, in_memory = b'', in_memory_ptr = 0, test = False):
    # setup interpreter
    Interpreter.memory = bytearray(in_memory)
    Interpreter.memory_ptr = in_memory_ptr



    # move





