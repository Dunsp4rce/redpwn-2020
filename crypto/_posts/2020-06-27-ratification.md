---
layout: post
title: "ratification"
author: "raghul-rajasekar"
---

Proclamation on ratification of redpwnCTF.

`nc 2020.redpwnc.tf 31752`

**Files:**
- [server.py]({{site.baseurl}}/assets/ratification/server.py)

## Solution

`server.py` contains the following code:

```python
#!/usr/bin/env python3
import numpy as np
from Crypto.Util.number import *
from random import randint

flag = open('flag.txt','rb').read()

p = getPrime(1024)
q = getPrime(1024)
n = p*q
e = 65537

message = bytes_to_long(b'redpwnCTF is a cybersecurity competition hosted by the redpwn CTF team.')

def menu():
    print()
    print('[1] Sign')
    print('[2] Verify')
    print('[3] Exit')
    return input()

print(p)

while True:
	choice = menu()

	if choice == '1':
		msg = bytes_to_long(input('Message: ').encode())
		if msg == message:
			print('Invalid message!')
			continue

		n1 = [randint(0,11) for _ in range(29)]
		n2 = [randint(0,2**(max(p.bit_length(),q.bit_length())-11)-1) for _ in range(29)]
		a = sum(n1[i]*n2[i] for i in range(29))

		enc = [pow(msg,i,n) for i in n2]
		P = np.prod(list(map(lambda x,y: pow(x,y,p),enc,n1)))
		Q = np.prod(list(map(lambda x,y: pow(x,y,q),enc,n1)))
		
		b = inverse(e,(p-1)*(q-1))-a
		sig1 = b%(p-1)+randint(0,q-2)*(p-1)
		sig2 = b%(q-1)+randint(0,p-2)*(q-1)
		print(sig1,sig2)
		
		sp = pow(msg,sig1,n)*P%p
		sq = pow(msg,sig2,n)*Q%q
		s = (q*inverse(q,p)*sp + p*inverse(p,q)*sq) % n

		print(s)
		print("Signed!")

	elif choice == '2':
		try:
			msg = bytes_to_long(input('Message: ').encode())
			sig = int(input('Signature: '))
			if pow(sig,e,n) == msg:
				print("Verified!")
				if msg == message:
					print("Here's your flag: {}".format(flag))
			else:
				print("ERROR HAS OCCURRED...")
		except:
			print("Invalid signature!")

	elif choice == '3':
		print("Good bye!")
		break
```

While the code may seem quite convoluted, this appears to be closest to [RSA signing using CRT](https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Using_the_Chinese_remainder_algorithm). The information we have is the value of `e`, `p`, `sig1` and `sig2`. We can send multiple queries to get multiple values of `sig1` and `sig2` as well. `sig1` is an integer congruent to `d - a` modulo `p-1`, where `d` is the inverse of `e` modulo `(p-1)(q-1)` and `a` is basically a randomly chosen integer (which is calculated from the `n1` and `n2` arrays in a slightly convoluted way). We note that since `p-1` divides `(p-1)(q-1)`, `d` is congruent to the inverse of `e` modulo `p-1`.

From how `a` is calculated, it is clear that it is orders of magnitude smaller than `p` and `q`. As we can calculate the inverse of `e` modulo `p-1` (let's call this value `dp`), we can find the value of `a` as `a = dp - sig1` (Note that since `a` is relatively small, it is likely that equality holds and not just congruence). Adding `a` to `sig2` gives us a value which is congruent to the inverse of `e` modulo `q-1` (let's call this value `dq`). That is, `a + sig2 = dq + k1(q-1)`, where k1 is the result of the `randint(0, p-2)` call.

If we make more queries, we can find more values of the type `dq + k(q-1)`. To find `q-1` and hence `q` from these values, we can take the `gcd` of the difference between all such pairs of values. I arrived at the correct value of `q` after just 3-4 queries. Once we know `q`, we can now calculate `d` and then the signature for `message = 
bytes_to_long(b'redpwnCTF is a cybersecurity competition hosted by the redpwn CTF team.')` as `signature = pow(message, d, p*q)`. Sending this to the server will give us the flag.

## Flag

`flag{random_flags_are_secure-2504b7e69c65676367aef1d9658821030011f8968a640b504d320846ab5d5029b}`
