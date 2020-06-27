---
layout: post
title: "12-shades-of-redpwn"
author: "anishbadhri"
tags: ['crypto']
---

Everyone's favorite guess god Tux just sent me a flag that he somehow encrypted with a color wheel!

I don't even know where to start, the wheel looks more like a clock than a cipher... can you help me crack the code?

**Files**:
- [ciphertext.jpg]({{site.baseurl}}/assets/12-shades-of-redpwn/ciphertext.jpg)
- [color-wheel.jpg]({{site.baseurl}}/assets/12-shades-of-redpwn/color-wheel.jpg)

## Solution

If the colors in the color-wheel are assigned numbers 0 to 11 as in a clock, the colors in the ciphertext can be written as number pairs.

Number Pairs: [cipher.txt]({{site.baseurl}}/assets/12-shades-of-redpwn/cipher.txt)

These number pairs can be interpreted as a Base12 number with two digits as each digit allows numbers in the range 0 to 11. Converting the pairs to Base10 returns the flag.

**Solution**
- [solution.py]({{site.baseurl}}/assets/12-shades-of-redpwn/solution.py)

## Flag
```
flag{9u3ss1n9_1s_4n_4rt}
```
