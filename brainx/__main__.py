#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from argparse import ArgumentTypeError
from argparse import Action
from sys import argv



parser = ArgumentParser(description='TODO', epilog='TODO')

# --- adding parameters according to functional requirements ---


if '--lc2f' or '--f2lc' or '-h' or '--help' in argv:
    # Translater LC2F
    # b) Translation of picture to stdout or text file
    subparsers = parser.add_subparsers()
    subparser_lc2f = subparsers.add_parser('--lc2f', help='Translates picture (brainlotter or braincopter) '
                                                     'to brinfuck sourcecode.')
    subparser_f2lc = subparsers.add_parser('--f2lc', help='')

    subparser_lc2f.add_argument('input_file', nargs=1, help='Name of source file to be translated.')
    subparser_lc2f.add_argument('output_file', nargs='?', help='Name of target file to contain ctanslated code. '
                                                               'If missing, code is sent to stdout.')
    subparser_f2lc.add_argument('-i', nargs=2, help='input file')
    subparser_f2lc.add_argument('-o', nargs=1, help='output file')
else:
    # No translater
    # a) Interpreter itself
    parser.add_argument('sourcefile', nargs='?', help='Name of file with sourcecode to be executed'
                                                      '(in brainfuck, brainlotter or '
                                                      'braincopter). If missing, the interpreter switches'
                                                      ' to interactive mode.')
# TODO: remove '...' in methavar (occurs beacuse of nargs='+').
#   c) Translation of text file (brainfuck sourcecode) to brainlotter or braincopter image


#   d) Test output to file
#   e) Advanced testing options
#   f) Help (implemented by angpars as default)

# parser.add_argument('--lc2f', action = 'lc2f', help = 'Translate brainlotter or braincopter '
#                                                      'image to brainfuck source code')


args = parser.parse_args()
print(args)