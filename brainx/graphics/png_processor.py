#!/usr/bin/env python3
from zlib import decompress
from zlib import crc32

LANG_BRAINLOLLER = 0
LANG_BRAINCOPTER = 1


class FileErrorException(Exception):
    pass


class PNGWrongHeaderError(Exception):
    pass


class PNGNotImplementedError(Exception):
    pass

btoi = lambda b: int.from_bytes(b, byteorder='big', signed=False)


# returns False if name containg anything different from capital latter
def obligatory_chunk(name):
    for ch in name:
        if not ord('A') <= ch <= ord('Z'):
            return False
    return True


# needed for defilter, copypaste from lections
def paeth(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    elif pb <= pc:
        return b
    else:
        return c


# prev_row does not contain type!
def defilter(row, prev_row):
    # retrieve type and remove sype from row
    filt_type = row[0]
    row = row[1:]
    output_row = bytearray()
    # previous pixels (as defined in w3 specification)
    a = lambda idx: 0 if idx - 3 < 0 else row[idx - 3]
    b = lambda idx: 0 if prev_row is None else prev_row[idx]
    c = lambda idx: 0 if idx - 3 < 0 or prev_row is None else prev_row[idx - 3]
    #print('Type: {}'.format(filt_type))

    if filt_type == 0:
        return row
    elif filt_type == 1:
        for i, x in enumerate(row):
            output_row.append((x + a(i)) % 256)
    elif filt_type == 2:
        for i, x in enumerate(row):
            output_row.append((x + b(i)) % 256)
    elif filt_type == 3:
        for i, x in enumerate(row):
            output_row.append((x + (a(i) + b(i)) // 2) % 256)
    elif filt_type == 4:
        for i, x in enumerate(row):
            #print('i = {}, a = {}, b = {}, c = {}'.format(i, a(i), b(i), c(i)))
            output_row.append((x + paeth(a(i), b(i), c(i))) % 256)
    else:
        raise FileErrorException('Illegal filtration type {} occured'.format(filt_type))
    return bytes(output_row)


def process_png(filename):
    with open(filename, mode='rb') as file:
        # control if the file is PNG
        if file.read(8) != b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A':
            raise PNGWrongHeaderError()
        else:
            # analyze file. finish when IEND chunk found
            img_width = None
            img_heigth = None
            compressed_img_data = bytes()
            while True:
                read = file.read(4)
                print('READ: ' + str(read))
                if read == b'':
                    raise FileErrorException('Unexpected end of file')
                data_len = btoi(read)
                print('DATA LEN:' + str(data_len))

                # read chunk (containing cunk name + other chunk data)
                data = file.read(4 + data_len)
                # read crc
                crc = btoi(file.read(4))
                if crc32(data) != crc:
                    raise FileErrorException('File data currupted (CRC mismatch)')
                chunk = data[:4]
                if chunk == b'IHDR':
                    # analyze IHDR
                    img_width = btoi(data[4:8])
                    img_heigth = btoi(data[8:12])
                    other_opts = data[12:17]

                    if other_opts != b'\x08\x02\x00\x00\x00':
                        raise PNGNotImplementedError
                    continue
                elif chunk == b'IDAT':
                    # append data
                    compressed_img_data += data[4:]
                elif chunk == b'IEND':
                    print('REACHED END')
                    break
                elif obligatory_chunk(chunk):
                    raise NotImplementedError('Unexpected obligatory chunk {} in file {}'.format(str(chunk), filename))
                else:
                    pass
        #print(compressed_img_data)
        # decompress and defilter image data
        decompressed_img_data = decompress(compressed_img_data)
        row_idx = 0
        img_data = []
        print('DECOMPRESSED DATA, {}x{}\n-------\n'.format(img_width, img_heigth))
        #print(decompressed_img_data)
        decompressed_data_w = img_width * 3 + 1
        previous_row = None
        while row_idx < img_heigth:
            row = decompressed_img_data[row_idx * decompressed_data_w: (row_idx + 1) * decompressed_data_w]
            print('Processing : {}'.format(row))
            row = (defilter(row, previous_row))
            print('Processed : {}\n'.format(row))
            previous_row = row
            row_idx += 1
        #print(img_data)
        print('-------')
        return img_data, img_width, img_heigth


# parces colorcode from binary data
def get_image_matrix(data, w, h):
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

