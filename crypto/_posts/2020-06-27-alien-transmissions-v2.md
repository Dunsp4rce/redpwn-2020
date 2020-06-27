---
layout: post
title: "alien-transmissions-v2"
author: "raghul-rajasekar"
---

The aliens are at it again! We've discovered that their communications are in base 512 and have transcribed them in base 10. However, it seems like they used XOR encryption twice with two different keys! We do have some information:

-   This alien language consists of words delimitated by the character represented as 481
-   The two keys appear to be of length 21 and 19
-   The value of each character in these keys does not exceed 255

Find these two keys for me; concatenate their ASCII encodings and wrap it in the flag format.

**Files:**
- [encrypted.txt]({{site.baseurl}}/assets/alien-transmissions-v2/encrypted.txt)

# Solution

From the question, it's clear that the character corresponding to 481 must occur in the plaintext with much higher frequency than the other characters. Since the ciphertext has been XORed with both `key1` and `key2` (which are the first and second halves of the flag respectively), we have the relation `ciphertext[i] = plaintext[i] ^ key1[i%21] ^ key2[i%19]`. Thus, for positions separated by a multiple of `21 * 19 = 399`, the plaintext is XORed with the same value (`key1[i%21] ^ key2[i%19]`) there. We can create 399 frequency tables this way based on the value of `i%399`. The character occurring the most for each value of `i%399` must be the encrypted value of the character 481.

Based on this, we can find all values of `481 ^ key1[i] ^ key2[j]` for `0 ≤ i ≤ 20` and `0 ≤ j ≤ 18`, from which we can find all the corresponding values of `key1[i] ^ key2[j]`. However, to find the flag from this, we'll have to guess some character using brute-force. I brute-forced the value of `key1[0]` and got all the values in `key2`, from which I could easily get `key1`.
`key1 = h3r3'5_th3_f1r5t_h4lf`
`key2 = _th3_53c0nd_15_th15`

# Flag

`flag{h3r3'5_th3_f1r5t_h4lf_th3_53c0nd_15_th15}`
