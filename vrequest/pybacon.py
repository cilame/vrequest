def bacon_enc(string,a='a',b='b',ver='v1'):
    if ver == 'v1':
        maps = {
            'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa', 'F': 'aabab', 
            'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaab', 'K': 'ababa', 'L': 'ababb', 
            'M': 'abbaa', 'N': 'abbab', 'O': 'abbba', 'P': 'abbbb', 'Q': 'baaaa', 'R': 'baaab', 
            'S': 'baaba', 'T': 'baabb', 'U': 'babaa', 'V': 'babab', 'W': 'babba', 'X': 'babbb', 
            'Y': 'bbaaa', 'Z': 'bbaab'
        }
    elif ver == 'v2':
        maps = {
            "A":"aaaaa", "G":"aabba", "N":"abbaa", "T":"baaba", "B":"aaaab", "H":"aabbb",
            "O":"abbab", "C":"aaaba", "P":"abbba", "W":"babaa",
            "D":"aaabb", "K":"abaab", "Q":"abbbb", "X":"babab", "E":"aabaa", "L":"ababa",
            "R":"baaaa", "Y":"babba", "F":"aabab", "M":"ababb", "S":"baaab", "Z":"babbb",
            "U":"baabb", "V":"baabb", # "U-V":"baabb"
            "I":"abaaa", "J":"abaaa", # "I-J":"abaaa"
        }
    r = []
    for i in string.upper():
        if i in maps:
            r.append(maps.get(i).replace('a', a).replace('b', b))
        else:
            r.append('[unfind:{}]'.format(i))
    return ' '.join(r)

def bacon_dec(string,a='a',b='b',ver='v1'):
    if ver == 'v1':
        maps = {
            'aaaaa': 'A', 'aaaab': 'B', 'aaaba': 'C', 'aaabb': 'D', 'aabaa': 'E', 'aabab': 'F', 
            'aabba': 'G', 'aabbb': 'H', 'abaaa': 'I', 'abaab': 'J', 'ababa': 'K', 'ababb': 'L', 
            'abbaa': 'M', 'abbab': 'N', 'abbba': 'O', 'abbbb': 'P', 'baaaa': 'Q', 'baaab': 'R', 
            'baaba': 'S', 'baabb': 'T', 'babaa': 'U', 'babab': 'V', 'babba': 'W', 'babbb': 'X', 
            'bbaaa': 'Y', 'bbaab': 'Z'
        }
    elif ver == 'v2':
        maps = {
            "aaaaa":"A", "aabba":"G", "abbaa":"N", "baaba":"T", "aaaab":"B", 
            "aabbb":"H", "abbab":"O", "baabb":"U-V", "aaaba":"C", "abaaa":"I-J", 
            "abbba":"P", "babaa":"W", "aaabb":"D", "abaab":"K", "abbbb":"Q", 
            "babab":"X", "aabaa":"E", "ababa":"L", "baaaa":"R", "babba":"Y", 
            "aabab":"F", "ababb":"M", "baaab":"S", "babbb":"Z", 
        }
    r = []
    _string = string.replace(a, 'a').replace(b, 'b')
    for i in _string.split():
        if i.lower() in maps:
            r.append(maps.get(i.lower())[-1]) # v2 模式统统使用最后一个字符解密
        else:
            r.append('[unfind:{}]'.format(i))
    return ''.join(r)

def bacon_v1_enc(string,a='a',b='b'): return bacon_enc(string,a=a,b=b,ver='v1')
def bacon_v2_enc(string,a='a',b='b'): return bacon_enc(string,a=a,b=b,ver='v2')
def bacon_v1_dec(string,a='a',b='b'): return bacon_dec(string,a=a,b=b,ver='v1')
def bacon_v2_dec(string,a='a',b='b'): return bacon_dec(string,a=a,b=b,ver='v2')

if __name__ == '__main__':
    s = 'lkasjdklfjalsdf'
    s = bacon_v1_enc(s)
    print(s)
    s = bacon_v1_dec(s)
    print(s)
    s = 'lkasjdklfjalsdf'
    s = bacon_v2_enc(s)
    print(s)
    s = bacon_v2_dec(s)
    print(s)