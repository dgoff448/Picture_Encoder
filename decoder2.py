"""decoder2.py: Decodes files produced by encoder2.py"""

import sys
import math
from progress import Progress
import numpy as np
from PIL import Image
from pathlib import Path

def get_length(pixel: tuple) -> int:
    """convert the 3 digit base 256 integer to a base 10 value"""
    return int(pixel[0]) * (256**2) + int(pixel[1])* (256**1) + int(pixel[2])

def int_to_char(num: int) -> str:
    """convert an integer (between 0 and 127) to an ASCII character"""

    binary = format(num, "08b")
    char = chr(int(binary[1:], 2))
    return char if char != "\x00" else ""

def ints_to_str(pixel_list: list, spacing: int, end: int) -> str:
    """Convert a list of RGB values into a string"""
    contents = ""
    pixels_processed = 0
    prog = Progress(end, "Decoding file. . .", True, True)

    for i in range(0, len(pixel_list)):
        for j in range(0, len(pixel_list[i]), spacing):
            prog.printProgress(pixels_processed)
            pixels_processed += 1
            for k in pixel_list[i][j]:
                contents += int_to_char(k)
                if pixels_processed > end:
                    prog.printComplete("Decoded file")
                    return contents


if len(sys.argv) == 2:
    picture_file = sys.argv[1]
    if not Path(picture_file).is_file():
        print("usage: python decoder2.py [<image_path>]")
        exit(1)
else:
    picture_file = "outputs/encoded_picture.png"

with Image.open(picture_file) as img:
    img_data = np.array(img)
    payload_length = get_length(img_data[-1][-1]) # last tuple stores length of the payload
    ext_len = get_length(img_data[-1][-2]) # second-last tuple stores length of the extension
    
    width, height = img.size
    total_pixels = width * (height - 1)
    payload_pixels = (payload_length + ext_len) // 3
    spacing = math.floor(total_pixels // payload_pixels)


    raw_data = ints_to_str(img_data, spacing, payload_pixels)
    ext = "." + raw_data[:ext_len]
    if not ext[1:].isalnum():
        ext = ""
    message = raw_data[ext_len:]

with open("outputs/output" + ext, "w") as file:
    file.write(message)
