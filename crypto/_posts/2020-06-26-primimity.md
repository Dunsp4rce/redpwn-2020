---
layout: post
title: "primimity"
author: "Anonymous"
tags: ['crypto']
---

People claim that RSA with two 1024-bit primes is secure. But I trust no one. That's why I use three 1024-bit primes.

I even created my own prime generator to be extra cautious!

**Files**
- [primimity.py]({{site.baseurl}}/assets/primimity/primimity.py)
- [primimity-public-key.txt]({{site.baseurl}}/assets/primimity/primimity-public-key.txt)

## Solution

It can be seen that in the prime number generator, the three primes generated `p`, `q` and `r` are generated such that 

- `p < q < r` 
- If `p` is the `i`<sup>th</sup> prime, then `q` is atmost the `(i + 256)`<sup>th</sup> prime and `r` is atmost the `(i + 512)`<sup>th</sup> prime.

From this, it can be inferred that the difference between two primes is small. We can also infer the same with multiple runs of the generator program.

Using this inference, N can be factorized easily into p, q and r.
Since `N = p * q * r` and `p < q < r`, p < N<sup>1/3</sup>, q < r

Solution: [solution.py]({{site.baseurl}}/assets/primimity/solution.py)

## Flag
```
flag{pr1m3_pr0x1m1ty_c4n_b3_v3ry_d4ng3r0u5}
```