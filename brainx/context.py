#!/usr/bin/env python3
# 'constant' strings

from os import path
from sys import stderr
from traceback import print_exc
#from traceback import print_exc

HELP = 'HELP!!!!!'
USAGE = '''Usage:
    Interpreter:    brainx [sourcefile] [-t|--test] [-m memory] [-p memory_pointer_position] [--pnm|--pbm] [-h|--help]
    Translater:     brainx [-t|--test] [--pnm|--pbm] [-h|--help] ( --lc2f input_bl_bc_file [output_bf_file] | --f2lc -i input_bf_file [input_png_file] -o output_bl_bc_file )'''

UNKNOWN_OPTS = lambda unknwn_opt: 'Error. Unknown option \'{}\' occured.\n'.format(unknwn_opt) + USAGE

# 'constant' ints
RETURN_OK = 0
RETURN_ERROR = 1

LANG_BRAINLOLLER = 0
LANG_BRAINCOPTER = 1

is_opt = lambda str_opt: str_opt.startswith('-')

DUPLICATE_OPT = lambda opt: 'Duplicate setting of option {} occured.'.format(opt)
OPT_NOT_FOR_TRANSLATE_MOD = lambda opt: 'Option {} is not suttable for tarnsaltion mode (i.e. for program launched with ' \
                                        'options --lc2f or --f2lc).'.format(opt)
OPT_REQIRES_JUST_ONE_ARG = lambda opt: 'Option {} reqires one argument.'.format(opt)
OPT_REQIRES_AT_LEAST_ONE_ARG = lambda opt: 'Option {} reqires at least one argument.'.format(opt)

class OptsException(Exception):
    pass

class ArgsException(Exception):
    pass


