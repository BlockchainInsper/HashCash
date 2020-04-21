import bitarray as bt
import struct
from enum import Enum
import math






class MD5Buffer():
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476

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
        self.k = []
        for i in range(64):
            self.k.append(math.floor(232*abs(math.sin(i+1))))
        
    
    def chunkIt(self, seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0

        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg

        return out

    def padding(self, mesage):
        byte_padded_mesage = bt.bitarray(endian="big")
        byte_padded_mesage.frombytes(mesage.encode('utf-8'))
        byte_padded_mesage.append(1)

        while (byte_padded_mesage.length() % 512 != 448):
            byte_padded_mesage.append(0)
        byte_padded_mesage = bt.bitarray(byte_padded_mesage, endian="little")

        return byte_padded_mesage

    def extend(self, byte_padded_mesage):
        extended_mesage = bt.bitarray(endian="little")
        lenght_b = bt.bitarray(endian="little")
        lenght_b.frombytes(struct.pack("<Q", byte_padded_mesage.length()))
        b = len(lenght_b)
        extended_mesage = byte_padded_mesage
        extended_mesage.extend(lenght_b)

        return extended_mesage

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
        a = MD5Buffer.A
        b = MD5Buffer.B
        c = MD5Buffer.C
        d = MD5Buffer.D
        for i in range(64):
            if 0 <= i <= 15:
                F = self.calculate_f(b, c, d)
                g = i
            elif 16 <= i <= 31:
                F = self.calculate_f(d, b, c)
                g = (5*i + 1) % 16
            elif 32 <= i <= 47:
                F = self.calculate_h(b, c, d)
                g = (3*i + 5) % 16
            elif 48 <= i <= 63:
                F = self.calculate_i(c, b, d)
                g = (7*i) % 16


            F = self.modular_add(F, words[g])
            F = self.modular_add(F, self.k[i])
            F = self.modular_add(F, a)
            F = self.left_rotate(F, self.s[i])
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
        treated_mesage = self.extend(self.padding(mesage))
        n_blocks = len(treated_mesage)/512
        blocks = self.chunkIt(treated_mesage, n_blocks)

        A = MD5Buffer.A
        B = MD5Buffer.B
        C = MD5Buffer.C
        D = MD5Buffer.D

        for b in blocks:
            a, b, c, d = self.block(b)
            A = self.modular_add(a,A)
            B = self.modular_add(b,B)
            C = self.modular_add(c,C)
            D = self.modular_add(d,D)

        return self.format_result(A, B, C, D)
        





        




def main():
    md5 = Md5()
    print(md5.hash("adwdaa"))


if __name__ == "__main__":
    main()


