def ascii_deviation(string, n):
    r = []
    for i in string.encode():
        r.append(i + n)
    try:
        return bytes(r).decode()
    except:
        return 'error decoding. {}'.format(bytes(r))


if __name__ == '__main__':
    s = 'YXNkZg=='
    s = 'cbXudqGG'
    for i in range(-20,20):
        v = '{:>3} --- {}'.format(i, ascii_deviation(s, i))
        print(v)