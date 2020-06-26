---
layout: post
title: "SMarT-solver"
author: "vishalananth"
---

Find the correct flag. :)

NOTE: All letters in the flag are lowercase

**Files**
- [SMarT-solver]({{site.baseurl}}/assets/SMarT-solver/SMarT-solver)

## Solution

We are given an ELF 64-bit executable file. Opening it with IDA causes IDA Graph view to crash because of the enormous
code size, we have almost 25k lines of assembly code in  main itself. Analyzing this code, we see that there are
73 variables(var_11F to var_D8 and s) declared and the input string is checked if it has length >=73. 
```
.text:0000000000000917                 call    _strlen
.text:000000000000091C                 cmp     rax, 48h
```

All this helps us realize that the length of the input should 73. Also towards the end there is a check to see if all our characters are in lowercase
and if the last letter is "}".

```
.text:000000000001B97B                 cmp     [rbp+var_125], 7Dh ; '}'
```

Seeing this we confirm that the input we have to give is indeed the flag.

On closer observation, we see that the program compares every 2 indices in the input string we give against a condition.
For example:

```
.text:0000000000000926                 movzx   edx, [rbp+s]
.text:000000000000092D                 movzx   eax, [rbp+var_11F]
.text:0000000000000934                 cmp     dl, al
.text:0000000000000936                 jnb     loc_1B9C8

This is just input[0] < input[1]

.text:000000000000093C                 movzx   edx, [rbp+s]
.text:0000000000000943                 movzx   eax, [rbp+var_11E]
.text:000000000000094A                 cmp     dl, al
.text:000000000000094C                 jbe     loc_1B9CE

Which is input[0] > input[2]
...
....
```

So if we can find a string which follows all these 73*72(a few conditions were not there :P) constrains we can find our flag. When we see the question,
we notice that the words SMT are capitalised. That is one more clue that an SMT solver should be used to solve for these for constrains and get the flag.

So we write a python script([genZ3.py]({{site.baseurl}}/assets/SMarT-solver/genZ3.py)) that goes through the assembly, parses the conditions and changes that into python Z3 code.
Sample Conversion:

**Objdump:**
```
926:	0f b6 95 e0 fe ff ff 	movzbl -0x120(%rbp),%edx
92d:	0f b6 85 e1 fe ff ff 	movzbl -0x11f(%rbp),%eax
934:	38 c2                	cmp    %al,%dl
936:	0f 83 8c b0 01 00    	jae    1b9c8 <main+0x1b16e>
93c:	0f b6 95 e0 fe ff ff 	movzbl -0x120(%rbp),%edx
943:	0f b6 85 e2 fe ff ff 	movzbl -0x11e(%rbp),%eax
94a:	38 c2                	cmp    %al,%dl
94c:	0f 86 7c b0 01 00    	jbe    1b9ce <main+0x1b174>
```
**Equivalent Python Z3 Code:**
```
from z3 import *
s = Solver()
var120 = Int('var120') # Declare and Initiliaze the variable the first time we encounter it
s.add(var120 >= 97) # lowercase lowerlimit condition
s.add(var120 <= 122) # lowercase upperlimit condition
var11f = Int('var11f')
s.add(var11f >= 97)
s.add(var11f <= 122)
s.add(var120 < var11f) # First jae statement
var11e = Int('var11e')
s.add(var11e >= 97)
s.add(var11e <= 122)
s.add(var120 > var11e) # Second jbe statement
```

Similarly we can parse all the assembly jump conditions, and generate the full Z3 code([equationsolver.py]({{site.baseurl}}/assets/SMarT-solver/equationsolver.py)). Running this code gets us the solution that satisfy all the equations.
Converting the integers to char and appending them in the right position gives us the flag.
