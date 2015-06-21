#!/usr/bin/env python3
# 'constant' strings

from os import path
from sys import stderr
from traceback import print_exc
#from traceback import print_exc

HELP = \
    '''This program can interpret brainfuck, brainloller or braincopter programs and translate program code between
brainfuck and brainloller/braincopter.
Program can be ran as interpreter (Interpreter mode) to interpret a program or as translator (Translator mode) to
translate program from one language to another. These modes have different interface.

Program runs in Translator mode if --lc2f or --f2lc occurs in the parameters. Otherwise it runs in Interpreter mode.

Parameters valid in both modes:
    -h,    --help  display this help and exit
    --pnm, --pbm   write input and output image files also to PNM file in P6 format
    -t,    --test  write debug information into debug file after the program is interpreted / translated

Parameters valid in Interpreter mode:
   programfile                          name of file containing brainfuck, brainloller or braincopter program that is
supposed to be ran. Must end with '.b' if it is a text file with brainfuck program. Otherwise program recognizes
the file as an image file (see below)
   brainfuck_code                       brainfuck code that is supposed to be interpreted
    -m,  --memory    b'memory_state'     set starting state of memory. memory_state argument must be a description of
desired state in a format of python bytes (as noted in the start of this line)
    -p,  --memory_pointer_position   n   set starting position of memory pointer. n is the desired position. Must be
greater or equal to 0 and less then length of memory (that is 1 by default)
    --prin, --program-input [program_input_file]    set program input. If program_input_file is defined, infut will be
read from it. Otherwise interpreter will get it from user in interactive mode (the use will be asked to insert input
when the program is started; if inrepreter is already running in interactive mode, the user will be asked to insert
input after he or she inserts code). If program gets input via this option, the input deined in program code (with !)
is ignored.

Program launched without arguments acts as an interpreter in interactive mode. The user is asked to insert brainfuck
code. The retrieved code will be interpreted.

Parameters valid in Translator mode:
    --f2lc [--bl_spiral] -i input_bf_file [input_png_file]    -o output_bl_bc_file   translate brainfuck code to brainloller or
braincopter. -i specifies arguments input_bf_file and input_png_file. The first one that is the name of text file
containing the brainfuck code to be translated. The second one is the name of the image file that will be used for
translation to braincopter. If this argument is missing, the program will be translate to brainloller. If --bl_spiral
option is set the brinfuck input will be translated into brainloller and the instructions in the oputput file will be
arranged into spiral. In this case argument input_png_file will be ignored. The program will be translated into
brainloller even if this argument presents.
-o output_bl_bc_file contains the name of image file where the result brainloller/braincopter image will be written to
    --lc2f  input_bl_bc_file    [output_bf_file]                        translate image in brainloller/braincopter
form input_bl_bc_file file to brainfuck code. The result will be written to text file with name specified in
output_bf_file. It in not needed to specify if the image is contains brainloller or braincopter program. The translator
will do it itself.

Files' names and formats:
    Text files with brainfuck code must be text files with ASCII encoding. Their names must end with ".b" extension.
If the name of this file is given as a value of input_bf_file or output_bf_file without ".b" extension, the program will
correct it automatically. It will not correct programfile though because in this case ".b" is used to distinguish
the text file with brainfuck from image files.
    Debug files are text files encoded with ASCII with name debug_NN.log where NN is number of file. These files
content information about state of interpreter/translator during or after running/translating the code.
    An input image file must be in PNG format with bit depth set to 8, color type set to 2 and compression method,
filter method and interlace method set to 0. It also must not contain any obligatory chunks except
IHDR, IDAT and IEND.
    Output PNG files have bit depth set to 8, color type set to 2 and compression method, filter method and interlace
method set to 0. They only contain IHDR, IDAT and IEND chunks. All data is saved into one IDAT chunk.
    Output PNM files are in format P6 and use whitespace as a separator for header fields. They are named
"input_image_in_pnm" (containing input image of program) or "output_image_in_pnm" (containing output image of program)

Exit codes:
    0 if Ok,
    1 any other problem,
    4 attempt to process an image file, that's format is not supported
    8 attempt to process an image file, that contains obligatory chunks, that's processing is not implemented
'''

