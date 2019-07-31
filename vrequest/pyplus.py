import html
import urllib.parse

import re


def bitstring_to_base_8(bitstring, encoding='utf-8'):
    return ''.join([oct(i).replace('0o','\\o') for i in bitstring])

def base_8_to_bitstring(string, encoding='utf-8'):
    func = lambda i: int(i, 8)
    return bytes(list(map(func, re.findall('[0-7]{1,3}',string)))).decode(encoding)

def bitstring_to_base_10(bitstring, encoding='utf-8'):
    return ''.join(['\\'+str(i) for i in bitstring])

def base_10_to_bitstring(string, encoding='utf-8'):
    return bytes(list(map(int, re.findall('[0-9]{1,3}',string)))).decode(encoding)

def bitstring_to_base_16(bitstring, encoding='utf-8'):
    return ''.join([hex(i).replace('0x','\\x') for i in bitstring])

def base_16_to_bitstring(string, encoding='utf-8'):
    func = lambda i: int(i, 16)
    return bytes(list(map(func, re.findall('[0-9a-fA-F]{2}',string)))).decode(encoding)

def quote_to_bitstring(string, encoding='utf-8'):
    return urllib.parse.quote(string.decode(encoding), encoding=encoding)

def bitstring_to_quote(bitstring, encoding='utf-8'):
    return urllib.parse.unquote(bitstring, encoding=encoding)

def escape_to_bitstring(string, encoding='utf-8'):
    return html.escape(string.decode(encoding))

def bitstring_to_escape(bitstring, encoding='utf-8'):
    return html.unescape(bitstring)



html_quote = {
    'base_8':(bitstring_to_base_8, base_8_to_bitstring),
    'base_10':(bitstring_to_base_10, base_10_to_bitstring),
    'base_16':(bitstring_to_base_16, base_16_to_bitstring),
    'escape':(escape_to_bitstring, bitstring_to_escape), 
    'quote':(quote_to_bitstring, bitstring_to_quote), 
}

if __name__ == '__main__':
    k = b'123123123asdf891(*&^&%^'
    v = bitstring_to_base_8(k)
    print(v)
    v = base_8_to_bitstring(v)
    print(v)
    print()

    v = bitstring_to_base_10(k)
    print(v)
    v = base_10_to_bitstring(v)
    print(v)
    print()

    v = bitstring_to_base_16(k)
    print(v)
    v = base_16_to_bitstring(v)
    print(v)
    print()

    v = html.escape(k.decode())
    print(v)
    v = html.unescape(v)
    print(v)
    print()

    v = urllib.parse.quote(k.decode())
    print(v)
    v = urllib.parse.unquote(v)
    print(v)


    v = base_16_to_bitstring(r'\xe6\x9c\x89\xe7\x82\xb9\xe5\x8f\xaf\xe7\x88\xb1')
    print(v)