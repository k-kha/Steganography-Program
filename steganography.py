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
    picTo8BitBinary = bytesNeededBin(bytes_needed, pixels_bin) #picture in 8bit binary: ['11111111', ...]
    msgTo8BitBinary = msgBinary(msg) #message in 8 bit binary
    split8BitBinary = msgLSB(msgTo8BitBinary) #list individual binary: [0,1,...]
    msgIn2LSB = mod2LSB(listdict, picTo8BitBinary, split8BitBinary) # list 8bit binary: ['11111101', ...]
    LSBtoDec = binToDec(msgIn2LSB) #list of binary above to dec
    newDecToList = newPixels(bytes_needed, data, LSBtoDec) #adds the decimal to list
    rgbValues = finalImage(data, newDecToList, bytes_needed) #the list turns into the RGB image values
    secretImg = Image.fromarray((rgbValues).astype(np.uint8))
    secretImg.save("Secret_Image.png")

    print("Encoding Success!")
    return 
 
def decoding(data, listdict, bytes_needed, pixels_bin, pw):
#def decoding(data, listdict, bytes_needed, pixels_bin):   
    picToDec = bytesNeededDec(data, bytes_needed)#picture in dec: ['255', ...]
    picToBin = decToBin(picToDec) #picture from dec to 8-bit binary
    pic2Lsb = get2LSB(picToBin) #gets the 2 LSB from the list above
    get2Lsb = filter2LSB(listdict, pic2Lsb)
    combineLsb = ''.join(map(str,[str(x) for x in get2Lsb])) 
    newPic2Lsb = [combineLsb[i:i+8] for i in range(0, len(combineLsb), 8)] 
    newPicDec = binToDec(newPic2Lsb)
    getChar = [chr(x) for x in newPicDec]
    
    print("The secret message is:")
    secretMsg = ''.join(map(str,[str(x) for x in getChar]))
    #print(j) #this line is for no encryption

    # Encryption:
    encodedMsg = secretMsg.encode("utf-8")  
    finalMsg = decrypt(encodedMsg,pw)
    print(bytes.decode(finalMsg))
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
