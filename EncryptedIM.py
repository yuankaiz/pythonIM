from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
import Crypto

def pad(s):
    return s + (32 - len(s)%32) * chr(32 - len(s)%32)

def unpad(s):
    return s[:-ord(s[-1])]

def toBytes(s):
    return bytearray([ord(c) for c in s])

s = 'helloworld'
CONFKEY = 'CONFKEY'
AUTHKEY = 'AUTHKEY'

padded = pad(s) # pad s

hkey = SHA256.new(toBytes(AUTHKEY)).digest()

hmac = HMAC.new(hkey, msg=padded, digestmod=Crypto.Hash.SHA256) # compute hmac
# print hmac.hexdigest()

h = SHA256.new(toBytes(CONFKEY)) # confkey


from Crypto.Cipher import AES
from Crypto import Random


key = h.digest()
iv = Random.new().read(16)

enc = AES.new(key, AES.MODE_CBC, iv)
cipher = iv + enc.encrypt(hmac.digest() + padded) # cipher -> iv (16) + enc(hmac(32) + padded)

dec = AES.new(key, AES.MODE_CBC, cipher[:16])
plain = dec.decrypt(cipher[16:])

computedhmac = HMAC.new(hkey, msg=plain[32:], digestmod=Crypto.Hash.SHA256) # compute hmac
# print computedhmac.hexdigest()

if hmac.hexdigest() == computedhmac.hexdigest():
    print 'Authenticated'
else:
    print 'Fake'

print len(unpad(plain[32:]))
print unpad(plain[32:])
