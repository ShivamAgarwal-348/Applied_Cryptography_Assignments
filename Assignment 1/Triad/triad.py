
from bitarray import bitarray
from bitstring import Bits
import os


def triadSC(key, nonce, message):

    a = bitarray(80)
    b = bitarray(88)
    c = bitarray(88)
    a.setall(0)
    b.setall(0)
    c.setall(0)
    
    cipher = bitarray()

    if isinstance(key, str): 
        key = Bits(bytes(key, 'utf-8')).bin
        nonce = Bits(bytes(nonce, 'utf-8')).bin

    elif isinstance(key, bytes): 
        key = Bits(key).bin
        nonce = Bits(nonce).bin
        
    if isinstance(message, str): 
        message = Bits(bytes(message, 'utf-8')).bin

    elif isinstance(message, bytes):
        message = Bits(message).bin

    


    for i in range(0, 80, 16):
        for j in range(8):
            a[8+i+j] = int(key[32-i+j])
    
    for j in range(8):
        a[j] = int(nonce[j])

    for i in range(16, 80, 16):
        for j in range(8):
            a[i+j] = 1

    a[71] = 0
        
    for i in range(0, 88, 8):
        for j in range(8):
            b[i+j] = int(nonce[88-i+j])
            c[i+j] = int(key[120-i+j])

    a, b, c = triadP(a, b, c)

    for i in range(len(message)//8):
        c_array = bitarray(8)
        c_array.setall(0)
        for j in range(7, -1, -1):
            a, b, c, z = triadUpdate(a, b, c, 0)

            c_array[j] = z ^ int(message[i*8 +j])

        cipher += c_array

    return cipher.tobytes()


    

def triadUpdate(a, b, c, msg):

    output_a = a[67] ^ a[79] ^ (b[84] and c[84])
    output_b = b[63] ^ b[87]
    output_c = c[67] ^ c[87]

    z = output_a ^ output_b ^ output_c

    input_a = output_c ^ a[73] ^ (c[76] and c[86]) ^ msg
    input_b = output_a ^ b[65] ^ (a[72] and a[78]) ^ msg
    input_c = output_b ^ c[83] ^ (b[64] and b[86]) ^ msg

    a = bitarray(1) + a[:79]
    b = bitarray(1) + b[:87]
    c = bitarray(1) + c[:87]

    a[0] = input_a
    b[0] = input_b
    c[0] = input_c

    return a, b, c, z

def triadP(a, b, c):

    for i in range(1024):
        a, b, c, z = triadUpdate(a, b, c, 0)
    
    return a, b, c

    
    
def triadEncrypt(key, nonce, message):

    cipher = triadSC(key, nonce, message)
    return cipher

def triadDecrypt(key, nonce, cipher):

    message = triadSC(key, nonce, cipher)
    return message


# k = "abcdabcdabcdabcd"
# n = "abcdabcdabcd"

# m = "qwe323rwerwerweffvdfvdbf"

# v = triadEncrypt(k, n, m)
# print(v)
# print(triadDecrypt(k, n, v))
