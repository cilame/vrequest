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

def urlquote_to_bitstring(string, encoding='utf-8'):
    def quote_val(url):
        for i in re.findall(r'[\?&][^=&]*=([^&]*)',url):
            url = url.replace(i,'{}'.format(urllib.parse.quote_plus(i, encoding=encoding)))
        return url
    return quote_val(string.decode(encoding))

def bitstring_to_urlquote(bitstring, encoding='utf-8'):
    def unquote_val(url):
        for i in re.findall(r'[\?&][^=&]*=([^&]*)',url):
            url = url.replace(i,'{}'.format(urllib.parse.unquote_plus(i, encoding=encoding)))
        return url
    return unquote_val(bitstring)

def escape_to_bitstring(string, encoding='utf-8'):
    return html.escape(string.decode(encoding))

def bitstring_to_escape(bitstring, encoding='utf-8'):
    return html.unescape(bitstring)

def bitstring_to_unicode(string, encoding='utf-8'):
    return string.encode(encoding).decode('unicode_escape')

def unicode_to_bitstring(bitstring, encoding='utf-8'):
    return bitstring.decode(encoding).encode('unicode_escape').decode(encoding)


def bitstring_to_binary(string, encoding='utf-8'):
    return bytes(list(map(lambda i:int(i, 2), re.findall('[0-1]{1,8}',string)))).decode(encoding)

def binary_to_bitstring(bitstring, encoding='utf-8'):
    r = []
    for i in bitstring:
        r.append('{:>08}'.format(bin(i)[2:]))
    return ' '.join(r)


html_quote = {
    'base_2':   (binary_to_bitstring,   bitstring_to_binary),
    'base_8':   (bitstring_to_base_8,   base_8_to_bitstring),
    'base_10':  (bitstring_to_base_10,  base_10_to_bitstring),
    'base_16':  (bitstring_to_base_16,  base_16_to_bitstring),
    'escape':   (escape_to_bitstring,   bitstring_to_escape), 
    'quote':    (quote_to_bitstring,    bitstring_to_quote), 
    'urlquote': (urlquote_to_bitstring, bitstring_to_urlquote), 
    'unicode':  (unicode_to_bitstring,  bitstring_to_unicode), 
}

if __name__ == '__main__':
    try:
        # 处理 sublime 执行时输出乱码
        import io
        import sys
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
        sys.stdout._CHUNK_SIZE = 1
    except:
        pass


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

    url = 'https://www.baidu.com/s?ie=UTF-8&wd=%E7%99%BE%E5%BA%A6'
    v = bitstring_to_urlquote(url)
    print(v)
    v = urlquote_to_bitstring(v.encode())
    print(v)

    v = base_16_to_bitstring(r'\xe6\x9c\x89\xe7\x82\xb9\xe5\x8f\xaf\xe7\x88\xb1')
    print(v)
    v = base_16_to_bitstring(r'e69c89e782b9e58fafe788b1')
    print(v)

    v = '你好'.encode()
    v = unicode_to_bitstring(v)
    print(v)
    v = bitstring_to_unicode(v)
    print(v)
    
    v = '你好'.encode()
    v = binary_to_bitstring(v)
    print(v)
    v = bitstring_to_binary(v)
    print(v)
    
    
    
