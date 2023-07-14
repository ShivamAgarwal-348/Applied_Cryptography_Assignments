
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

def triadPB(a, b, c):

    a, b, c, z = triadUpdate(a, b, c, 1)

    for i in range(1,1024):
        a, b, c, z = triadUpdate(a, b, c, 0)
    
    return a, b, c

    
    
def triadEncrypt(key, nonce, message):

    cipher = triadSC(key, nonce, message)
    return cipher

def triadDecrypt(key, nonce, cipher):

    message = triadSC(key, nonce, cipher)
    return message

def triadHash(key, nonce, message):
    a = bitarray(80)
    b = bitarray(88)
    c = bitarray(88)
    a.setall(0)
    b.setall(0)
    c.setall(0)
    
    hash = bitarray(256)
    hash.setall(0)

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

    B1 = "{0:08b}".format(int("b7e151628ae", 16))
    B2 = "{0:08b}".format(int("243f6a8885a", 16))
    B2 = "00" + B2

    for i in range(44):
        b[i] = int(B1[i])

    for i in range(44):
        b[i + 44] = int(B2[i])

    pad = 32 - len(message) % 32

    if pad != 0:
        message += "1"
        for i in range(pad - 1):
            message += "0"

    hlen = len(message) // 32

    for i in range(hlen):
        for j in range(32):
            a[j] = a[j] ^ int(message[i*32 + j])
        a, b, c = triadP(a, b, c)

    for i in range(10):
        for j in range(8):
            hash[120 - (8*i) + j] = a[(i*8) + j]

    for i in range(6):
        for j in range(8):
            hash[40 - (8*i) + j] = b[(i*8) + j]

    a, b, c = triadP(a, b, c)

    for i in range(10):
        for j in range(8):
            hash[248 - (8*i) + j] = a[(i*8) + j]

    for i in range(6):
        for j in range(8):
            hash[168 - (8*i) + j] = b[(i*8) + j]

    return hash.tobytes()

def triadMac(key, nonce, message, associated_data):
    a = bitarray(80)
    b = bitarray(88)
    c = bitarray(88)
    a.setall(0)
    b.setall(0)
    c.setall(0)
    
    mac = bitarray(64)
    mac.setall(0)

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

    if isinstance(associated_data, str): 
        associated_data = Bits(bytes(associated_data, 'utf-8')).bin

    elif isinstance(associated_data, bytes):
        associated_data = Bits(associated_data).bin

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

    a, b, c = triadPB(a, b, c)

    adlen = len(associated_data) // 8
    mlen = len(message) // 8

    for i in range(adlen + 7):
        _a = _A(associated_data, i)

        for j in range(7, -1, -1):
            a, b, c, z = triadUpdate(a, b, c, int(_a[j]))

    for i in range(mlen):
        for j in range(7, -1, -1):
            a, b, c, z = triadUpdate(a, b, c, int(message[(i*8) + j]))

    a, b, c = triadPB(a, b, c)

    for i in range(8):
        for j in range(7, -1, -1):
            a, b, c, mac[(i*8) + j] = triadUpdate(a, b, c, 0)

    return mac.tobytes()   


def _A(associated_data, i):

    adlen = len(associated_data) // 8
    if i>=0 and i<adlen:
        return associated_data[i*8:i*8 +8]

    else:
        j = i - adlen
        _a = (adlen >> (j*8)) & 255
        _a = '{:08b}'.format(_a)
        return _a


k = "abcdabcdabcdabcd"
n = "abcdabcdabcd"

m = "qwe323rw3erw3er2w4effvdfvdbf"
a = "sdsdf344444444444434t3fg234234g3g4g34t34g34g34g34t3g335g45g45334t34rwef"

# v = triadEncrypt(k, n, m)
# print(v)
# print(triadDecrypt(k, n, v))
print(triadHash(k, n, m))
print(triadMac(k, n, m, a))
