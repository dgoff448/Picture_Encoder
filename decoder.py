from PIL import Image

def get_length(pixel: tuple) -> int:
    """converts the 3 digit base 256 integer to a base 10 value"""
    return int(pixel[0]) * (256**2) + int(pixel[1])* (256**1) + int(pixel[2])

def int_to_char(num: int) -> str:
    """converts an integer (between 0 and 127) to an ASCII character"""
    
    binary = format(num, "08b")
    char = chr(int(binary[1:], 2))
    return char if char != "\x00" else ""

def ints_to_str(int_list: list) -> str:
    contents = ""
    for i in int_list:
        contents += int_to_char(i)
    return contents

with Image.open("encoded_picture.png") as img:
    img_data = list(img.getdata())
    payload_length = get_length(img_data.pop()) # last tuple stores length of the payload
    print("Payload length:", payload_length)
    ext_len = get_length(img_data.pop()) # second-last tuple stores length of the extension
    print("Extension length:", ext_len)

    img_data = [x for pixels in img_data for x in pixels[:3]]
    ext = ints_to_str(img_data[payload_length:payload_length+ext_len])
    print("Extension:", ext)

    message = ints_to_str(img_data[:payload_length])

with open("outputs/output." + ext, "w") as file:
    file.write(message)
