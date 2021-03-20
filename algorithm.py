
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