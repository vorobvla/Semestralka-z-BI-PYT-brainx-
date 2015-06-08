#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from argparse import ArgumentTypeError
from argparse import Action

# store one or two arguments (add a None if second is missing)
def store_one_or_two():
    class OneOrTwo(Action):
        def __call__(self, parser, namespace, values, option_string=None):
            print('DB')
            if 1 <= len(values) <= 2:
                if len(values) == 1:
                    values.append(None)
                pass
            else:
                raise ArgumentTypeError('One or two arguments expected with option {}.'.format(self.dest))
            setattr(namespace, self.dest, values)
    return OneOrTwo


parser = ArgumentParser(description='TODO', epilog='TODO')

# --- adding parameters according to functional requirements ---

#   a) Interpreter itself
parser.add_argument('sourcefile', nargs='?', help='Name of file with sourcecode to be executed'
                                                  '(in brainfuck, brainlotter or '
                                                  'braincopter). If missing, the interpreter switches'
                                                  ' to interactive mode.')
#   b) Translation of picture to stdout or text file
# TODO: remove '...' in methavar (occurs beacuse of nargs='+').
parser.add_argument('--lc2f', nargs='+', action=store_one_or_two(), help='Translates picture (brainlotter or braincopter)'
                    'to brinfuck sourcecode. If name of output file missing sends output to stdout.',
                    metavar=('input_file', 'output_file'))
#   c) Translation of text file (brainfuck sourcecode) to brainlotter or braincopter image
parser.add_argument()
#   d) Test output to file
#   e) Advanced testing options
#   f) Help (implemented by angpars as default)

# parser.add_argument('--lc2f', action = 'lc2f', help = 'Translate brainlotter or braincopter '
#                                                      'image to brainfuck source code')


args = parser.parse_args()
print(args)