---
layout: post
title: "coffer-overflow-0"
author: "raghul-rajasekar"
---

Can you fill up the coffers? We even managed to find the source for you.
`nc 2020.redpwnc.tf 31199`

**Files:**
- [coffer-overflow-0]({{site.baseurl}}/assets/coffer-overflow-0/coffer-overflow-0)
- [coffer-overflow-0.c]({{site.baseurl}}/assets/coffer-overflow-0/coffer-overflow-0.c)

## Solution

The source file contains the following code:

```
#include <stdio.h>
#include <string.h>

int main(void)
{
  long code = 0;
  char name[16];
  
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  puts("Welcome to coffer overflow, where our coffers are overfilling with bytes ;)");
  puts("What do you want to fill your coffer with?");

  gets(name);

  if(code != 0) {
    system("/bin/sh");
  }
}
```

It's clear that we just have to change the value of `code` somehow to get shell access. Since buffer overflow from `name` will leak into `code` first, any suitably-sized input (I used the input `ABCDABCDABCDABCDABCDABCDABCD` of length 28 bytes) would grant shell access.

## Flag

`flag{b0ffer_0verf10w_3asy_as_123}`

