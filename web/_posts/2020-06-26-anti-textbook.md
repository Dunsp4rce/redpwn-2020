---
layout: post
title: "anti-textbook"
author: "vishalananth"
---

It's important for public keys to be transparent.

Hint: certificate-transparency.org

**Files**
- [data.txt]({{site.baseurl}}/assets/anti-textbook/data.txt)

## Solution

We are given a data.txt file which contains, the modulus(n) and the exponent(e) for RSA.
Looking at the hint and previous writeups, we understand that we have to create a public-key with this and search in crt.sh to
get more details about the website which might potentially have the flag.

So, we form the [def.asn1]({{site.baseurl}}/assets/anti-textbook/def.asn1) file required to get the publickey, we use OpenSSL to generate the public key as follows:

```
openssl asn1parse -genconf def.asn1 -out pubkey.der -noout

openssl rsa -in pubkey.der -inform der -pubin -out pubkey.pem
```

Opening the pubkey.pem, we get this

```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuffuWhYrpTW8cdcAWUwe
T8oZYCp/8pKPYj4eZ3pd7mhYoCkSSeqZ5e+L33O38SoMANogM1NBayYlumOcPxC/
C9PHMF6AlaLDH+yX/Fg+a055m0O7+5pJNUVuRn9z7aYhhubnRyjk2cVTHLmOHqK9
FPM1QBBdouddMgZYE6plaBdBIMwQ8txuZQs6t862zJfA0/cgT47TtiTNkouHkAuT
VXBPcbM5pXIu7MoflJrUjQ0ljuOIFgXQ7wCFusXrIpvuVpqLzRvTD69GA7Cj0Dt9
ij7KPrBFM2jFyR8vnm5w+T6sGafXgJEEj0sLmbIReWcNeyHC2Tl9OniyMEqPeLsZ
oQIDAQAB
-----END PUBLIC KEY-----
```

Now we tried the advanced filter in crt.sh and found a SHA256(SubjectPublicKeyInfo) there. So generated our digest using OpenSSL as follows:

```
openssl rsa -in pubkey.pem -pubin -outform der | openssl dgst -sha256
```

We got the digest and on searching we got 2 certificates, both of which contained a link in the Subject -> Common Name.
Opening the link gave us the flag.
