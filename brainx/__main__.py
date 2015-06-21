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
        enclose_with_b = lambda str: str if str.endswith('.b') else str + '.b'
        # --f2lc
        # will contain strings representing input and output images
        rgb_in = None
        rgb_out = None
        # will contain code
        if context.Settings.opt_f2lc:
            # retrieve bf source
            context.Settings.arg_input_bf_file = enclose_with_b(context.Settings.arg_input_bf_file)
            with open(context.Settings.arg_input_bf_file, encoding='ASCII', mode='r') as file:
                    bf_code = file.read()
            input_img = None
            if context.Settings.arg_input_png_file is not None:
                input_img = png_processor.process_png(context.Settings.arg_input_png_file)
                if context.Settings.opt_pnm_pbm:
                    input_img.to_pnm(context.PNM_IN_NAME)
                rgb_in = input_img.to_text()
            if context.Settings.opt_bl_spiral:
                output_img = translater.f_to_l_spiral(bf_code)
            else:
                output_img = translater.f_to_lc(bf_code, input_img)
            output_img.to_png(context.Settings.arg_output_bl_bc_file)
            rgb_out = output_img.to_text()
            if context.Settings.opt_pnm_pbm:
                output_img.to_pnm(context.PNM_OUT_NAME)

        # --lc2f
        elif context.Settings.opt_lc2f:
            input_img = png_processor.process_png(context.Settings.arg_input_bl_bc_file)
            bf_code = translater.lc_to_f(input_img)
            if context.Settings.arg_output_bf_file is None:
                print(bf_code)
            else:
                context.Settings.arg_output_bf_file = enclose_with_b(context.Settings.arg_output_bf_file)
                with open(context.Settings.arg_output_bf_file, encoding='ASCII', mode='w') as file:
                    file.write(bf_code)
            rgb_in = input_img.to_text()
            if context.Settings.opt_pnm_pbm:
                input_img.to_pnm(context.PNM_IN_NAME)
        # print debug file
        #print('asd: {}'.format(context.Settings.opt_test))
        if context.Settings.opt_test:
            logger.Logger.log_to_file(program_data=bf_code, rgb_input=rgb_in, rgb_output=rgb_out)

    # run as interpreter
    else:
        # defined here to call interpret_bf in one place
        rgb_in = None
        # retrieve source code (retrieves it from just one place)
        # from user input (or stdinput)
        if context.Settings.interactive_mode:
            #read input with prompt
            sourcecode = input('Please, insert brainfuck code:\n')
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
                if context.Settings.opt_pnm_pbm:
                    img.to_pnm(context.PNM_IN_NAME)
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

