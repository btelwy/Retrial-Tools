assert("RGB" == 'RGB')
class colorObj:
    def __init__(self, color, isTransparent=None):
        self.color = color #string attribute
        self.isTransparent = isTransparent #optional boolean attribute


def reverseEndianness(str):
    return str[2: ] + str[ :2]

def convertBGRA5551ToRGB(BGRA5551Str):
    #form of BGRA5551Str is e.g. ABCD
    BGRA5551Int = int(reverseEndianness(BGRA5551Str), base=16)

    isTransparent = False
    if (BGRA5551Int & 0b1000000000000000 != 0): #the alpha bit is the most significant one
        isTransparent = True

    binaryString = bin(BGRA5551Int)[2: ] #remove "0b" prefix

    if (len(binaryString) == 16):
        binaryString = binaryString[1: ] #take off the alpha bit
    while len(binaryString) < 15:
        binaryString += '0' #make sure each item in the list is 15 digits long

    RGBStr = ""

    for color in range(0, 3): #cycle through blue, green, red
        correspondingBit = 15 - 5 * color
        componentStr = binaryString[correspondingBit - 5:correspondingBit] #select corresponding five bits
        valueOutOf31 = int(componentStr, base=2)
        valueOutOf255 = round(valueOutOf31 * 255/31)
        
        RGBStr += str(valueOutOf255) + ' '

    return colorObj(RGBStr, isTransparent)


def convertRGBToBGRA5551(RGBStr):
    #form of RGBStr is e.g. 255,255,255 or 17,53,112
    RGBComponents = RGBStr.split(',')
    assert(len(RGBComponents) == 3)

    binaryString = "0b0"
    for component in range(2, -1, -1):
        valueOutOf255 = int(RGBComponents[component])
        valueOutOf31 = round(valueOutOf255 * 31/255)
        binaryComponent = bin(valueOutOf31)[2: ] #remove the "0b" prefix
        
        while (len(binaryComponent) < 5):
            binaryComponent += '0' #ensures each string is five digits long

        binaryString += binaryComponent

    hexStringPrefixed = hex(int(binaryString, base=2)) #convert to decimal int to convert to hex string
    hexString = hexStringPrefixed[2: ]

    while (len(hexString) < 4): #hex string must be four bytes
        hexString += '0'

    return colorObj(reverseEndianness(hexString))


colorType = input("Input RGB or BGRA5551 color?\n")
assert(colorType == "RGB" or colorType == "BGRA" or colorType == "BGRA5551")

if (colorType == "BGRA" or colorType == "BGRA5551"):
    colorInput = input("Input one or more BGRA5551 colors of form ABCD separated by spaces:\n").split(' ')
    for color in colorInput:
        conversion = convertBGRA5551ToRGB(color)
        print(f"Conversion: {conversion.color}-- transparent: {conversion.isTransparent}")

elif (colorType == "RGB"):
    colorInput = input("Input one or more RGB colors of form 255,255,255 separated by spaces:\n").split(' ')
    for color in colorInput:
        conversion = convertRGBToBGRA5551(color)
        print(f"Conversion: {conversion.color}")