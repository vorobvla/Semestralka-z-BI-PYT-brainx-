#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Vladimir Vorobyev'


from sys import argv
from maintainance import context
from maintainance import logger
from lang import interpreter
from lang import translater
from graphics import png_processor
from graphics import image
from traceback import print_exc
from sys import stderr
#from  import logger


# parse options
context.Settings.parse_opts(argv)


try:
    # run as translater
    if context.Settings.translate_mode:
        # --f2lc
        if context.Settings.opt_f2lc:
            print('run f2lc translater')

        # --lc2f
        elif context.Settings.opt_lc2f:
            img = png_processor.process_png(context.Settings.arg_input_bl_bc_file)
            bf_code = translater.lc_to_f(img)
            if context.Settings.arg_output_bf_file is None:
                print(bf_code)
            else:
                if not context.Settings.arg_output_bf_file.endswith('.b'):
                    context.Settings.arg_output_bf_file += '.b'
                with open(context.Settings.arg_output_bf_file, encoding='ASCII', mode='w') as file:
                    file.write(bf_code)
            # print debug file
            if context.Settings.opt_test:
                logger.Logger.log_to_file(program_data=bf_code, rgb_output=img.to_text())

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
            # ... from file that supposed to be an image file (name does not end with .b)
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

