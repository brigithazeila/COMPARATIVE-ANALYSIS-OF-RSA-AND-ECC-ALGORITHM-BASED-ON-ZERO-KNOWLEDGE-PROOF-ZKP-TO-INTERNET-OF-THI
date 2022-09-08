from socket import *
from threading import Thread
from noknow.core import ZK, ZKSignature, ZKParameters, ZKData, ZKProof
from queue import Queue
from datetime import datetime

from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
import random
import time
import sys

def generate_keys():
    key = generate_eth_key()

    privKey = key.to_hex()
    pubKey = key.public_key.to_hex()
    with open('ecc_key/pubkey.pem', 'w') as f:
        f.write(pubKey)

    with open('ecc_key/privkey.pem', 'w') as f:
        f.write(privKey)

def load_keys():
    with open('ecc_key/pubkey.pem', 'r') as f:
        pubKey = f.read()

    with open('ecc_key/privkey.pem', 'r') as f:
        privKey = f.read()

    return pubKey, privKey

def encryptText(msg, key):
    return encrypt(key, msg.encode('ascii'))

pubKey, privKey = load_keys()

host = 'localhost'
# host = gethostbyname(gethostname())
port = 42001
address = (host, port)

count_argv = 1
if len(sys.argv) > 1:
    count_argv = int(sys.argv[1])

loop_count = 0
for i in range(count_argv): 
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(address)

    msg = str(random.randint(0, 1000))
    ciphertext = encryptText(msg, pubKey)

    print(msg)

    loop_count = i + 1
    client.send(bytes(ciphertext))

print("\n----------------------------------------------")
print(loop_count, " packages sent")