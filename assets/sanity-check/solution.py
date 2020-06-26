import base64

f = open("cipher.txt").read()

for _ in range(25):
	f = base64.b64decode(f)

print(f)