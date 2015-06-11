#!/usr/bin/env python3
# 'constant' strings

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
    # must be bytes!!!
    arg_memory = b'\x00'
    arg_memory_pointer = 0
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
        argv = []
        idx = 0
        while idx < len(opts):
            if not is_opt(opts[idx]):
                argv.append(opts[idx])

            elif opts[idx] == '--lc2f':
                if is_opt(opts[idx+1]):
                    raise ArgsException('--lc2f reqires at least one argument')
                Settings.arg_input_bl_bc_file = opts[idx+1]
                idx += 2
                if not is_opt(opts[idx+2]):
                    Settings.arg_output_bf_file = opts[idx+2]
                    idx += 1
                continue

            elif opts[idx] == '--f2lc':
                sub_idx = idx + 1
                #sikp --f2lc
                idx += 1
                #other arg processed -- time to break
                break_flag = False
                while sub_idx < idx + 6:
                    try:
                        if opts[sub_idx] == '-i':
                            #sikp -i
                            sub_idx = idx = idx + 1
                            if is_opt(opts[sub_idx + 1]):
                                raise ArgsException('\'--f2lc -i\' reqires at least one argument')
                            Settings.arg_input_bf_file = opts[sub_idx + 1]
                            Settings.image_lang = LANG_BRAINLOLLER
                            #sikp arg1
                            idx += 1
                            if not is_opt(opts[sub_idx + 2]):
                                Settings.arg_input_png_file = opts[sub_idx + 2]
                                Settings.image_lang = LANG_BRAINCOPTER
                                #sikp arg2
                                sub_idx = idx = idx + 1
                        elif opts[sub_idx] == '-o':
                            if is_opt(opts[sub_idx + 1]):
                                raise ArgsException('\'--f2lc -o\' reqires one argument')
                            Settings.arg_output_bl_bc_file = opts[sub_idx + 1]
                            idx += 2
                        else:
                            raise ArgsException('Unexpected token \'{}\' occured after --f2lc'.format(opts[sub_idx]))
                        if break_flag:
                            break
                        else:
                            break_flag = True
                            continue
                    except IndexError:
                        raise ArgsException('--f2lc got wrong number of argumnts')
                    sub_idx += 1

            elif opts[idx] == '-t' or opts[idx] == '--test':
                if Settings.translate_mode:
                    raise OptsDependencyException('Interpter oprions together with tanslate occured')
                Settings.opt_test = True

            elif opts[idx] == '-m' or opts[idx] == '--memory':
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
                raise ArgsException('-m reqires one argument')

            elif opts[idx] == '-p' or opts[idx] == '--memory-pointer':
                if Settings.translate_mode:
                    raise OptsDependencyException('Interpter oprions together with tanslate occured')
                try:
                    if not is_opt(opts[idx + 1]):
                        # print('\n\nProcessing -p.\nGot: ' + str(opts[idx + 1]))
                        Settings.arg_memory_pointer = opts[idx + 1]
                        # print('Saved: ' + str(Settings.arg_memory_pointer ))
                        idx += 2
                        continue
                except IndexError:
                    pass
                raise ArgsException('-p reqires one argument')

            elif opts[idx] == '--pnm':
                if Settings.opt_pbm:
                    raise OptsDependencyException('attampt to set --pnm when -pbm is set')
                Settings.opt_pnm = True

            elif opts[idx] == '--pbm':
                if Settings.opt_pnm:
                    raise OptsDependencyException('attampt to set --pbm when -pnm is set')
                Settings.opt_pbm = True

            elif opts[idx] == '-h' or opts[idx] == '--help':
                print(HELP)
            else:
                # TODO: suspitious place: uncomment and change print to throw
                pass
                #print(UNKNOWN_OPTS(opts[idx]))
                #exit(RETURN_ERROR)
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
            elif not argv[1].endswith('.b'):
                Settings.arg_console_sourcecode = argv[1]
            else:
                Settings.arg_source_file = argv[1]
        else:
            pass
            raise ArgsException('Unexpected arguments occured: \'{}\''.format(', '.join(argv[2:])))