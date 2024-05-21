from PIL import Image
import numpy as np
import math
import sys
import time
import progress
import argparse

# Argument Handling *********************************************************************************************
parser = argparse.ArgumentParser(description="Encode a payload file into an image.")
parser.add_argument('Payload_Filename', type=str)
parser.add_argument('Image_Filename', type=str)
parser.add_argument('-pb', '--progress_bar', action='store_true')           # show Progress Bar
parser.add_argument('-fract', '--fraction', action='store_true')            # show Progress Fraction
parser.add_argument('-perc', '--percent', action='store_true')              # show Progress Percentage
parser.add_argument('-progall', '--progress_all', action='store_true')      # show all Progress Types
args = parser.parse_args()
# ***************************************************************************************************************


class Payload:
    def __init__(self, picture_fn:str, payload_fn:str, pb:bool, fract:bool, perc:bool):
        self.picture_fn = picture_fn                                        # Image Filename
        self.payload_fn = payload_fn                                        # Payload Filename
        self.pb = pb                                                        # show Progress Bar
        self.fract = fract                                                  # show Progress Fraction
        self.perc = perc                                                    # show Progress Percentage
        self.noProgress = (not pb) and (not fract) and (not perc)           # no Progress Visuals
        self.payload_ext = payload_fn.split(".")[-1]                        # Payload File Extension
        self.img = Image.open(picture_fn)                               
        self.maxChars = (self.img.size[0] * self.img.size[1] * 3) - 6       # Maximum amount of chars the image can hold
        self.payload = ""                                                   # Empty string for payload to be appeded to

        # Reading input from payload file.
        with open(payload_fn, 'r', encoding="UTF-8") as f:
            prog = progress.Progress(100)                                   # Instantiating Progress for messages only
            prog.printInProgress("Reading Payload File. . .")               # Progress Message
            for line in f.readlines():
                self.payload += line
            prog.printComplete("Payload File Read.")                        # Progress Completion Message

        self.payload_len = len(self.payload)                                # BEFORE EXTENSION ADDED
        self.payload = self.payload_ext + self.payload + '\n'               # Inserting Payload File Extension to front of payload string

    # Checks if image can hold payload.
    def canFit(self) -> bool:
        return False if len(self.payload) > self.maxChars else True
    
    # Converts length int to an RGB tuple
    def to_base_256(self, n:int):
        result = []
        while n > 0:
            result.append(n % 256)
            n = n // 256
        if len(result) == 1:
            result.append(0)
            result.append(0)
        elif len(result) == 2:
            result.append(0)
        result.reverse()                   # because we need the most significant byte first
        return tuple(result)
    
    # Encode payload into image array
    def encode(self):
        spreadRes = self.img.size[0] * (self.img.size[1] - 1)       # Amount of space in image to work with
        spread = math.floor(spreadRes // (len(self.payload) // 3))  # Number of pixels to move for every encoded pixel


        arr = np.array(self.img)                                    # converts img into an array of pixels
        arr[-1][-1] = self.to_base_256(self.payload_len)            # last RGB value holds the length of the payload (read like a normal num)
        arr[-1][-2] = self.to_base_256(len(self.payload_ext))       # second-to-last RGB value holds the length of the payload extension

        nonASCII = []
        pc = 0                                                                                              # payload counter
        prog = progress.Progress(self.payload_len, "Encoding File ", self.pb, self.fract, self.perc, 30)    # Instantiating Progress Visuals
        for i in range(0, len(arr)):                                                                        # Iterating over rows of pixels
            for j in range(0, len(arr[i]), spread):                                                         # Iterating over each pixel in row
                newArr = [0, 0, 0]                                                                          # Instantiating array to hold encoded pixels
                for k in range(0, len(arr[i][j])):                                                          # Iterating over each "sub-pixel" in a pixel
                    if self.payload[pc] in ["‘", "’"]:                                                      # Checks for special characters outside of ASCII table
                        newArr[k] = int(format(arr[i][j][k], "08b")[:1] + format(ord("'"), "08b")[1:], 2)
                    elif self.payload[pc] in ['“', '”']:                                                    # Checks for special characters outside of ASCII table
                        newArr[k] = int(format(arr[i][j][k], "08b")[:1] + format(ord('"'), "08b")[1:], 2)
                    elif self.payload[pc] in ["—", "–"]:
                        newArr[k] = int(format(arr[i][j][k], "08b")[:1] + format(ord('-'), "08b")[1:], 2)
                    elif ord(self.payload[pc]) > 127:
                        nonASCII.append(self.payload[pc])
                    else:                                                                                   # No special characters found
                        newArr[k] = int(format(arr[i][j][k], "08b")[:1] + format(ord(self.payload[pc]), "08b")[1:], 2)
                    pc += 1                                     # Increment Payload Counter
                    if not self.noProgress:
                        prog.printProgress(pc)                  # Progress Update
                    if pc > len(self.payload)-1:                # If payload counter is bigger than payload length, no more to encode
                        break
                arr[i][j] = tuple(newArr)                       # Convert encoded array into a tuple and replace existing pixel with encoded pixel
                if pc > len(self.payload)-1:                    # Redundancy
                        print(f"The following non-ASCII characters were found in the payload file: {set(nonASCII)}.")
                        if not self.noProgress:
                            prog.printComplete("File Encoded.") # Progress Completion Message
                        return arr                              # return the image array that now contains encoded pixels
        print(f"The following non-ASCII characters were found in the payload file: {set(nonASCII)}.")
        if not self.noProgress:                                 # Redundancy
            prog.printComplete("File Encoded.")                 # Progress Completion Message
        return arr                                              # Redundancy
    
    def saveImage(self, arr):
        prog = progress.Progress(100)                                       # Instantiating Progress for messages only
        prog.printInProgress("Creating Image. . .")                         # Progress Message        
        img = Image.fromarray(arr)                                          # Convert image array to Image object
        img.save('outputs/encoded_picture.png', quality=100, subsampling=0) # save the image
        prog.printComplete("Encoded Image Created.")                         # Progress Completion Message
        


# Main ************************************************************************************************************************************
start = time.perf_counter()
if args.progress_all:   # If show all progress visuals
    pl = Payload(f"images/{args.Image_Filename}", f"payloads/{args.Payload_Filename}", True, True, True)
else: 
    pl = Payload(f"images/{args.Image_Filename}", f"payloads/{args.Payload_Filename}", args.progress_bar, args.fraction, args.percent)

if not pl.canFit():
    raise("Not enough space in image to encode payload.")

pl.saveImage(pl.encode())               # Encoding and Saving New Image
end = time.perf_counter()
print(f"Took {end-start:.3f} seconds")