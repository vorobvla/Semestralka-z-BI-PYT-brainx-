﻿#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Vladimir Vorobyev'


from sys import argv
from sys import stderr
import context
import interpreter
import graphic_langs
from traceback import print_exc


# parse options
context.Settings.parse_opts(argv)

#print(argv)

'''
print('\n\n\n-------\n')
print(context.Settings.arg_memory)
print(context.Settings.arg_memory_pointer)
print(type(interpreter.Interpreter.memory_ptr))
print('\n\n')

print(argv)
'''
# remove options (don't need them already)
# argv = [arg for arg in argv if not context.is_opt(arg)]
#print(vars(context.Settings))
if context.Settings.opt_f2lc:
    print('run f2lc translater')

elif context.Settings.opt_lc2f:
    print('run lc2f translater')

elif context.Settings.interactive_mode:
    #read input
    sourcecode = input('Please, insert brainfuck code: ')

elif context.Settings.arg_console_sourcecode is not None:
    sourcecode = context.Settings.arg_console_sourcecode

elif context.Settings.arg_source_file is not None:
    #analyze file
    if context.Settings.arg_source_file.endswith('.b'):
        #read text file
        with open(context.Settings.arg_source_file, encoding='ASCII', mode='r') as file:
            sourcecode = file.read()
    else:
        try:
            graphic_langs.analyze_png(context.Settings.arg_source_file)
        except graphic_langs.PNGWrongHeaderError:
            print_exc(file=stderr)
            exit(4)
        except graphic_langs.PNGNotImplementedError:
            print_exc(file=stderr)
            exit(8)
    pass

if not context.Settings.translate_mode:
# run sourcecode
    output = interpreter.interpret_bf(sourcecode, context.Settings.arg_memory, int(context.Settings.arg_memory_pointer),
                                  context.Settings.opt_test)

'''
print('source file: ')
print(context.Settings.arg_source_file)
print('command line:')
print(context.Settings.arg_console_sourcecode)
print('Source code: ' + sourcecode)

print('Output: "{}"'.format(bytes(output)))
'''
print(output.decode('ASCII'), end='')