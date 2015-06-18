#!/usr/bin/env python3
from graphics import image

def is_b_loller(img_matrix):
    for row in img_matrix:
        for px in row:
            if not (px == (255, 0, 0) or px == (128, 0, 0) or px == (0, 255, 0) or px == (0, 128, 0)
                or px == (0, 0, 255) or px == (0, 0, 128) or px == (255, 255, 0) or px == (128, 128, 0)
                or px == (0, 255, 255) or px == (0, 128, 128) or px == (0, 0, 0)):
                return False
    return True


# lranslate braincopter of brainloller image to brainfuck source
def lc_to_f(lc_sourceimage):
    bf_sourcecode = ''
    # analyze colors and define apropriate lambda functions for more comfortable futher work
    if is_b_loller(lc_sourceimage.content):
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

    # init instruction pointer and stuff connected with it
    inst_ptr_x = 0
    inst_ptr_y = 0
    ip_move = (0, 1)
    # usage: new_move = ip_turn_x[old_move]
    ip_turn_r = {(0, 1):(1, 0), (1, 0):(0, -1), (0, -1):(-1, 0), (-1, 0):(0, 1)}
    ip_turn_l = {(0, 1):(-1, 0), (-1, 0):(0, -1), (0, -1):(1, 0), (1, 0):(0, 1)}

    # translate
    while 0 <= inst_ptr_y < lc_sourceimage.heigth and 0 <= inst_ptr_x < lc_sourceimage.width:
        # get new pixel
        px = px_encode(lc_sourceimage.get_px(inst_ptr_y, inst_ptr_x))
        # turn?
        if is_ip_rt(px):
            ip_move = ip_turn_r[ip_move]
        elif is_ip_lt(px):
            ip_move = ip_turn_l[ip_move]
        try:
            bf_sourcecode += instr[px]
        except KeyError:
            # nop
            pass
        inst_ptr_y += ip_move[0]
        inst_ptr_x += ip_move[1]
#        print(inst_ptr_y, ' ', inst_ptr_x)

    return bf_sourcecode