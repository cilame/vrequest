from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# [*] AES       len(key) [128, 192, 256, 512]  len(iv) 128
# [*] Camellia  len(key) [128, 192, 256]       len(iv) 128
# [*] SEED      len(key) [128]                 len(iv) 128
#     ChaCha20  len(key) [256]                 len(iv) 128 (nonce)
# [*] Blowfish  len(key) range(32, 449, 8)     len(iv) 64
# [*] CAST5     len(key) range(40, 129, 8)     len(iv) 64
# [*] IDEA      len(key) [128]                 len(iv) 64
# [*] TripleDES len(key) [64, 128, 192]        len(iv) 64
# [*] DES       len(key) [64, 128, 192]        len(iv) 64
#     ARC4      len(key) [40, 56, 64, 80, 128, 160, 192, 256] # 不使用iv
# 带有 [*] 的可以有不同的加密模式

algos = dict(
    AES       = algorithms.AES,
    ARC4      = algorithms.ARC4,
    Blowfish  = algorithms.Blowfish,
    CAST5     = algorithms.CAST5,
    Camellia  = algorithms.Camellia,
    ChaCha20  = algorithms.ChaCha20,
    IDEA      = algorithms.IDEA,
    SEED      = algorithms.SEED,
    TripleDES = algorithms.TripleDES,
    DES       = algorithms.TripleDES, # 注意，DES 事实上等于 TripleDES 的密钥长度为 64bit 时的加解密
)

def get_encryptor(algoname, key, iv=None, mode='ecb', padd='pkcs7'):
    backend  = default_backend()
    if algoname == 'ChaCha20':
        algoer = algorithms.ChaCha20(key, iv)
        cipher = Cipher(algoer, None, backend=backend)
    elif algoname == 'ARC4':
        algoer = algorithms.ARC4(key)
        cipher = Cipher(algoer, None, backend=backend)
    else:
        algoer = algos[algoname](key)
        if mode == 'ecb': mode = modes.ECB()
        if mode == 'cfb': mode = modes.CFB(iv)
        if mode == 'ofb': mode = modes.OFB(iv)
        if mode == 'cbc': mode = modes.CBC(iv)
        if mode == 'ctr': mode = modes.CTR(iv)
        cipher = Cipher(algoer, mode, backend=backend)

    def enc(bitstring):
        if algoname not in ['ARC4', 'ChaCha20']:
            if padd.upper() == 'PKCS7':
                padder    = padding.PKCS7(algoer.block_size).padder()
                bitstring = padder.update(bitstring) + padder.finalize()
            elif padd.upper() == 'ANSIX923':
                padder    = padding.ANSIX923(algoer.block_size).padder()
                bitstring = padder.update(bitstring) + padder.finalize()
        encryptor = cipher.encryptor()
        return encryptor.update(bitstring) + encryptor.finalize()

    def dec(bitstring):
        decryptor = cipher.decryptor()
        ddata = decryptor.update(bitstring) + decryptor.finalize()
        if algoname not in ['ARC4', 'ChaCha20']:
            if padd.upper() == 'PKCS7':
                unpadder  = padding.PKCS7(algoer.block_size).unpadder()
                ddata = unpadder.update(ddata) + unpadder.finalize()
            elif padd.upper() == 'ANSIX923':
                unpadder  = padding.ANSIX923(algoer.block_size).unpadder()
                ddata = unpadder.update(ddata) + unpadder.finalize()
        return ddata
    class f:pass
    f.encrypt = enc
    f.decrypt = dec
    return f


if __name__ == '__main__':
    key         = b'1234567812345678'   # 密码
    iv          = b'1234567812345678'   # 某些加密模式需要的参数，（ARC4，ChaCha20 加密或者所有的 ecb 模式下，该参数无效！！）
    algoname    = 'DES'                 # 加密名字
    mode        = 'ecb'                 # ARC4，ChaCha20 模式下该参数无效
    padd        = 'pkcs7'               # 默认使用该 padding 方式。
    encryptor = get_encryptor(algoname, key, iv, mode, padd)

    # key, iv 的长度请阅读头部注释注意
    bitstring = b'1234567812345678'
    v = encryptor.encrypt(bitstring)
    print(v)
    import base64; print(base64.b64encode(v))
    v = encryptor.decrypt(v)
    print(v)




# 这里是常用模式 aes/cbc/pkcs7 模式下的 get_encryptor 简化代码
# 上面的代码是考虑完全的通用性以及在工具内部被使用的必要多封装，这里主要是为了更加方便使用的简写
#import base64
#from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
#from cryptography.hazmat.primitives import padding
#from cryptography.hazmat.backends import default_backend
#def get_encryptor(key, iv=None):
#    algoer = algorithms.AES(key) #若要使用DES这里改成TripleDES
#    mode   = modes.CBC(iv)       #模式若是ecb则为 modes.ECB(), 其余模式均为一个参数 mode.***(iv)
#    cipher = Cipher(algoer, mode, backend=default_backend())
#    def enc(bitstring):
#        padder    = padding.PKCS7(algoer.block_size).padder()
#        bitstring = padder.update(bitstring) + padder.finalize()
#        encryptor = cipher.encryptor()
#        return encryptor.update(bitstring) + encryptor.finalize()
#    def dec(bitstring):
#        decryptor = cipher.decryptor()
#        ddata     = decryptor.update(bitstring) + decryptor.finalize()
#        unpadder  = padding.PKCS7(algoer.block_size).unpadder()
#        return unpadder.update(ddata) + unpadder.finalize()
#    class f:pass
#    f.encrypt = enc
#    f.decrypt = dec
#    return f
#if __name__ == '__main__':
#    key         = b'1234567890123456'   #密码
#    iv          = b'1234567890123456'   #某些加密模式需要的参数，（ARC4，ChaCha20 加密或者所有的 ecb 模式下，该参数无效！！）
#    data        = '2LWYSMdnDJSym1TSN54uesXryeud7lOPCtlpWV16dAw='.encode()
#    db64        = base64.b64decode(data)
#    encryptor   = get_encryptor(key, iv)
#    v = encryptor.decrypt(db64)
#    print(v)