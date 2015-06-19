#!/usr/bin/env python3
from graphics import image
from math import sqrt
from math import ceil
from maintainance import logger

class TranslationError(Exception):
    pass

def is_b_loller(img_matrix):
    for row in img_matrix:
        for px in row:
            if not (px == (255, 0, 0) or px == (128, 0, 0) or px == (0, 255, 0) or px == (0, 128, 0)
                or px == (0, 0, 255) or px == (0, 0, 128) or px == (255, 255, 0) or px == (128, 128, 0)
                or px == (0, 255, 255) or px == (0, 128, 128) or px == (0, 0, 0)):
                return False
    return True

# computes number of code without ! # and any tokens that are not bf instructions
def bf_no_extentions_len(code):
    cnt = 0
    for t in code:
        if t == '+' or t == '-' or t == '<' or t == '>' or t == '.' or t == ',' or t == '[' or t == ']':
            cnt += 1
    return cnt

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

def turn_around_and_write(move_method, turn_method, write_method, write_what):
        write_method(write_what)
        turn_method()
        move_method()

def f_to_lc(bf_sourcecode, img=None):
    def deal_with_boarder(right_wite_what, left_write_what):
        # analyze postition & set bl instr if needed
        if img.get_move_direction() == 'e' and img.pos_x == img.width - 1:
            # turn adound and write 'rotate IP to the right' on proper places
            turn_around_and_write(img.move_pos, img.turn_r, write_instr, right_wite_what)
            turn_around_and_write(img.move_pos, img.turn_r, write_instr, left_write_what)
        elif img.get_move_direction() == 'w' and img.pos_x == 0:
            # turn adound and write 'rotate IP to the right left' on proper places
            turn_around_and_write(img.move_pos, img.turn_l, write_instr, 'LT')
            turn_around_and_write(img.move_pos, img.turn_l, write_instr, 'LT')

    if img is None:
        # loller
        instrs = { '>' : (255, 0, 0), '<' : (128, 0, 0), '+' : (0, 255, 0), '-' : (0, 128, 0), '.' : (0, 0, 255),
                   ',' : (0, 0, 128), '[' : (255, 255, 0), ']' : (128, 128, 0),
                   'RT' : (0, 255, 255), 'LT' : (0, 128, 128), 'NOP' : (0, 0, 0) }
        def write_instr(instr_key):
            img.write_to_pos(instrs[instr_key])
        # image is going to be square + 2 px for IP rotation
        side = ceil(sqrt(len(bf_sourcecode))) + 2
        img = image.Image(side, side)
    else:
        # copter
        instrs = { '>' : 0, '<' : 1, '+' : 2, '-' : 3, '.' : 4, ',' : 5,
                   '[' : 6, ']' : 7, 'RT' : 8, 'LT' : 9, 'NOP': 10 }
        def write_instr(instr_key):
            raw_px = img.read_from_pos()
            # difference between actual coding value and the value we whant
            delta = instrs[instr_key] - (-2*raw_px[0] + 3*raw_px[1] + raw_px[2]) % 11
            # compute improved blue value (changing blue color beacoue it's not multiplyed by anythibg un formula)
            b = (raw_px[2] + delta) % 256
            # write new pixel with improved value
            img.write_to_pos((raw_px[0], raw_px[1], b))

        # check if code will fit into image
            if bf_no_extentions_len(bf_sourcecode) > ((img.width - 2) * img.heigth) + 1:
                raise TranslationError('Program is not foing to fit in the image')

    for token in bf_sourcecode:
        # turn and leave proper instruction if needed
        deal_with_boarder('RT', 'LT')

        # process tokens from source
        if token == '#':
            # TODO bc input
            logger.Logger.log_to_file(program_data=bf_sourcecode, rgb_output=img.to_text())
        elif token == '!':
            # cant code input
            break
        else:
            # write & move on
            try:
                write_instr(token)
                img.move_pos()
            except KeyError:
                pass

    # fill rest of image with NOP
    while True:
        try:
            # analyze postition & set bl instr if needed
            deal_with_boarder('NOP', 'NOP')
            write_instr('NOP')
            img.move_pos()
        except image.OutOfBoardersException:
            break


    return img


