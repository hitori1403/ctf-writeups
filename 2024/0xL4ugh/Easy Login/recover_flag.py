# tags: easy, rc4

from base64 import b64decode

aaaaa_passwd = bytes.fromhex("a83fac4d8a93d57432a959a2540f7fd042d90a2b6dddcd44cfda19")
key = bytes([c ^ 97 for c in aaaaa_passwd])

enc = b64decode("pDG/SbSehGM2l16sRzFmxRDZNCti2PNXzY9Z")

for i, j in zip(enc, key):
    print(chr(i ^ j), end="")
