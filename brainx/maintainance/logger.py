#!/usr/bin/env python3


class Logger():
    file_num = 1

    # all args must be strings (for conveniance)
    @staticmethod
    def log_to_file(program_data=None, memory=None, memory_pointer=None, output=None, rgb_input=None, rgb_output=None):
        # UNIX endline
        lf = chr(10)
        with open('debug_{:02}.log'.format(Logger.file_num), encoding='ASCII', mode='w') as debug_file:
            if program_data is not None:
                debug_file.write('# program data' + lf + program_data + lf + lf)
            if memory is not None:
                debug_file.write('# memory' + lf + memory + lf + lf)
            if memory is not None:
                debug_file.write('# memory pointer' + lf + memory_pointer + lf + lf)
            if memory is not None:
                debug_file.write('# output' + lf + output + lf + lf)
            if rgb_input is not None:
                debug_file.write('# RGB input' + lf + rgb_input + lf + lf)
            if rgb_output is not None:
                debug_file.write('# RGB output' + lf + rgb_output + lf + lf)

        Logger.file_num = Logger.file_num + 1 if Logger.file_num < 99 else 1

