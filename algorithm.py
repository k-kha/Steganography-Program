"""
Explanation of our Algorithm (By Kevin Kha and Tiancheng Dai): 
1.  im=Image.open('image1.png')
    w,h = im.size
2.  a = nthPrime(w)
    b = nthPrime(h)
3.  n = a*b
4.  for i in d:
        if (int(i)%2) == 0: #even
            count0 += 1
            listdict['0'] += 1
        if (int(i)%2) == 1: #odd
            count1 += 1
            listdict['1'] += 1
    return listdict
    #Where list is the dictionary ['0': (occurrences of even), '1': (occurrences of odd), '2': n]
5.  if listdict['0']<2 or listdict['1']<2:
        replaceNum = 0
        listdict['2'] = '01'
    elif listdict['0'] <= listdict['1']:
        replaceNum = 0
    else:
        replaceNum = 1
6.  index = 0
    for i in list:
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
    #Where piclsb is the combination of the picture's 2 LSB and our message being mixed in
"""

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
