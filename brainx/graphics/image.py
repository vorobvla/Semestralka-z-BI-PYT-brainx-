#!/usr/bin/env python3


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