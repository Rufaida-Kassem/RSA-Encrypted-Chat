# convert the message into numbers
import random
import math
import sympy

def from_character_conversion(msg):
    # keep 0 -> 9 as it is
    # 0-9 should return their value 0→0, 5→5, 9→9
    # a should map to 10, b to 11, c to 12 etc. up to z→35
    # Space should map to 36
    # any other character should map to 36 like space
    # return the list of numbers
    numbers_list = []
    numbers_list = [ord(c) - 48 if ord(c) in range(48, 58) else ord(c) - 87 if ord(c) in range(97, 123) else 36 for c in msg]
    return numbers_list

# encode the message before encryption
# each 5 characters map to one plaintext value
def encode(numbers_list):
    # Group the plaintext into sets of five characters per group. If the last grouping does not have
    # exactly five characters, then append some space to the end of the plaintext message to fill out
    # the last grouping. Each group must have five characters
    # Here is an example. Assume our plaintext grouping is [hi s7]. First we translate the characters
    # into numbers:
    # c4 = ’h’ = 17
    # c3 = ’i’ = 18
    # c2 = ’ ’ = 36
    # c1 = ’s’ = 28
    # c0 = ’7’ = 7
    # Then we compute the plaintext number:
    # 17 · 37^4 + 18 · 37^3 + 36 · 37^2 + 28 · 37^1 + 7 = 32,822,818
    plain_text = []
    for i in range(0, len(numbers_list), 5):
        if len(numbers_list[i:i+5]) < 5:
            numbers_list.extend([36] * (5 - len(numbers_list[i:i+5])))
        # calculate the plaintext number
        plain_text.append(sum([numbers_list[i+j] * (37 ** (4 - j)) for j in range(5)]))
    return plain_text

# encrypt the message using RSA
# c = m^e mod n
# c is the ciphertext
# m is the plaintext
# e is the public key
# n is the product of two large prime numbers
# return the list of ciphertexts

def encrypt(msg, e, n):
    plain_text = encode(from_character_conversion(msg))
    cipher_text = []
    cipher_text = [pow(m, e, n) for m in plain_text]       
    return cipher_text


# decrypt the message using RSA
def decrypt(cipher_text, d, n):
    plain_text = pow(cipher_text, d, n)
    char_list = to_character_conversion(decode(plain_text))
    return char_list

def decode(plain_text):
    # convert the plaintext number into a list of numbers
    # 32,822,818 = 17 · 37^4 + 18 · 37^3 + 36 · 37^2 + 28 · 37^1 + 7
    # 32,822,818 % 37^4 = 7
    # 32,822,818 % 37^3 = 28
    # 32,822,818 % 37^2 = 36
    # 32,822,818 % 37^1 = 18
    # 32,822,818 % 37^0 = 17
    # use mod and divide to get the numbers
    numbers_list = []
    m = plain_text
    for i in range(4, -1, -1):
        numbers_list.append(m // (37 ** i))
        m = m % (37 ** i)
    
    return numbers_list

# convert the numbers into characters
def to_character_conversion(numbers_list):
    # reverse the from_character_conversion function
    # 0→0, 5→5, 9→9
    # a should map to 10, b to 11, c to 12 etc. up to z→35
    # Space should map to 36
    # any other character should map to 36 like space
    char_list = []
    char_list = [chr(n + 48) if n in range(0, 10) else chr(n + 87) if n in range(10, 36) else ' ' for n in numbers_list]
    # return the list of characters as a string
    return ''.join(char_list)

# calculate the public key and private key
def generate_keys(n_number_of_bits):
    # generate random prime numbers p and q
    p = random_prime(int(math.floor(n_number_of_bits + 1/ 2)))
    q = random_prime(int(math.floor(n_number_of_bits / 2)))
    
    # print("p = ", p)
    # print("q = ", q)
    
    n = p * q
    phi = (p - 1) * (q - 1)

    # print("n = ", n)
    # print("phi = ", phi)
    
    # choose e such that 1 < e < phi and gcd(e, phi) = 1
    # choose e prime and less than phi
    
    e = sympy.randprime(1, phi)
    # print("e = ", e)
    
    
    # d is the modular multiplicative inverse of e mod phi
    d = pow(e, -1, phi)
    # print("d = ", d)
    return e, d, n

# random prime number generator
def random_prime(number_of_bits):
    p = sympy.randprime(2 ** (number_of_bits - 1), 2 ** number_of_bits)
    return p
