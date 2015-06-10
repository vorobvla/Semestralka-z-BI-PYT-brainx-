#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Vladimir Vorobyev'


from sys import argv
import context


# parse options
context.Settings.parse_opts(argv)

# remove options (don't need them already)
# argv = [arg for arg in argv if not context.is_opt(arg)]

# importaint! to count argc after removing options



print()
print(vars(context.Settings))
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