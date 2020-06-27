---
layout: post
title: "cookie-recipes-v2"
author: "shreyas-sriram"
---

I want to buy some of these recipes, but they are awfully expensive. Can you take a look?

Site: `cookie-recipes-v2.2020.redpwnc.tf`

## Files
* [index.js]({{site.baseurl}}/assets/cookie-recipes-v2/index.js)

# Solution

> Note : This solution is unintended.

* Source code reveals that the value of the **flag** is got from `.env` file
* The application contains a path traversal vulnerability
* Exploiting this, we can get the required file `.env`<br/>

URL  :  `https://cookie-recipes-v2.2020.redpwnc.tf/css/../../.env`
* Find the **flag** in the file<br/>
`flag{n0_m0r3_gu3551ng}`

> Note : There are more than one ways to solve a problem.
