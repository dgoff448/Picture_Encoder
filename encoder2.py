from PIL import Image
import numpy as np
import math

class Payload:
    def __init__(self, picture_fn, payload_fn):
        self.picture_fn = picture_fn
        self.payload_fn = payload_fn
        self.payload_ext = payload_fn.split(".")[-1]
        self.img = Image.open(picture_fn)
        self.maxChars = (self.img.size[0] * self.img.size[1] * 3) - 6
        self.payload = ""

        with open(payload_fn, 'r', encoding="UTF-8") as f:
            for line in f.readlines():
                self.payload += line

        self.payload_len = len(self.payload) # BEFORE EXTENSION ADDED
        print(self.payload)
        print(f"Payload Length: {len(self.payload)}")
        print(f"Extension Length: {len(self.payload_ext)}")
        self.payload = self.payload + self.payload_ext

    # Checks if image can hold payload.
    def canFit(self) -> bool:
        return False if len(self.payload) > self.maxChars else True
    
    # Converts length int to an RGB tuple
    def to_base_256(self, n):
        result = []
        while n > 0:
            result.append(n % 256)
            n = n // 256
        if len(result) == 1:
            result.append(0)
            result.append(0)
        elif len(result) == 2:
            result.append(0)
        result.reverse()  # because we need the most significant byte first
        return tuple(result)
    
    # Encode payload into image array
    def encode(self):
        spreadRes = self.img.size[0] * (self.img.size[1] - 1)
        spread = math.floor(spreadRes // len(self.payload) // 3)
        


        arr = np.array(self.img)
        arr[-1][-1] = self.to_base_256(self.payload_len)     # last RGB value holds the length of the payload (read like a normal num)
        arr[-1][-2] = self.to_base_256(len(self.payload_ext))    # second-to-last RGB value holds the length of the payload extension

        print(arr[-1][-1], print(arr[-1][-2]))

        pc = 0
        for i in range(0, len(arr)):# for i, ar in enumerate(arr):
            for j in range(0, len(arr[i])): # for j, a in enumerate(ar):
                oldTup = list(arr[i][j])
                newArr = [0, 0, 0]
                for k in range(0, len(arr[i][j])): # for k, rgb in enumerate(oldTup):
                    if self.payload[pc] in ["‘", "’"]:
                        newArr[k] = int(format(arr[i][j][k], "08b")[:1] + format(ord("'"), "08b")[1:], 2)
                    elif self.payload[pc] in ['“', '”']:
                        newArr[k] = int(format(arr[i][j][k], "08b")[:1] + format(ord('"'), "08b")[1:], 2)
                    else:
                        newArr[k] = int(format(arr[i][j][k], "08b")[:1] + format(ord(self.payload[pc]), "08b")[1:], 2)
                    pc += 1
                    if pc > len(self.payload)-1:
                        break
                arr[i][j] = tuple(newArr)
                if pc > len(self.payload)-1:
                        return arr
    
    def saveImage(self, arr):
        img = Image.fromarray(arr)
        img.save('encoded_picture.png', quality=100, subsampling=0)


# Main 
payload_file = input("Enter Payload Filename: ")
picture_file = input("Enter Picture Filename: ")
pl = Payload(f"images/{picture_file}", f"payloads/{payload_file}")
print(pl.payload_ext)
if not pl.canFit():
    raise("Not enough space in image to encode payload.")

pl.saveImage(pl.encode())
