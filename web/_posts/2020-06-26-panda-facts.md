---
layout: post
title: "panda-facts"
author: "anishbadhri"
tags: ['web']
---

I just found a hate group targeting my favorite animal. Can you try and find their secrets? We gotta take them down!

Site: [panda-facts.2020.redpwnc.tf](panda-facts.2020.redpwnc.tf)

**Files**:
- [index.js]({{site.baseurl}}/assets/panda-facts/index.js)

## Solution

In `index.js` we can see that the token stored in cookie is an encryption of the string formed with
```
const token = `{"integrity":"${INTEGRITY}","member":0,"username":"${username}"}`
```
The `username` in this string is used directly without adding any `\` before special characters to escape them. Thus, can set a `username` which consists of `"` such that member can be set.
A username of `panda","member":"1` would result in the token string as
```
const token = `{"integrity":"12370cc0f387730fb3f273e4d46a94e5","member":0,"username":"panda","member":"1"}`
```
JSON parsers typically consider only the last usage of key which results in `member` being set to 1.
Thus, the flag can now be obtained.

## Flag
```
flag{1_c4nt_f1nd_4_g00d_p4nd4_pun}
```