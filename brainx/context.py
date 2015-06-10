#!/usr/bin/env python3
# 'constant' strings

import lex_analyzer

HELP = 'HELP!!!!!'
USAGE = 'Usage: brainx [sourcefile] [-t|--test] [-m memory] [-p memory_pointer_position] [--pnm|--pbm] [-h|--help]' \
        '| --lc2f input_bl_bc_file [output_bf_file] |' \
        ' --f2lc -i input_bf_file [input_png_file] -o output_bl_bc_file'
UNKNOWN_OPTS = lambda unknwn_opt: 'Error. Unknown option \'{}\' occured.\n'.format(unknwn_opt) + USAGE

# 'constant' ints
RETURN_OK = 0
RETURN_ERROR = 1

LANG_BRAINLOLLER = 0
LANG_BRAINCOPTER = 1

is_opt = lambda str_opt: str_opt.startswith('-')


class OptsDependencyException(Exception):
    pass

class ArgsException(Exception):
    pass


class Settings:
    opt_lc2f = False
    opt_f2lc = False
    opt_test = False
    arg_memory = False
    arg_memory_pointer = False
    opt_pnm = False
    opt_pbm = False
    translate_mode = False
    interactive_mode = False
    image_lang = None
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
        for idx, opt in enumerate(opts):
            if not is_opt(opt):
                pass

            elif opt == '--lc2f':
                if is_opt(opts[idx+1]):
                    raise ArgsException('--lc2f reqires at least one argument')
                Settings.arg_input_bl_bc_file = opts[idx+1]
                Settings.arg_output_bf_file = None if is_opt(opts[idx+2]) else opts[idx+2]

            elif opt == '--f2lc':
                for sub_idx in range(idx + 1, idx + 6):
                    try:
                        if not is_opt(opts[sub_idx]):
                            pass
                        elif opts[sub_idx] == '-i':
                            if is_opt(opts[sub_idx + 1]):
                                raise ArgsException('\'--f2lc -i\' reqires at least one argument')
                            Settings.arg_input_bf_file = opts[sub_idx + 1]
                            Settings.image_lang = LANG_BRAINLOLLER
                            if not is_opt(opts[sub_idx + 2]):
                                Settings.arg_input_png_file = opts[sub_idx + 2]
                                Settings.image_lang = LANG_BRAINCOPTER
                        elif opts[sub_idx] == '-o':
                            if is_opt(opts[sub_idx + 1]):
                                raise ArgsException('\'--f2lc -o\' reqires one argument')
                            Settings.arg_output_bl_bc_file = opts[sub_idx + 1]
                    except IndexError:
                        raise ArgsException('--f2lc got wrong number of argumnts')

            elif opt == '-i' or opt == '-o':
                pass

            elif opt == '-t' or opt == '--test':
                if Settings.translate_mode:
                    raise OptsDependencyException('Interpter oprions together with tanslate occured')
                Settings.opt_test = True

            elif opt == '-m' or opt == '--memory':
                try:
                    if not is_opt(opts[idx + 1]):
                        Settings.arg_memory = opts[idx + 1]
                        continue
                except IndexError:
                    pass
                raise ArgsException('-m reqires one argument')

            elif opt == '-p' or opt == '--memory-pointer':
                if Settings.translate_mode:
                    raise OptsDependencyException('Interpter oprions together with tanslate occured')
                try:
                    if not is_opt(opts[idx + 1]):
                        Settings.arg_memory = opts[idx + 1]
                        continue
                except IndexError:
                    pass
                raise ArgsException('-p reqires one argument')

            elif opt == '--pnm':
                if Settings.opt_pbm:
                    raise OptsDependencyException('attampt to set --pnm when -pbm is set')
                Settings.opt_pnm = True

            elif opt == '--pbm':
                if Settings.opt_pnm:
                    raise OptsDependencyException('attampt to set --pbm when -pnm is set')
                Settings.opt_pbm = True

            elif opt == '-h' or opt == '--help':
                print(HELP)
            else:
                print(UNKNOWN_OPTS(opt))
                exit(RETURN_ERROR)
        argv = [arg for arg in opts if not is_opt(arg)]
        print(argv)
        argc = len(argv)
        if argc == 1:
            Settings.interactive_mode = True
        elif argc == 2:
            # TODO: note in help that quotes need to be quoted
            if argv[1].startswith('"') and argv[1].endswith('"'):
                Settings.arg_console_sourcecode = argv[1][1:-1]
            elif lex_analyzer.is_bf(argv[1]):
                Settings.arg_console_sourcecode = argv[1]
            else:
                Settings.arg_source_file = argv[1]
        else:
            pass
            # raise ArgsException('Unexpected arguments occured: \'{}\''.format(', '.join(argv[2:])))