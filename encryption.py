#Encryption
import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2

def get_private_key(pw):
    salt = b"CIS628 cryptography"
    temp = PBKDF2(pw, salt, 64, 1000)
    pr_key = temp[:32]
    return pr_key

def encrypt(raw, pw):   
    blockSize = 16
    pad = lambda x: x + (blockSize - len(x) % blockSize) * chr(blockSize - len(x) % blockSize)
    pr_key = get_private_key(pw)
    padded = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(pr_key, AES.MODE_CBC, iv)
    encryptedMsg = base64.b64encode(iv + cipher.encrypt(padded))
    return encryptedMsg

def decrypt(encMsg, pw):
    unpad = lambda x: x[:-ord(x[len(x) - 1:])]
    pr_key = get_private_key(pw)
    encMsg = base64.b64decode(encMsg)
    iv = encMsg[:16]
    cipher = AES.new(pr_key, AES.MODE_CBC, iv)
    decryptedMsg = unpad(cipher.decrypt(encMsg[16:]))
    return decryptedMsg