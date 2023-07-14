
import tables


def array_to_matrix(array):
    matrix = []
    factor = len(array) // 4
    for i in range(0, len(array), factor):
        matrix.append(list(array[i:i+factor]))
    matrix = transpose(matrix)
    return matrix

def matrix_to_array(matrix):
    array = []
    matrix = transpose(matrix)
    for i in range(len(matrix)):
        array.extend(matrix[i])
    return array

def matrix_to_bytes(matrix):
    b_string = bytes(matrix_to_array(matrix))
    return b_string

def sbox(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = tables.Sbox[matrix[i][j]]

    return matrix

def sbox_array(array):
    for i in range(len(array)):
            array[i] = tables.Sbox[array[i]]

    return array

def inv_sbox(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = tables.Sbox_inv[matrix[i][j]]

    return matrix

def shift_rows(matrix):
    temp_matrix = [[0]*4,[0]*4,[0]*4,[0]*4]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            temp_matrix[i][j] = matrix[i][(j+(i)) % 4]

    return temp_matrix

def inv_shift_rows(matrix):
    temp_matrix = [[0]*4,[0]*4,[0]*4,[0]*4]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            temp_matrix[i][j] = matrix[i][(j+(4-i)) % 4]

    return temp_matrix

def column_extractor(matrix, column_no):
    col = []
    for row in matrix:
        col.append(row[column_no])
    return col

def transpose(matrix):
    mat = []
    for i in range(len(matrix[0])): 
        mat.append(column_extractor(matrix,i))
    return mat

def xor_array(array_a, array_b):
    array_c = []
    for i in range(len(array_a)):
        array_c.append(array_a[i] ^ array_b[i])
    return array_c
        
def xor_matrix(matrix_a, matrix_b):
    matrix_c = []
    for i in range(len(matrix_a)):
        matrix_c.append(xor_array(matrix_a[i], matrix_b[i]))
    return matrix_c

xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def mix_single_column(a):
    # see Sec 4.1.2 in The Design of Rijndael
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)


def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])
    
    return s

def inv_mix_columns(s):
    # see Sec 4.1.3 in The Design of Rijndael
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v

    s = mix_columns(s)
    return s


def rotate_array(array):
    temp = [0]*4
    for i in range(len(array)):
        temp[i] = array[(i+1) % 4]

    return temp

def key_expansion(key, security_parameter):
    if security_parameter == 128:
        rounds = 11
    elif security_parameter == 192:
        rounds = 13
    else :
        rounds = 15

    round_keys = []
    key = array_to_matrix(key)
    round_keys.append(key)
    prev_col = key[len(key[0])-1]
    for i in range(rounds-1):
        round_key = []
        
        prev_col = rotate_array(prev_col)
        prev_col = sbox_array(prev_col)
        prev_col = xor_array(prev_col, [tables.Rcon[i],0,0,0])

        for j in range(security_parameter//32):

            
            round_column = round_keys[i][j]
            xor_column = xor_array(prev_col, round_column)
            round_key.append(xor_column)
            prev_col = xor_column

        round_keys.append(round_key)
    
    return round_keys



def aes_enc(message, key, security_parameter):

    round_keys = key_expansion(key, security_parameter)
    cipher = []
    if security_parameter == 128:
        rounds = 11
    elif security_parameter == 192:
        rounds = 13
    else :
        rounds = 15

    for i in range(rounds):

        if i == 0:
            cipher = xor_matrix(((array_to_matrix(message))), round_keys[i])
        
        elif i==rounds-1:
            
            cipher = sbox(cipher)
            cipher = shift_rows(cipher)            
            cipher = xor_matrix(cipher, (round_keys[i]))
        else:
            
            cipher = sbox(cipher)
            cipher = shift_rows(cipher)
            cipher = mix_columns(cipher)
            cipher = xor_matrix(cipher, (round_keys[i]))
            
    cipher = (cipher)
    cipher = matrix_to_bytes(cipher)
    return cipher

def aes_dec(cipher, key, security_parameter):
    round_keys = key_expansion(key, security_parameter)
    message = []
    if security_parameter == 128:
        rounds = 11
    elif security_parameter == 192:
        rounds = 13
    else :
        rounds = 15

    for i in range(rounds-1,-1,-1):

        if i == rounds-1:
            message = xor_matrix((array_to_matrix(cipher)), round_keys[i])
            message = inv_shift_rows(message)
            message = inv_sbox(message)
            
            
        elif i == 0:
            message = xor_matrix(message, round_keys[i])
        else:
            
            message = xor_matrix(message, round_keys[i])
            message = inv_mix_columns(message)
            message = inv_shift_rows(message)
            message = inv_sbox(message)
            
    message = matrix_to_bytes(message)
    return message

    





# a = b'Thats my Kung Fu'

# c = aes_enc(b'Two One Nine Two', a, 128)
# print(c)

# print(aes_dec(c,a,128))







    
