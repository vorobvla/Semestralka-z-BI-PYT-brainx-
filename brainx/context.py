#!/usr/bin/env python3
# 'constant' strings
HELP = 'HELP!!!!!'
USAGE = 'Usage: brainx [sourcefile]'
UNKNOWN_OPTS = lambda unknwn_opt: 'Error. Unknown option \'{}\' occured.\n'.format(unknwn_opt) + USAGE

# 'constant' ints
RETURN_OK = 0
RETURN_ERROR = 1

is_opt = lambda str_opt: str_opt.startswith('-')


class OptsDependencyException(Exception):
    pass

class ArgsException(Exception):
    pass


class OptsArgs:
    __opt_lc2f = False
    __opt_f2lc = False
    __opt_test = False
    __opt_memory = False
    __opt_memory_pointer = False
    __opt_pnm = False
    __opt_pbm = False
    __translate_mode = False
    __arg_source_file = None
    __arg_input_bf_file = None
    __arg_input_png_file = None
    __arg_output_bc_file = None
    __input_bl_bc_file = None
    __output_bf_file = None

    def set_lc2f(self):
        if self.opt_f2lc:
            raise OptsDependencyException()
        else:
            __optf2lc = True
