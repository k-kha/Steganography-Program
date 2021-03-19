# 2222222222 Decoding 2222222222
#converts the pixel bytes to binary
def decToBin(dec):
    secret_bin = []
    for i in dec:
        secret_bin.append(f'{i:08b}')
    return secret_bin

#gets the last 2 LSB of each byte
def get2LSB(secret_bin): 
    last2 = []
    for i in secret_bin: 
        for j in i[6:8]:
            last2.append(j)
    return last2

def filter2LSB(listdict, last2):
    piclsb = []
    replaceNum = 0
    index = 0

    #the lower even or odd occurence gets replaced
    if listdict['0']<2 or listdict['1']<2:
        replaceNum = 0
        listdict['2'] = '01'
    elif listdict['0'] <= listdict['1']:
        replaceNum = 0
    else:
        replaceNum = 1

    #filters the right matching bits out of the image
    for i in last2:
        if int(listdict['2'][index])%2 == replaceNum:
            piclsb.append(i)
            index += 1
            if index >= len(listdict['2']):
                index = 0
        else: 
            index += 1
            if index >= len(listdict['2']):
                index = 0
    return piclsb
# 2222222222 Decoding end 2222222222