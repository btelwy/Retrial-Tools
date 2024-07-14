from PIL import Image
import math

#converts a .png into AJ's raw image format, found in cpac2d.bin/subarc-01
#in this format, there is no palette in the file, and no header
#this program assumes that the .png is already compatible with the format, not a random .png

#if true, draws pixels in order of tiles; if false, draws linearly, left to right
drawTilewise = False

mode = input("Draw tilewise (t) or linearly (l)?\n")
assert(mode == "t" or mode == "l")
if (mode == "t"):
    drawTilewise = True
elif (mode == "l"):
    pass




#put name of file to be converted in here
fileName = input("Input filename in:\n")
source = Image.open(fileName)

fileOutName = input("Input filename out:\n")





class paletteObj():
    def __init__(self, palette, name):
        self.palette = palette #tuple of strings attribute
        self.name = name #string attribute




#use palette from subarc-00 at offset 0x1000 in unedited subarc-00 file,
#first color is used as transparent color, so doesn't matter what it is
subarc00Palette = paletteObj(
    ('0000', '1042', '9456', '586B', 'CE10', 'F214', '3519', '4504', 'CA10', '0E19', 'B521',\
        'F825', '5A2E', '9D36', 'FE42', 'C15E'
    ), "subarc00")

#alternatively, for option buttons, this is the palette to use:
optionPalette = paletteObj(
    ('E003', '1863', 'DE7B', 'FF7F', '9D73', '5C6B', '3B63', 'FA5A', 'B84E', '5742', '1532',\
        'B425', '9321', '3111', 'F008', 'AF00'
    ), "option")

#or, (removed E720 from the first element)
trucyPalette = (
    ('0000', 'A610', '2835', 'EF39', '0D56', 'AB49', '6F62', 'FF7B' '356B', 'D32D', '5736', 'EC14', 'FC4A', '9A3E', 'B220', 'DD24'
    ), "Trucy")

presetPalettes = (subarc00Palette, optionPalette, trucyPalette)




palette = None

paletteTypeInput = input("Choose preset palette (p) or custom palette (c)?\n")
assert(paletteTypeInput == "p" or paletteTypeInput == "c")

if (paletteTypeInput == "p"): #use preset
    print(f"The preset palettes are:\n{[preset.name + " | " for preset in presetPalettes]}\n")
    selectedPresetName = input("Enter the name of the palette to use:\n")
    for preset in presetPalettes:
        if (selectedPresetName == preset.name):
            palette = preset.palette

elif (paletteTypeInput == "c"): #use custom
    palette = input("Input custom palette:\n")
    NotImplementedError




paletteRGB = []

for color in palette:
    flippedColor = bytearray.fromhex(color)[::-1] #change endianness of two-byte color
    flippedColor = int(flippedColor.hex(), base=16) #convert it to decimal

    #separate the number into R, G, B
    #each color is then between 0 and 31, so convert to a 0-255 scale
    red = round(((flippedColor & 0b11111) << 0) * (255/31))
    green = round(((flippedColor & 0b1111100000) >> 5) * (255/31))
    blue = round(((flippedColor & 0b111110000000000) >> 10) * (255/31))

    paletteRGB.append((red, green, blue))




width, height = source.size #image dimensions
startWidth, startHeight = 0, 0 #the coordinates to start iterating at for each tile
tilesPerRow = width / 8

pixels = source.load() #get a view object of the pixel color values
currentPixel = ()

tempList = []

buffer = []

with open(fileOutName, "wb") as convertedImage: #create .bin file
    #if drawing tile by tile
    if drawTilewise:
        for tiles in range(0, round(width*height/64)):
            startWidth = (tiles % tilesPerRow) * 8
            startHeight = ((tiles - (tiles % tilesPerRow))/tilesPerRow)*8 #lower to nearest start of row, then multiply by tile height
                
            for y in range (0, 8):
                for x in range (0, 8): #iterate through each tile row to row, top to bottom
                    currentPixel = pixels[startWidth+x, startHeight+y]

                    tempList = list(currentPixel)
                    
                    currentPixel = tuple(tempList)

                    #due to rounding and stuff the current pixel won't exactly match anything in the palette
                    #so use a similarity metric to find the closest match: distance in a 3D plane
                    similarity = math.inf
                    match = 0

                    for index, item in enumerate(paletteRGB):
                        distance = (item[0]-currentPixel[0])**2 + (item[1]-currentPixel[1])**2 + \
                            (item[2]-currentPixel[2])**2
                        distance = math.sqrt(distance)

                        if (distance < similarity):
                            similarity = distance

                            match = index

                            #don't know what bug requires this, but each nybble is one greater than should be
                            if (match > 1):
                                match -= 1

                    buffer.append(match)

                    #write one nybble per pixel by waiting until you have two nybbles to write both at once
                    if (len(buffer) == 2):
                        pixel = hex(buffer[1])[2:] + hex(buffer[0])[2:] #concatenate the two nybbles
                        pixel = int.to_bytes(int(pixel, base=16)) #convert into a bytes object
                        
                        convertedImage.write(pixel)

                        buffer = [] #empty buffer

    #if drawing linearly
    else:
        for y in range(height):
            for x in range(width):
                #really should use a function here to increase readability, but too lazy

                currentPixel = pixels[x, y]
                

                #due to rounding and stuff the current pixel won't exactly match anything in the palette
                #so use a similarity metric to find the closest match: distance in a 3D plane
                similarity = math.inf
                match = 0

                for index, item in enumerate(paletteRGB):
                    distance = (item[0]-currentPixel[0])**2 + (item[1]-currentPixel[1])**2 + \
                        (item[2]-currentPixel[2])**2
                    distance = math.sqrt(distance)

                    if (distance < similarity):
                        similarity = distance

                        match = index

                        #don't know what bug requires this, but each nybble is one greater than should be
                        #if (match > 1):
                            #match -= 1

                buffer.append(match)

                #write one nybble per pixel by waiting until you have two nybbles to write both at once
                if (len(buffer) == 2):
                    pixel = hex(buffer[1])[2:] + hex(buffer[0])[2:] #concatenate the two nybbles
                    pixel = int.to_bytes(int(pixel, base=16)) #convert into a bytes object
                        
                    convertedImage.write(pixel)

                    buffer = [] #empty buffer back to length 0



print("Finished.")