USAGE = \
'''Usage:
    Interpreter mode:    brainx [programfile | "brainfuck_code"] [-t|--test] [-m|memory b'memory_state']
[-p|memory_pointer_position n] [--pnm|--pbm] ['--prin'|'--program-input' [program_input_file]] [-h|--help]
    Translator mode:     brainx [-t|--test] [--pnm|--pbm] [-h|--help] ( --lc2f input_bl_bc_file [output_bf_file] |
--f2lc [--bl_spiral] -i input_bf_file [input_png_file] -o output_bl_bc_file )'''

UNKNOWN_OPTS = lambda unknwn_opt: 'Error. Unknown option \'{}\' occured.\n'.format(unknwn_opt) + USAGE

# 'constant' ints
RETURN_OK = 0
RETURN_ERROR = 1

LANG_BRAINLOLLER = 0
LANG_BRAINCOPTER = 1

PNM_IN_NAME = 'input_image_in_pnm'
PNM_OUT_NAME = 'output_image_in_pnm'

is_opt = lambda str_opt: str_opt.startswith('-')

DUPLICATE_OPT = lambda opt: 'Duplicate setting of option {} occured.'.format(opt)
OPT_NOT_FOR_TRANSLATE_MOD = lambda opt: 'Option {} is not suttable for tarnsaltion mode (i.e. for program launched with ' \
                                        'options --lc2f or --f2lc).'.format(opt)
OPT_REQIRES_JUST_ONE_ARG = lambda opt: 'Option {} reqires one argument.'.format(opt)
OPT_REQIRES_AT_LEAST_ONE_ARG = lambda opt: 'Option {} reqires at least one argument.'.format(opt)
CANNOT_ACCESS_FILE = lambda file: 'Connot access file named \'{}\''.format(file)

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
    opt_bl_spiral = False
    # will contain input file name or True for intaractive mode
    arg_program_input = None


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
                        if not path.isfile(Settings.arg_input_bl_bc_file):
                            raise ArgsException(CANNOT_ACCESS_FILE(Settings.arg_input_bl_bc_file))
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
                                if not path.isfile(Settings.arg_input_bf_file):
                                    raise ArgsException(CANNOT_ACCESS_FILE(Settings.arg_input_bf_file))
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
                                    if not path.isfile(Settings.arg_input_png_file):
                                        raise ArgsException(CANNOT_ACCESS_FILE(Settings.arg_input_png_file))
                                except IndexError:
                                    break
                            elif opts[idx] == '-o':
                                if o_is_set:
                                    raise OptsException(DUPLICATE_OPT('--f2lc -o'))
                                # skip -o
                                idx += 1
                                if is_opt(opts[idx]):
                                    raise ArgsException(OPT_REQIRES_JUST_ONE_ARG('--f2lc -o'))
                                Settings.arg_output_bl_bc_file = opts[idx]
                                o_is_set = True
                                # skip arg3
                                idx += 1
                            elif opts[idx] == '--bl_spiral':
                                Settings.opt_bl_spiral = True
                                idx += 1
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
                            Settings.arg_memory_pointer = opts[idx + 1]
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
                    print(USAGE)
                    print(HELP)
                    exit(0)

                elif opts[idx] == '--prin' or '--program-input':
                    # interactive input
                    Settings.arg_program_input = True
                    idx +=1
                    try:
                        if not is_opt(opts[idx]):
                            # input file
                            Settings.arg_program_input = opts[idx]
                            idx += 1
                    except IndexError:
                        pass
                    continue

                else:
                    raise OptsException('Unknown opt {} occured'.format(opts[idx]))
                idx += 1
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