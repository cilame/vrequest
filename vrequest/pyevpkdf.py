import os
import base64
from hashlib import new




# cryptojs 的默认加密方式每次加密都不一样，并且都有 U2FsdGVkX1 这个头标志
# 虽然每次加密的数据都不一样，但是解密都是一样的，这是因为他使用了一个随机数，并且这个随机数是放在加密数据里面
# 用这个随机数进行散列算法，算出 key 以及 iv 使用固定的模式进行加密就可以每次加密不同了。
# 将这个随机参数作为 salt 算出 key和iv 后进行加密
# 通过 result = base64('Salted__' + salt + encodedata) 算出真实地加密后地数据结果，
# （另外 EvpKDF 算法是从 cryptojs js代码中逆向出的 python 算法，不知道以后有没有可能成为什么标准。）

def EvpKDF(hash_name, password, salt, iterations, dklen=None):
    dkey = b''
    block = None
    hasher = new(hash_name)
    while len(dkey) < dklen:
        if block:
            hasher.update(block)
        hasher.update(password)
        hasher.update(salt)
        block = hasher.digest()
        hasher = new(hash_name)
        for i in range(1, iterations):
            hasher.update(block)
            block = hasher.digest()
            hasher = new(hash_name)
        dkey += block
    return dkey[:dklen]

def make_cryptojs_from_default_params(key, block_size, iv_size, randomsalt=True):
    dklen    = (block_size+iv_size)//8
    blocklen = block_size//8
    ivlen    = iv_size//8
    salt     = os.urandom(8) if randomsalt else b'\x00'*8 # 默认使用随即盐,否则使用八位0填充
    v = EvpKDF('md5', key, salt, 1, dklen=dklen) # 从 cryptojs 逆向出的默认 iterations 为 1
    key, iv = v[:blocklen], v[-ivlen:]
    return key, iv, salt

def parse_cryptojs_from_default_params(key, block_size, iv_size, data):
    dklen    = (block_size+iv_size)//8
    blocklen = block_size//8
    ivlen    = iv_size//8
    salt = data[8:16] # 固定长度 8.
    v = EvpKDF('md5', key, salt, 1, dklen=dklen) # 从 cryptojs 逆向出的默认 iterations 为 1
    key, iv, salt, data = v[:blocklen], v[-ivlen:], salt, data[16:] # 16位之后是真实的加密数据，抛出去还需要正式的算法解密
    return key, iv, salt, data





if __name__ == '__main__':

    # 这里的加密模式固定使用 cbc/pkcs7 
    #（这里仅仅使用了aes示范，如果是des或其他的算法，key和iv的长度多少会有一定的变化）
    # 是为了示范怎么使用当前的加解密的参数，
    #     如果你需要用下面代码并使用自定义的各种参数，请注意下面四个注释部分的参数修改：算法，模式，block_size，iv_size。 
    #     如果你掌握js逆向想要从 cryptojs 里面检查加密正确，请注意js里面的 EvpKDF 函数以及传入参数的各种正确性以便调整
    # aes/cbc/pkcs7
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
    def get_encryptor(key, iv=None):
        algoer = algorithms.AES(key) #这里的AES算法（若要换成des算法，这里换成TripleDES，该加密库中，DES 事实上等于 TripleDES 的密钥长度为 64bit 时的加解密）
        cipher = Cipher(algoer, modes.CBC(iv), backend=default_backend()) #这里的CBC模式
        def enc(bitstring):
            padder    = padding.PKCS7(algoer.block_size).padder()
            bitstring = padder.update(bitstring) + padder.finalize()
            encryptor = cipher.encryptor()
            return encryptor.update(bitstring) + encryptor.finalize()
        def dec(bitstring):
            decryptor = cipher.decryptor()
            ddata     = decryptor.update(bitstring) + decryptor.finalize()
            unpadder  = padding.PKCS7(algoer.block_size).unpadder()
            return unpadder.update(ddata) + unpadder.finalize()
        class f:pass
        f.encrypt = enc
        f.decrypt = dec
        return f
    def cryptojs_default_aes_enc(realkey, realdata):
        block_size, iv_size = 256, 128 # aes block_size 256 # iv_size 128（若要换成des，这里改成(64,64)）
        key,iv,salt = make_cryptojs_from_default_params(realkey, block_size, iv_size)
        encryptor   = get_encryptor(key, iv)
        return base64.b64encode(b'Salted__' + salt + encryptor.encrypt(realdata))
    def cryptojs_default_aes_dec(realkey, encdata):
        block_size, iv_size = 256, 128 # aes block_size 256 # iv_size 128（若要换成des，这里改成(64,64)）
        key,iv,salt,_data = parse_cryptojs_from_default_params(realkey, block_size, iv_size, base64.b64decode(encdata))
        encryptor   = get_encryptor(key, iv)
        return encryptor.decrypt(_data)

    # 加解密混合验证
    realkey     = b'123'
    realdata    = b'something'
    encdata = cryptojs_default_aes_enc(realkey, realdata)
    decdata = cryptojs_default_aes_dec(realkey, encdata)
    print(encdata)
    print(decdata)
    print()

    # 直接使用网站获取的加密结果进行验证
    realkey = b'123'
    encdata = b'U2FsdGVkX19e0LihgCXF3n6vPFLihWnI3CDRHrKwzAk='
    decdata = cryptojs_default_aes_dec(realkey, encdata)
    print(decdata)