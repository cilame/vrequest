import zlib
import lzma
import gzip
import base64


def format_compress_string(data, base, compress, width, encode):
    return format_compress(data, base, compress, width, encode, is_file=False)

def format_compress_file(base, compress, width, encode):
    return format_compress(None, base, compress, width, encode, is_file=True)

def format_compress(data, base, compress, width, encode, is_file=False):
    if not is_file:
        data = data.encode(encode)
    else:
        import tkinter.filedialog
        file = tkinter.filedialog.askopenfiles()
        if file:
            file = file[0].name
            with open(file, 'rb') as f:
                data = f.read()
        else:
            return ''

    if base == 'base64': _encode, _decode = base64.b64encode, base64.b64decode
    if base == 'base85': _encode, _decode = base64.b85encode, base64.b85decode

    if compress == 'None': zcompress, zdecompress = lambda i:i,                      lambda i:i
    if compress == 'zlib': zcompress, zdecompress = lambda i:zlib.compress(i)[2:-4], lambda i:zlib.decompress(i,-15)
    if compress == 'lzma': zcompress, zdecompress = lambda i:lzma.compress(i),       lambda i:lzma.decompress(i)
    if compress == 'gzip': zcompress, zdecompress = lambda i:gzip.compress(i),       lambda i:gzip.decompress(i)

    if base == 'base64': fbstring = 'zstring = base64.b64decode(zstring)'
    if base == 'base85': fbstring = 'zstring = base64.b85decode(zstring)'
    if compress == 'None': importstring = 'import base64';       fzstring = ''
    if compress == 'zlib': importstring = 'import base64, zlib'; fzstring = 'zstring = zlib.decompress(zstring,-15)'
    if compress == 'lzma': importstring = 'import base64, lzma'; fzstring = 'zstring = lzma.decompress(zstring)'
    if compress == 'gzip': importstring = 'import base64, gzip'; fzstring = 'zstring = gzip.decompress(zstring)'

    if is_file:
        datastring = 'bitdata = zstring\nprint(bitdata[:100])'
    else:
        datastring = 'string = zstring.decode("{}")\nprint(string)'.format(encode)

    zdata = zcompress(data)
    edata = _encode(zdata).decode()
    pack = []
    for idx,i in enumerate(edata,1):
        pack.append(i)
        if idx % width == 0:
            pack.append("'\n'")
    packdata = "'{}'".format(''.join(pack))
    leninfo = '# len(zstring): {}'.format(len(edata))

    return r'''
zstring = (
{}
)

{}
{}
{}{}
{}
'''.format(packdata, leninfo, importstring, fbstring, '\n' + fzstring if fzstring else fzstring, datastring).strip()

if __name__ == '__main__':
    string = r'''testcode'''
    v = format_compress_string(string, 'base64', 'None', 10)
    print(v)

    v = format_compress_file('base64', 'None', 10)
    print(v)