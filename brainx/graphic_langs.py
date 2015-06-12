#!/usr/bin/env python3


class PNGWrongHeaderError(Exception):
    pass


class PNGNotImplementedError(Exception):
    pass

btoi = lambda b : int.from_bytes(b, byteorder='big', signed=False)


def analyze_png(filename):
    with open(filename, mode='rb') as file:
        # control if the file is PNG
        if file.read(8) != b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A':
            raise PNGWrongHeaderError()
        else:
            # analyze file. finish when IEND chunk found
            img_width = None
            img_heigth = None
            while True:
                data_len = btoi(file.read(4))
                chunk = file.read(4)
                if chunk == b'IHDR':
                    # analyze IHDR
                    img_width = btoi(file.read(4))
                    img_heigth = btoi(file.read(4))
                    other_opts = file.read(5)
                    if other_opts != b'\x08\x02\x00\x00\x00' and other_opts != b'\x08\x02\x00\x00\x01':
                        raise PNGNotImplementedError
                    else:
                        break
                elif chunk == b'IEND':
                    break
                else:
                    file.read(data_len)
    print(data_len)
    print(img_width)
    print(img_heigth)


