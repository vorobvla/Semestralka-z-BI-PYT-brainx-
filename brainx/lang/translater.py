#!/usr/bin/env python3
from graphics import image
from math import sqrt
from math import ceil


def is_b_loller(img_matrix):
    for row in img_matrix:
        for px in row:
            if not (px == (255, 0, 0) or px == (128, 0, 0) or px == (0, 255, 0) or px == (0, 128, 0)
                or px == (0, 0, 255) or px == (0, 0, 128) or px == (255, 255, 0) or px == (128, 128, 0)
                or px == (0, 255, 255) or px == (0, 128, 128) or px == (0, 0, 0)):
                return False
    return True


# lranslate braincopter of brainloller image to brainfuck source
def lc_to_f(source_img):
    bf_sourcecode = ''
    # analyze colors and define apropriate lambda functions for more comfortable futher work
    if is_b_loller(source_img.content):
        #setup for loller
        instr = {
            (255, 0, 0) : '>',
            (128, 0, 0) : '<',
            (0, 255, 0) : '+',
            (0, 128, 0) : '-',
            (0, 0, 255) : '.',
            (0, 0, 128) : ',',
            (255, 255, 0) : '[',
            (128, 128, 0) : ']'
        }
        is_ip_rt = lambda px: True if px == (0, 255, 255) else False
        is_ip_lt = lambda px: True if px == (0, 128, 128) else False
        # no change
        px_encode = lambda px: px
    else:
        # setup for copter
        instr = { 0 : '>', 1 : '<', 2 : '+', 3 : '-', 4 : '.', 5 : ',', 6 : '[', 7 : ']' }
        is_ip_rt = lambda px: True if px == 8 else False
        is_ip_lt = lambda px: True if px == 9  else False
        # px to number for copter
        px_encode = lambda px: (-2*px[0] + 3*px[1] + px[2]) % 11

    # translate
    while True:
        try:
            # get new pixel
            px = px_encode(source_img.read_from_pos())
            # turn?
            if is_ip_rt(px):
                source_img.turn_r()
            elif is_ip_lt(px):
                source_img.turn_l()
            try:
                bf_sourcecode += instr[px]
            except KeyError:
                # nop
                pass
            source_img.move_pos()
        except image.OutOfBoardersException:
            break
#        print(inst_ptr_y, ' ', inst_ptr_x)

    return bf_sourcecode

def f_to_l(bf_sourcecode):
    instr = {
        '>' : (255, 0, 0),
        '<' : (128, 0, 0),
        '+' : (0, 255, 0),
        '-' : (0, 128, 0),
        '.' : (0, 0, 255),
        ',' : (0, 0, 128),
        '[' : (255, 255, 0),
        ']' : (128, 128, 0),
        'R' : (0, 255, 255),
        'L' : (0, 128, 128)
    }
    # image is going to be quare + 2 px for IP rotation
    side = ceil(sqrt(len(bf_sourcecode))) + 2
    bl_img = image.Image(side, side)
    # make shure  R L will not occur
    bf_sourcecode.replace('R', '')
    bf_sourcecode.replace('L', '')

    for token in bf_sourcecode:
        # analyze postition & set bl instr if needed
        if bl_img.get_move_direction() == 'e' and bl_img.pos_x == side - 1:
            bl_img.write_to_pos(instr['R'])
            bl_img.turn_r()
            bl_img.move_pos()
            bl_img.write_to_pos(instr['R'])
            bl_img.turn_r()
            bl_img.move_pos()
        elif bl_img.get_move_direction() == 'w' and bl_img.pos_x == 0:
            bl_img.write_to_pos(instr['L'])
            bl_img.turn_l()
            bl_img.move_pos()
            bl_img.write_to_pos(instr['L'])
            bl_img.turn_l()
            bl_img.move_pos()

        # process tokens from source
        if token == '#':
            pass #TODO: debug log
        elif token == '!':
            break
        else:
            # write & move on
            try:
                bl_img.write_to_pos(instr[token])
                bl_img.move_pos()
            except KeyError:
                pass
    return bl_img


