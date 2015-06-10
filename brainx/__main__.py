#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Vladimir Vorobyev'


from sys import argv
import context


# parse options
context.Settings.parse_opts(argv)

# remove options (don't need them already)
# argv = [arg for arg in argv if not context.is_opt(arg)]

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
    if context.Settings.arg_source_file[-2:] == '.b':
        #read text file
        with open(context.Settings.arg_source_file, encoding='ASCII') as file:
            sourcecode = file.read()
    pass

# run sourcecode



#print(vars(context.Settings))
print('source file: ')
print(context.Settings.arg_source_file)
print('command line:')
print(context.Settings.arg_console_sourcecode)
print('Source code: ' + sourcecode)
# --- adding parameters according to functional requirements ---

    #

    # Translater LC2F
    # b) Translation of picture to stdout or text file
#   c) Translation of text file (brainfuck sourcecode) to brainlotter or braincopter image


#   d) Test output to file
#   e) Advanced testing options
#   f) Help (implemented by angpars as default)

# parser.add_argument('--lc2f', action = 'lc2f', help = 'Translate brainlotter or braincopter '
#                                                      'image to brainfuck source code')