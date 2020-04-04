import bitarray as bt
import struct

from enum import Enum

class MD5Buffer(Enum):
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476

class Md5:
    def __init__(self, mesage):
        self.mesage = mesage
        self.byte_padded_mesage = bt.bitarray(endian="big")
        self.extended_mesage = bt.bitarray(endian="little")
        self.len_mesage = 0

    def padding(self):
        self.byte_padded_mesage.frombytes(self.mesage.encode('utf-8'))
        self.len_mesage = self.byte_padded_mesage.length()
        self.byte_padded_mesage.append(1)

        while (self.byte_padded_mesage.length() % 512 != 448):
            self.byte_padded_mesage.append(0)
        self.byte_padded_mesage = bt.bitarray(self.byte_padded_mesage, endian="little")

    def extend(self):
        lenght_b = bt.bitarray(endian="little")
        lenght_b.frombytes(struct.pack("<Q", self.len_mesage))
        b = len(lenght_b)
        self.extended_mesage = self.byte_padded_mesage
        self.extended_mesage.extend(lenght_b)

        




def main():
    md5 = Md5("oi")
    md5.padding()
    md5.extend()
    print((md5.extended_mesage))
    print(len(md5.extended_mesage))


if __name__ == "__main__":
    main()


