from PIL import Image
import math

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

def ints_to_str(int_list: list, spacing: int) -> str:
    contents = ""
    print("length of array:", len(int_list))
    # print(int_list)
    for i in range(0, len(int_list), spacing):
        for j in int_list[i]:
            contents += int_to_char(j)

    
    return contents

with Image.open("outputs/encoded_picture.png") as img:
    img_data = list(img.getdata())
    payload_length = get_length(img_data.pop()) # last tuple stores length of the payload
    print("Payload length:", payload_length)
    ext_len = get_length(img_data.pop()) # second-last tuple stores length of the extension
    print("Extension length:", ext_len)
    print("Total length:", payload_length + ext_len)

    print(img_data[:15])
    
    width, height = img.size
    total_pixels = width * (height - 1)
    payload_pixels = (payload_length + ext_len) // 3
    spacing = math.floor(total_pixels // payload_pixels)
    print("Spacing:", spacing)

    # ext = ints_to_str(img_data[payload_length:payload_length+ext_len], spacing)
    # print("Extension:", ext)

    message = ints_to_str(img_data, spacing)

with open("outputs/output", "w") as file:
    file.write(message)
