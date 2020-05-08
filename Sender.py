import Md5
import Email




def check_zeros(bynary_string):
    bynary_string = bin(int(bynary_string, 16))[2:].zfill(128)
    counter = 0
    for bit in bynary_string:
        if bit == "0":
            counter += 1
        if bit == "1":
            break
    return counter

def mine(mesage, target):
    nounce = 0
    block = mesage + str(nounce)
    md5_hash = Md5.md5_hash(block)
    while(check_zeros(md5_hash) <= target):
        nounce += 1
        block = mesage + str(nounce)
        md5_hash = Md5.md5_hash(block)


    return nounce, md5_hash