class Settings:
    opt_lc2f = False
    opt_f2lc = False
    opt_test = False
    # must be bytes!!!
    arg_memory = b'\x00'
    arg_memory_pointer = 0
    opt_pnm_pbm = False
    translate_mode = False
    interactive_mode = False
    arg_source_file = None
    arg_input_bf_file = None
    arg_input_png_file = None
    arg_output_bl_bc_file = None
    arg_input_bl_bc_file = None
    arg_output_bf_file = None
    arg_console_sourcecode = None


    # parses opts. returns a list of unparced arguments
    @staticmethod
    def parse_opts(opts):
        try:
            argv = []
            idx = 0
            flag_mem_set = False
            flag_mem_ptr_set = False
            while idx < len(opts):
                # print('IDX {}'.format(idx))
                if not is_opt(opts[idx]):
                    argv.append(opts[idx])

                elif opts[idx] == '--lc2f':
                    Settings.translate_mode = True
                    Settings.opt_lc2f = True
                    try:
                        if is_opt(opts[idx+1]):
                            raise ArgsException(OPT_REQIRES_AT_LEAST_ONE_ARG('--lc2f'))
                        Settings.arg_input_bl_bc_file = opts[idx+1]
                    except IndexError:
                        raise ArgsException(OPT_REQIRES_AT_LEAST_ONE_ARG('--lc2f'))
                    # skip --lc2f and it's 1st arg
                    idx += 2
                    try:
                        if not is_opt(opts[idx]):
                            Settings.arg_output_bf_file = opts[idx]
                            idx += 1
                    except IndexError:
                        break
                    continue

                elif opts[idx] == '--f2lc':
                    # skip --f2lc
                    idx += 1
                    i_is_set = False
                    o_is_set = False
                    Settings.translate_mode = True
                    Settings.opt_f2lc = True
                    # idx must pint on a supposed subopt at the beginning of every iteration
                    while True:
                        try:
                            if opts[idx] == '-i':
                                if i_is_set:
                                    raise OptsException(DUPLICATE_OPT('--f2lc -i'))
                                # skip -i
                                idx += 1
                                #process arg1 (input bf)
                                if is_opt(opts[idx]):
                                    raise ArgsException(OPT_REQIRES_AT_LEAST_ONE_ARG('--f2lc -i'))
                                Settings.arg_input_bf_file = opts[idx]
                                i_is_set = True
                                # skip arg1
                                idx += 1
                                try:
                                    if is_opt(opts[idx]):
                                        continue
                                    else:
                                        Settings.arg_input_png_file = opts[idx]
                                        # skip arg2
                                        idx += 1
                                except IndexError:
                                    break
                            elif opts[idx] == '-o':
                                if o_is_set:
                                    raise OptsException(DUPLICATE_OPT('--f2lc -o'))
                                # skip -o
                                idx += 1
                                if is_opt(opts[idx]):
                                    raise ArgsException(OPT_REQIRES_AT_ONE_ARG('--f2lc -o'))
                                Settings.arg_output_bl_bc_file = opts[idx]
                                o_is_set = True
                                # skip arg3
                                idx += 3
                            else:
                                # implemented this way to be able to add non-oblogatory opts
                                if i_is_set and o_is_set:
                                    break
                                raise ArgsException('Unexpected token \'{}\' occured after \'--f2lc\''.format(opts[idx]))
                        except IndexError:
                            if i_is_set and o_is_set:
                                break
                            else:
                                raise ArgsException('Suboptions of --f2lc got wrong number of argumnts')

                elif opts[idx] == '-t' or opts[idx] == '--test':
                    if Settings.opt_test:
                        raise OptsException(DUPLICATE_OPT('-t or --test'))
                    Settings.opt_test = True

                elif opts[idx] == '-m' or opts[idx] == '--memory':
                    if Settings.translate_mode:
                        raise OptsException(OPT_NOT_FOR_TRANSLATE_MOD('-m or --memory'))
                    if flag_mem_set:
                        raise OptsException(DUPLICATE_OPT('-m or --memory'))
                    flag_mem_set = True
                    try:
                        if not is_opt(opts[idx + 1]):
                            # print('\n\nProcessing -m.\nGot: ' + str(opts[idx + 1]))
                            memory_str = opts[idx + 1]
                            memory_str = memory_str[1:] if memory_str.startswith('b') else memory_str
                            if memory_str.startswith('\'') and memory_str.endswith('\''):
                                memory_str = memory_str[1:-1]
                            exec('Settings.arg_memory = b\'{}\''.format(memory_str))
                            # Settings.arg_memory = opts[idx + 1]
                            # print('Saved: ' + str(Settings.arg_memory ))
                            idx += 2
                            continue
                    except IndexError:
                        pass
                    raise ArgsException(OPT_REQIRES_JUST_ONE_ARG('--memory'))

                elif opts[idx] == '-p' or opts[idx] == '--memory-pointer':
                    if Settings.translate_mode:
                        raise OptsException(OPT_NOT_FOR_TRANSLATE_MOD('-p or --memory-pointer'))
                    if flag_mem_ptr_set:
                        raise OptsException(DUPLICATE_OPT('-p or --memory-pointer'))
                    flag_mem_ptr_set = True
                    try:
                        if not is_opt(opts[idx + 1]):
                            # print('\n\nProcessing -p.\nGot: ' + str(opts[idx + 1]))
                            Settings.arg_memory_pointer = opts[idx + 1]
                            # print('Saved: ' + str(Settings.arg_memory_pointer ))
                            idx += 2
                            continue
                    except IndexError:
                        pass
                    raise ArgsException(OPT_REQIRES_JUST_ONE_ARG('--memory-pointer'))

                elif opts[idx] == '--pnm':
                    if Settings.opt_pnm_pbm:
                        raise OptsException(DUPLICATE_OPT('--pbm or --pnm'))
                    Settings.opt_pnm_pbm = True

                elif opts[idx] == '--pbm':
                    if Settings.opt_pnm_pbm:
                        raise OptsException(DUPLICATE_OPT('--pbm or --pnm'))
                    Settings.opt_pnm_pbm = True

                elif opts[idx] == '-h' or opts[idx] == '--help':
                    print(HELP)
                    exit(0)
                else:
                    raise OptsException('Unknown opt {} occured'.format(opts[idx]))
                idx += 1
            # argv = [arg for arg in opts if not is_opt(arg)]
            # print("ARGV::: ")
            # print(argv)
            argc = len(argv)
            if argc == 1:
                Settings.interactive_mode = True
            elif argc == 2:
                if argv[1].startswith('"') and argv[1].endswith('"'):
                    Settings.arg_console_sourcecode = argv[1][1:-1]
                elif not path.isfile(argv[1]):
                    #try:
                    raise ArgsException('Can not recognize argument \'{}\'. If You whant to pass file to interpreter, '
                                        'check whether this file exists and accessible. If You want to pass brainfuck '
                                        'source code, try to escape quotes. If You whant to use translation mode, you'
                                        ' this argument is not supposed to be used.'.format(argv[1]))
                    #except:
                    #    print_exc(file=stderr)
                    #    exit(4)
                else:
                    Settings.arg_source_file = argv[1]
            else:
                pass
                raise ArgsException('Unexpected arguments occured: \'{}\''.format(', '.join(argv[2:])))
        except (ArgsException, OptsException):
            print_exc()
            print(USAGE)
            exit(RETURN_ERROR)