#!/usr/bin/env python3
from zlib import crc32
from zlib import compress

itob = lambda i, offset: i.to_bytes(offset, byteorder='big')


class OutOfBoardersException(Exception):
    pass


# it's possible to move in it
class Image:
    width = 0
    heigth = 0
    content = []
    pos_x = 0
    pos_y = 0
    delta_xy = (1, 0)
    turn_r_d = {(1, 0): (0, 1), (0, 1): (-1, 0), (-1, 0): (0, -1), (0, -1): (1, 0)}
    turn_l_d = {(1, 0): (0, -1), (0, -1): (-1, 0), (-1, 0): (0, 1), (0, 1): (1, 0)}
    # east, north, west, south
    delta_name = {(1, 0): 'e', (0, -1): 'n', (-1, 0): 'w', (0, 1): 's'}
    # extend when moving pos out of bounds?
    autoextend = False

    # append a black line to the bottom
    def extend(self):
        row = []
        for px in range(self.width):
            row.append((0, 0, 0))
        self.content.append(row)
        self.heigth += 1

    # content is 2d array of byte strings representing data from png or None if we whant black image of given size
    def __init__(self, width, heigth, content=None):
        self.width = width
        self.heigth = heigth
        # bulid 2d array of content
        if content is None:
            # whant new image
            self.content = []
            # heigth must be 0 because we whant to extend till appropriate size
            self.heigth = 0
            # empty if no content given
            for row in range(heigth):
                self.extend()
        else:
            for row in content:
                img_row = []
                for i in range(0, width * 3, 3):
                    pixel = (row[i], row[i + 1], row[i + 2])
                    # TODO: analyze lang
                    #if pixel != (255, 0, 0) or pixel != (128, 0, 0) or pixel != (,,)
                    img_row.append(pixel)
                self.content.append(img_row)

    def to_text(self):
        output = ''
        for row in self.content:
            output += '    {},\n'.format(row)
        return '[\n{}]'.format(output)

    def read_from_pos(self):
        return self.content[self.pos_y][self.pos_x]

    # input must be tuple of len = 3
    def write_to_pos(self, in_px):
        self.content[self.pos_y][self.pos_x] = in_px
        #print('write to: x = {} / {}, y = {} / {} dir = {}'.format(self.pos_x, self.width, self.pos_y, self.heigth, self.delta_name[self.delta_xy]))


    # new_delta = ip_turn_x[old_delta]
    def turn_r(self):
        self.delta_xy = self.turn_r_d[self.delta_xy]

    def turn_l(self):
        self.delta_xy = self.turn_l_d[self.delta_xy]

    def move_pos(self):
        self.pos_x += self.delta_xy[0]
        self.pos_y += self.delta_xy[1]
        # may autoextend down
        if not self.pos_y < self.heigth:
            if self.autoextend:
                # print(self.content)
                self.extend()
            else:
                raise OutOfBoardersException('x = {}, y = {}'.format(self.pos_x, self.pos_y))
        if (not 0 <= self.pos_x < self.width) or (not 0 <= self.pos_y):
            raise OutOfBoardersException('x = {}, y = {}'.format(self.pos_x, self.pos_y))

    def get_move_direction(self):
        return self.delta_name[self.delta_xy]

    def to_png(self, filename):
        with open(filename, mode='wb') as file:
            def write_chunk(name, data):
                # length of data, hdr, data, crc(name + data)
                file.write(itob(len(data), 4) + name + data + itob(crc32(name + data), 4))
            file.write(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A')
            # write IHDR
            write_chunk(b'IHDR', itob(self.width, 4) + itob(self.heigth, 4) + b'\x08\x02\x00\x00\x00')
            # write IDAT (just one chunk yet)
            data = bytearray()
            for row in self.content:
            # filtering is 0 on every row
                data.append(0)
                for px in row:
                    data.append(px[0])
                    data.append(px[1])
                    data.append(px[2])
            write_chunk(b'IDAT', compress(data))
            # write IEND
            write_chunk(b'IEND', b'')

    def to_pnm(self, filename):
        # prepare binary data (contetn of image)
        bin_content = b''
        for row in self.content:
            for px in row:
                bin_content += itob(px[0], 1) + itob(px[1], 1) + itob(px[2], 1)
        # write header and data to file
        with open(filename, mode='wb') as file:
            file.write(eval('b\'P6 {} {} 255 \' + {}'.format(self.width, self.heigth, bin_content)))