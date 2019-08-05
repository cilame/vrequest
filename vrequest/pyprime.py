import random

# miller-rabin 算法素性检测
def isprime_mr(a,b=None):
    if b is None: b = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    if a == 2:return True
    if a%2==0 or a==1:return False
    for x in b:
        t = a - 1
        while t%2 == 0:
            v = pow(x,t,a)# python自带函数pow就带有快速幂取模功能
            if v not in [0,1,a-1]:
                return False
            else:
                if v in [0,a-1]: break
                t //= 2
    return True

# Pollcard Rho 质因数分解，比普通质因分解更好的一种算法，能处理更大的数字
def prime_list_rho(n,root=None):
    # 之所以不用 def prime_list_rho(n,root=[]): 的方式是因为这里有坑
    # 作为函数对象的内部参数的临时地址多次使用会一直引用一个地址，
    # 所以考虑到该参数最后会作为结果返回出去，所以需要考虑初始化处理
    if root is None: root = []
    if not root and n<2:
        raise ValueError(n)
    if isprime_mr(n):
        root.append(n)
        return root
    from random import randint
    from math import gcd
    while True:
        x = randint(0,n-1) + 1
        c = randint(0,n-1) + 1
        y = x
        i = j = 2
        while True:
            x = ((x**2)+c)%n
            z = abs(x - y)
            d = gcd(z,n)
            if d>1 and d<n:
                prime_list_rho(d,root)
                prime_list_rho(n//d,root)
                return root
            if x == y: break
            if i == j:
                y = x
                j <<= 1
            i += 1

# 根据长度随机迭代，获取质数
def get_prime(bitlen=1024):
    num = (1<<(bitlen-1)) + random.randint(0,1<<(bitlen-1)) | 1
    while True:
        num += 2
        if isprime_mr(num):
            return num

# 根据二进制数字长度需求生成rsa密钥，length需要为2的倍数
def create_rsa_key(length=1024, e=65537):
    assert length%2 == 0, 'bit length must be even number'
    # 确保公共参数n的位数，以便保证密钥长度。
    while True:
        p = get_prime(length//2)
        q = get_prime(length//2)
        n = p * q
        if n.bit_length() == length and p != q:
            break
    fn  = (p-1) * (q-1)
    # 扩展欧几里得算法获取乘法模逆元
    def ex_gcd(a,b):
        if b == 0:
            return (1,0,a)
        (x, y, r) = ex_gcd(b,a%b)
        t = x
        x = y
        y = t - a//b*y
        return (x,y,r)
    # 由于主动设定了e为素数，所以一次获取肯定能获取到符合要求的模逆元
    # 该数也是一般通用标准，是为了方便计算机计算而选的数字：0x10001==65537
    a, b, r = ex_gcd(fn, e)
    d = b + fn
    # 公钥n,e 私钥n,d
    return e,d,n

if __name__ == '__main__':
    print('============= test =============')
    # 测试rsa密钥生成效率
    e,d,n = create_rsa_key(1024,885158609)#默认生成1024位的密钥
    print('(rsa publicKey n,e) {} --- {}'.format(n,e))
    print('(rsa PrivateKey n,d) {} --- {}'.format(n,d))

    print('============= test =============')
    # 测试rsa密钥加密解密
    # rsa可以加解密一个 1024bit 位的数据，所以通常加密数据过长就需要切分处理
    def test(o):
        print('(rsa original data) {}'.format(o))
        c = pow(o,e,n) # 加密
        v = pow(c,d,n) # 解密
        print('(rsa decoding data) {}'.format(v))
        print('(rsa encoding data) {}'.format(c))
    test(12345678987654321)
    test(11111111111111111222222222222222222222000)
    test(33333333333333333333333333333333333333333333333)

    print();print();print()

    # 测试质因数分解
    def test_rho(num):
        print('=========== Pollcard Rho ============')
        import time
        c = time.time()
        try:
            print(v)
        except:
            pass
        v = prime_list_rho(num)
        q = 1
        for i in v:
            q *= i
        print('prime_list',v)
        print('test num:      ',num)
        print('multiplicative:',q)
        print('cost time:',time.time()-c)

    test_rho(12345678987654321)
    test_rho(2222222222222222222222222222)
