#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Vladimir Vorobyev'


from sys import argv
import context


# parse options
context.OptsArgs.parse_opts(argv)
'''
for opt in argv:
    if not context.is_opt(opt):
        pass
    elif opt == '--lc2f':
        pass
    elif opt == '--f2lc':
        pass
    elif opt == '-i':
        pass
    elif opt == '-o':
        pass
    elif opt == '-t' or opt == '--test':
        pass
    elif opt == '-m' or opt == '--memory':
        pass
    elif opt == '-p' or opt == '--memory-pointer':
        pass
    elif opt == '--pnm':
        pass
    elif opt == '--pbm':
        pass
    elif opt == '-h' or opt == '--help':
        print(context.HELP)
    else:
        print(context.UNKNOWN_OPTS(opt))
        exit(context.RETURN_ERROR)'''

# remove options (don't need them already)
# argv = [arg for arg in argv if not context.is_opt(arg)]

# importaint! to count argc after removing options
argc = len(argv)


# parse args
if argc == 1:
    # a) Interpreter itself (interactive mode)
    print('run interactive interpreter')
    exit(c.RETURN_OK)


print(argv)
print()
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