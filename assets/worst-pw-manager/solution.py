from os import listdir
from os.path import isfile, join
import string

files = [f[:-4] for f in listdir("passwords/") if isfile(join("passwords/", f))]

arr = []
for filename in files:
	(idx, tmpplain) = filename.split('_')
	idx = int(idx)
	plain = "".join([chr((((c - ord("0") - i) % 10) + ord("0")) * int(chr(c) not in string.ascii_lowercase) + (((c - ord("a") - i) % 26) + ord("a")) * int(chr(c) in string.ascii_lowercase)) for c, i in zip([ord(a) for a in tmpplain], range(0xffff))])
	cipher = open("passwords/"+filename+".enc", "rb").read()
	arr.append((idx, plain, cipher))	

arr.sort(key = lambda x:x[0])

def rc4(text, key): # definitely not stolen from stackoverflow
    S = [i for i in range(256)]
    j = 0
    out = bytearray()

    #KSA Phase
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i] , S[j] = S[j] , S[i]

    #PRGA Phase
    i = j = 0
    for char in text:
        i = ( i + 1 ) % 256
        j = ( j + S[i] ) % 256
        S[i] , S[j] = S[j] , S[i]
        out.append(ord(char) ^ S[(S[i] + S[j]) % 256])

    return out

# Set to 129 initially
flag_len = 43
flag = [' '] * flag_len

for cur in arr:
	for i in range(256):
		if rc4(cur[1], [i] * 8) == cur[2]:
			flag[(cur[0]*8 + 7) % flag_len] = chr(i)
			break


print("".join(flag))