#!/usr/bin/env python3
from zlib import crc32
from zlib import compress

itob = lambda i, offset: i.to_bytes(offset, byteorder='big')


class Image:
    width = 0
    heigth = 0
    content = []

    # data is array of byte strings representing data from png
    def __init__(self, data, width, heigth, ):
        self.width = width
        self.heigth = heigth
        # bulid 2d array of content
        for row in data:
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

    def get_px(self, y, x):
        return self.content[y][x]

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

