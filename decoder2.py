from PIL import Image
import math
import numpy as np

def get_length(pixel: tuple) -> int:
    '''
    converts the 3 digit base 256 integer to a base 10 value
    '''
    return int(pixel[0]) * (256**2) + int(pixel[1])* (256**1) + int(pixel[2])

def int_to_char(num: int) -> str:
    '''
    converts an integer (between 0 and 127) to an ASCII character
    '''

    binary = format(num, "08b")
    char = chr(int(binary[1:], 2))
    return char if char != "\x00" else ""

def ints_to_str(int_list: list, spacing: int, end: int) -> str:
    contents = ""
    pixel_processed = 0
    for i in range(0, len(int_list)):
        for j in range(0, len(int_list[i]), spacing):
            pixel_processed += 1
            for k in int_list[i][j]:
                contents += int_to_char(k)
                if pixel_processed > end:
                    return contents

with Image.open("outputs/encoded_picture.png") as img:
    img_data = np.array(img)
    payload_length = get_length(img_data[-1][-1]) # last tuple stores length of the payload
    print("Payload length:", payload_length)
    ext_len = get_length(img_data[-1][-2]) # second-last tuple stores length of the extension
    print("Extension length:", ext_len)
    print("Total length:", payload_length + ext_len)
    
    width, height = img.size
    total_pixels = width * (height - 1)
    payload_pixels = (payload_length + ext_len) // 3
    spacing = math.floor(total_pixels // payload_pixels)
    print("Width x height:", width, height)
    print("Spacing:", spacing)

    raw_data = ints_to_str(img_data, spacing, payload_pixels)
    end_of_payload = len(raw_data) - ext_len
    print(raw_data[end_of_payload:])
    ext = raw_data[end_of_payload:end_of_payload + ext_len]
    print("Extention:", ext)
    message = raw_data[:len(raw_data)-ext_len-1]


with open("outputs/output." + ext, "w") as file:
    file.write(message)
