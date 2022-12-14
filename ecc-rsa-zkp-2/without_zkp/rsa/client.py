from itertools import count
from socket import *
from threading import Thread
from noknow.core import ZK, ZKSignature, ZKParameters, ZKData, ZKProof
from getpass import getpass
from queue import Queue
from datetime import datetime

import rsa 
import random
import time
import sys

def generate_keys():
    (pubKey, privKey) = rsa.newkeys(3072)
    with open('rsa_key/pubkey.pem', 'wb') as f:
        f.write(pubKey.save_pkcs1('PEM'))

    with open('rsa_key/privkey.pem', 'wb') as f:
        f.write(privKey.save_pkcs1('PEM'))

def load_keys():
    with open('rsa_key/pubkey.pem', 'rb') as f:
        pubKey = rsa.PublicKey.load_pkcs1(f.read())

    with open('rsa_key/privkey.pem', 'rb') as f:
        privKey = rsa.PrivateKey.load_pkcs1(f.read())

    return pubKey, privKey

def encrypt(msg, key):
    return rsa.encrypt(msg.encode('ascii'), key)

pubKey, privKey = load_keys()

host = 'localhost'
# host = gethostbyname(gethostname())
port = 42000
address = (host, port)

count_argv = 1
if len(sys.argv) > 1:
    count_argv = int(sys.argv[1])

loop_count = 0
for i in range(count_argv): 
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(address)

    msg = str(random.randint(0, 1000))
    ciphertext = encrypt(msg, pubKey)
    now = str(datetime.now().timestamp())

    print(msg)

    loop_count = i + 1
    client.send(bytes(ciphertext))

print("\n----------------------------------------------")
print(loop_count, " packages sent")