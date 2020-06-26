import re

f1 = open("gdbdump.txt","r")

c = 0
l = []

print("from z3 import *")
print("s = Solver()")
while True:
    line = f1.readline()
    if not line:
        break
    p = re.compile("0x(.*)\(")
    v1 = p.findall(line)[0]
    line = f1.readline()
    p = re.compile("0x(.*)\(")
    v2 = p.findall(line)[0]
    line = f1.readline()
    line = f1.readline()
    p = re.compile("j.e")

    if v1 not in l:
        l.append(v1)
        print("var" + v1 + " = Int(\'" + "var" + v1 +"\')")
        if(v1 != "11c" and v1 != "d8"):
            print("s.add(var" + v1 + " >= 97)")
            print("s.add(var" + v1 + " <= 122)")
        
    if v2 not in l:
        l.append(v2)
        print("var" + v2 + " = Int(\'" + "var" + v2 +"\')")
        if(v2 != "11c" and v2 != "d8"):
            print("s.add(var" + v2 + " >= 97)")
            print("s.add(var" + v2 + " <= 122)")

    if p.findall(line)[0] == "jae":
        print("s.add(var" + v1 + " < " + "var" + v2 + ")")
    else:
        print("s.add(var" + v1 + " > " + "var" + v2 + ")")
print("ans = \'\'")
print("print(s.check())")
print("model = s.model()")
print("print(model)")
print("for i in model:")
print("\tmodel_map[str(i)] = chr(int(str(model[i])))")
for i in l:
    print("ans += model_map[\'var" + i + "\']")
print("print(ans)")