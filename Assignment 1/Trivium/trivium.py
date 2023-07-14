
from bitarray import bitarray
from bitstring import Bits
import os


def trivium(key, iv, l):

    a = bitarray(93)
    b = bitarray(84)
    c = bitarray(111)
    a.setall(0)
    b.setall(0)
    c.setall(0)

    if isinstance(key, str): 
        key = Bits(bytes(key, 'utf-8')).bin
        iv = Bits(bytes(iv, 'utf-8')).bin

    elif isinstance(key, bytes): 
        key = Bits(key).bin
        iv = Bits(iv).bin


    for i in range(80):
        a[i] = int(key[i])
        b[i] = int(iv[i])
    

    

    def get_bits(a, b, c, l):
        output = bitarray()
        for i in range(l):

            output_a = a[92] ^ a[65]
            output_b = b[68] ^ b[83]
            output_c = c[110] ^ c[65]

            z = output_a ^ output_b ^ output_c
            output += bitarray(1)
            output[-1] = z
            input_a = output_c ^ a[68] ^ (c[108] and c[109])
            input_b = output_a ^ b[77] ^ (a[91] and a[90])
            input_c = output_b ^ c[86] ^ (b[81] and b[82])

            a = bitarray(1) + a[:92]
            b = bitarray(1) + b[:83]
            c = bitarray(1) + c[:110]

            a[0] = input_a
            b[0] = input_b
            c[0] = input_c
        
        with open(os.path.realpath(__file__) + "output.txt", 'w') as file:
            file.write(output.to01())

        
    get_bits(a, b, c, l)


# trivium(os.urandom(10), os.urandom(10), 1000000)
# output is stored inside the text file created in this folder.