#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Vladimir Vorobyev'


from sys import argv
import context
from lang import interpreter
from lang import translater
from graphics import png_processor
from graphics import image
from traceback import print_exc
from sys import stderr


# parse options
context.Settings.parse_opts(argv)


try:
    # run as translater
    if context.Settings.translate_mode:
        if context.Settings.opt_f2lc:
            print('run f2lc translater')

        elif context.Settings.opt_lc2f:
            print('run lc2f translater')

    # run as interpreter
    else:
        #defined here to call interpret_bf in one place
        rgb_in = None
        # retrieve source code
        # from user input
        if context.Settings.interactive_mode:
            #read input
            sourcecode = input('Please, insert brainfuck code: ')
        # from console
        elif context.Settings.arg_console_sourcecode is not None:
            sourcecode = context.Settings.arg_console_sourcecode
        # from file ...
        elif context.Settings.arg_source_file is not None:
            # ... from text file .b
            if context.Settings.arg_source_file.endswith('.b'):
                with open(context.Settings.arg_source_file, encoding='ASCII', mode='r') as file:
                    sourcecode = file.read()
            else:
            # from file that supposed to be an image file (name does not end with .b)
                img = png_processor.process_png(context.Settings.arg_source_file)
                sourcecode = translater.lc_to_f(img)
                rgb_in = img.to_text()
            pass

        # run sourcecode
        output = interpreter.interpret_bf(sourcecode, context.Settings.arg_memory, int(context.Settings.arg_memory_pointer),
                                      context.Settings.opt_test, rgb_in)
        # print output
        print(output.decode('ASCII'), end='')
    exit(context.RETURN_OK)

except png_processor.PNGWrongHeaderError:
    print_exc(file=stderr)
    exit(4)
except png_processor.PNGNotImplementedError:
    print_exc(file=stderr)
    exit(8)

