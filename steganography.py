"""
@author: Tiancheng Dai and Kevin Kha
"""
#pip3 install cryptography
from PIL import Image
import numpy as np
import sys

from algorithm import isPrime
from algorithm import nthPrime
from algorithm import getMod
from encryption import get_private_key
from encryption import encrypt
from encryption import decrypt
from decode import decToBin
from decode import get2LSB
from decode import filter2LSB
from encode import bytesNeededBin
from encode import bytesNeededDec
from encode import msgBinary
from encode import msgLSB
from encode import mod2LSB
from encode import binToDec
from encode import newPixels
from encode import finalImage
          
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
