# 栅栏密码
def rail_fence_enc(string, n, padding=None):
    # 增加padding主要是为了加密的鲁棒性
    b = []
    q = []
    for idx,i in enumerate(string, 1):
        q.append(i)
        if idx % n == 0:
            b.append(q)
            q = []
    r = []
    if q:
        for i in '@~!#$%^&*': # 自动选一个padding进行处理
            if i not in string:
                padding = i
                break
        if padding is None: 
            raise 'cannot find a padding, cos @~!#$%^&* all in string.'
        q += [padding] * (n - len(q))
        b.append(q)
    for i in zip(*b):
        r.extend(i)
    return ''.join(r), padding

def rail_fence_dec(string, n, padding=None, return_matrix=False):
    # 这里的输入必须可以生成矩阵，否则会有异常情况
    a = len(string)/n
    b = len(string)//n
    n = b if a == b else b+1
    b = []
    for i in range(0,n):
        b.append(string[i::int(n)])
    r = []
    for i in zip(b):
        r.extend(i)
    if return_matrix:
        return r
    return ''.join(r).rstrip(padding)


def get_primes(_int):
    r = []
    for i in range(2, _int):
        if _int % i == 0:
            r.append(i)
    return r

def rail_fence_enum(string, return_matrix=False):
    prs = get_primes(len(string))
    r = []
    for i in prs:
        v = rail_fence_dec(string, i, return_matrix=return_matrix)
        a, b = i, len(string)//i
        r.append((a,b,v))
    return r


if __name__ == '__main__':
    # 栅栏加密，默认使用带填充模式
    # 也可以通过 padding 来判断加密是否存在自动填充情况
    s, padding = rail_fence_enc('asdfasdfasdff', 3)
    print(s)
    print(padding)
    s = rail_fence_dec(s, 3, padding=padding)
    print(s)
    print()


    s, padding = rail_fence_enc('abcdefghijklmn', 7)
    print(s)
    for i in rail_fence_enum(s):
        print(i)