---
layout: post
title: "secret-flag"
author: "raghul-rajasekar"
---

There's a super secret flag in printf that allows you to LEAK the data at an address??
`nc 2020.redpwnc.tf 31826`

**Files:**
- [secret-flag]({{site.baseurl}}/assets/secret-flag/secret-flag)

## Solution

Sadly, there's no source file provided with this question, so let's take a look at the disassembly of `secret-flag` using IDA:

![secret-flag disassembly]({{site.baseurl}}/assets/secret-flag/secret-flag.png)

From the beginning and end of the disassembly, we can see that a canary is being set, so buffer overflow will be a lot harder to pull off. However, we can make a few interesting observations:
- The flag is being read from `flag.txt` and stored in a buffer pointed to by `[rbp - 0x28]`
- The input received from the user is directly printed to the screen using `printf`

The second observation means that we have a format string vulnerability! Any format specifiers we provide in our input will be processed by `printf` thus enabling us to leak the stack. But that's not all! If there's an address to a buffer on the stack, we can use the `%s` format specifier suitably to print the string contained within that buffer, which is exactly what we need here to print the flag!

Now, all we need to do is find the exact offset from `rsp` at which the pointer to the buffer containing the flag is located. For this, we note that `rbp = rsp + 0x30` (because of the instruction `sub rsp, 30h` at the beginning of the `main` function). Combining that with our knowledge that the required pointer is stored at `rbp - 0x28`, we conclude that the pointer is at `rsp + 0x30 - 0x28 = rsp + 0x8`, basically making it the 7<sup>th</sup> argument to `printf` (the first 5 arguments are in registers `rsi`, `rdx`, `rcx`, `r8` and `r9` while the remaining arguments are taken from the stack, starting at the top).

So how can we use this information? The format string `%n$s` will print the string pointed to by the n<sup>th</sup> argument to `printf`. Thus, by giving `%7$s` as the input, we get the flag.

## Flag

`flag{n0t_s0_s3cr3t_f1ag_n0w}`
