from mod import Mod
import gmpy2

file = open("primimity-public-key.txt").read().split('\n')

N = int(file[0].split()[1])
e = int(file[1].split()[1])
c = int(file[2].split()[1])

n_cube_root = int(gmpy2.iroot(N, 3)[0])

p = -1
q = -1
r = -1

for i in range(n_cube_root, 1, -1):
	if N % i == 0:
		p = i
		break

for i in range(p+1, N):
	if N % i == 0:
		if q == -1:
			q = i
		else:
			r = i
			break

phi = (p-1) * (q-1) * (r-1)
e_mod = Mod(e, phi)
d = Mod(int(1 // e_mod), N)

ciph_long = int(c ** d)
print(bytes.fromhex(hex(ciph_long)[2:]).decode("utf-8"))