# 凯撒密码
def caesar(t, n, keys='abcdefghijklmnopqrstuvwxyz'):
    s = list(keys)
    r = ''
    for i in t:
        if i in s:
            r += s[(s.index(i) + n)% len(keys)]
        else:
            r += i
    return r

if __name__ == '__main__':
    s = 'qianshanniaofeijue1234'
    for i in range(0, 26):
        v = caesar(s, i)
        print('deviation: {:>2} --- result: {} '.format(i, v))