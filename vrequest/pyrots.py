def rot5(string):
    s = '0123456789'
    r = []
    for i in string:
        if i in s:
            v = s[(s.index(i)+len(s)//2)% len(s)]
        else:
            v = i
        r.append(v)
    return ''.join(r)

def rot13(string):
    s = 'abcdefghijklmnopqrstuvwxyz'
    u = s.upper()
    r = []
    for i in string:
        if i in s:
            v = s[(s.index(i)+len(s)//2)% len(s)]
        elif i in u:
            v = u[(u.index(i)+len(u)//2)% len(u)]
        else:
            v = i
        r.append(v)
    return ''.join(r)

def rot18(string):
    s = '0123456789abcdefghijklmnopqrstuvwxyz'
    u = s.upper()
    r = []
    for i in string:
        if i in s:
            v = s[(s.index(i)+len(s)//2)% len(s)]
        elif i in u:
            v = u[(u.index(i)+len(u)//2)% len(u)]
        else:
            v = i
        r.append(v)
    return ''.join(r)

def rot47(string):
    s = list(range(33,127))
    r = []
    for i in string.encode():
        if i in s:
            v = s[(s.index(i)+len(s)//2)% len(s)]
        else:
            v = i
        r.append(v)
    return bytes(r).decode()


if __name__ == '__main__':
    s = 'nihaoaxiongdi1234567890_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    s = rot5(s); print('enc>',s)
    s = rot5(s); print('dec=',s)
    s = rot13(s); print('enc>',s)
    s = rot13(s); print('dec=',s)
    s = rot18(s); print('enc>',s)
    s = rot18(s); print('dec=',s) # 注意，加密数据若存在数字，则逆运算的大小将无法全部还原
    s = rot47(s); print('enc>',s)
    s = rot47(s); print('dec=',s) # 注意，加密数据若存在数字，则逆运算的大小将无法全部还原
    print()