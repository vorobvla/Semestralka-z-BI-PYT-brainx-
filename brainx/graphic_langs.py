#!/usr/bin/env python3
from zlib import decompress


class FileErrorException(Exception):
    pass


class PNGWrongHeaderError(Exception):
    pass


class PNGNotImplementedError(Exception):
    pass

btoi = lambda b: int.from_bytes(b, byteorder='big', signed=False)


def obligatory_chunk(name):
    for ch in name:
        if not ord('A') <= ch <= ord('Z'):
            return False
    return True


def process_png(filename):
    with open(filename, mode='rb') as file:
        # control if the file is PNG
        if file.read(8) != b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A':
            raise PNGWrongHeaderError()
        else:
            # analyze file. finish when IEND chunk found
            img_width = None
            img_heigth = None
            comprimated_data = bytes()
            while True:
                read = file.read(4)
                print('READ: ' + str(read))
                if read == b'':
                    raise FileErrorException('Unexpected end of file')
                data_len = btoi(read)
                print('DATA LEN:' + str(data_len))
                chunk = file.read(4)
                if chunk == b'IHDR':
                    # analyze IHDR
                    img_width = btoi(file.read(4))
                    img_heigth = btoi(file.read(4))
                    other_opts = file.read(5)

                    if other_opts != b'\x08\x02\x00\x00\x00' and other_opts != b'\x08\x02\x00\x00\x01':
                        raise PNGNotImplementedError
                    file.read(4)
                    continue
                elif chunk == b'IDAT':
                    # append data
                    comprimated_data += file.read(data_len)
                    file.read(4)
                elif chunk == b'IEND':
                    print('REACHED END')
                    break
                elif obligatory_chunk(chunk):
                    raise FileErrorException('Unexpected obligatory chunk {} in file {}'.format(str(chunk), filename))
                else:
                    # skip chunks that are not interesting for us
                    file.read(data_len + 4)
        print(comprimated_data)
        return decompress(comprimated_data), img_width, img_heigth


# parces colorcode from binary data
def parce_colorcode(data, w, h):
    act_h = 0
    img_matrix = []
    idx = 0
    while act_h < h:
        act_h += 1
        act_w = 0
        row = []
        while act_w < w:
            act_w += 1
            row.append((data[idx], data[idx + 1], data[idx + 2]))
            idx += 3
        img_matrix.append(row)

    return img_matrix

