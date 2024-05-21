from PIL import Image
import numpy as np
import math
import sys
import time
import progress
import argparse

# Argument Handling *********************************************************************
parser = argparse.ArgumentParser(description="Encode a payload file into an image.")
parser.add_argument('Payload_Filename', type=str)
parser.add_argument('Image_Filename', type=str)
parser.add_argument('-pb', '--progress_bar', action='store_true')
parser.add_argument('-fract', '--fraction', action='store_true')
parser.add_argument('-perc', '--percent', action='store_true')
parser.add_argument('-progall', '--progress_all', action='store_true')
args = parser.parse_args()
# ***************************************************************************************


class Payload:
    def __init__(self, picture_fn, payload_fn, pb, fract, perc):
        self.picture_fn = picture_fn
        self.payload_fn = payload_fn
        self.pb = pb
        self.fract = fract
        self.perc = perc
        self.noProgress = (not pb) and (not fract) and (not perc)
        self.payload_ext = payload_fn.split(".")[-1]
        self.img = Image.open(picture_fn)
        self.maxChars = (self.img.size[0] * self.img.size[1] * 3) - 6
        self.payload = ""

        with open(payload_fn, 'r', encoding="UTF-8") as f:
            prog = progress.Progress(100)
            prog.printInProgress("Reading Payload File. . .") # Cosmetics
            for line in f.readlines():
                self.payload += line
            prog.printComplete("Payload File Read.")

        self.payload_len = len(self.payload) # BEFORE EXTENSION ADDED
        # print(f"Payload Length: {len(self.payload)}")
        # print(f"Extension Length: {len(self.payload_ext)}")
        self.payload = self.payload_ext + self.payload + '\n'

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
        spread = math.floor(spreadRes // (len(self.payload) // 3))
        # print(f"spreadRes: {spreadRes}\nTotal Length: {len(self.payload)}\nSpread: {spread}")  # Debug line


        arr = np.array(self.img)
        arr[-1][-1] = self.to_base_256(self.payload_len)     # last RGB value holds the length of the payload (read like a normal num)
        arr[-1][-2] = self.to_base_256(len(self.payload_ext))    # second-to-last RGB value holds the length of the payload extension

        # print(f"Payload Length Pixel: {arr[-1][-1]}\nExtension Length Pixel: {arr[-1][-2]}")      # Debug print to show last to pixels

        pc = 0
        prog = progress.Progress(self.payload_len, "Encoding File ", self.pb, self.fract, self.perc, 30)
        for i in range(0, len(arr)): # for i, ar in enumerate(arr):
            for j in range(0, len(arr[i]), spread): # for j, a in enumerate(ar):
                oldTup = list(arr[i][j]) 
                newArr = [0, 0, 0]
                saveArrays = []
                for k in range(0, len(arr[i][j])): # for k, rgb in enumerate(oldTup):
                    if self.payload[pc] in ["‘", "’"]:
                        newArr[k] = int(format(arr[i][j][k], "08b")[:1] + format(ord("'"), "08b")[1:], 2)
                    elif self.payload[pc] in ['“', '”']:
                        newArr[k] = int(format(arr[i][j][k], "08b")[:1] + format(ord('"'), "08b")[1:], 2)
                    else:
                        newArr[k] = int(format(arr[i][j][k], "08b")[:1] + format(ord(self.payload[pc]), "08b")[1:], 2)
                        # print(f"Old Val: {format(arr[i][j][k])}\n Pay Val: {format(ord(self.payload[pc]))}")
                    pc += 1
                    if not self.noProgress:
                        prog.printProgress(pc) # Cosmetics
                    if pc > len(self.payload)-1:
                        break
                arr[i][j] = tuple(newArr)
                saveArrays.append(newArr)
                if pc > len(self.payload)-1:
                        if not self.noProgress:
                            prog.printComplete("File Encoded.") # Cosmetics
                        return arr
        if not self.noProgress:
            prog.printComplete("File Encoded.") # Cosmetics
        # print(saveArrays)
        return arr
    
    def saveImage(self, arr):
        prog = progress.Progress(100) # Cosmetics
        prog.printInProgress("Creating Image. . .")
        img = Image.fromarray(arr)
        img.save('outputs/encoded_picture.png', quality=100, subsampling=0)
        prog.printComplete("Encoded Image Created") # Cosmetics
        


# Main ************************************************************************************************************************************


start = time.perf_counter()
if args.progress_all:
    pl = Payload(f"images/{args.Image_Filename}", f"payloads/{args.Payload_Filename}", True, True, True)
else:
    pl = Payload(f"images/{args.Image_Filename}", f"payloads/{args.Payload_Filename}", args.progress_bar, args.fraction, args.percent)
print(f"Extension: {pl.payload_ext}")
if not pl.canFit():
    raise("Not enough space in image to encode payload.")

pl.saveImage(pl.encode())
end = time.perf_counter()
print(f"Took {end-start:.3f} seconds")