import base64

def rc4(data, 
        key = b'default-key', 
        mode = "encode", 
        enfunc=base64.b64encode, 
        defunc=base64.b64decode):
    if mode == "decode": data = defunc(data)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i%len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i, j = 0, 0
    R = []
    for c in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = c ^ (S[(S[i] + S[j]) % 256])
        R.append(t)
    if mode == "encode": return enfunc(bytes(R))
    return bytes(R)

if __name__ == '__main__':
    data  = '123'
    key   = '123'

    print('key:', key)
    print('data:', data)
    
    key = key.encode()
    data = data.encode()
    encd = rc4(data,key,mode='encode');print('rc4 encode:',encd.decode())
    decd = rc4(encd,key,mode='decode');print('rc4 decode:',decd.decode())