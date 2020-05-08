import bitarray as bt
import struct
from enum import Enum
import math
import MD5Buffer as buffer

class Md5:
    def __init__(self):
        self.s = [7, 12, 17, 22, 7, 12, 17, 22,
                  7, 12, 17, 22, 7, 12, 17, 22,
                  5, 9, 14, 20, 5, 9, 14, 20, 5,
                  9, 14, 20, 5, 9, 14, 20, 4, 11,
                  16, 23, 4, 11, 16, 23, 4, 11, 16,
                  23, 4, 11, 16, 23, 6, 10, 15, 21,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10,
                  15, 21]
        
        self.k = [math.floor(pow(2, 32) * abs(math.sin(i + 1))) for i in range(64)]
        
    
    def chunkIt(self, seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0

        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg

        return out

    def padding(self, mesage):
        # Convert the string to a bit array.
        bit_array = bt.bitarray(endian="big")
        bit_array.frombytes(mesage.encode("utf-8"))

        # Pad the string with a 1 bit and as many 0 bits required such that
        # the length of the bit array becomes congruent to 448 modulo 512.
        # Note that padding is always performed, even if the string's bit
        # length is already conguent to 448 modulo 512, which leads to a
        # new 512-bit message block.
        bit_array.append(1)
        while bit_array.length() % 512 != 448:
            bit_array.append(0)

        # For the remainder of the MD5 algorithm, all values are in
        # little endian, so transform the bit array to little endian.
        return bt.bitarray(bit_array, endian="little")

    def extend(self, byte_padded_message, message):
        length = (len(message) * 8) % pow(2, 64)
        length_bit_array = bt.bitarray(endian="little")
        length_bit_array.frombytes(struct.pack("<Q", length))
        
        result = byte_padded_message.copy()
        result.extend(length_bit_array)
        return result

    def calculate_f(self, x, y, z):
        return ( x & y ) | ( ~x & z )

    def calculate_g(self, x, y, z):
        return ( x & z ) | ( y & ~z )

    def calculate_h(self, x, y, z):
        return x ^ y ^ z

    def calculate_i(self, x, y, z):
        return y ^ ( x | ~z )

    def left_rotate(self, x, c):
        return ( x << c ) | ( x >> (32 - c))

    def modular_add(self, a, b):
        return ( a + b ) % pow(2, 32)
    
    def block(self, block):
        words = self.chunkIt(block, 16)
        words = [int.from_bytes(word.tobytes(), byteorder="little") for word in words]
        a = buffer.MD5Buffer.A
        b = buffer.MD5Buffer.B
        c = buffer.MD5Buffer.C
        d = buffer.MD5Buffer.D
        for i in range(64):
            if 0 <= i <= 15:
                F = self.calculate_f(b, c, d)
                g = i
                self.s = [7, 12, 17, 22]
            elif 16 <= i <= 31:
                F = self.calculate_f(d, b, c)
                g = (5*i + 1) % 16
                self.s = [5, 9, 14, 20]
            elif 32 <= i <= 47:
                F = self.calculate_h(b, c, d)
                g = (3*i + 5) % 16
                self.s = [4, 11, 16, 23]
            elif 48 <= i <= 63:
                F = self.calculate_i(b, c, d)
                g = (7*i) % 16
                self.s = [6, 10, 15, 21]


            F = self.modular_add(F, words[g])
            F = self.modular_add(F, self.k[i])
            F = self.modular_add(F, a)
            F = self.left_rotate(F, self.s[i%4])
            F = self.modular_add(F, b)

            a = d
            d = c
            c = b
            b = F

        return a, b, c, d

    def format_result(self, a, b, c, d):
        A = struct.unpack("<I", struct.pack(">I", a))[0]
        B = struct.unpack("<I", struct.pack(">I", b))[0]
        C = struct.unpack("<I", struct.pack(">I", c))[0]
        D = struct.unpack("<I", struct.pack(">I", d))[0]
        return f"{format(A, '08x')}{format(B, '08x')}{format(C, '08x')}{format(D, '08x')}"
        

    def hash(self, mesage):
        treated_mesage = self.extend(self.padding(mesage), mesage)
        n_blocks = len(treated_mesage)//512
        blocks = self.chunkIt(treated_mesage, n_blocks)

        A = buffer.MD5Buffer.A
        B = buffer.MD5Buffer.B
        C = buffer.MD5Buffer.C
        D = buffer.MD5Buffer.D

        for b in blocks:
            a, b, c, d = self.block(b)
            A = self.modular_add(a,A)
            B = self.modular_add(b,B)
            C = self.modular_add(c,C)
            D = self.modular_add(d,D)

        return self.format_result(A, B, C, D)
        

def md5_hash(string: str):
    md5 = Md5()
    return md5.hash(string)



