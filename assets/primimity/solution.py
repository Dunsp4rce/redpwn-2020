from mod import Mod

def nth_root(x, n):
    upper_bound = 1
    while upper_bound ** n <= x:
        upper_bound *= 2
    lower_bound = upper_bound // 2
    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound) // 2
        mid_nth = mid ** n
        if lower_bound < mid and mid_nth < x:
            lower_bound = mid
        elif upper_bound > mid and mid_nth > x:
            upper_bound = mid
        else:
            return mid
    return mid + 1

file = open("primimity-public-key.txt").read().split('\n')

N = int(file[0].split()[1])
e = int(file[1].split()[1])
c = int(file[2].split()[1])

n_cube_root = nth_root(N, 3)

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