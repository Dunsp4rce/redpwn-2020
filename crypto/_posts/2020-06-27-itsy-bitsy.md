---
layout: post
title: "itsy-bitsy"
author: "raghul-rajasekar"
---

The itsy-bitsy spider climbed up the water spout...
`nc 2020.redpwnc.tf 31284`

**Files:**
- [itsy-bitsy.py]({{site.baseurl}}/assets/itsy-bitsy/itsy-bitsy.py)

# Solution

`itsy-bitsy.py` contains the following code:
```python
#!/usr/bin/env python3

from Crypto.Random.random import randint

def str_to_bits(s):
    bit_str = ''
    for c in s:
        i = ord(c)
        bit_str += bin(i)[2:]
    return bit_str

def recv_input():
    i = input('Enter an integer i such that i > 0: ')
    j = input('Enter an integer j such that j > i > 0: ')
    try:
        i = int(i)
        j = int(j)
        if i <= 0 or j <= i:
            raise Exception
    except:
        print('Error! You must adhere to the restrictions!')
        exit()
    return i,j

def generate_random_bits(lower_bound, upper_bound, number_of_bits):
    bit_str = ''
    while len(bit_str) < number_of_bits:
        r = randint(lower_bound, upper_bound)
        bit_str += bin(r)[2:]
    return bit_str[:number_of_bits]

def bit_str_xor(bit_str_1, bit_str_2):
    xor_res = ''
    for i in range(len(bit_str_1)):
        bit_1 = bit_str_1[i]
        bit_2 = bit_str_2[i]
        xor_res += str(int(bit_1) ^ int(bit_2))
    return xor_res

def main():
    with open('flag.txt','r') as f:
        flag = f.read()
    for c in flag:
        i = ord(c)
        assert i in range(2**6,2**7)
    flag_bits = str_to_bits(flag)
    i,j = recv_input()
    lb = 2**i
    ub = 2**j - 1
    n = len(flag_bits)
    random_bits = generate_random_bits(lb,ub,n)
    encrypted_bits = bit_str_xor(flag_bits,random_bits)
    print(f'Ciphertext: {encrypted_bits}')

if __name__ == '__main__':
    main()
```

The gist of it is that the flag is being XORed with a seemingly "random" set of bits and printed in binary form. Of course, the problem would be unsolvable if truly random bits were used, so let's take a closer look at how these "random" bits are generated. They appear to be a concatenation of the binary forms of random integers chosen between $2^i$ and $2^j - 1$, where $i$ and $j$ are chosen by us as input such that $0 < i < j$, implying that $1 < 2^i < 2^j$. 

We can make a couple of observations:
- The MSB for each concatenated binary string is always 1.
- If $j = i+1$, each random integer is chosen from $[2^i, 2^{i+1} - 1]$, meaning that each integer will surely have a bit length of $i+1$ bytes.

From this, we can devise a method to find out what the bit at the $k^{th}$ position (0-indexed) of the flag is:
- Give $i = k-1$ and $j = k$ as input to the program.
- As each integer chosen to form the random set of bits is of bit length $k$, the MSB of the second integer chosen would be at position $k$ and would be equal to 1 for sure.
- Thus, the bit at the $k^{th}$ position of the flag would have surely been XORed with 1 and would therefore be equal to the negation of the bit at the $k^{th}$ position of the ciphertext.

This can be repeated for all $k$ to finally reveal the flag, which is done by the code below:
```python
from pwn import remote
ans = '11'
for i in range(2, 301): 
    p = remote('2020.redpwnc.tf', 31284) 
    p.read() 
    p.write(f'{i-1}\n') 
    p.read() 
    p.write(f'{i}\n') 
    ret1 = p.read() 
    ret = ret1[12:313] 
    ans += chr(ret[i] ^ 1) 
    p.close()
print(''.join([chr(int(ans[i:i+7], 2)) for i in range(0, 301, 7)]))
```
>Note: Unfortunately, this method can't be used to find the bit at index 1 of the flag. I assumed the bit would be 1 as the flag format was `flag{?*}`.

# Flag

`flag{bits_leaking_out_down_the_water_spout}`
