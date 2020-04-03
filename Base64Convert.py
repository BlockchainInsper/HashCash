base64_dict = {
    "A": 0, "B": 1, "C": 2,
    "D": 3, "E": 4, "F": 5,
    "G": 6, "H": 7, "I": 8,
    "J": 9, "K": 10, "L": 11,
    "M": 12, "N": 13, "O": 14,
    "P": 15, "Q": 16, "R": 17,
    "S": 18, "T": 19, "U": 20,
    "V": 21, "W": 22, "X": 23,
    "Y": 24, "Z": 25, "a": 26,
    "b": 27, "c": 28, "d": 29,
    "e": 30, "f": 31, "g": 32,
    "h": 33, "i": 34, "j": 35,
    "k": 36, "l": 37, "m": 38,
    "n": 39, "o": 40, "p": 41,
    "q": 42, "r": 43, "s": 44,
    "t": 45, "u": 46, "v": 47,
    "w": 48, "x": 49, "y": 50,
    "z": 51, "0": 52, "1": 53,
    "2": 54, "3": 55, "4": 56, 
    "5": 57, "6": 58, "7": 59, 
    "8": 60, "9": 61, "+": 62,
    "/": 63,
}

def ConvertTo6BitBlock(message):
    charlist = []
    bit6block = []
    blocks6bits = []

    # --------------------------------------------------------------------------------
    # For each char in the message, transform it to its ASCII value and then
    # transform that ASCII value to its binary 8bit format
    # --------------------------------------------------------------------------------
    count6 = 0
    for character in message:
        charlist.append(format(ord(character), '08b'))

    # --------------------------------------------------------------------------------
    # For each of the binaries made, separate them into blocks of 6bit
    # binaries. If a block does not reach a length of 6 bits, we add 0s
    # until it does. So if we have 11001001, we should end up with: 110010, 010000
    # --------------------------------------------------------------------------------
    for binboy in charlist:
        i = 0
        while i < len(binboy):
            bit6block.append(binboy[i])
            count6 += 1
            i += 1
            if(count6 >= 6):
                blocks6bits.append(''.join(bit6block))
                bit6block = []
                count6 = 0
    
    if len(bit6block) > 0:
        while len(bit6block) < 6:
            bit6block.append('0')
        blocks6bits.append(''.join(bit6block))

    # --------------------------------------------------------------------------------
    # Since Base64 separates data into 6 bit blocks and recieves data in 8 bit format,
    # every 3 characters in the unencoded input, we recieve 4 encoded characters.
    # That means that if the unencoded input isn't a multiple of 3, the encoded blocks
    # will also not be a multiple of 4. The strategy used to calculate the needed padding
    # for the output is simple: 
    # We see how many 6 bit blocks we formed, if it isn't a multiple of 4, we add paddings
    # equal to the number of blocks it needs to be a multiple of four
    # For exmaple: We have 9 6bit blocks. So 9%4 = 1. That means we have 1 block out of the
    # needed 4, so we simply add 4 - 1 paddings.
    # --------------------------------------------------------------------------------
    if (len(blocks6bits)%4 != 0):
        PadsToAdd = 4 - len(blocks6bits)%4
    else:
        PadsToAdd = 0

    return blocks6bits, PadsToAdd

def ConvertToBase64(Message):

    BlocksOfBits, PadsToAdd = ConvertTo6BitBlock(Message)

    Converted = []

    # --------------------------------------------------------------------------------
    # After making the 6bit blocks, we simply transform each block to their decimal
    # representation, and then we transform that decimal to its base64 value, as per the
    # dictionary: base64_dict
    # --------------------------------------------------------------------------------
    for i in range(len(BlocksOfBits)):
        for key, value in base64_dict.items():
            if int(BlocksOfBits[i],2) == value:
                Converted.append(key)

    # --------------------------------------------------------------------------------
    # Join all the characters in the list, and add the needed paddings to the end and we
    # have our message encoded in Base64.
    # --------------------------------------------------------------------------------
    return (''.join(Converted) + PadsToAdd*'=')
    
message = input("Input message to convert: ")

print(ConvertToBase64(message))