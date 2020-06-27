---
layout: post
title: "worst-pw-manager"
author: "anishbadhri"
tags: ['crypto']
---

I found this in-progress password manager on a dead company's website. Seems neat.

**Files**
- [worst-pw-manager]({{site.baseurl}}/assets/worst-pw-manager/worst-pw-manager.zip)

## Solution

### Obtaining Plaintexts and Ciphertexts

The first step would be to obtain the plaintext-ciphertext pairs for each password. The plaintext is masked as filename and the ciphertext is the contents of that file.

The list-comprehension for `masked_file_name` encrypts the cipher such that for a character in the `i`<sup>th</sup> index of the original text
- The value will be increased by `i` and wrapped to stay within `'0'-'9'` if `password[i]` is an integer
- The value will be increased by `i` and wrapped to stay within `'a'-'z'` if `password[i]` is an alphabet

Thus, to decrypt, it would be sufficient to subtract by `i` for each position to get the orignal plaintext back.

Thus a tuple of index, plain-text and cipher-text would be obtained from the list of files.

### Finding key for encoding

This part is a bit tricky and needs understanding of the `generate-key` and `take` function. On running separately for multiple cases, it is observed that the key each time would a string of length 8 consisting of just one character in all 8 places.

Furthermore, the chosen character from the flag would be the dependent on the iteration number such that the index of the chosen character is `8 * iteration_numer + 7`.

That is, the file with index 0 would be generated with key as the character from 7<sup>th</sup> index of the flag, index 1 generated with key as character from 15<sup>th</sup> index of the flag.

For each file, every character can be checked against the plaintext to check if it produces the desired ciphertext.

### Length of flag

The string obtained from the previous step would result in a lot of empty spaces. This is because the length of the flag has not be accounted for yet. If it is accounted for, the chosen character's position would be `(8 * iteration_number + 7) % length_of_flag`.

After a few observations, it is seen that the file with index `i` and index `i + 129` have the same key for all indices. Thus, the length of flag is atmost 129.

When running the script with the length as 129, the flag is printed thrice and thus the flag is obtained. The original flag's length is 43.

**Program**
- [solution.py]({{site.baseurl}}/assets/worst-pw-manager/solution.py)

## Flag
```
flag{crypto_is_stupid_and_python_is_stupid}
```
