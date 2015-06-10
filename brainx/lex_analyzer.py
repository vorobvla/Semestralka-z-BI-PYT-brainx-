#!/usr/bin/env python3


def is_bf(code):
    for c in code:
        if c == '[' or c == ']' or c == '.' or c == ',' or c == '+' or c == '-'\
                or c == '<' or c == '>' or c == '#' or c == '!':
            pass
        elif c.isspace():
            pass
        else:
            return False
    return True
