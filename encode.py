from PIL import Image
import numpy as np
import sys

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