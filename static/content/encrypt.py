import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

password_provided = "123" # This is input in the form of a string
password = password_provided.encode() # Convert to type bytes
salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once

#message="3-18".encode()
#f = Fernet(key)
#encrypted = f.encrypt(message)

#f = Fernet(key)
#decrypted = f.decrypt(encrypted)

#filename='data.txt'
#fp=open(filename,"a")
#fp.write('\n'+str(encrypted))
#fp.close()
    
filename1='data.txt'
fp1=open(filename1,"rb")
rr = fp1.readlines()
fp1.close()
enc = rr[1].strip()
##enc=b'gAAAAABdznTzi_QnaVRNGnsVfDsIh8oeHC2m4vs1ukzsS08mzbjMw3auYso-7Azzc0Ajczo7q-eL8d9u_1Qd0Qo9jG1fWKQhuA=='
##print(enc)
#f = Fernet(key)
#decrypted = f.decrypt(enc)
#print(decrypted)

