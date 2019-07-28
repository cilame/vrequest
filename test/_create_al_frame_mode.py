
def create_new_al(flag, alname):
    s = r'''
    # 这里后续需要考虑增加各种各样的加密解密以及代码的记录
    # 光是aes就有5种加解密方式
    def $change_cbit_1(*content):
        if content:
            encd = $line1_fent1.get().strip()
            blen = len(content[0].encode(encd))*8
            $line1_cbit1['text'] = str(blen)+'bit'
            return True
    def $change_cbit_2(*content):
        if content:
            encd = $line1_fent1.get().strip()
            blen = len(content[0].encode(encd))*8
            $line2_cbit2['text'] = str(blen)+'bit'
            return True

    $change_cbit1 = root.register($change_cbit_1)
    $change_cbit2 = root.register($change_cbit_2)
    $title = Frame(ff0)
    $title.pack(side=tkinter.TOP,fill=tkinter.X)
    Label($title, text=$titlestring).pack(fill=tkinter.X,expand=True)
    $line1 = Frame(ff0)
    $line1.pack(side=tkinter.TOP,fill=tkinter.X)
    Label($line1, text='密码',width=4).pack(side=tkinter.LEFT,padx=2)
    $line1_ent1 = Entry($line1,width=17,validate='key',validatecommand=($change_cbit1, '%P'))
    $line1_ent1.pack(side=tkinter.LEFT)
    $line1_ent1.bind('<Key>', $change_cbit1)
    $line1_cbit1 = Label($line1, text='0bit',width=6)
    $line1_cbit1.pack(side=tkinter.LEFT,padx=6)
    $line1_mode1 = Combobox($line1,width=4,state='readonly')
    $line1_mode1['values'] = ['b16','b32','b64','b85']
    $line1_mode1.current(2)
    $line1_mode1.pack(side=tkinter.RIGHT)
    Label($line1, text='编码',width=4).pack(side=tkinter.RIGHT,padx=5)
    def _$swich_encd1(*a):
        s = $line1_fent1.get().strip()
        if s == 'utf-8':
            $line1_fent1.delete(0,tkinter.END)
            $line1_fent1.insert(0,'gbk')
        elif s == 'gbk':
            $line1_fent1.delete(0,tkinter.END)
            $line1_fent1.insert(0,'utf-8')
        else:
            $line1_fent1.delete(0,tkinter.END)
            $line1_fent1.insert(0,'utf-8')
        $change_cbit_1($line1_ent1.get().strip())
        $change_cbit_2($line2_ent2.get().strip())
    $line1_fent1 = Entry($line1,width=5)
    $line1_fent1.insert(0,'utf-8')
    $line1_fent1.pack(side=tkinter.RIGHT)
    Button($line1, text='密码/iv/数据编码格式',command=_$swich_encd1).pack(side=tkinter.RIGHT)
    $line1_mode2 = Combobox($line1,width=4,state='readonly')
    $line1_mode2['values'] = ['cbc','cfb','ofb','ctr','ecb',]
    $line1_mode2.current(0)
    $line1_mode2.pack(side=tkinter.RIGHT)
    Label($line1, text='模式',width=4).pack(side=tkinter.RIGHT,padx=5)
    $line2 = Frame(ff0)
    $line2.pack(side=tkinter.TOP,fill=tkinter.X)
    Label($line2, text='iv',width=4).pack(side=tkinter.LEFT,padx=2)
    $line2_ent2 = Entry($line2,width=17,validate='key',validatecommand=($change_cbit2, '%P'))
    $line2_ent2.pack(side=tkinter.LEFT)
    
    $line2_cbit2 = Label($line2, text='128:bit',width=6)
    $line2_cbit2.pack(side=tkinter.LEFT,padx=6)
    $line2_ent2.insert(0,'1234567890123456')
    Label($line2, text='ecb模式：iv无效；ctr模式：iv长度不限制',).pack(side=tkinter.LEFT,padx=6)

    def _$alname_encode(*a):
        encd = $line1_fent1.get().strip()
        mode = $line1_mode2.get().strip()
        eout = $line1_mode1.get().strip()
        key  = $line1_ent1.get().strip().encode(encd)
        iv   = $line2_ent2.get().strip().encode(encd)
        data = ftxt.get(0.,tkinter.END).strip('\n').encode(encd)
        limitnum = int(entlimit.get().strip())
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyaes
        except:
            # 请勿在本脚本测试时安装了 pyaes，pyaes的源码部分有问题
            import pyaes
        if eout == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if eout == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if eout == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if eout == 'b85':_encode = base64.b85encode; _decode = base64.b85decode
        Encrypter = pyaes.Encrypter
        Counter = pyaes.Counter
        AESModesOfOperation = pyaes.AESModesOfOperation

        try:
            if mode in 'ctr':
                enc = Encrypter(AESModesOfOperation[mode](key, Counter(int.from_bytes(iv, 'big'))))
            elif mode == 'ecb':
                enc = Encrypter(AESModesOfOperation[mode](key))
            else:
                enc = Encrypter(AESModesOfOperation[mode](key, iv))
            en = _encode(enc.feed(data)).decode(encd)
            if len(en) > limitnum:
                print('警告！')
                print('加密数据长度({})过长（超过{}字符，超过的部分不显示）'.format(len(en),limitnum))
                print('因为 tkinter 性能瓶颈，不宜在 tkinter 窗口展示，请使用算法在别的IDE内实现')
                print('---------------------------------------------------')
                print(en[:limitnum])
            else:
                print(en)
        except:
            print(traceback.format_exc())

    def _$alname_decode(*a):
        encd = $line1_fent1.get().strip()
        mode = $line1_mode2.get().strip()
        eout = $line1_mode1.get().strip()
        key  = $line1_ent1.get().strip().encode(encd)
        iv   = $line2_ent2.get().strip().encode(encd)
        data = ftxt.get(0.,tkinter.END).strip('\n').encode(encd)
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyaes
        except:
            # 请勿在本脚本测试时安装了 pyaes，pyaes的源码部分有问题
            import pyaes
        if eout == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if eout == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if eout == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if eout == 'b85':_encode = base64.b85encode; _decode = base64.b85decode
        Decrypter = pyaes.Decrypter
        Counter = pyaes.Counter
        AESModesOfOperation = pyaes.AESModesOfOperation

        try:
            if mode in 'ctr':
                dec = Decrypter(AESModesOfOperation[mode](key, Counter(int.from_bytes(iv, 'big'))))
            elif mode == 'ecb':
                dec = Decrypter(AESModesOfOperation[mode](key))
            else:
                dec = Decrypter(AESModesOfOperation[mode](key, iv))
            dc = dec.feed(_decode(data)).decode(encd)
            print(dc)
        except:
            print(traceback.format_exc())

    def _$alname_code(*a):
        try:
            from . import pyaes
        except:
            import pyaes
        ftxt.delete(0.,tkinter.END)
        with open(pyaes.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button($line2, text='[算法]',command=_$alname_code,width=5).pack(side=tkinter.RIGHT)
    Button($line2, text='解密',command=_$alname_decode,width=5).pack(side=tkinter.RIGHT)
    Button($line2, text='加密',command=_$alname_encode,width=5).pack(side=tkinter.RIGHT)
'''

    s = s.replace('$alname', alname)
    s = s.replace('$line1_cbit1', flag + '1_cbit1')
    s = s.replace('$line1_ent1', flag + '1_ent1')
    s = s.replace('$line1_fent1', flag + '1_fent1')
    s = s.replace('$line1_mode1', flag + '1_mode1')
    s = s.replace('$line1_mode2', flag + '1_mode2')
    s = s.replace('$line2_cbit2', flag + '2_cbit2')
    s = s.replace('$line2_ent2', flag + '2_ent2')
    s = s.replace('$titlestring', repr('     以下算法为 AES 加解密算法 [密码长度需注意:128bit,192bit,256bit] [iv长度需注意:128bit]。'))
    s = s.replace('$line2', flag + '2')
    s = s.replace('$line1', flag + '1')
    s = s.replace('$title', flag + '0')
    s = s.replace('$change_cbit1', flag + '_change_cbit1')
    s = s.replace('$change_cbit2', flag + '_change_cbit2')
    s = s.replace('$change_cbit_1', flag + '_change_cbit_1')
    s = s.replace('$change_cbit_2', flag + '_change_cbit_2')
    s = s.replace('$swich_encd1', flag + 'swich_encd1')
    return s

alname = 'serpent'
s = create_new_al('f200', alname)
print(s)