    # -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 01:40:12 2020

@author: Tiancheng Dai and Kevin Kha
"""
#pip3 install cryptography
from PIL import Image
import numpy as np
import sys

#Encryption
import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2

from algorithm import isPrime
from algorithm import nthPrime
from algorithm import getMod
from decode import decToBin
from decode import get2LSB
from decode import filter2LSB

# 1111111111 Encoding 1111111111
# returns the bytes needed from picture in binary
def bytesNeededBin(bytes_needed, pixels_bin): 
    pic_binary = []
    count = bytes_needed
    for i in pixels_bin:
        for j in i:
            for k in j:
                if count > 0:
                    #print(k)
                    count = count - 1
                    pic_binary.append(k)
    return (pic_binary)

# returns the bytes needed from picture in decimal
def bytesNeededDec(data, bytes_needed): 
    counter = 0
    pic_dec = []
    for x in data:
        for y in x:
            for z in y:
                if counter < bytes_needed:
                    pic_dec.append(z)
                    counter = counter + 1
    return (pic_dec)

#returns the individual message characters to 8-bit binary
def msgBinary(msg):
    msg_binary = []
    for i in msg:
        msg_binary.append(f'{ord(i):08b}') #adds it all to this list
    return (msg_binary)

#returns the split up (individually) of 8-bit binary of message
def msgLSB(msg_binary):
    #print(msg_binary)
    msg_lsb = []
    for i in msg_binary:
        for j in i:
            #print(j, end='')
            msg_lsb.append(int(j))
    return (msg_lsb)

# modifying 2 LSB, adding the message to the picture's 2 LSB
def mod2LSB(listdict, pic_binary, msg_lsb):
    first6 = []
    place7 = []
    place8 = []
    piclsb = []
    replaceNum = 0
    index = 0
    count = 0
    count2 = 0
    pixelsList = []
    pixelsListStr = ''
    
    for i in pic_binary:
        first6.append(i[:6])
        piclsb.append(i[6:8])
        
    for i in piclsb:
        for j in i:
            pixelsList.append(j)

    #the lower even or odd occurence gets replaced
    if listdict['0']<2 or listdict['1']<2:
        replaceNum = 0
        listdict['2'] = '01'
    elif listdict['0'] <= listdict['1']:
        replaceNum = 0
    else:
        replaceNum = 1
    #print(listdict)
    
    #replaces the digit
    for i in pixelsList:
        if int(listdict['2'][index])%2 == replaceNum:
            pixelsList[count] = msg_lsb[count2]
            pixelsListStr += str(pixelsList[count])
            count += 1
            count2 += 1
            index += 1
            if index >= len(listdict['2']):
                index = 0
        else: 
            pixelsListStr += str(pixelsList[count])
            count += 1
            index += 1
            if index >= len(listdict['2']):
                index = 0
    #print(pixelsListStr)
    for i in pixelsListStr:
        pixelsList.append(i)
    #print(pixelsList)
    
    #adding first 6 bits of picture with new 2 bits
    for i in pixelsList[::2]: 
        place7.append(str(i))
        for j in pixelsList[1::2]:
            place8.append(str(j))
            #last2.append(str(j) + str(msg_lsb[msg_lsb.index(j)+1]))
    return ([x+y+z for x,y,z in zip(first6,place7,place8)])

#convert binary to decimal
def binToDec(binlist):
    zipped8_dec = []
    for i in binlist:
        zipped8_dec.append(int(i,2)) 
    return (zipped8_dec)

# Puts all of the new decimal (RGB values) to a list
def newPixels(bytes_needed, m, zipped8_dec):
    new_pix = []
    new_pix2 = []
    count = bytes_needed
    count2 = 0
    less2 = 0
    for i in m:
        for j in i:
            for k in j:
                if (count >= 0) and (count2 < len(zipped8_dec)) and less2 < 3:
                    new_pix.append(zipped8_dec[count2])
                    count = count - 1
                    count2 = count2 + 1
                    if less2 == 2 or count == 0:
                        new_pix2.extend(new_pix)
                        new_pix.clear()
                    if less2 == 2:
                        less2 = 0
                    else: 
                        less2 = less2 + 1
    new_pix3 = np.array(new_pix2)
    return (new_pix3)

# Adds all of the new decimal (RGB values) to new image
def finalImage(data, new_pix, bytes_needed):
    final = new_pix
    counter = 0
    for i in data:
                for j in i:
                    for k in j:
                        if counter >= bytes_needed:
                            final = np.append(final,k)
                        counter = counter + 1
    #if data2.size < bytes_needed:
    #    print("Message has too much data, Input a bigger picture!")
    final = final.reshape(data.shape)
    return final
# 1111111111 Encoding end 1111111111

# 3333333333 Algorithm Implementation 3333333333
def isPrime(n):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    for i in range(2, n):
        if n % i == 0:
            return False
    return True
    
def nthPrime(n):
    count = 0
    num = 2
    if n < 1: return 
    #if n == 1: return 2
    while True:
        if isPrime(num):
            count += 1
            if count == n:
                return num
        num += 1
        
def getMod(w, h):
    a = nthPrime(w) 
    b = nthPrime(h)
    c = a*b
    #print(c)
    d = str(c)
    
    list = dict();
    list['0'] = 0
    list['1'] = 0
    list['2'] = d
    count0 = 0
    count1 = 0
    for i in d:
        if (int(i)%2) == 0: #even
            count0 += 1
            list['0'] += 1
        if (int(i)%2) == 1: #odd
            count1 += 1
            list['1'] += 1
    return list
# 3333333333 Algorithm Implementation end 3333333333
    
# 4444444444 Encryption 4444444444
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
# 4444444444 Encryption end 4444444444
          
def encoding(data, listdict, bytes_needed, pixels_bin, msg):             
    a = bytesNeededBin(bytes_needed, pixels_bin) #picture in 8bit binary: ['11111111', ...]
    c = msgBinary(msg) #message in 8 bit binary
    d = msgLSB(c) #list individual binary: [0,1,...]
    e = mod2LSB(listdict, a, d) # list 8bit binary: ['11111101', ...]
    f = binToDec(e) #list of binary above to dec
    h = newPixels(bytes_needed, data, f) #adds the decimal to list
    i = finalImage(data, h, bytes_needed) #the list turns into the RGB image values
    im2 = Image.fromarray((i).astype(np.uint8))
    im2.save("Secret_Image.png")

    print("Encoding Success!")
    return 
 
def decoding(data, listdict, bytes_needed, pixels_bin, pw):
#def decoding(data, listdict, bytes_needed, pixels_bin):   
    b = bytesNeededDec(data, bytes_needed)#picture in dec: ['255', ...]
    c = decToBin(b) #picture from dec to 8-bit binary
    d = get2LSB(c) #gets the 2 LSB from the list above
    e = filter2LSB(listdict, d)
    f = ''.join(map(str,[str(x) for x in e])) 
    g = [f[i:i+8] for i in range(0, len(f), 8)] 
    h = binToDec(g)
    i = [chr(x) for x in h]
    
    print("The secret message is:")
    j = ''.join(map(str,[str(x) for x in i]))
    #print(j) #this line is for no encryption

    # Encryption:
    k = j.encode("utf-8")  
    l = decrypt(k,pw)
    print(bytes.decode(l))
    return
    
def main(): 
    args = len(sys.argv)
    argPlace = sys.argv
    pw = "CIS628 Syracuse University"
    
    # Encoding
    if args == 4 and argPlace[1] == "-e":
        print("Encoding:")
        file = open(argPlace[2], "r")
        msg = file.read()
        im = Image.open(argPlace[3])
        im = im.convert('RGB')
        
        #Encryption:
        w, h = im.size
        sz = (w*h*3)/4
        data = np.array(im)
        encMsg = (encrypt(msg, pw))
        secMsg = encMsg.decode("utf-8")
        
        listdict = getMod(w, h)
        #bytes_needed = (len(secMsg) * 4)
        bytes_needed = (len(secMsg) * 2 * len(listdict['2']))
        pixels_bin = [[[f'{x:08b}' for x in y] for y in z] for z in data] # all picture pixel values in binary
        
        if len(msg) > sz:
            print("Encoding failed!")
            print("Picture is too small to contain the message.")
            print("Pick a larger image.")
        else: 
            # encoding(data, bytes_needed, pixels_bin, msg) # for no encryption
            encoding(data, listdict, bytes_needed, pixels_bin, secMsg)
        file.close()
        
    # Decoding
    if args == 4 and argPlace[1] == "-d":
        print("Decoding:")
        file = open(argPlace[2], "r")
        msg = file.read()
        
        im = Image.open(argPlace[3])
        im = im.convert('RGB')
        w, h = im.size
        data = np.array(im)
        encMsg = (encrypt(msg, pw))
        secMsg = encMsg.decode("utf-8")
        listdict = getMod(w, h)
        #bytes_needed = (len(secMsg) * 4)
        bytes_needed = (len(secMsg) * 2 * len(listdict['2']))
        pixels_bin = [[[f'{x:08b}' for x in y] for y in z] for z in data]
        #decoding(data, bytes_needed, pixels_bin) #for no encryption
        decoding(data, listdict, bytes_needed, pixels_bin, pw)
        file.close()
        
    if args != 4:
        print("Wrong arguments entered.")
    
    
if __name__ == "__main__":
    main()
