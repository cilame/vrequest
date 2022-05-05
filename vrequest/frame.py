try:
    import requests
except:
    requests = None

import io
import os
import re
import sys
import json
import zlib
import time
import hmac
import queue
import shutil
import base64
import hashlib
import tempfile
import traceback
import threading
import tkinter
import inspect
import zipfile
import itertools
import urllib.parse as ps
import tkinter.messagebox
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.font import Font
from tkinter.simpledialog import askstring
from binascii import a2b_hex, b2a_hex

try:
    from .root import DEFAULTS_HEADERS,root
except:
    from root import DEFAULTS_HEADERS,root

Text = scrolledtext.ScrolledText
#Text = tkinter.Text
Label = ttk.Label
Button = ttk.Button
Combobox = ttk.Combobox
Listbox = tkinter.Listbox
Entry = ttk.Entry
Checkbutton = tkinter.Checkbutton

# 测试两种 Frame 效果
# Frame = ttk.Frame # ttk.Frame 没有 highlightthickness 这个参数
Frame = tkinter.Frame

frame_setting = {}

pdx = 0
pdy = 0
lin = 0

def request_window(setting=None):
    fr = Frame()
    ft = Font(family='Consolas',size=10)

    def change_method(*a):
        method = cbx.get()
        if method == 'POST':
            temp_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.BOTTOM)
        elif method == 'GET':
            temp_fr2.pack_forget()

    def test_code(*a):
        from .tab import create_test_code
        create_test_code()

    def scrapy_code(*a):
        from .tab import create_scrapy_code
        create_scrapy_code()

    def urllib_code(*a):
        from .tab import create_test_code_urllib
        create_test_code_urllib()

    def send_req(*a):
        from .tab import send_request
        send_request()

    def _swich_encd(*a):
        s = ent1.get().strip()
        if s == 'utf-8':
            ent1.delete(0,tkinter.END)
            ent1.insert(0,'gbk')
        elif s == 'gbk':
            ent1.delete(0,tkinter.END)
            ent1.insert(0,'utf-8')
        else:
            ent1.delete(0,tkinter.END)
            ent1.insert(0,'utf-8')

    def _swich_quote(*a):
        s = ent2.get().strip()
        if s == 'yes':
            ent2.delete(0,tkinter.END)
            ent2.insert(0,'no')
        elif s == 'no':
            ent2.delete(0,tkinter.END)
            ent2.insert(0,'yes')
        else:
            ent2.delete(0,tkinter.END)
            ent2.insert(0,'yes')

    def _select_create_code(*a):
        from .tab import nb
        from .tab import SimpleDialog
        q = [   '生成[requests]代码[Alt+c]', 
                '生成[scrapy]代码[Alt+s]', 
                '生成[urllib]代码[Alt+u]', ]
        d = SimpleDialog(nb,
            text="请选择生成的代码",
            buttons=q,
            default=0,
            cancel=-1,
            title="生成代码")
        id = d.go()
        if id == -1: return
        if id == 0: test_code()
        if id == 1: scrapy_code()
        if id == 2: urllib_code()

    temp_fr0 = Frame(fr)
    methods = ('GET','POST')
    cbx = Combobox(temp_fr0,width=10,state='readonly')
    cbx['values'] = methods     # 设置下拉列表的值
    cbx.current(0)
    cbx.pack(side=tkinter.RIGHT)
    cbx.bind('<<ComboboxSelected>>', change_method)
    temp_fr0.pack(fill=tkinter.X)
    btn1 = Button(temp_fr0, text='发送请求[Ctrl+r]', command=send_req)
    btn1.pack(side=tkinter.RIGHT)
    ent1 = Entry(temp_fr0,width=6)
    ent1.pack(side=tkinter.RIGHT)
    btnurlencode = Button(temp_fr0, width=14, text='url中文编码格式', command=_swich_encd)
    btnurlencode.pack(side=tkinter.RIGHT)
    ent2 = Entry(temp_fr0,width=4)
    ent2.pack(side=tkinter.RIGHT)
    btnurlencode1 = Button(temp_fr0, width=32, text='url是否编码“+”符号(url中有base64编码)', command=_swich_quote)
    btnurlencode1.pack(side=tkinter.RIGHT)
    lab1 = Label(temp_fr0, text='请尽量发送请求后生成代码，那样会有更多功能：')
    lab1.pack(side=tkinter.LEFT)
    # btn6 = Button(temp_fr0, text='生成[requests]代码[Alt+c]', command=test_code)
    # btn6.pack(side=tkinter.LEFT)
    # btn7 = Button(temp_fr0, text='生成[scrapy]代码[Alt+s]', command=scrapy_code)
    # btn7.pack(side=tkinter.LEFT)
    # btn8 = Button(temp_fr0, text='生成[urllib]代码[Alt+u]', command=urllib_code)
    # btn8.pack(side=tkinter.LEFT)

    def local_collection(*a):
        def _show(*a, stat='show'):
            try:
                if stat == 'show': et.pack(side=tkinter.RIGHT)
                if stat == 'hide': et.pack_forget()
            except:
                pass
        _show(stat='show') if va.get() else _show(stat='hide')
    va = tkinter.IntVar()
    rb = Checkbutton(temp_fr0,text='使用代理',variable=va,command=local_collection)
    rb.deselect()
    et = Entry (temp_fr0, width=16)
    et.insert(0, '127.0.0.1:8888')
    rb.pack(side=tkinter.RIGHT)

    btn9 = Button(temp_fr0, text='选择生成代码', command=_select_create_code)
    btn9.pack(side=tkinter.LEFT)

    temp_fr1 = Frame(fr,highlightthickness=lin)
    temp_fold_fr1 = Frame(temp_fr1)
    temp_fold_fr2 = Frame(temp_fr1)
    lb1 = Label (temp_fold_fr1,text='url')
    tx1 = Text  (temp_fold_fr1,height=1,width=1,font=ft)
    lb1.pack(side=tkinter.TOP)
    tx1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP,padx=pdx,pady=pdy)

    lb2 = Label (temp_fold_fr2,text='headers')
    tx2 = Text  (temp_fold_fr2,height=1,width=1,font=ft)
    lb2.pack(side=tkinter.TOP)
    tx2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP,padx=pdx,pady=pdy)
    temp_fold_fr1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.LEFT)
    temp_fold_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.LEFT)
    temp_fr1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)


    temp_fr2 = Frame(fr,highlightthickness=lin)
    lb3 = Label (temp_fr2,text='body')
    tx3 = Text  (temp_fr2,height=1,width=1,font=ft)
    lb3.pack(side=tkinter.TOP)
    tx3.pack(fill=tkinter.BOTH,expand=True,padx=pdx,pady=pdy)
    if setting and setting.get('method') == 'POST':
        cbx.current(methods.index('POST'))
        temp_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.BOTTOM)

    if setting:
        tx1.insert(0.,setting['url'].strip())
        tx2.insert(0.,setting['headers'].strip())
        tx3.insert(0.,setting['body'].strip())
        ent1.insert(0,setting.get('urlenc') or 'utf-8')
        ent2.insert(0,setting.get('qplus') or 'no')
        if setting.get('proxy'):
            et.delete(0, tkinter.END)
            et.insert(0, setting.get('proxy'))
            et.pack(side=tkinter.RIGHT)
            rb.select()
    else:
        tx2.insert(0.,DEFAULTS_HEADERS.strip())
        ent1.insert(0,'utf-8')
        ent2.insert(0,'no')

    frame_setting[fr] = {}
    frame_setting[fr]['type'] = 'request'
    frame_setting[fr]['fr_method'] = cbx
    frame_setting[fr]['fr_url'] = tx1
    frame_setting[fr]['fr_headers'] = tx2
    frame_setting[fr]['fr_body'] = tx3
    frame_setting[fr]['fr_urlenc'] = ent1
    frame_setting[fr]['fr_qplus'] = ent2
    frame_setting[fr]['fr_proxy'] = va, et
    return fr


def response_window(setting=None):

    '''
    这里的 setting 结构应该就是一个请求信息的数据结构
    并且应该是整理好数据类型的字典，在这里请求任务结束之后返回的数据
    就按照展示结构放在 response 的结构框架里面。
    url     :str
    method  :str
    headers :dict
    body    :str
    '''

    def insert_txt(fr_txt, txt):
        try:
            fr_txt.delete(0.,tkinter.END)
            fr_txt.insert(0.,re.sub('[\uD800-\uDBFF][\uDC00-\uDFFF]|[\U00010000-\U0010ffff]','',txt))
        except:
            pass

    doc0 = '''选择列表解析路径方式
冒号后面配置的的内容为 xpath
<xpath:>
*组合功能！
如果先使用了 “分析xpath” 功能后解析到路径
那么使用该功能时会自动弹出选择窗口
选择窗中的内容为自动解析xpath中解析出的 xpath
'''

    doc1 = '''纯文字内容解析
解析某个 xpath 路径下面的所有文字字符串，默认是 //html 路径下的所有文字
<normal_content://html>
'''

    doc2 = '''根据字符串自动分析 xpath 路径
一般用于列表形式的路径
通常来说这个功能针对简单的网页结构还勉强有用，并非一定能够解析
所以一些比较复杂的网页或许还是需要考虑自行分析xpath。

冒号后面配置需要处理的字符串
多个字符串可以通过空格分隔
eg.:
    <auto_list_xpath:白天 黑夜>
不写则为查找所有 "string(.)" (xpath语法)
能解析出含有非空字符串的内容路径
'''

    doc3 = '''简单分析json数据内容
找出最长的list进行初步的迭代分析，并给出分析结果在输出框
如果没有主动选择某一个json列表，则默认使用第一个最长的列表
进行默认的代码生成
<auto_list_json:>
'''

    doc4 = '''选择分析的json列表
选择的json列表的解析方式放在auto_list_json配置的后面
当你生成代码的时候将会使用这个进行对列表解析自动生成对应的代码
下面是一个例子：
<auto_list_json:jsondata["data"]["list"]>
'''

    doc5 = '''生成scrapy代码
如果存在 “解析xpath”、“自动json” 或 “获取纯文字” 状态
则会在生成代码中包含相应的代码
'''

    doc6 = '''生成requests代码
如果存在 “解析xpath”、“自动json” 或 “获取纯文字” 状态
则会在生成代码中包含相应的代码
'''

    def document(*a):
        method = cbx.get()
        if methods.index(method) == 0:
            insert_txt(tx3,doc0)
        if methods.index(method) == 1:
            insert_txt(tx3,doc1)
        if methods.index(method) == 2:
            insert_txt(tx3,doc2)
        if methods.index(method) == 3:
            insert_txt(tx3,doc3)
        if methods.index(method) == 4:
            insert_txt(tx3,doc4)
        if methods.index(method) == 5:
            insert_txt(tx3,doc5)
        if methods.index(method) == 6:
            insert_txt(tx3,doc6)
        switch_show(onlyshow=True)

    fr = Frame()
    ft = Font(family='Consolas',size=10)
    def switch_show(*a, onlyshow=False):
        try:
            temp_fold_fr2.pack_info()
            packed = True
        except:
            packed = False
        if packed:
            if not onlyshow:
                temp_fold_fr2.pack_forget()
        else:
            temp_fold_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.LEFT)

    def html_pure_text(*a):
        from .tab import get_html_pure_text
        get_html_pure_text()

    def xpath_elements(*a):
        from .tab import get_xpath_elements
        get_xpath_elements()

    def auto_xpath(*a):
        from .tab import get_auto_xpath
        get_auto_xpath()

    def auto_json(*a):
        from .tab import get_auto_json
        get_auto_json()

    def choice_json(*a):
        from .tab import choice_auto_json
        choice_auto_json()

    def test_code(*a):
        from .tab import create_test_code
        create_test_code()

    def scrapy_code(*a):
        from .tab import create_scrapy_code
        create_scrapy_code()

    def urllib_code(*a):
        from .tab import create_test_code_urllib
        create_test_code_urllib()

    def jsonformat(*a):
        from .tab import response_jsonformat
        response_jsonformat()

    def xpath_finder(*a):
        from .tab import nb
        from .tab import create_xpath_finder
        setting = {}
        setting['content'] = tx1.get(0.,tkinter.END).strip()
        setting['master'] = nb
        s = create_xpath_finder(setting)
        tx2.delete(0., tkinter.END)
        tx2.insert(0., '<just_info:>\n' + s)

    def _select_analysis(*a):
        from .tab import nb
        from .tab import SimpleDialog
        q = [   '(Alt+f)分析xpath',
                '(Alt+x)选择xpath',
                '(Alt+z)分析json',
                '(Alt+q)选择json',
                '(Alt+d)获取纯文字', 
                'xpath内容分析', ]
        d = SimpleDialog(nb,
            text="请选择分析内容的方式，分析后再生成代码，会自动在代码内带有分析处理的代码块。",
            buttons=q,
            default=0,
            cancel=-1,
            title="分析内容")
        id = d.go()
        if id == -1: return
        if id == 0: auto_xpath()
        if id == 1: xpath_elements()
        if id == 2: auto_json()
        if id == 3: choice_json()
        if id == 4: html_pure_text()
        if id == 5: xpath_finder()

    def _select_create_code(*a):
        from .tab import nb
        from .tab import SimpleDialog
        q = [   '生成[requests]代码[Alt+c]', 
                '生成[scrapy]代码[Alt+s]', 
                '生成[urllib]代码[Alt+u]', ]
        d = SimpleDialog(nb,
            text="请选择生成的代码",
            buttons=q,
            default=0,
            cancel=-1,
            title="生成代码")
        id = d.go()
        if id == -1: return
        if id == 0: test_code()
        if id == 1: scrapy_code()
        if id == 2: urllib_code()

    temp_fr0 = Frame(fr)
    lab1 = Label(temp_fr0, text='功能说明：')
    lab1.pack(side=tkinter.LEFT)
    methods = ('(Alt+x) 选择xpath','(Alt+d) 获取纯文字','(Alt+f) 分析xpath','(Alt+z) 分析json','(Alt+q) 选择json', '(Alt+s) 生成 scrapy代码', '(Alt+c) 生成 requests代码')
    cbx = Combobox(temp_fr0,width=18,state='readonly')
    cbx['values'] = methods     # 设置下拉列表的值
    cbx.current(0)
    cbx.pack(side=tkinter.LEFT)
    cbx.bind('<<ComboboxSelected>>', document)
    temp_fr0.pack(fill=tkinter.X)
    btn11 = Button(temp_fr0, text='选择内容分析', command=_select_analysis)
    btn11.pack(side=tkinter.LEFT)
    # btn3 = Button(temp_fr0, text='(f)分析xpath', command=auto_xpath)
    # btn3.pack(side=tkinter.LEFT)
    # btn4 = Button(temp_fr0, text='(x)选择xpath', command=xpath_elements)
    # btn4.pack(side=tkinter.LEFT)
    # btn5 = Button(temp_fr0, text='(z)分析json', command=auto_json)
    # btn5.pack(side=tkinter.LEFT)
    # btn9 = Button(temp_fr0, text='(q)选择json', command=choice_json)
    # btn9.pack(side=tkinter.LEFT)
    # btn2 = Button(temp_fr0, text='(d)获取纯文字', command=html_pure_text)
    # btn2.pack(side=tkinter.LEFT)
    # btn10 = Button(temp_fr0, text='xpath内容分析', command=xpath_finder)
    # btn10.pack(side=tkinter.LEFT)
    btn9 = Button(temp_fr0, text='json格式化', command=jsonformat)
    btn9.pack(side=tkinter.LEFT)
    style = ttk.Style()
    style.map("TEST.TButton",
        foreground=[('!focus', '#EE6363')],
    )
    lab2 = Label(temp_fr0, text="正在请求", style='TEST.TButton')
    lab2.pack(side=tkinter.LEFT)
    btn1 = Button(temp_fr0, text='显示/隐藏配置', command=switch_show)
    btn1.pack(side=tkinter.RIGHT)
    # btn6 = Button(temp_fr0, text='生成[requests]代码', command=test_code)
    # btn6.pack(side=tkinter.RIGHT)
    # btn7 = Button(temp_fr0, text='生成[scrapy]代码', command=scrapy_code)
    # btn7.pack(side=tkinter.RIGHT)
    # btn8 = Button(temp_fr0, text='生成[urllib]代码', command=urllib_code)
    # btn8.pack(side=tkinter.RIGHT)
    btn9 = Button(temp_fr0, text='选择生成代码', command=_select_create_code)
    btn9.pack(side=tkinter.RIGHT)

    def _swich_encd(*a):
        s = ent1.get().strip()
        if s == 'utf-8':
            ent1.delete(0,tkinter.END)
            ent1.insert(0,'gbk')
        elif s == 'gbk':
            ent1.delete(0,tkinter.END)
            ent1.insert(0,'utf-8')
        else:
            ent1.delete(0,tkinter.END)
            ent1.insert(0,'utf-8')

    def _swich_quote(*a):
        s = ent2.get().strip()
        if s == 'yes':
            ent2.delete(0,tkinter.END)
            ent2.insert(0,'no')
        elif s == 'no':
            ent2.delete(0,tkinter.END)
            ent2.insert(0,'yes')
        else:
            ent2.delete(0,tkinter.END)
            ent2.insert(0,'yes')

    ent1 = Entry(temp_fr0,width=6)
    ent1.pack(side=tkinter.RIGHT)
    btnurlencode = Button(temp_fr0, width=14, text='url中文编码格式', command=_swich_encd)
    btnurlencode.pack(side=tkinter.RIGHT)
    urlenc = (setting.get('urlenc') or 'utf-8') if setting is not None else 'utf-8'
    ent1.insert(0, urlenc)
    ent2 = Entry(temp_fr0,width=4)
    ent2.pack(side=tkinter.RIGHT)
    btnurlencode1 = Button(temp_fr0, width=18, text='url是否编码“+”符号', command=_swich_quote)
    btnurlencode1.pack(side=tkinter.RIGHT)
    qplus = (setting.get('qplus') or 'no') if setting is not None else 'no'
    ent2.insert(0, qplus)
    proxy = None
    if setting and setting.get('proxy'):
        varify = re.findall(r'(\d+)\.(\d+)\.(\d+)\.(\d+):(\d+)', setting.get('proxy'))
        if varify:
            a,b,c,d,e = map(int, varify[0])
            if a >= 0 and a <= 255 and b >= 0 and b <= 255 and c >= 0 and c <= 255 and d >= 0 and d <= 255 and e >= 0 and e <= 65535:
                Label(temp_fr0, text='使用代理: {}'.format(setting.get('proxy'))).pack(side=tkinter.RIGHT)
                proxy = setting.get('proxy').strip()
            else:
                Label(temp_fr0, text='错误的代理: {}'.format(setting.get('proxy'))).pack(side=tkinter.RIGHT)

    temp_fr1 = Frame(fr,highlightthickness=lin)
    temp_fold_fr1 = Frame(temp_fr1)
    lb1 = Label (temp_fold_fr1,text='HTML文本展示')
    tx1 = Text  (temp_fold_fr1,height=1,width=1,font=ft,wrap='none')
    lb1.pack(side=tkinter.TOP)
    tx1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP,padx=pdx,pady=pdy)

    temp_fold_fr2 = Frame(temp_fr1)
    temp_fold_fold_fr1 = Frame(temp_fold_fr2)
    temp_fold_fold_fr2 = Frame(temp_fold_fr2)
    lb2 = Label (temp_fold_fold_fr1,text='配置数据')
    tx2 = Text  (temp_fold_fold_fr1,height=1,width=1,font=ft)
    lb2.pack(side=tkinter.TOP)
    tx2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP,padx=pdx,pady=pdy)
    lb3 = Label (temp_fold_fold_fr2,text='执行说明')
    tx3 = Text  (temp_fold_fold_fr2,height=1,width=1,font=ft)
    lb3.pack(side=tkinter.TOP)
    tx3.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP,padx=pdx,pady=pdy)
    temp_fold_fold_fr1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)
    temp_fold_fold_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)
    temp_fold_fr1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.LEFT)
    # temp_fold_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.LEFT)
    temp_fr1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)

    temp_fr2 = Frame(fr,highlightthickness=lin)
    lb4 = Label (temp_fr2,text='解析内容[Esc 开启/关闭解析显示]')
    tx4 = Text  (temp_fr2,height=1,width=1,font=ft)
    lb4.pack(side=tkinter.TOP)
    tx4.pack(fill=tkinter.BOTH,expand=True,padx=pdx,pady=pdy)
    #temp_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.BOTTOM)

    frame_setting[fr] = {}
    frame_setting[fr]['type'] = 'response'
    frame_setting[fr]['fr_setting'] = setting # 用于生成代码时候需要调用到
    frame_setting[fr]['fr_html_content'] = tx1
    frame_setting[fr]['fr_local_set'] = tx2 # 当前解析脚本的方法类型以及配置
    frame_setting[fr]['fr_local_info'] = tx3 # 一个辅助说明的文本空间
    frame_setting[fr]['fr_parse_info'] = tx4
    frame_setting[fr]['fr_temp2'] = temp_fr2 # 解析输出的 Text 框，这里用外部frame是为了挂钩esc按键显示/关闭该窗口
    frame_setting[fr]['fr_urlenc'] = ent1
    frame_setting[fr]['fr_qplus'] = ent2

    # 统一数据格式
    def format_content(content):
        def parse_content_type(content, types=['utf-8','gbk']):
            for tp in types:
                try:    return tp, content.decode(tp)
                except: pass
            etp = types[:]
            try:
                import chardet
                tp = chardet.detect(content)['encoding']
                if tp not in etp: etp.append(tp); return tp, content.decode(tp)
            except: pass
            import re # 有些网站明明就是gbk或utf-8编码但就是解析失败，所以用errors=ignore模式下中文数量来兜底编码格式
            utf8len = len(re.findall('[\\u4e00-\\u9fa5]', content.decode('utf-8', errors='ignore')[:4096]))
            gbklen  = len(re.findall('[\\u4e00-\\u9fa5]', content.decode('gbk', errors='ignore')[:4096]))
            gtp = 'gb18030' if gbklen > utf8len else 'utf-8'
            tp = '{} {}'.format(gtp, 'ignore')
            return tp, content.decode(gtp, errors='ignore')
        if type(content) is bytes:
            typ,content = parse_content_type(content)
            insert_txt(tx3, '解析格式：{}'.format(typ))
            return typ,content
        else:
            einfo = 'type:{} is not in type:[bytes]'.format(type(content))
            raise TypeError(einfo)

    from urllib import request
    from urllib.parse import quote, unquote, unquote_plus, quote_plus, urlencode

    if qplus == 'yes':
        _quote,_unquote = quote_plus,unquote_plus
        _rep = '%2B'
    elif qplus == 'no':
        _quote,_unquote = quote,unquote
        _rep = '+'
    def quote_val(url, enc): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+_quote(_unquote(i.group(2), encoding=enc), encoding=enc).replace('+', _rep), url)

    def urllib_myget(url, headers, proxies):
        r = request.Request(url, method='GET')
        for k, v in headers.items():
            if k.lower() == 'accept-encoding': continue # urllib并不自动解压缩编码，所以忽略该headers字段
            r.add_header(k, v)
        opener = request.build_opener(request.ProxyHandler(proxies))
        return opener.open(r)

    def urllib_mypost(url, headers, body, proxies):
        r = request.Request(url, method='POST')
        for k, v in headers.items():
            if k.lower() == 'accept-encoding': continue # urllib并不自动解压缩编码，所以忽略该headers字段
            r.add_header(k, v)
        opener = request.build_opener(request.ProxyHandler(proxies))
        return opener.open(r, data=body)

    proxies = {'http':'http://{}'.format(proxy), 'https':'http://{}'.format(proxy)} if proxy else None
    def _request(method,url,headers,body):
        # from .tab import dprint
        # dprint(url)
        if requests.__dict__.get('get') and requests is not None:
            rurl = quote_val(_unquote(url, encoding=urlenc), enc=urlenc)
            if method == 'GET':
                s = requests.get(rurl,headers=headers,verify=False,proxies=proxies)
                tp,content = format_content(s.content)
            elif method == 'POST':
                if isinstance(body, str): body = body.encode('utf-8')
                s = requests.post(rurl,headers=headers,data=body,verify=False,proxies=proxies)
                tp,content = format_content(s.content)
        else:
            # 备用的请求工具，主要还是考虑如果 requests 不能用的情况下依旧至少能够走完发包的流程
            url = quote_val(_unquote(url, encoding=urlenc), enc=urlenc)
            if method == 'GET':
                s = urllib_myget(url, headers, proxies)
                tp, content = format_content(s.read())
            elif method == 'POST':
                body = urlencode(body).encode('utf-8') if isinstance(body, dict) else body.encode('utf-8')
                s = urllib_mypost(url, headers, body, proxies)
                tp, content = format_content(s.read())
        return tp, content

    def _handle_dh_key_too_small():
        try:
            requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
            requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += ':HIGH:!DH:!aNULL'
        except AttributeError:
            pass
        import ssl
        ssl._DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

    # 为了兼容旧的 3DES 传输，（新标准中删除是因为不安全，但是架不住有些服务器用，所以需要考虑兼容）
    _bak_init_poolmanager = requests.adapters.HTTPAdapter.init_poolmanager
    _bak_proxy_manager_for = requests.adapters.HTTPAdapter.proxy_manager_for
    def create_ssl_context():
        import ssl
        ctx = ssl.create_default_context()
        ctx.set_ciphers( 'ECDH+3DES:DH+3DES:RSA+3DES:!aNULL:!eNULL:!MD5' )
        if getattr(ctx, 'check_hostname', None) is not None:
            ctx.check_hostname = False
        return ctx
    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = create_ssl_context()
        return _bak_init_poolmanager(self, *args, **kwargs)
    def proxy_manager_for(self, *args, **kwargs):
        kwargs['ssl_context'] = create_ssl_context()
        return _bak_proxy_manager_for(self, *args, **kwargs)
    def _handle_3des_drop_out_stand():
        requests.adapters.HTTPAdapter.init_poolmanager = init_poolmanager
        requests.adapters.HTTPAdapter.proxy_manager_for = proxy_manager_for
    def _unhook_handle_3des_drop_out_stand():
        requests.adapters.HTTPAdapter.init_poolmanager = _bak_init_poolmanager
        requests.adapters.HTTPAdapter.proxy_manager_for = _bak_proxy_manager_for

    tp = None
    extra = []
    import queue
    Q = queue.Queue()
    # 使用新增线程执行请求，防止卡顿，优化。
    def req_in_thead():
        nonlocal tp, extra, fr, Q
        def inier_func():
            nonlocal tp, extra, fr
            if setting is not None:
                method  = setting.get('method')
                url     = setting.get('url')
                headers = setting.get('headers')
                body    = setting.get('body')
                try:
                    tp, content = _request(method,url,headers,body)
                except:
                    einfo = traceback.format_exc()
                    if 'dh key too small' in einfo:
                        extra.append('dh key too small')
                        _handle_dh_key_too_small()
                        tp, content = _request(method,url,headers,body)
                    elif '''SSLError("bad handshake: SysCallError(-1, 'Unexpected EOF')",)''' in einfo:
                        extra.append('3des drop out stand')
                        _handle_3des_drop_out_stand()
                        tp, content = _request(method,url,headers,body)
                        _unhook_handle_3des_drop_out_stand()
                    else:
                        tkinter.messagebox.showinfo('Error',einfo)
                        Q.put(["请求失败", einfo])
                        raise
                return content
        Q.put(["请求成功", inier_func()])
        frame_setting[fr]['fr_parse_type'] = tp
        frame_setting[fr]['fr_extra'] = extra
    threading.Thread(target=req_in_thead).start()
    def loop_in_tkinter():
        nonlocal Q, tx1
        from .tab import nb
        while Q.qsize():
            try:
                lab2['text'], content = Q.get_nowait()
                insert_txt(tx1, content)
            except queue.Empty:
                pass
        nb.after(200, loop_in_tkinter)
    loop_in_tkinter()
    # tp = None
    # extra = []
    # if setting is not None:
    #     method  = setting.get('method')
    #     url     = setting.get('url')
    #     headers = setting.get('headers')
    #     body    = setting.get('body')
    #     try:
    #         tp, content = _request(method,url,headers,body)
    #     except:
    #         einfo = traceback.format_exc()
    #         if 'dh key too small' in einfo:
    #             extra.append('dh key too small')
    #             _handle_dh_key_too_small()
    #             tp, content = _request(method,url,headers,body)
    #         else:
    #             tkinter.messagebox.showinfo('Error',einfo)
    #             raise
    #         # insert_txt(tx1, traceback.format_exc())
    # frame_setting[fr]['fr_parse_type'] = tp
    # frame_setting[fr]['fr_extra'] = extra
    return fr




# 暂时考虑用下面的方式来试着挂钩函数执行的状态。
# 不过似乎还是有些漏洞，先就这样，后面再补充完整。
# 当初我不知道我为啥要这么傻逼的使用这样的方式来处理，可能当时还没有找到怎么实现 tkinter 的多线程执行怎么处理吧
# 现在已经明白了，所有 tkinter 的控件一定要在住线程内执行，可以使用无限递归的的函数来实现 重点是 after 函数，
import sys
__org_stdout__ = sys.stdout
__org_stderr__ = sys.stderr
# class stdhooker:
#     def __init__(self, hook=None, style=None):
#         if hook.lower() == 'stdout':
#             self.__org_func__ = __org_stdout__
#         elif hook.lower() == 'stderr':
#             self.__org_func__ = __org_stderr__
#         else:
#             raise 'stdhooker init error'
#         self.cache = ''
#         self.style = style
#         self.predk = {}
#     def write(self,text):
#         self.logtx = get_tx()
#         if self.logtx not in self.predk:
#             self.predk[self.logtx] = 0
#         self.cache += text
#         if '\n' in self.cache:
#             _text = self.cache.rsplit('\n',1)
#             self.cache = '' if len(_text) == 1 else _text[1]
#             _text_ = _text[0] + '\n'
#             if self.logtx:
#                 try:
#                     self.logtx.insert(tkinter.END, _text_)
#                 except:
#                     self.logtx.insert(tkinter.END, re.sub('[\uD800-\uDBFF][\uDC00-\uDFFF]|[\U00010000-\U0010ffff]','',_text_))
#                 # self.logtx.insert(tkinter.END, _text_)
#                 self.logtx.see(tkinter.END)
#                 self.logtx.update()
#     def flush(self):
#         try:
#             self.__org_func__.flush()
#         except:
#             pass
# def get_tx():
#     for i in inspect.stack():
#         if '__very_unique_cd__' in i[0].f_locals:
#             return i[0].f_locals['cd']
# sys.stdout = stdhooker('stdout',style='normal')



_w3lib_html_body_declared_encoding_code = """
# 这里的解码代码 == from w3lib.encoding import html_body_declared_encoding，只是
# 这里的代码可以不需要依赖 w3lib库了，更加自由一点。另外，这是 scrapy默认的对未知编码进行解码的方式
import re, codecs, encodings
def html_body_declared_encoding(html_body_str:bytes):
    _TEMPLATE = r'''%s\\s*=\\s*["']?\\s*%s\\s*["']?'''
    _SKIP_ATTRS = '''(?x)(?:\\\\s+
        [^=<>/\\\\s"'\\x00-\\x1f\\x7f]+  # Attribute name
        (?:\\\\s*=\\\\s*
        (?:  # ' and " are entity encoded (&apos;, &quot;), so no need for \\', \\"
            '[^']*'   # attr in '
            |
            "[^"]*"   # attr in "
            |
            [^'"\\\\s]+  # attr having no ' nor "
        ))?
    )*?'''
    _HTTPEQUIV_RE = _TEMPLATE % ('http-equiv', 'Content-Type')
    _CONTENT_RE = _TEMPLATE % ('content', r'(?P<mime>[^;]+);\\s*charset=(?P<charset>[\\w-]+)')
    _CONTENT2_RE = _TEMPLATE % ('charset', r'(?P<charset2>[\\w-]+)')
    _XML_ENCODING_RE = _TEMPLATE % ('encoding', r'(?P<xmlcharset>[\\w-]+)')
    _BODY_ENCODING_PATTERN = r'<\\s*(?:meta%s(?:(?:\\s+%s|\\s+%s){2}|\\s+%s)|\\?xml\\s[^>]+%s|body)' % (
        _SKIP_ATTRS, _HTTPEQUIV_RE, _CONTENT_RE, _CONTENT2_RE, _XML_ENCODING_RE)
    _BODY_ENCODING_STR_RE = re.compile(_BODY_ENCODING_PATTERN, re.I)
    _BODY_ENCODING_BYTES_RE = re.compile(_BODY_ENCODING_PATTERN.encode('ascii'), re.I)
    DEFAULT_ENCODING_TRANSLATION = {
        'ascii': 'cp1252', 'big5': 'big5hkscs', 'euc_kr': 'cp949', 'gb2312': 'gb18030', 'gb_2312_80': 'gb18030', 'gbk': 'gb18030', 
        'iso8859_11': 'cp874', 'iso8859_9': 'cp1254', 'latin_1': 'cp1252', 'macintosh': 'mac_roman', 'shift_jis': 'cp932',
        'tis_620': 'cp874', 'win_1251': 'cp1251', 'windows_31j': 'cp932', 'win_31j': 'cp932', 'windows_874': 'cp874', 'win_874': 'cp874',
        'x_sjis': 'cp932', 'zh_cn': 'gb18030'
    }
    def _c18n_encoding(encoding):
        normed = encodings.normalize_encoding(encoding).lower()
        return encodings.aliases.aliases.get(normed, normed)
    def resolve_encoding(encoding_alias):
        c18n_encoding = _c18n_encoding(encoding_alias)
        translated = DEFAULT_ENCODING_TRANSLATION.get(c18n_encoding, c18n_encoding)
        try: return codecs.lookup(translated).name
        except LookupError: return None
    chunk = html_body_str[:4096]
    match = _BODY_ENCODING_BYTES_RE.search(chunk) if isinstance(chunk, bytes) else _BODY_ENCODING_STR_RE.search(chunk)
    if match:
        encoding = match.group('charset') or match.group('charset2') or match.group('xmlcharset')
        if encoding: return resolve_encoding(encoding)
"""

# 生成代码临时放在这里
def code_window(setting=None):
    fr = Frame()
    ft = Font(family='Consolas',size=10)

    if setting.get('type') == 'request':
        va,prox = setting.get('fr_proxy')
        proxy   = prox.get().strip() if va.get() else None
    if setting.get('type') == 'response':
        proxy   = setting.get('fr_setting').get('proxy')
    if proxy and setting.get('code_string'):
        rep = "None # {'http':'http://127.0.0.1:8888', 'https':'http://127.0.0.1:8888'}"
        rpl = "{'http':'http://" +proxy+ "', 'https':'http://" +proxy+ "'}"
        setting['code_string'] = setting['code_string'].replace(rep, rpl)

    def _execute_code(*a):
        from .tab import execute_code
        execute_code()

    def save_script_in_desktop(*a):
        name = askstring('脚本名','请输入脚本文件名，尽量小写无空格。')
        if not name: return
        if not name.endswith('.py'): name += '.py'
        desktop_script = os.path.join(os.path.expanduser("~"),'Desktop\\{}'.format(name))
        if not os.path.isfile(desktop_script):
            with open(desktop_script, 'w', encoding='utf-8') as f:
                f.write(tx.get(0.,tkinter.END))
        else:
            tkinter.messagebox.showwarning('脚本已存在','脚本已存在')

    def _add_w3lib_html_body_declared_encoding_code(*a):
        script = tx.get(0.,tkinter.END).rstrip('\n')
        if "def html_body_declared_encoding" not in script:
            tx.delete(0.,tkinter.END)
            topcode = _w3lib_html_body_declared_encoding_code.lstrip()
            script = topcode + script
            tx.insert(0.,script)
            tx.update()

    def _add_vthread_pool(*a):
        script = tx.get(0.,tkinter.END).rstrip('\n')
        scriptfile = os.path.join(os.path.split(__file__)[0],'py_vthread.py')
        if "class KillThreadParams(Exception): pass" not in script:
            with open(scriptfile, 'r', encoding='utf-8') as f:
                topcode = f.read().strip()
            tx.delete(0.,tkinter.END)
            script = topcode + '\n'*10 + script
            tx.insert(0.,script)
            tx.update()

    def _add_mini_requests(*a):
        script = tx.get(0.,tkinter.END).rstrip('\n')
        scriptfile = os.path.join(os.path.split(__file__)[0],'py_mini_requests.py')
        if "mini_requests" not in script:
            with open(scriptfile, 'r', encoding='utf-8') as f:
                topcode = f.read().strip()
            tx.delete(0.,tkinter.END)
            script = topcode + '\n'*10 + script
            tx.insert(0.,script)
            tx.update()

    tframe = Frame(fr)
    tframe.pack(side=tkinter.TOP)

    btn00 = Button(tframe, text='增加w3lib编码解析函数', command=_add_w3lib_html_body_declared_encoding_code)
    btn00.pack(side=tkinter.LEFT)
    btn01 = Button(tframe, text='增加vthread线程池装饰器代码', command=_add_vthread_pool)
    btn01.pack(side=tkinter.LEFT)
    btn02 = Button(tframe, text='增加mini_requests脚本', command=_add_mini_requests)
    btn02.pack(side=tkinter.LEFT)
    btn1 = Button(tframe, text='保存脚本到桌面', command=save_script_in_desktop)
    btn1.pack(side=tkinter.LEFT)
    btn2 = Button(tframe, text='执行代码 [Alt+v]', command=_execute_code)
    btn2.pack(side=tkinter.LEFT)
    tx = Text(fr,height=1,width=1,font=ft)
    cs = setting.get('code_string')
    if cs:
        tx.delete(0.,tkinter.END)
        tx.insert(0.,cs)
    tx.pack(fill=tkinter.BOTH,expand=True,padx=pdx,pady=pdy)

    temp_fr2 = Frame(fr,highlightthickness=lin)
    lb = Label (temp_fr2,text='执行结果[Esc 显示/隐藏执行结果]')
    cd = Text  (temp_fr2,height=1,width=1,font=ft)
    lb.pack(side=tkinter.TOP)
    cd.pack(fill=tkinter.BOTH,expand=True,padx=pdx,pady=pdy)

    # 在 tkinter 里面实现线程真的稍微有点累人的。
    import queue
    Q = queue.Queue() # 用来传递打印的数据
    S = queue.Queue() # 用来传递脚本数据
    def execute_func_window():
        # 额外的线程有一个非常需要注意的地方，就是涉及到任何使用 tkinter 内的结构的时候一定不能在这里实现
        # 一定都要使用 Queue 来传递参数。窗口自己带一个超级递归的循环。
        nonlocal Q, S
        Q.put('V|GETSCRIPT')
        cs = S.get()
        td = tempfile.mkdtemp()
        tf = os.path.join(td,'temp.py')
        with open(tf,'w',encoding='utf-8') as f:
            f.write(cs)
        s = sys.executable
        s = s + ' ' + tf
        import subprocess
        p = subprocess.Popen(s, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, encoding='utf-8')
        Q.put('V|DELETE')
        Q.put('============================== start ==============================\n')
        for line in iter(p.stdout.readline, ''):
            if line:
                Q.put(line)
            else:
                break
        Q.put('==============================  end  ==============================')
        p.wait()
        p.stdout.close()
        shutil.rmtree(td)

    def loop_in_tkinter():
        __very_unique_cd__ = None
        nonlocal cd, Q, S
        from .tab import nb
        c = []
        while Q.qsize():
            try:
                i = Q.get_nowait()
                if i == 'V|DELETE':
                    cd.delete(0., tkinter.END)
                elif i == 'V|GETSCRIPT':
                    cs = tx.get(0.,tkinter.END)
                    S.put(cs)
                else:
                    try:
                        cd.insert(tkinter.END, i)
                    except:
                        cd.insert(tkinter.END, re.sub('[\uD800-\uDBFF][\uDC00-\uDFFF]|[\U00010000-\U0010ffff]','',i))
                    cd.see(tkinter.END)
                    cd.update()
            except queue.Empty:
                pass
        nb.after(200, loop_in_tkinter)
    loop_in_tkinter()

    def execute_func():
        threading.Thread(target=execute_func_window).start()

    frame_setting[fr] = {}
    frame_setting[fr]['type'] = 'code'
    frame_setting[fr]['execute_func'] = execute_func
    frame_setting[fr]['fr_temp2'] = temp_fr2 # 代码执行框，这里仍需挂钩esc按键显示/关闭该窗口

    try:
        from idlelib.colorizer import ColorDelegator
        from idlelib.percolator import Percolator
        p = ColorDelegator()
        Percolator(tx).insertfilter(p)
    except:
        traceback.print_exc()

    return fr






# 暂时废弃"后验证代码的功能"
post_verification_model = r"""
    '''
    # [后验证代码模板]
    # 只需在正常请求前加上下面两段便可处理重验证的操作
    # 该重验证包含了，原始请求的重新提交以及验证次数的接口暴露
    # 并且加了这一段验证代码之后你只需要对验证更新的部分修改即可。

    # 使用时只需要修改两处
    # 1. 修改后验证请求的信息的请求信息
    # 2. 修改后验证的更新请求配置的信息（通常更新cookie，已有基本模板）
    def parse(self, response):
        def revalidate(response):
            times = response.meta.get('_revalidate_times') or 0
            # 重验次数，为了测试，这里使用的条件是，重验次数少于2则直接重验
            # 几乎就等于无条件重验证两次，在实际情况下请注意验证条件的编写
            if times >= 2:
                return True

        if not revalidate(response):
            # ============ 请修改此处的验证请求信息 =============
            # 这里只需要传入重验证需要请求的信息即可，会自动重验证和重新请求本次验证失败的请求
            rurl     = 'https://www.baidu.com/'
            rheaders = {}
            rbody    = None # body为None则验证请求为get,否则为post
            yield self.revalidate_pack(response, rurl, rheaders, rbody)
            return

        # 后续是正常的解析操作
    '''
    def revalidate_pack(self, response, rurl=None, rheaders=None, rbody=None):
        def mk_revalidate_request(_plusmeta):
            method = 'GET' if rbody is None else 'POST'
            meta = {}
            meta['_plusmeta'] = _plusmeta
            r = Request(
                    rurl,
                    method   = method,
                    headers  = rheaders,
                    body     = rbody,
                    callback = self.revalidate_parse,
                    meta     = meta,
                    dont_filter = True,
                )
            return r
        _plusmeta = dict(
            url     = response.request.url,
            headers = response.request.headers.to_unicode_dict(),
            body    = response.request.body.decode(),
            method  = response.request.method,
            meta    = response.request.meta,
            cbname  = response.request.callback.__name__,
        )
        return mk_revalidate_request(_plusmeta)

    def revalidate_parse(self, response):
        '''
        验证请求结束，返回验证信息则更新一些信息，重新对原来未验证的请求进行验证
        有时是通过 set-cookie 来实现更新 cookie 的操作，所以这里的 cookie 需要考虑更新的操作。
        可以通过 response.headers.to_unicode_dict() 将返回的headers里面的 key value 转换成字符串
        这样操作会少一些处理 bytes 类型的麻烦。
        '''
        def update(_plusmeta):
            # ============ 请修改此处的验证跟新 =============
            # 一般的后验证通常会在这里对 _plusmeta 中的 cookie 更新，由于to_unicode_dict函数的关系
            # 所有的key都是小写，所以不用担心大小写问题，这里给了一个简单的小模板，如需更多功能请自行修改
            # 这里也可以更新一些 self 的参数，将验证进行持久化
            newcookie = response.headers.to_unicode_dict().get('set-cookie')
            if newcookie:
                _plusmeta['headers']['cookie'] = newcookie

            _plusmeta['meta']['_revalidate_times'] = (_plusmeta['meta'].get('_revalidate_times') or 0) + 1
            return _plusmeta

        _plusmeta = update(response.meta['_plusmeta'])
        url     = _plusmeta['url']
        method  = _plusmeta['method']
        headers = _plusmeta['headers']
        body    = _plusmeta['body']
        meta    = _plusmeta['meta']
        cbname  = _plusmeta['cbname']
        r = Request(
                url,
                method   = method,
                headers  = headers,
                body     = body,
                callback = getattr(self, cbname),
                meta     = meta,
                dont_filter = True,
            )
        yield r
"""

single_script_comment_part1 = '''
    # 工具作者有时会偏向将某些临时生成的文件放到固定地址(例如桌面)，统一管理，便于工作
    # 若使用相对路径存放文件，则无需添加 file:/// 的前缀
    desktoppath = os.path.join(os.path.expanduser("~"),'Desktop')  # 获取桌面地址的通用代码
    filename    = 'file:///' + os.path.join(desktoppath, filename) # 使用绝对地址时存文件需增加前缀，注意
    jobdir      = os.path.join(desktoppath, jobdir)
'''.strip('\n')

_pyinstaller_scrapy = '--add-data "$sysexec\\Lib\\site-packages\\scrapy;scrapy" --add-data "$sysexec\\Lib\\email;email" --add-data "$sysexec\\Lib\\site-packages\\twisted;twisted" --add-data "$sysexec\\Lib\\site-packages\\queuelib;queuelib" --add-data "$sysexec\\Lib\\sqlite3;sqlite3" --add-binary "$sysexec\\DLLs\\_sqlite3.pyd;." --add-binary "$sysexec\\DLLs\\sqlite3.dll;." --exclude-module numpy --exclude-module scipy --exclude-module matplotlib --exclude-module PyQt5 --noupx'
_pyinstaller_scrapy = _pyinstaller_scrapy.replace('$sysexec', os.path.dirname(sys.executable))
single_script_comment_part2 = """
    # 基础中间件介绍
    # 通过实例动态增加中间件（解耦了之前只能通过配置中间件字符串），方便单脚本实现增加中间件功能，例如数据库存储方面的内容。
    # 便于单脚本利用别人的中间件。（将别人的中间件脚本粘贴进该脚本，实例化添加即可。示例如下，解开注释到 #(1) 即可测试。）
    # class VPipeline(object):
    #     def process_item(self, item, spider):
    #         print('\\n==== 这里是动态增加的“下载中间件”部分 ====\\n')
    #         return item
    # for i in p.crawlers: i.engine.scraper.itemproc._add_middleware(VPipeline()) #(1)

    # for i in p.crawlers: i.engine.scraper.spidermw._add_middleware(...)         #(2) 这里的...需要一个对应的中间件对象
    # for i in p.crawlers: i.engine.downloader.middleware._add_middleware(...)    #(3) 这里的...需要一个对应的中间件对象
    #1) 通过对象动态增加 itemmiddlewares，目前仅在数据管道部分这种处理方式比较常用（因默认item中间件为空，不会被默认配置影响）
    #2) 通过对象动态增加 spidermiddlewares     # i.engine.scraper.spidermw.middlewares        # 当前全部“爬虫中间件”
    #3) 通过对象动态增加 downloadermiddlewares # i.engine.downloader.middleware.middlewares   # 当前全部“下载中间件”
    #*) 注意: 2,3两种中间件的动态增加不常用。因 p.crawl 函数执行后就已初始化默认中间件顺序。新的中间件只能“后添加”，缺乏灵活。


    # 【图片下载】 中间件介绍
    # 图片相关的文件下载中间件的添加，注意：图片相关的资源需要绑定 spider 以及 crawler。示例如下。
    # 在一般的脚本 item['src'] 中添加字符串下载地址即可，一个 item 一个字符串下载地址，便于管理。详细阅读下面代码。
    # 解开下面的代码块即可使用该功能
    # import logging, hashlib
    # from scrapy.pipelines.images import ImagesPipeline
    # from scrapy.exceptions import DropItem
    # class VImagePipeline(ImagesPipeline):
    #     def get_media_requests(self, item, info):
    #         yield Request(item['src'], meta=item) 
    #     def file_path(self, request, response=None, info=None):
    #         url = request if not isinstance(request, Request) else request.url
    #         image_name = request.meta.get('image_name') # 使用 item中的 image_name 字段作为文件名进行存储，没有该字段则使用 url的 md5作为文件名存储
    #         image_name = re.sub(r'[/\\\\:\\*"<>\\|\\?]', '_', image_name).strip()[:80] if image_name else hashlib.md5(url.encode()).hexdigest()
    #         return '%s.jpg' % image_name # 生成的图片文件名字，此处可增加多级分类路径（路径不存在则自动创建），使用 image_name 请注意重名可能性。
    #     def item_completed(self, results, item, info): # 判断下载是否成功
    #         k, v = results[0]
    #         if not k: logging.info('download fail {}'.format(item))
    #         else:     logging.info('download success {}'.format(item))
    #         item['image_download_stat'] = 'success' if k else 'fail'
    #         item['image_path'] = v['path'] if k else None # 保留文件名地址
    #         return item
    # for i in p.crawlers: 
    #     vimage = VImagePipeline('./image',settings=i.settings) # 生成的文件地址，默认跟随脚本路径下生成的一个 image文件夹
    #     vimage.spiderinfo = vimage.SpiderInfo(i.spider)
    #     vimage.crawler = i
    #     i.engine.scraper.itemproc._add_middleware(vimage)


    # 【数据库存储】 中间件介绍
    # 当你需要直接将数据传入数据库的时候只需要在 item里面加一个字段: item['__mysql__'] = __mysql__
    # 代码片如下：
    #         d['__mysql__'] = {
    #             'host':'127.0.0.1',  # str 【可选】 （默认 'localhost'）
    #             'port':3306 ,        # int 【可选】 （默认 3306）
    #             'user':'user',       # str 该配置是必须的
    #             'password':'mypass', # str 该配置是必须的
    #             'table':'mytable',   # str 该配置是必须的（如果数据库内没有该表则会自动创建）注意！创建后的表结构不可改变。
    #             'db':'mydb',         # str 【可选】 （默认vrequest）（如果没有则自动创建）
    #         }
    # 这个字段里面需要详细描述需要连接的数据库以及需要传入的表的名字，
    # 注意，这里会根据 __mysql__ 的值的 hash 进行数据库连接池的创建，不同配置使用不同连接池，优化连接
    # 之所以使用这样的接口处理是因为，这样可以使得一个任务能根据配置写入不同的数据库，非常方便
    # 解开下面的代码块即可使用该功能
    # import hmac, logging, traceback
    # from twisted.enterprise import adbapi
    # class VMySQLPipeline(object):
    #     dbn = {}
    #     def process_item(self, item, spider):
    #         mysql_config = item.pop('__mysql__', None) # 存储时自动删除配置
    #         if mysql_config and item:
    #             if type(mysql_config) is dict:
    #                 table = mysql_config.pop('table', None)
    #                 db = mysql_config.get('db', None) or 'vrequest'
    #                 mysql_config.setdefault('charset','utf8mb4')
    #                 mysql_config.setdefault('db', db)
    #                 dbk = hmac.new(b'',json.dumps(mysql_config, sort_keys=True).encode(),'md5').hexdigest()
    #                 if dbk not in self.dbn:
    #                     self.dbn[dbk] = adbapi.ConnectionPool('pymysql', **mysql_config)
    #                     self.init_database(self.dbn[dbk], mysql_config, db, table, item)
    #                 self.dbn[dbk].runInteraction(self.insert_item, db, table, item)
    #                 return item
    #             else:
    #                 raise TypeError('Unable Parse mysql_config type:{}'.format(type(mysql_config)))
    #         else:
    #             return item
    #     def insert_item(self, conn, db, table, item):
    #         table_sql = ''.join(["'{}',".format(json.dumps(v, ensure_ascii=False).replace("'","\\\\'")) for k,v in item.items()])
    #         insert_sql = 'INSERT INTO `{}`.`{}` VALUES({})'.format(db, table, table_sql.strip(','))
    #         try: 
    #             conn.execute(insert_sql)
    #             logging.info('insert sql success')
    #         except Exception as e: 
    #             logging.info('insert sql fail: {}'.format(insert_sql))
    #             logging.error(traceback.format_exc())
    #     def init_database(self, pool, mysql_config, db, table, item):
    #         # 需要注意的是，在一些非常老的版本的mysql 里面并不支持 utf8mb4。这是 mysql 的设计缺陷，赶紧使用大于 5.5 版本的 mysql !
    #         # 创建db，创建表名，所有字段都以 MEDIUMTEXT 存储，用 json.dumps 保证了数据类型也能存储，后续取出时只需要每个值 json.loads 这样就能获取数据类型
    #         # 例如一个数字类型    123 -> json.dumps -> '123' -> json.loads -> 123，统一类型存储，取出时又能保证数据类型，这种处理会很方便
    #         # MEDIUMTEXT 最大能使用16M 的长度，所以对于一般的 html 文本也非常足够。如有自定义字段类型的需求，请注意修改该处。
    #         db, charset = mysql_config.pop('db'), mysql_config.get('charset')
    #         try:
    #             conn = pool.dbapi.connect(**mysql_config)
    #             cursor = conn.cursor()
    #             table_sql = ''.join(['`{}` MEDIUMTEXT NULL,'.format(str(k)) for k,v in item.items()])
    #             cursor.execute('Create Database If Not Exists {} Character Set {}'.format(db, charset))
    #             cursor.execute('Create Table If Not Exists `{}`.`{}` ({})'.format(db, table, table_sql.strip(',')))
    #             conn.commit(); cursor.close(); conn.close()
    #         except Exception as e:
    #             traceback.print_exc()
    # for i in p.crawlers: i.engine.scraper.itemproc._add_middleware(VMySQLPipeline())


    # 【视频下载】 中间件介绍
    # 以下包含了比较主流的下载器的使用代码片，请任选一个进行使用。you-get 或 youtube-dl
    # 如果存在一些 m3u8 的视频需要下载，那么建议下载 ffmpeg，并使用 youtube-dl 进行下载。
    # ffmpeg如果没有配置环境变量则请将 ffmpeg_location 设置为 ffmpeg.exe 文件的路径即可。
    # 解开下面的代码块即可使用该功能
    # class VVideoPipeline(object):
    #     def process_item(self, item, spider):
    #         url = item['src']
    #         ### 【you-get】
    #         import you_get.common
    #         you_get.common.skip_existing_file_size_check = True # 防止发现重复视频时会强制要求输入“是否覆盖”，卡住程序，默认不覆盖
    #         you_get.common.any_download(url, output_dir='./video', merge=True, info_only=False)
    #         ### 【youtube-dl】
    #         # from youtube_dl import YoutubeDL
    #         # ytdl = YoutubeDL({'outtmpl': './video/%(title)s.%(ext)s', 'ffmpeg_location':None}) # 如果已配置ffmpeg环境则不用修改
    #         # info = ytdl.extract_info(url, download=True)
    #         return item
    # for i in p.crawlers: i.engine.scraper.itemproc._add_middleware(VVideoPipeline())


    # 如果使用 pyinstaller 打包 scrapy 脚本成为单个 exe，那也很方便
    # 将下面的一行内容拼接到 “pyinstaller -F $你的scrapy单脚本.py ” 命令的后面就可以了。（这里为纯scrapy打包，若还有额外第三方库请按照类似方式添加）
    # $pyinstaller_scrapy
    # 注意，这里的打包默认去除最常见影响大小的库 numpy scipy matplotlib，如有需要引用请删除这里的部分 --exclude-module
""".strip('\n').replace('$pyinstaller_scrapy', _pyinstaller_scrapy)

_main_2_list_2_info_model = r'''
            def mk_url_headers(d):
                def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote_plus(unquote_plus(i.group(2))), url)
                url = response.urljoin(d['href'])
                url = quote_val(url)
                headers = {
                    "accept-encoding": "gzip, deflate",
                    "accept-language": "zh-CN,zh;q=0.9",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
                }
                return url,headers
            url,headers = mk_url_headers(d)
            meta = {}
            meta['proxy'] = self.proxy
            meta['_plusmeta'] = {**_meta, **d} # keys word transfer
            r = Request(
                    url,
                    headers  = headers,
                    callback = self.parse_info,
                    meta     = meta,
                    # method   = 'POST', # if post is used, pls uncomment here and create the body parameter
                    # body     = urlencode(body), 
                )
            yield r

    def parse_info(self, response):
        d = response.meta.get('_plusmeta') or {}
        d['someting1'] = 'pls fill in the fields collected on this page.'
        d['someting2'] = 'pls fill in the fields collected on this page.'
        d['someting3'] = 'pls fill in the fields collected on this page.'
        print('------------------------------ split ------------------------------')
        import pprint
        pprint.pprint(d)
        yield d
'''


_single_distributed = r'''# -*- coding: utf-8 -*-
def hook_to_scrapy_redis(namespace='default'):
    import redis
    from scrapy.http import Request
    from scrapy.utils.python import to_unicode, to_native_str
    from scrapy.utils.misc import load_object
    def request_to_dict(request, spider=None):
        if callable(request.callback): request.callback = _find_method(spider, request.callback)
        if callable(request.errback):  request.errback  = _find_method(spider, request.errback)
        d = {
            'url': to_unicode(request.url),  # urls should be safe (safe_string_url)
            'callback': request.callback,
            'errback': request.errback,
            'method': request.method,
            'headers': dict(request.headers),
            'body': request.body,
            'cookies': request.cookies,
            'meta': request.meta,
            '_encoding': request._encoding,
            'priority': request.priority,
            'dont_filter': request.dont_filter,
            'flags': request.flags,
        }
        if type(request) is not Request:
            d['_class'] = request.__module__ + '.' + request.__class__.__name__
        return d
    def request_from_dict(d, spider=None):
        if d['callback'] and spider: d['callback'] = _get_method(spider, d['callback'])
        if d['errback']  and spider: d['errback']  = _get_method(spider, d['errback'])
        request_cls = load_object(d['_class']) if '_class' in d else Request
        _cls = request_cls(
            url=to_native_str(d['url']),
            callback=d['callback'],
            errback=d['errback'],
            method=d['method'],
            headers=d['headers'],
            body=d['body'],
            cookies=d['cookies'],
            meta=d['meta'],
            encoding=d['_encoding'],
            priority=d['priority'],
            dont_filter=d['dont_filter'],
            flags=d.get('flags'))
        return _cls
    def _find_method(obj, func):
        if obj: return func.__name__
        raise ValueError("Function %s is not a method of: %s" % (func, obj))
    def _get_method(obj, name):
        name = str(name)
        try:
            return getattr(obj, name)
        except AttributeError:
            raise ValueError("Method %r not found in: %s" % (name, obj))
    import pickle
    class _serializer:
        def loads(s):   return pickle.loads(s)
        def dumps(obj): return pickle.dumps(obj, protocol=-1)
    class BaseQueue(object):
        def __init__(self, server, spider, key):
            self.server = server
            self.spider = spider
            self.key = key % {'spider': spider.name}
            self.serializer = _serializer
        def _encode_request(self, request):         obj = request_to_dict(request, self.spider);  return self.serializer.dumps(obj)
        def _decode_request(self, encoded_request): obj = self.serializer.loads(encoded_request); return request_from_dict(obj, self.spider)
        def __len__(self):        raise NotImplementedError
        def push(self, request):  raise NotImplementedError
        def pop(self, timeout=0): raise NotImplementedError
        def clear(self):          self.server.delete(self.key)
    class FifoQueue(BaseQueue):
        def __len__(self):        return self.server.llen(self.key)
        def push(self, request):  self.server.lpush(self.key, self._encode_request(request))
        def pop(self, timeout=0):
            if timeout > 0:
                data = self.server.brpop(self.key, timeout)
                if isinstance(data, tuple):
                    data = data[1]
            else:
                data = self.server.rpop(self.key)
            if data:
                return self._decode_request(data)
    import logging
    from scrapy.dupefilters import BaseDupeFilter
    from scrapy.utils.request import request_fingerprint
    _logger = logging.getLogger(__name__)
    class RFPDupeFilter(BaseDupeFilter):
        logger = _logger
        def __init__(self, server, key, debug=False):
            self.server = server
            self.key = key
            self.debug = debug
            self.logdupes = True
        def request_seen(self, request): return self.server.sadd(self.key, self.request_fingerprint(request)) == 0
        def request_fingerprint(self, request): return request_fingerprint(request)
        def close(self, reason=''): self.clear()
        def clear(self): self.server.delete(self.key)
        def log(self, request, spider):
            if self.debug:
                msg = "Filtered duplicate request: %(request)s"
                self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            elif self.logdupes:
                msg = ("Filtered duplicate request %(request)s"
                       " - no more duplicates will be shown"
                       " (see DUPEFILTER_DEBUG to show all duplicates)")
                self.logger.debug(msg, {'request': request}, extra={'spider': spider})
                self.logdupes = False
    import pprint
    from datetime import datetime, timedelta
    class RedisStatsCollector:
        def __init__(self, crawler):
            self._spider_id_task_format = TASK_STATS
            self._dump      = crawler.settings.getbool('STATS_DUMP')
            self._local_max = 'DEPTH'
            self._maxdp     = 0
            self.server     = redis.StrictRedis(**REDIS_PARAMS)
            self.server.ping()
            self.encoding   = self.server.connection_pool.connection_kwargs.get('encoding')
        def get_stats(self, spider=None):
            _stat = {}
            for key,val in self.server.hgetall(self._spider_id_task_format).items():
                key,val = key.decode(self.encoding),val.decode(self.encoding)
                try:
                    if   key in ['finish_reason']:              _stat[key] = val
                    elif key in ['finish_time', 'start_time']:  _stat[key] = datetime.strptime(val, "%Y-%m-%d %H:%M:%S.%f")
                    else: _stat[key] = int(val) 
                except:
                    _stat[key] = val
            return _stat
        def set_value(self, key, value, spider=None):
            tname = self._spider_id_task_format
            if type(value) == datetime: value = str(value + timedelta(hours=8)) # 将默认utc时区转到中国，方便我使用
            self.server.hsetnx(tname, key, value)
        def inc_value(self, key, count=1, start=0, spider=None):
            if spider: self.server.hincrby(self._spider_id_task_format, key, count)
        def max_value(self, key, value, spider=None):
            if value > self._maxdp: self._maxdp = value; self.server.hset(self._spider_id_task_format, key, value)
        def open_spider(self, spider): pass
        def close_spider(self, spider, reason):
            if self._dump:
                _logger.info("Dumping Scrapy stats:\n" + pprint.pformat(self.get_stats(spider)), extra={'spider': spider})
    class Scheduler(object):
        def __init__(self, server, persist=False, flush_on_start=False, idle_before_close=0):
            self.server = server
            self.persist = persist
            self.flush_on_start = flush_on_start
            self.idle_before_close = idle_before_close
            self.stats = None
            self.queue_key = QUEUE_KEY
            self.dupefilter_key = DUPEFILTER_KEY
        def __len__(self): return len(self.queue)
        @classmethod
        def from_settings(cls, settings):
            server = redis.StrictRedis(**REDIS_PARAMS)
            server.ping()
            return cls(server=server, **EXTRA_SETTING)
        @classmethod
        def from_crawler(cls, crawler):
            instance = cls.from_settings(crawler.settings)
            instance.stats = crawler.stats
            return instance
        def open(self, spider):
            self.spider = spider
            try: self.queue = FifoQueue(server=self.server, spider=spider, key=self.queue_key % {'spider': spider.name})
            except TypeError as e: raise ValueError("Failed to instantiate queue class '%s': %s", self.queue_cls, e)
            try: self.df = RFPDupeFilter(server=self.server, key=self.dupefilter_key % {'spider': spider.name}, debug=False)
            except TypeError as e: raise ValueError("Failed to instantiate dupefilter class '%s': %s", self.dupefilter_cls, e)
            if self.flush_on_start: self.flush()
            if len(self.queue): spider.log("Resuming crawl (%d requests scheduled)" % len(self.queue))
        def close(self, reason): 
            if not self.persist: self.flush()
        def flush(self): self.df.clear(); self.queue.clear()
        def enqueue_request(self, request):
            if not request.dont_filter and self.df.request_seen(request): self.df.log(request, self.spider); return False
            if self.stats: self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
            self.queue.push(request)
            return True
        def next_request(self):
            block_pop_timeout = self.idle_before_close
            request = self.queue.pop(block_pop_timeout)
            if request and self.stats: self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
            return request
        def has_pending_requests(self): return len(self) > 0
    from scrapy import signals
    from scrapy.core.scraper import Scraper
    from scrapy.core.engine import ExecutionEngine
    from scrapy.utils.misc import load_object
    def __hook_init__(self, crawler, spider_closed_callback):
        self.crawler = crawler
        self.settings = crawler.settings
        self.signals = crawler.signals
        self.logformatter = crawler.logformatter
        self.slot = None
        self.spider = None
        self.running = False
        self.paused = False
        self.scheduler_cls = Scheduler
        downloader_cls = load_object(self.settings['DOWNLOADER'])
        self.downloader = downloader_cls(crawler)
        self.scraper = Scraper(crawler)
        self._spider_closed_callback = spider_closed_callback
    ExecutionEngine.__init__ = __hook_init__
    _bak_next_request = ExecutionEngine._next_request
    START_TOGGLE_HOOK = True
    def __hook_next_request(self, spider):
        nonlocal START_TOGGLE_HOOK
        if START_TOGGLE_HOOK:
            r = self.crawler.stats.server.hincrby(TASK_STATS, 'start_toggle_requests')
            if r != 1: self.slot.start_requests = None # 让其他非首次启动的 start_requests 不执行
            START_TOGGLE_HOOK = False
        _bak_next_request(self, spider)
    ExecutionEngine._next_request = __hook_next_request
    import scrapy.spiders
    from scrapy import signals
    from scrapy.exceptions import DontCloseSpider
    from scrapy.spiders import Spider
    class RedisMixin(object):
        redis_key = None
        redis_batch_size = None
        redis_encoding = None
        server = None
        def start_requests(self): return self.next_requests()
        def setup_redis(self, crawler=None):
            if self.server is not None: return
            settings = crawler.settings
            self.redis_key = QUEUE_KEY
            self.redis_batch_size = settings.getint('CONCURRENT_REQUESTS')
            self.server = redis.StrictRedis(**REDIS_PARAMS)
            crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        def next_requests(self):
            fetch_one = self.server.lpop
            found = 0
            while found < self.redis_batch_size:
                data = fetch_one(self.redis_key)
                if not data: break
                req = self.make_request_from_data(data)
                if req:
                    yield req
                    found += 1
                else:
                    self.logger.debug("Request not made from data: %r", data)
            if found:
                self.logger.debug("Read %s requests from '%s'", found, self.redis_key)
        def make_request_from_data(self, data): return self.make_requests_from_url(data.decode(self.redis_encoding))
        def schedule_next_requests(self):
            for req in self.next_requests(): self.crawler.engine.crawl(req, spider=self)
        def spider_idle(self):
            self.schedule_next_requests()
            raise DontCloseSpider
    class RedisSpider(RedisMixin, Spider):
        @classmethod
        def from_crawler(self, crawler, *args, **kwargs):
            obj = super(RedisSpider, self).from_crawler(crawler, *args, **kwargs)
            obj.setup_redis(crawler)
            return obj
    scrapy.Spider = RedisSpider
    import scrapy.spiders
    import scrapy.extensions.telnet
    import scrapy.extensions.memusage
    import scrapy.extensions.logstats
    import scrapy.statscollectors
    scrapy.extensions.telnet.TelnetConsole.__init__  = lambda self,_:None   # 关闭这个插件，我不用(这种关闭插件的方式小孩子可不要学哦~)
    scrapy.extensions.memusage.MemoryUsage.__init__  = lambda self,_:None   # 同样的理由，我不用
    scrapy.extensions.logstats.LogStats.from_crawler = lambda self:None     # 同样的理由，我不用
    scrapy.statscollectors.MemoryStatsCollector = RedisStatsCollector       # 挂钩默认日志，让其自动支持redis日志(这种抽象的钩子技术小孩子可不要学哦~)
    import json
    import scrapy.pipelines
    from scrapy.core.spidermw import SpiderMiddlewareManager
    TASK_COLLECTION = None
    class VRedisPipeline(object):
        def __init__(self):
            self.key = TASK_COLLECTION
            self.server = redis.StrictRedis(**REDIS_PARAMS)
            self.server.ping()
        def process_item(self, item, spider):
            if self.key:
                self.server.lpush(self.key, json.dumps(item))
            return item
    def __hook_scraper_init__(self, crawler):
        self.slot = None
        self.spidermw = SpiderMiddlewareManager.from_crawler(crawler)
        itemproc_cls = scrapy.pipelines.ItemPipelineManager()
        self.itemproc = itemproc_cls.from_crawler(crawler)
        self.itemproc._add_middleware(VRedisPipeline()) # 挂钩scraper的初始化，在此刻增加redis写入中间件
        self.concurrent_items = crawler.settings.getint('CONCURRENT_ITEMS')
        self.crawler = crawler
        self.signals = crawler.signals
        self.logformatter = crawler.logformatter
    import scrapy.core.scraper
    scrapy.core.scraper.Scraper.__init__ = __hook_scraper_init__
    EXTRA_SETTING = {
        'persist': True,            # 任务(意外或正常)结束是否保留过滤池或任务队列(使用默认配置即可)
        'flush_on_start': False,    # 任务开始时是否需要进行队列和过滤池的清空处理(使用默认配置即可)
        'idle_before_close': 0,     # 约等于redis中的(包括且不限于)函数 brpop(key,timeout) 中的参数 timeout
    }
    REDIS_PARAMS = {
        'host':'127.0.0.1',         # 最需要主动配置的部分1
        'port':6379,                # 最需要主动配置的部分2
        'password': None,           # 最需要主动配置的部分3
        'socket_timeout': 30,
        'socket_connect_timeout': 30,
        'retry_on_timeout': True,
        'encoding': 'utf-8',
    }
    QUEUE_KEY       = 'scrapy_redis:{}:TASK_QUEUE'.format(namespace)  # 任务队列(当任务正常执行完，必然是空)
    DUPEFILTER_KEY  = 'scrapy_redis:{}:DUPEFILTER'.format(namespace)  # 过滤池(用于放置每个请求的指纹)
    TASK_STATS      = 'scrapy_redis:{}:TASK_STATS'.format(namespace)  # 任务状态日志
    TASK_COLLECTION = 'scrapy_redis:{}:COLLECTION'.format(namespace)  # 数据收集的地方(默认使用redis收集json.dumps的数据)，注释这行数据就不收集到redis

# 使用这个函数后爬虫自动变成分布式(注意要先设置好 redis 连接的配置)
# 使用时尽量一个任务一个 namespace，因为一旦任务启动，相同 namespace 下的爬虫的 start_requests 函数只会执行一次。
#     除非主动修改 TASK_STATS 中的 start_toggle_requests 字段为0，新的任务才会执行 start_requests
hook_to_scrapy_redis(namespace='vilame') # 不想用分布式直接注释掉该行函数执行即可。
''' + '\n'*16

_single_script_middleware_new = '''# -*- coding: utf-8 -*-
# 挂钩中间件加载的处理，让通过“字符串”加载中间件的函数能够同时兼容用“类”加载中间件
import scrapy.utils.misc
import scrapy.utils.deprecate
_bak_load_object      = scrapy.utils.misc.load_object
_bak_update_classpath = scrapy.utils.deprecate.update_classpath
def _load_object(path_or_class):
    try: return _bak_load_object(path_or_class)
    except: return path_or_class
def _update_classpath(path_or_class):
    try: return _bak_update_classpath(path_or_class)
    except: return path_or_class
scrapy.utils.misc.load_object = _load_object
scrapy.utils.deprecate.update_classpath = _update_classpath

# 如果使用 pyinstaller 打包 scrapy 脚本成为单个 exe，打包命令如下。（注意修改脚本名称）
# pyinstaller -F $你的scrapy单脚本.py '''+_pyinstaller_scrapy+'''
# 注意，这里的打包默认去除最常见影响大小的库 numpy scipy matplotlib PyQt5，如有需要引用请删除这里的部分 --exclude-module

# 基础 item 中间件模板
class VPipeline(object):
    def process_item(self, item, spider):
        print('\\n==== 这里是动态增加的“下载中间件”部分 ====\\n')
        return item

# 图片下载 item 中间件
import logging, hashlib
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
class VImagePipeline(ImagesPipeline):
    IMAGES_STORE = None
    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func, settings)
        VImagePipeline.IMAGES_STORE = settings.get('IMAGES_STORE')
    def get_media_requests(self, item, info):
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        item = item.copy()
        item['download_timeout'] = 180 # 下载单张图片的时间限制
        yield Request(item['src'], headers=headers, meta=item) 
    def file_path(self, request, response=None, info=None):
        url = request if not isinstance(request, Request) else request.url
        image_name = request.meta.get('image_name') # 使用 item中的 image_name 字段作为文件名进行存储，没有该字段则使用 url的 md5作为文件名存储
        image_name = re.sub(r'[/\\\\:\\*"<>\\|\\?]', '_', image_name).strip()[:80] if image_name else hashlib.md5(url.encode()).hexdigest()
        return '%s.jpg' % image_name # 生成的图片文件名字，此处可用/符号增加多级分类路径（路径不存在则自动创建），使用 image_name 请注意重名可能性。
    def item_completed(self, results, item, info): # 判断下载是否成功
        k, v = results[0]
        item['image_download_stat'] = 'success' if k else 'fail'
        item['image_path'] = os.path.join(VImagePipeline.IMAGES_STORE, v['path']).replace('\\\\', '/') if k else None # 保留文件名地址
        if not k: logging.info('download fail {}'.format(item))
        else:     logging.info('download success {}'.format(item))
        return item

# 文件下载 item 中间件
import logging, hashlib
from scrapy.pipelines.files import FilesPipeline
class VFilePipeline(FilesPipeline):
    FILES_STORE = None
    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func, settings)
        VFilePipeline.FILES_STORE = settings.get('FILES_STORE')
    def get_media_requests(self, item, info):
        headers = {
            "accept-encoding": "gzip, deflate", # auto delete br encoding. cos requests and scrapy can not decode it.
            "accept-language": "zh-CN,zh;q=0.9",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        item = item.copy()
        item['download_timeout'] = 180 # 下载单条文件的时间限制
        yield Request(item['src'], headers=headers, meta=item) 
    def file_path(self, request, response=None, info=None):
        url = request if not isinstance(request, Request) else request.url
        file_name = request.meta.get('file_name')
        file_type = request.meta.get('file_type')
        file_name = re.sub(r'[/\\\\:\\*"<>\\|\\?]', '_', file_name).strip()[:80] if file_name else hashlib.md5(url.encode()).hexdigest()
        if not file_type:
            file_type = request.url.rsplit('.', 1)[-1]
            file_type = file_type if '/' not in file_type else 'unknown'
        return '{}.{}'.format(file_name, file_type)
    def item_completed(self, results, item, info): # 判断下载是否成功
        k, v = results[0]
        item['file_download_stat'] = 'success' if k else 'fail'
        item['file_path'] = os.path.join(VFilePipeline.FILES_STORE, v['path']).replace('\\\\', '/') if k else None # 保留文件名地址
        if not k: logging.info('download fail {}'.format(item))
        else:     logging.info('download success {}'.format(item))
        return item

# 阿里 Oss 文件上传中间件模板
# 依赖 pip install oss2
class VOssPipeline:
    BUCKET_STORE = None
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        import oss2
        aid = 'kkkkkkkkkkkkkkkkkkkkkkkk'
        ack = 'vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv'
        enp = 'http://oss-cn-hangzhou.aliyuncs.com'
        _bucket = '<bucket name>'
        VOssPipeline.BUCKET_STORE = oss2.Bucket(oss2.Auth(aid,ack), enp, _bucket)
        return s
    def process_item(self, item, spider):
        # 示例: 用于将下载到的图片上传到Oss的代码如下
        # ipath = item.get('image_path')
        # if ipath and os.path.isfile(ipath): self.update_data(ipath, ipath)
        return item
    def update_data(self, object_name, localfile_name):
        VOssPipeline.BUCKET_STORE.put_object_from_file(object_name, localfile_name)

# import you_get.extractors         # 使用 pyinstaller 打包 you-get    时，需要在全局环境显式导入该行代码，让 pyinstaller 自动包含该库内容
# from youtube_dl import YoutubeDL  # 使用 pyinstaller 打包 youtube-dl 时，需要在全局环境显式导入该行代码，让 pyinstaller 自动包含该库内容
# 视频下载 item 中间件
import os, sys
import logging, hashlib, traceback
from scrapy.exceptions import NotConfigured
class VVideoPipeline(object):
    MEDIAS_STORE = None
    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler.settings)
        return s
    def __init__(self, settings=None):
        VVideoPipeline.MEDIAS_STORE = settings.get('MEDIAS_STORE')
        if not VVideoPipeline.MEDIAS_STORE:
            err = 'before use VVideoPipeline. pls set MEDIAS_STORE first !!!'
            logging.error('\\n--------------\\n{}\\n--------------'.format(err))
            raise NotConfigured
    def process_item(self, item, spider):
        url = item['src']
        localpage_ = os.path.dirname(os.path.realpath(sys.argv[0])) # 确保下载路径为“该脚本”或“被pytinstaller打包时候的工具”路径下的video文件夹
        localpage  = os.path.join(localpage_, VVideoPipeline.MEDIAS_STORE)
        try:
            ### 【you-get】
            # import you_get.common
            # you_get.common.skip_existing_file_size_check = True # 防止发现重复视频时会强制要求输入“是否覆盖”，卡住程序，默认不覆盖
            # you_get.common.any_download(url, output_dir=localpage, merge=True, info_only=False)
            ### 【youtube-dl】 （推荐使用这个，因为这个在存储的文件名字的自定义存储上会更强）
            from youtube_dl import YoutubeDL
            file_name, file_type = item.get('file_name'), item.get('file_type')
            fpath = '{}/%(title)s.%(ext)s'.format(item.get('file_path').strip('/\\\\')) if item.get('file_path') else '%(title)s.%(ext)s'
            fpath = os.path.join(localpage, fpath).replace('\\\\', '/')
            fpath = fpath.replace('%(title)s', file_name) if file_name else fpath
            fpath = fpath.replace('%(ext)s', file_type) if file_type else fpath
            ytdl = YoutubeDL({'outtmpl': fpath, 'ffmpeg_location':None}) # 如果已配置ffmpeg环境则不用修改
            info = ytdl.extract_info(url, download=True)
            dpath = {}
            if '%(title)s' in fpath: dpath['title'] = info['title']
            if '%(ext)s'   in fpath: dpath['ext'] = info['ext']
            path = fpath % dpath

            item['media_download_stat'] = 'success'
            item['media_path'] = path.replace(localpage_.replace('\\\\', '/'), '.') # 保留文件名地址
            logging.info('download success {}'.format(item))
        except:
            item['media_download_stat'] = 'fail'
            item['media_path'] = None
            logging.info('download fail {}'.format(item))
            logging.info('download reason {}'.format(traceback.format_exc()))
        return item

# 数据库上传 item 中间件(不考虑字段类型处理，每个字段统统使用 MEDIUMTEXT 类型存储 json.dumps 后的 value)
# 如果有数据库字段类型的个性化处理，请非常注意的修改 insert_item 和 init_database 两个函数中对于字段类型的初始化、插入的处理，process_item无需修改。
import hmac, logging, traceback
from twisted.enterprise import adbapi
class VMySQLPipeline(object):
    dbn = {}
    def process_item(self, item, spider):
        mysql_config = item.pop('__mysql__', None) # 存储时自动删除配置
        if mysql_config and item:
            if type(mysql_config) is dict:
                table = mysql_config.pop('table', None)
                db = mysql_config.get('db', None) or 'vrequest'
                mysql_config.setdefault('charset','utf8mb4')
                mysql_config.setdefault('db', db)
                dbk = hmac.new(b'',json.dumps(mysql_config, sort_keys=True).encode(),'md5').hexdigest()
                if dbk not in self.dbn:
                    self.dbn[dbk] = adbapi.ConnectionPool('pymysql', **mysql_config)
                    self.init_database(self.dbn[dbk], mysql_config, db, table, item)
                self.dbn[dbk].runInteraction(self.insert_item, db, table, item)
                return item
            else:
                raise TypeError('Unable Parse mysql_config type:{}'.format(type(mysql_config)))
        else:
            return item
    def insert_item(self, conn, db, table, item):
        table_sql = ''.join(["'{}',".format(json.dumps(v, ensure_ascii=False).replace("'","\\\\'")) for k,v in item.items()])
        insert_sql = 'INSERT INTO `{}`.`{}` VALUES({})'.format(db, table, table_sql.strip(','))
        try: 
            conn.execute(insert_sql)
            logging.info('insert sql success')
        except Exception as e: 
            logging.info('insert sql fail: {}'.format(insert_sql))
            logging.error(traceback.format_exc())
    def init_database(self, pool, mysql_config, db, table, item):
        # 需要注意的是，在一些非常老的版本的mysql 里面并不支持 utf8mb4。这是 mysql 的设计缺陷，赶紧使用大于 5.5 版本的 mysql !
        # 创建db，创建表名，所有字段都以 MEDIUMTEXT 存储，用 json.dumps 保证了数据类型也能存储，后续取出时只需要每个值 json.loads 这样就能获取数据类型
        # 例如一个数字类型    123 -> json.dumps -> '123' -> json.loads -> 123，统一类型存储，取出时又能保证数据类型，这种处理会很方便
        # MEDIUMTEXT 最大能使用16M 的长度，所以对于一般的 html 文本也非常足够。如有自定义字段类型的需求，请注意修改该处。
        db, charset = mysql_config.pop('db'), mysql_config.get('charset')
        try:
            conn = pool.dbapi.connect(**mysql_config)
            cursor = conn.cursor()
            table_sql = ''.join(['`{}` MEDIUMTEXT NULL,'.format(str(k)) for k,v in item.items()])
            cursor.execute('Create Database If Not Exists {} Character Set {}'.format(db, charset))
            cursor.execute('Create Table If Not Exists `{}`.`{}` ({})'.format(db, table, table_sql.strip(',')))
            conn.commit(); cursor.close(); conn.close()
        except Exception as e:
            traceback.print_exc()

# 多类型文件同时存储中间件(当你需要同时存储多种格式的文件存储时可以考虑增加这里的处理)
from scrapy.exporters import (
    JsonLinesItemExporter, JsonItemExporter, XmlItemExporter, CsvItemExporter,
    PickleItemExporter, MarshalItemExporter, PprintItemExporter,
)
class VMoreSavePipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    def __init__(self, crawler=None):
        # timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) 
        # 这里使用的 timestamp 是全局的，是为了保证时间戳一致，上面一行代码只是在这里描述一下该参数的生成过程
        self.fp = open('temp{}.csv'.format(timestamp), 'wb')
        self.exporter = CsvItemExporter(self.fp,include_headers_line=True,join_multivalued=',')
        # self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
        # self.exporter = PprintItemExporter(self.fp) 
        # 多数情况下只需要设置 XXXItemExporter(self.fp) 使用默认参数即可
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    def close_spider(self, spider):
        self.fp.close()

# scrapy 默认项目中的 SPIDER_MIDDLEWARES，DOWNLOADER_MIDDLEWARES 中间件的模板，按需修改
from scrapy import signals
class VSpiderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
    def process_spider_input(self, response, spider):
        return None
    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i
    def process_spider_exception(self, response, exception, spider):
        pass
    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
class VDownloaderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
    def process_request(self, request, spider):
        return None
    def process_response(self, request, response, spider):
        return response
    def process_exception(self, request, exception, spider):
        pass
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# 配置 selenium 的使用方式
import time
from scrapy.http import HtmlResponse
class VSeleniumMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s
    def process_request(self, request, spider):
        try:
            self.webdriver.get(url=request.url)
            time.sleep(2)
            # 部分智能等待的代码，提高浏览器效率的处理
            # from selenium.webdriver.common.by import By
            # from selenium.webdriver.support import expected_conditions as EC
            # from selenium.webdriver.support.wait import WebDriverWait as wbw
            # locator = (By.XPATH, '//img[@class="focus-item-img"]')
            # # wbw(self.webdriver,10).until(EC.presence_of_element_located(locator)) # 判断某个元素是否被加到了dom树里
            # wbw(self.webdriver,10).until(EC.visibility_of_element_located(locator)) # 判断某个元素是否被添加到了dom里并且可见，即宽和高都大于0
            current_url = self.webdriver.current_url
            page_source = self.webdriver.page_source
        except Exception as e:
            return self._parse_selenium_temp_exceptions(request, spider, e)
        # 若是出现请求异常(验证码，或者重新登陆之类的处理)，请在这里判断 page_source 是否是异常情况，并在这里处理重新进行登录或其他
        h = HtmlResponse(
            url      = current_url,
            headers  = {'Selenium':'Selenium cannot get a certain headers, This is the information created automatically by middleware.'},
            body     = page_source,
            encoding = 'utf-8',
            request  = request
        )
        return h
    def process_response(self, request, response, spider):
        return response
    def spider_opened(self, spider):
        spider.logger.info('Spider %s opened: %s' % (self.__class__.__name__, spider.name))
        self._open_webdriver()
        self._login()
    def spider_closed(self):
        if getattr(self, 'webdriver', None): self.webdriver.quit()
    def _parse_selenium_temp_exceptions(self, request, spider, e):
        stats = spider.crawler.stats
        if 'Failed to establish a new connection' in str(e): # 仅仅捕捉浏览器异常关闭的异常，尝试重启，并重新将请求发送到队列
            if getattr(self, 'restart_show_toggle', None) is None:
                self.restart_show_toggle = True
            if self.restart_show_toggle:
                self.restart_show_toggle = False # 让 Catch webdriver 仅显示一次
                spider.logger.info('Catch webdriver exception:{}, try to restart webdriver.'.format(e.__class__))
            self._open_webdriver()
            retries = request.meta.get('selenium_retry_times', 0) + 1 # 在 selenium 异常无法重启处理情况下一个请求最多尝试共3次请求
            if retries <= 3:
                retryreq = request.copy()
                retryreq.meta['selenium_retry_times'] = retries
                retryreq.dont_filter = True
                stats.inc_value('selenium_retry/count')
                return retryreq
            else:
                stats.inc_value('selenium_retry/max_reached')
                spider.logger.info("Gave up selenium_retrying %(request)s (failed %(retries)d times)",
                            {'request': request, 'retries': retries})
        else:
            stats.inc_value('selenium_unknow_error/count')
            stats.inc_value('selenium_unknow_error/reason_count/%s' % e.__class__.__name__)
            import traceback
            spider.logger.info('\\n'+traceback.format_exc().strip())
    def _open_webdriver(self): # 该函数同时作为重启 webdriver 功能使用
        try: self.spider_closed()
        except: pass
        from selenium import webdriver
        option = webdriver.ChromeOptions()
        extset = ['enable-automation', 'ignore-certificate-errors']
        ignimg = "profile.managed_default_content_settings.images"
        mobile = {'deviceName':'Galaxy S5'}
        option.add_argument("--disable-infobars")                       # 旧版本关闭“chrome正受到自动测试软件的控制”信息
        option.add_experimental_option("excludeSwitches", extset)       # 新版本关闭“chrome正受到自动测试软件的控制”信息
        option.add_experimental_option("useAutomationExtension", False) # 新版本关闭“请停用以开发者模式运行的扩展程序”信息
        # option.add_experimental_option('mobileEmulation', mobile)     # 是否使用手机模式打开浏览器
        # option.add_experimental_option("prefs", {ignore_image: 2})    # 开启浏览器时不加载图片(headless模式该配置无效)
        # option.add_argument('--start-maximized')                      # 开启浏览器时是否最大化(headless模式该配置无效)
        # option.add_argument('--headless')                             # 【*】 无界面浏览器，linux 使用 selenium 必须配置该项
        # option.add_argument('--no-sandbox')                           # 【*】 关闭沙箱模式，linux 使用 selenium 必须配置该项
        # option.add_argument('--disable-dev-shm-usage')                # 【*】 你只需要知道，linux 使用 selenium 需要尽量配置该项
        # option.add_argument('--window-size=1920,1080')                # 无界面打开浏览器时候只能用这种方式实现最大化
        # option.add_argument('--disable-gpu')                          # 禁用 gpu 硬件加速
        # option.add_argument("--auto-open-devtools-for-tabs")          # 开启浏览器时候是否打开开发者工具(F12)
        # option.add_argument("--user-agent=Mozilla/5.0 VILAME")        # 修改 UA 信息
        # option.add_argument('--proxy-server=http://127.0.0.1:8888')   # 增加代理

        # 处理 document.$cdc_asdjflasutopfhvcZLmcfl_ 参数的指纹的检测
        def check_magic_word(driver_path, rollback=False):
            import shutil
            cpdriver = shutil.which(driver_path)
            with open(cpdriver, 'rb') as f: filebit = f.read()
            a, b = b'$cdc_asdjflasutopfhvcZLmcfl_', b'$pqp_nfqwsynfhgbcsuipMYzpsy_'
            a, b = (b, a) if rollback else (a, b)
            mgc_o, mgc_t = a, b
            if mgc_o in filebit: 
                with open(cpdriver, 'wb') as f: f.write(filebit.replace(mgc_o, mgc_t))
        driver_path = 'chromedriver'
        check_magic_word(driver_path, rollback=False)

        # 启动 webdriver
        self.webdriver = webdriver.Chrome(options=option, executable_path=driver_path)
        try:
            # 让每打开一个网页首先执行部分 js代码，下面 js代码可以绕过部分 webdriver 检测。
            self.webdriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
              "source": """
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, "plugins", { get: () => [1,2,3,4,5] });
              """
            })
            self.webdriver.execute_cdp_cmd("Network.enable", {})
        except:
            import traceback
            print('[ ERROR! ] error in selenium webdriver execute_cdp_cmd func.')
            print(traceback.format_exc())
    def _login(self):
        # 如果有登录处理，则写在这里
        pass

# 定时任务执行插件
import types
import scrapy
from scrapy.exceptions import DontCloseSpider
from twisted.internet import task, defer, reactor
from scrapy import signals
class TimerRequest(object):
    def __init__(self, crawler, interval):
        self.interval = interval
        self.task = None
        self.crawler = crawler
    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler, crawler.settings.get('TIMER_INTERVAL') or 3)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.spider_idle, signal=signals.spider_idle)
        return o
    def spider_opened(self, spider):
        self.task = task.LoopingCall(self.new_request, spider)
        if getattr(spider, 'timer_task', None):
            d = defer.Deferred()
            reactor.callLater(self.interval, self.task.start, self.interval) 
        else:
            print('[ WARNING! ] Spider does not have timer_task function')
    def new_request(self, spider):
        r = getattr(spider, 'timer_task', None)()
        if isinstance(r, scrapy.Request):
            self.crawler.engine.crawl(r, spider=spider)
        elif isinstance(r, (types.GeneratorType, list)):
            for i in r:
                if isinstance(i, scrapy.Request):
                    self.crawler.engine.crawl(i, spider=spider)
    def spider_closed(self, spider, reason):
        if self.task and self.task.running:
            self.task.stop()
    def spider_idle(self):
        raise DontCloseSpider
'''

_single_script_middleware_new2 = '''
        # 【中间件/管道配置】
        # 这里使用中间件的方式和项目启动很相似，我在头部打了补丁函数，现在管道配置的第一个值可以同时用字符串或类配置，突破了原版只能用字符串的限制。
        'IMAGES_STORE':             'image',      # 默认在该脚本路径下创建文件夹、下载【图片】(不解开 VImagePipeline 管道注释则该配置无效)
        'FILES_STORE':              'file',       # 默认在该脚本路径下创建文件夹、下载【文件】(不解开 VFilePipeline 管道注释则该配置无效)
        'MEDIAS_STORE':             'media',      # 默认在该脚本路径下创建文件夹、下载【媒体】(不解开 VVideoPipeline 管道注释则该配置无效)
        'ITEM_PIPELINES': {
            # VPipeline:              101,        # 普通的中间件使用(解开即可测试，如需魔改，请在脚本顶部找对应的类进行自定义处理)
            # VImagePipeline:         102,        # 图片下载中间件，item 带有 src 字段则以此作为图片地址下载到 IMAGES_STORE 地址的文件夹内
            # VFilePipeline:          103,        # 文件下载中间件，item 带有 src 字段则以此作为文件地址下载到 FILES_STORE 地址的文件夹内
            # VVideoPipeline:         104,        # 视频下载中间件，item 带有 src 字段则以此作为媒体地址下载到 MEDIAS_STORE 文件夹内
            # VMySQLPipeline:         105,        # MySql 插入中间件，具体请看类的描述
            # VOssPipeline:           106,        # 将本地数据上传到 OSS 空间的管道模板，注意修改模板内 process_item 函数来指定上传文件地址
            # VMoreSavePipeline:      107,        # 如果需要同时存储多种格式的本地文件，可以使用这个模板(例如同时存储 jsonline 和 csv 文件)
        },
        'SPIDER_MIDDLEWARES': {
            # VSpiderMiddleware:      543,        # 原版模板的单脚本插入方式
        },
        'DOWNLOADER_MIDDLEWARES': {
            # VDownloaderMiddleware:  543,        # 原版模板的单脚本插入方式
            # VSeleniumMiddleware:    544,        # 单脚本 Selenium 中间件配置，解开自动使用 Selenium，详细请看 VSeleniumMiddleware 类中间件代码。
        },
        'TIMER_INTERVAL':             1,          # 定时执行任务插件参数，打开 TimerRequest 插件注释即可使用，如未设置默认为3
        'EXTENSIONS': {
            # TimerRequest:           101,        # 定时执行任务插件，在 VSpider 类中定义一个名为 timer_task 的函数，将会自动每n秒执行一次，
                                                  # 如果 timer_task 返回的结果是 scrapy.Request 对象或该对象列表(或迭代器)则自动发出请求。
                                                  # 开启该插件后脚本将不会自动停止。
            # 'scrapy.extensions.logstats.LogStats': None, 
            # 关闭 scrapy EXTENSIONS默认中间件方式如上，程序执行时，日志的头部有当前任务都有哪些中间件加载，按需在对应管道中配置为 None 即可关闭
            # 同理 SPIDER_MIDDLEWARES / DOWNLOADER_MIDDLEWARES 这两个“中间件配置”字典也可以用相同的方式关掉 scrapy 默认组件
            # 【*】注意：不同分类的默认中间件需在对应分类的“中间件配置”字典中配置才能关闭，
        },'''

# 生成代码临时放在这里
def scrapy_code_window(setting=None):
    fr = Frame()
    ft = Font(family='Consolas',size=10)

    if setting.get('type') == 'request':
        va,prox = setting.get('fr_proxy')
        proxy   = prox.get().strip() if va.get() else None
    if setting.get('type') == 'response':
        proxy   = setting.get('fr_setting').get('proxy')
    if proxy and setting.get('code_string'):
        rep = "proxy = None # 'http://127.0.0.1:8888'"
        rpl = "proxy = 'http://" +proxy+ "'"
        setting['code_string'] = setting['code_string'].replace(rep, rpl)

    def _execute_scrapy_code(*a):
        from .tab import execute_scrapy_code
        execute_scrapy_code()

    def _execute_code(*a):
        from .tab import execute_code
        execute_code()

    def save_project_in_desktop(*a):
        name = askstring('项目名称','请输入项目名称，尽量小写无空格。')
        if not name: return
        desktop = os.path.join(os.path.expanduser("~"),'Desktop\\{}'.format(name))
        if not os.path.isdir(desktop):
            with open(script,'w',encoding='utf-8') as f:
                f.write(tx.get(0.,tkinter.END))
            shutil.copytree(scrapypath, desktop)
            # if hva.get():
            #     with open(desktop + '\\v\\spiders\\v.py','a',encoding='utf-8') as f:
            #         f.write('\n'*10 + post_verification_model)
            toggle = tkinter.messagebox.askokcancel('创建成功',
                            '创建成功\n\n'
                            '注意！！！\n注意！！！\n注意！！！\n\n是否关闭当前工具并启动拷贝出的 shell 地址执行测试。\n'
                            '如果是，启动第一次shell测试后，后续需要再执行新的测试时请输入:\nscrapy crawl v\n\n'
                            '{}'.format(desktop))
            if not toggle:
                return
            # cmd = 'start explorer {}'.format(desktop) # 打开文件路径
            # os.system(cmd)
            pyscript = os.path.join(os.path.split(sys.executable)[0],'Scripts')
            toggle = any([True for i in os.listdir(pyscript) if 'scrapy.exe' in i.lower()])
            if toggle:
                scrapyexe = os.path.join(pyscript,'scrapy.exe')
                output = '-o {}'.format(et.get()) if va.get() else ''
                cwd = os.getcwd()
                os.chdir(desktop)
                try:
                    cmd = 'start powershell -NoExit "{}" crawl v -L {} {}'.format(scrapyexe,cbx.get(),output)
                    assert not os.system(cmd) # 返回0则正常执行
                except:
                    cmd = 'start cmd /k "{}" crawl v -L {} {}'.format(scrapyexe,cbx.get(),output)
                    os.system(cmd)
                os.chdir(cwd)
                cwd = os.getcwd()
            else:
                einfo = 'cannot find scrapy'
                tkinter.messagebox.showinfo('Error',einfo)
                raise EnvironmentError(einfo)
            exit()
        else:
            tkinter.messagebox.showwarning('文件夹已存在','文件夹已存在')

    def save_script_in_desktop(*a):
        name = askstring('脚本名','请输入脚本文件名，尽量小写无空格。')
        if not name: return
        if not name.endswith('.py'): name += '.py'
        desktop_script = os.path.join(os.path.expanduser("~"),'Desktop\\{}'.format(name))
        if not os.path.isfile(desktop_script):
            with open(desktop_script, 'w', encoding='utf-8') as f:
                f.write(tx.get(0.,tkinter.END))
        else:
            tkinter.messagebox.showwarning('脚本已存在','脚本已存在')

    home = os.environ.get('HOME')
    home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
    filename = '.vrequest_scrapy'
    scrapypath = os.path.join(home,filename)
    scriptpath = os.path.join(scrapypath, 'v/spiders/')
    script = os.path.join(scriptpath, 'v.py')

    def local_collection(*a):
        def _show(*a, stat='show'):
            try:
                if stat == 'show': et.pack(side=tkinter.RIGHT)
                if stat == 'hide': et.pack_forget()
            except:
                pass
        _show(stat='show') if va.get() else _show(stat='hide')

    def _add_single_script_file_save(*a):
        script = tx.get(0.,tkinter.END).rstrip('\n')
        tx.delete(0.,tkinter.END)
        if 'os.path.join(os.path.expanduser("~")' not in script:
            script = re.sub('\n    p = CrawlerProcess', '\n' + single_script_comment_part1 + '\n\n    p = CrawlerProcess', script)
        tx.insert(0.,script)
        tx.see(tkinter.END)

    def _add_single_script_comment(*a):
        script = tx.get(0.,tkinter.END).rstrip('\n')
        tx.delete(0.,tkinter.END)
        # if 'os.path.join(os.path.expanduser("~")' not in script:
        #     script = re.sub('\n    p = CrawlerProcess', '\n' + single_script_comment_part1 + '\n\n    p = CrawlerProcess', script)
        if 'VImagePipeline' not in script:
            # script = re.sub(r'p\.crawl\(VSpider\)', 'p.crawl(VSpider)\n\n' + single_script_comment_part2 + '\n', script)
            script = script.replace(r'p.crawl(VSpider)', 'p.crawl(VSpider)\n\n' + single_script_comment_part2 + '\n')
        tx.insert(0.,script)
        tx.see(tkinter.END)

    def _add_single_script_comment_new(*a):
        script = tx.get(0.,tkinter.END).rstrip('\n')
        tx.delete(0.,tkinter.END)
        # if 'os.path.join(os.path.expanduser("~")' not in script:
        #     script = re.sub('\n    p = CrawlerProcess', '\n' + single_script_comment_part1 + '\n\n    p = CrawlerProcess', script)
        if 'scrapy.utils.deprecate.update_classpath = _update_classpath' not in script:
            key = "'DOWNLOAD_DELAY':           1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多"
            script = script.replace(key, key+'\n'+_single_script_middleware_new2)
            script = _single_script_middleware_new + '\n'*16 + script
        tx.insert(0.,script)
        tx.see(tkinter.END)

    def _add_single_script_distributed_comment(*a):
        script = tx.get(0.,tkinter.END).rstrip('\n')
        tx.delete(0.,tkinter.END)
        if "hook_to_scrapy_redis(namespace='default')" not in script:
            script = _single_distributed + script
        tx.insert(0.,script)
        tx.see(tkinter.END)

    def _get_single_script_scrapy_redis_server(*a):
        script = tx.get(0.,tkinter.END).rstrip('\n')
        scriptfile = os.path.join(os.path.split(__file__)[0],'py_my_scrapy_redis_server.py')
        if "__callerr__ = _plusmeta.pop('__callerr__')" not in script:
            tx.delete(0.,tkinter.END)
            with open(scriptfile, encoding='utf-8') as f:
                v = f.read()
                lenv = len(v.splitlines())
                script = v + '\n'*20 + script
            tx.insert(0.,script)
            tx.see('{}.{}'.format(lenv-20, 0))
            tx.update()

    def _add_single_script_scrapy_redis_server_in_desktop(*a):
        script = tx.get(0.,tkinter.END).rstrip('\n')
        scriptfile = os.path.join(os.path.split(__file__)[0],'py_my_scrapy_redis_server.py')
        with open(scriptfile, encoding='utf-8') as f:
            scriptfile = f.read()
        gap = '    p.start()'
        server, client = scriptfile.split(gap)
        server = server + gap
        name = 'v_server.py'
        runname = 'v_server_run.bat'
        clientname = 'v_client.py'
        desktop_script = os.path.join(os.path.expanduser("~"),'Desktop\\{}'.format(name))
        desktop_runbat = os.path.join(os.path.expanduser("~"),'Desktop\\{}'.format(runname))
        desktop_client = os.path.join(os.path.expanduser("~"),'Desktop\\{}'.format(clientname))
        if not os.path.isfile(desktop_script):
            with open(desktop_script, 'w', encoding='utf-8') as f:
                f.write(server)
            with open(desktop_client, 'w', encoding='utf-8') as f:
                f.write('import re'+client.split('import re', 1)[1] + '\n'*20 + script)
            with open(desktop_runbat, 'w', encoding='utf-8') as f:
                f.write(sys.executable.replace('pythonw', 'python')+' '+desktop_script+' && pause')
        else:
            tkinter.messagebox.showwarning('脚本已存在','脚本已存在')

    def _add_middleware_script_and_so_on(*a):
        from .tab import nb
        from .tab import SimpleDialog
        q = [   '单脚本添加各种配置中间件方式(支持原版排序)', 
                # '【不推荐】旧版单脚本添加中间件方式(不支持用原版排序)', 
                '单脚本【单任务】分布式的处理(代码增加在头部,详细使用请看注释)', 
                '单脚本【多任务】分布式脚本代码，可控性更高，一次部署所有scrapy通用。',
                '增加绝对地址保存文件方式(win 系统 filename 使用绝对地址需加前缀)',
                '增加列表请求(尚在开发，不好解释用途，不会影响原始代码)',
                '*快速添加 “单脚本【多任务】分布式脚本代码” 脚本到桌面',
            ]
        d = SimpleDialog(nb,
            text="请选择一个增强功能",
            buttons=q,
            default=0,
            cancel=-1,
            title="选择")
        id = d.go()
        if id == -1: return
        if id == 0: _add_single_script_comment_new()
        # if id == 1: _add_single_script_comment()
        if id == 1: _add_single_script_distributed_comment()
        if id == 2: _get_single_script_scrapy_redis_server()
        if id == 3: _add_single_script_file_save()
        if id == 4: _add_sceeper_in_list_model()
        if id == 5: _add_single_script_scrapy_redis_server_in_desktop()

    def _add_sceeper_in_list_model(*a):
        script = tx.get(0.,tkinter.END).rstrip('\n')
        if "meta['_plusmeta'] = {}" not in script:
            q = re.findall(r'\n            d\["([^"]+)"\] *=', script)
            if not q: return
            from .tab import nb
            from .tab import SimpleDialog
            d = SimpleDialog(nb,
                text="请选择作为下一级请求链接的字段",
                buttons=q,
                default=0,
                cancel=-1,
                title="选择")
            id = d.go()
            if id == -1: return
            script = script.replace('''        # If you need to parse another string in the parsing function.''', 
                                    '''        _meta = response.meta.get('_plusmeta') or {}\n        # If you need to parse another string in the parsing function.''')
            script = script.replace('''meta = {}\n        meta['proxy'] = self.proxy\n        r = Request(''', 
                                    '''meta = {}\n        meta['proxy'] = self.proxy\n        meta['_plusmeta'] = {} # keys word transfer\n        r = Request(''')
            if 'from urllib.parse import unquote_plus, quote_plus' not in script:
                _tempstring = _main_2_list_2_info_model.replace('lambda i:i.group(1)+quote_plus(unquote_plus(i.group(2)))', 'lambda i:i.group(1)+quote(unquote(i.group(2)))')
            else:
                _tempstring = _main_2_list_2_info_model
            script = script.replace('''print('------------------------------ split ------------------------------')\n            import pprint\n            pprint.pprint(d)\n            yield d''', 
                                    '''# print('------------------------------ split ------------------------------')\n            # import pprint\n            # pprint.pprint(d)\n            # yield d''' \
                                    + _tempstring.replace("response.urljoin(d['href'])", "response.urljoin(d['{}'])".format(q[id])))
            tx.delete(0.,tkinter.END)
            tx.insert(0.,script)
            tx.see(tkinter.END)

    def pprint(*a):
        __org_stdout__.write(str(a)+'\n')
        __org_stdout__.flush()
    temp_fr0 = Frame(fr)
    va = tkinter.IntVar()
    rb = Checkbutton(temp_fr0,text='本地执行是否收集数据',variable=va,command=local_collection)
    rb.deselect()
    et = Entry (temp_fr0,width=60)
    
    ltime = '%04d%02d%02d-%02d%02d%02d' % time.localtime()[:6]
    dtopfile = os.path.join('file:///' + os.path.expanduser("~"),'Desktop\\v{}.json'.format(ltime))
    et.insert(0,dtopfile)
    bt2 = Button(temp_fr0,text='保存单脚本到桌面',command=save_script_in_desktop)
    bt2.pack(side=tkinter.LEFT)
    # bt3 = Button(temp_fr0,text='保存项目文件到桌面',command=save_project_in_desktop)
    # bt3.pack(side=tkinter.LEFT)
    # btn1 = Button(temp_fr0, text='执行项目代码 [Alt+w]', command=_execute_scrapy_code)
    # btn1.pack(side=tkinter.LEFT)
    btn1_1 = Button(temp_fr0, text='窗口执行代码 [Alt+v]', command=_execute_code)
    btn1_1.pack(side=tkinter.LEFT)
    btn2 = Button(temp_fr0, text='【单脚本中间件/管道】', command=_add_middleware_script_and_so_on)
    btn2.pack(side=tkinter.LEFT)
    # btn2 = Button(temp_fr0, text='增加单脚本中间件功能', command=_add_single_script_comment)
    # btn2.pack(side=tkinter.LEFT)
    # btn2 = Button(temp_fr0, text='增加单脚本分布式功能', command=_add_single_script_distributed_comment)
    # btn2.pack(side=tkinter.LEFT)
    # btn4 = Button(temp_fr0, text='增加列表请求', command=_add_sceeper_in_list_model)
    # btn4.pack(side=tkinter.LEFT)
    # hva = tkinter.IntVar()
    # hrb = Checkbutton(temp_fr0,text='拷贝项目增加后验证模板',variable=hva)
    # hrb.deselect()
    # hrb.pack(side=tkinter.LEFT)
    cbx = Combobox(temp_fr0,width=10,state='readonly')
    cbx['values'] = ('DEBUG','INFO','WARNING','ERROR','CRITICAL')
    cbx.current(1)
    cbx.pack(side=tkinter.RIGHT)
    lab1 = Label(temp_fr0, text='项目启动日志等级:')
    lab1.pack(side=tkinter.RIGHT)
    def open_test(*a):
        cmd = 'start explorer {}'.format(scrapypath)
        os.system(cmd)
    bt1 = Button(temp_fr0,text='打开本地文件路径',command=open_test)
    bt1.pack(side=tkinter.RIGHT)
    rb.pack(side=tkinter.RIGHT)

    temp_fr1 = Frame(fr)
    temp_fr0.pack(fill=tkinter.X)
    temp_fr1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)
    tx = Text(temp_fr1,height=1,width=1,font=ft)
    cs = setting.get('code_string')
    if cs:
        tx.delete(0.,tkinter.END)
        tx.insert(0.,cs)
    tx.pack(fill=tkinter.BOTH,expand=True,padx=pdx,pady=pdy)
    try:
        from idlelib.colorizer import ColorDelegator
        from idlelib.percolator import Percolator
        p = ColorDelegator()
        Percolator(tx).insertfilter(p)
    except:
        traceback.print_exc()

    def execute_func_console():
        if os.path.isdir(scriptpath):
            with open(script,'w',encoding='utf-8') as f:
                f.write(tx.get(0.,tkinter.END))
            pyscript = os.path.join(os.path.split(sys.executable)[0],'Scripts')
            toggle = any([True for i in os.listdir(pyscript) if 'scrapy.exe' in i.lower()])
            if toggle:
                scrapyexe = os.path.join(pyscript,'scrapy.exe')
                output = '-o {}'.format(et.get()) if va.get() else ''
                cwd = os.getcwd()
                os.chdir(scriptpath)
                try:
                    cmd = 'start powershell -NoExit "{}" crawl v -L {} {}'.format(scrapyexe,cbx.get(),output)
                    assert not os.system(cmd) # 返回0则正常执行
                except:
                    cmd = 'start cmd /k "{}" crawl v -L {} {}'.format(scrapyexe,cbx.get(),output)
                    os.system(cmd)
                os.chdir(cwd)
            else:
                einfo = 'cannot find scrapy'
                tkinter.messagebox.showinfo('Error',einfo)
                raise EnvironmentError(einfo)
        else:
            einfo = 'cannot find path: {}'.format(scriptpath)
            tkinter.messagebox.showinfo('Error',einfo)
            raise EnvironmentError(einfo)

    temp_fr2 = Frame(fr,highlightthickness=lin)
    lb = Label (temp_fr2,text='执行结果[Esc 显示/隐藏执行结果]')
    cd = Text  (temp_fr2,height=1,width=1,font=ft)
    lb.pack(side=tkinter.TOP)
    cd.pack(fill=tkinter.BOTH,expand=True,padx=pdx,pady=pdy)

    # 在 tkinter 里面实现线程真的稍微有点累人的。
    import queue
    Q = queue.Queue() # 用来传递打印的数据
    S = queue.Queue() # 用来传递脚本数据
    def execute_func_window():
        # 额外的线程有一个非常需要注意的地方，就是涉及到任何使用 tkinter 内的结构的时候一定不能在这里实现
        # 一定都要使用 Queue 来传递参数。窗口自己带一个超级递归的循环。
        nonlocal Q, S
        Q.put('V|GETSCRIPT')
        cs = S.get()
        td = tempfile.mkdtemp()
        tf = os.path.join(td,'temp.py')
        with open(tf,'w',encoding='utf-8') as f:
            cs = cs.replace("# import io, sys; sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')", "import io, sys; sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')")
            f.write(cs)
        s = sys.executable
        s = s + ' ' + tf
        import subprocess
        p = subprocess.Popen(s, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, encoding='utf-8')
        Q.put('V|DELETE')
        Q.put('============================== start ==============================\n')
        for line in iter(p.stdout.readline, ''):
            if line:
                Q.put(line)
            else:
                break
        Q.put('==============================  end  ==============================')
        p.wait()
        p.stdout.close()
        shutil.rmtree(td)

    def loop_in_tkinter():
        __very_unique_cd__ = None
        nonlocal cd, Q, S
        from .tab import nb
        c = []
        while Q.qsize():
            try:
                i = Q.get_nowait()
                if i == 'V|DELETE':
                    cd.delete(0., tkinter.END)
                elif i == 'V|GETSCRIPT':
                    cs = tx.get(0.,tkinter.END)
                    S.put(cs)
                else:
                    try:
                        cd.insert(tkinter.END, i)
                    except:
                        cd.insert(tkinter.END, re.sub('[\uD800-\uDBFF][\uDC00-\uDFFF]|[\U00010000-\U0010ffff]','',i))
                    cd.see(tkinter.END)
                    cd.update()
            except queue.Empty:
                import traceback
                tkinter.messagebox.showinfo('Error',traceback.format_exc())
        nb.after(200, loop_in_tkinter)
    loop_in_tkinter()

    def execute_func():
        threading.Thread(target=execute_func_window).start()

    frame_setting[fr] = {}
    frame_setting[fr]['type'] = 'scrapy'
    frame_setting[fr]['execute_func_console'] = execute_func_console
    frame_setting[fr]['execute_func'] = execute_func
    frame_setting[fr]['fr_temp2'] = temp_fr2
    return fr








# 帮助文档
def helper_window():
    fr = Frame()
    ft = Font(family='Consolas',size=10)
    hp = '''
vrequest：
基于 requests 和 lxml 库的爬虫请求测试工具
用于快速发起请求，快速生成且能执行的基于 requests 和 lxml 的代码
也可以生成且能执行 scrapy 代码，不过由于scrapy库依赖过重，该工具不会依赖下载
若需要执行 scrapy 代码，需额外下载 scrapy。
*点击帮助页按钮“安装完整功能库”(scrapy js2py jsbeautifier cryptography pillow)

通用快捷键 (该处多数功能右键窗口就能实现，只要记得右键窗口任意处即可)：
(Ctrl + q) 创建新的请求标签
(Ctrl + j) 创建 js 代码执行窗口
(Ctrl + e) 修改当前标签名字
(Ctrl + w) 关闭当前标签
(Ctrl + h) 创建帮助标签
(Ctrl + s) 保存当前全部请求配置(只能保存请求配置)
(Alt  + w) *创建 selenium 窗口(需要当前非scrapy代码页面)
(Ctrl + `) 直接打开IDLE
(Alt  + `) 用IDLE固定打开一个文件,方便长脚本测试

请求窗口快捷键：
(Ctrl + r) 发送请求任务并保存
*(Alt + c) 生成请求代码(一般建议在请求后处理分析再生成代码，那样包含解析代码)
           HEADERS 窗口接受 “:” 或 “=” 每行分割生成 字典参数
           BODY    窗口接受 “:” 或 “=” 每行分割生成 字典参数
                注意：对于 BODY 有时也会存在这里不需要对 dict 进行 urlencode 编码
                      的情况，这时候只要将传入的一行数据前后加上英文的双引号
                      程序会自动不对该 dict 进行编码，POST 请求时请留意该功能
*(Alt + s) 生成 scrapy 请求代码，格式化结构同上
*(Alt + u) 生成 urllib 请求代码，格式化结构同上

响应窗口快捷键：
*(Alt + r) 打开一个空的响应标签(不建议在响应窗口使用)
(Alt + f) 智能解析列表路径，解析后使用 xpath 解析功能会自动弹出解析选择窗
(Alt + x) <代码过程> 使用 xpath 解析
(Alt + z) <代码过程> 智能提取 json 列表(由长到短顺序排列，不选默认第一条)
(Alt + q) <代码过程> 选择一个 json 列表
(Alt + d) <代码过程> 获取纯文字内容
(Alt + c) 生成请求代码，有<代码过程>则生成代码中包含过程代码
(Alt + s) 生成 scrapy 请求代码，有<代码过程>则生成代码中包含过程代码
(Alt + u) 生成 urllib 请求代码，不包含过程(解析过程必依赖lxml,与无依赖理念冲突)
(Esc)     开启/关闭 response 解析窗口

scrapy 代码窗口快捷键：
(Alt + w) *scrapy 项目代码执行(需要当前为scrapy代码页面)

开源代码：
https://github.com/cilame/vrequest
赞助作者：
右键该窗口 -> “创建便捷加密编码窗口” -> “爆破;RSA;二维码” -> “赞助作者”
'''
    temp_fr1 = Frame(fr,highlightthickness=lin)

    def create_req_window(*a):
        from .tab import create_new_reqtab
        create_new_reqtab()

    def creat_shortcut(*a):
        from .tab import creat_windows_shortcut
        creat_windows_shortcut()

    def pip_install_allfunc(*a):
        from .tab import pipinstall_all
        pipinstall_all()

    fr1 = Frame(fr)
    fr1.pack()
    btn = Button(fr1,text='创建请求窗口/[右键创建请求窗口]', command=create_req_window)
    btn.pack(side=tkinter.LEFT)
    btn = Button(fr1,text='创建桌面快捷方式', command=creat_shortcut)
    btn.pack(side=tkinter.LEFT)
    btn = Button(fr1,text='安装完整功能库', command=pip_install_allfunc)
    btn.pack(side=tkinter.LEFT)
    lb1 = ttk.Label(temp_fr1,font=ft,text=hp)
    lb1.pack()
    temp_fr1.pack()

    return fr



def exec_js_window(setting=None):
    '''
    这里可能会使用两到三种js的加载方式，并且，js2py能生成 python 的代码，可能需要考虑生成python代码的功能
    目前暂时没有完全实现
    '''
    fr = Frame()
    ft = Font(family='Consolas',size=10)

    # js代码转python代码
    def translate_js_js2py():
        jscode = txt1.get(0.,tkinter.END)
        try:
            import js2py
            js2pycode = js2py.translate_js(jscode)
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,js2pycode)
        except:
            e = traceback.format_exc()
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,e)

    def translate_js_python():
        try:
            from . import pysimplejs2python
        except:
            import pysimplejs2python
        jscode = txt1.get(0.,tkinter.END)
        try:
            import jsbeautifier
            jscode   = txt1.get(0.,tkinter.END)
            btjscode = jsbeautifier.beautify(jscode)
            pycode   = pysimplejs2python.simplejs2python(btjscode)
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,pycode)
        except ImportError as e:
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,e)
        except:
            e = traceback.format_exc()
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,e)

    def get_script_from_tree(tree):
        from .main import escodegen
        if escodegen is None:
            import js2py.py_node_modules.escodegen as escodegen
        escodegen = escodegen.var.get('escodegen')
        generate = escodegen.get('generate')
        return generate(tree).to_python()

    def make_js_tree():
        try:
            import pyjsparser
            jscode = txt1.get(0.,tkinter.END)
            tree = pyjsparser.parse(jscode)
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,json.dumps(tree, indent=4))
        except:
            e = traceback.format_exc()
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,e)

    def defusion_js_code():
        try:
            try:
                from .pyjsdefusion import get_node_ctx, hook_popen_encoding, back_popen_encoding
            except:
                from pyjsdefusion import get_node_ctx, hook_popen_encoding, back_popen_encoding
            jscode = txt1.get(0.,tkinter.END)
            ctx = get_node_ctx()
            txt2.delete(0.,tkinter.END)
            hook_popen_encoding()
            txt2.insert(0.,ctx.call('muti_process_defusion', jscode))
        except:
            e = traceback.format_exc()
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,e)
        finally:
            back_popen_encoding()

    def defusion_ob_js_code():
        try:
            try:
                from .pyjsdefusion import get_ob_node_ctx, hook_popen_encoding, back_popen_encoding
            except:
                from pyjsdefusion import get_ob_node_ctx, hook_popen_encoding, back_popen_encoding
            jscode = txt1.get(0.,tkinter.END)
            ctx = get_ob_node_ctx()
            txt2.delete(0.,tkinter.END)
            hook_popen_encoding()
            txt2.insert(0.,ctx.call('muti_process_defusion', jscode))
        except:
            e = traceback.format_exc()
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,e)
        finally:
            back_popen_encoding()

    def js_mod_pack():
        try:
            try:
                from .pyjspack import comment
            except:
                from pyjspack import comment
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,comment)
        except:
            e = traceback.format_exc()
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,e)

    def make_js_script():
        from .tab import show_code_log
        show_code_log()
        try:
            jstree = txt2.get(0.,tkinter.END)
            script = get_script_from_tree(json.loads(jstree))
            cd.delete(0.,tkinter.END)
            cd.insert(0.,script)
        except:
            e = traceback.format_exc()
            cd.delete(0.,tkinter.END)
            cd.insert(0.,e)

    def change_module(*a):
        tp = cbx.get().strip()
        btn_create_python_code['text'] = re.sub(r'\[[^\[\]+]*\]',tp,btn_create_python_code['text'])

    def translate_js():
        tp = cbx.get().strip()
        jscode = txt1.get(0.,tkinter.END)
        if 'execjs' in tp:
            pythoncode = """
#coding=utf-8
jscode = r'''
$^^$jscode$^^$
'''

# 如果出现编码异常，可以尝试解开下面注释中的代码以处理 execjs 执行时期的编码问题。
# import subprocess
# _bak_Popen = subprocess.Popen
# def _Popen(*a, **kw):
#     kw['encoding'] = 'utf-8'
#     return _bak_Popen(*a, **kw)
# subprocess.Popen = _Popen

import execjs
ctx = execjs.compile(jscode)
result = ctx.call('func',10,20) # 执行函数，需要传参函数将参从第二个开始依次排在方法名后面
# result = ctx.eval('func(22,33)')
print(result)
""".replace('$^^$jscode$^^$', jscode.strip()).strip()
        if 'js2py' in tp:
            pythoncode = """
#coding=utf-8
jscode = r'''
$^^$jscode$^^$
'''

import js2py
# js = js2py.eval_js(jscode) 
# 这里的 js 是代码执行后最后一个 var 赋值的参数返回出来。
# print(js) # 这种模式有弊端，每次都要解析一遍。

# 请尽量使用下面的方式，这样可以直接用 . 调用内部函数或参数
js = js2py.EvalJs()
js.execute(jscode)
print(js.a)
print(js.func)
""".replace('$^^$jscode$^^$', jscode.strip()).strip()
        txt2.delete(0.,tkinter.END)
        txt2.insert(0.,pythoncode)


    import queue
    Q = queue.Queue()
    S = queue.Queue()
    def exec_javascript(*a):
        def _temp():
            __very_unique_cd__ = None
            nonlocal cd
            nonlocal Q, S
            Q.put('V|GETSCRIPT')
            cs = S.get()
            td = tempfile.mkdtemp()
            tf = os.path.join(td,'temp.py')
            with open(tf,'w',encoding='utf-8') as f:
                f.write(cs)
            s = sys.executable
            s = s + ' ' + tf
            import subprocess
            p = subprocess.Popen(s, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, encoding='utf-8')
            Q.put('V|DELETE')
            Q.put('============================== start ==============================\n')
            for line in iter(p.stdout.readline, ''):
                if line:
                    Q.put(line)
                else:
                    break
            Q.put('==============================  end  ==============================')
            p.wait()
            p.stdout.close()
            shutil.rmtree(td)
        threading.Thread(target=_temp).start()

    def loop_in_tkinter():
        __very_unique_cd__ = None
        nonlocal cd, Q, S
        from .tab import nb
        c = []
        while Q.qsize():
            try:
                i = Q.get_nowait()
                if i == 'V|DELETE':
                    cd.delete(0., tkinter.END)
                elif i == 'V|GETSCRIPT':
                    cs = txt2.get(0.,tkinter.END)
                    S.put(cs)
                else:
                    try:
                        cd.insert(tkinter.END, i)
                    except:
                        cd.insert(tkinter.END, re.sub('[\uD800-\uDBFF][\uDC00-\uDFFF]|[\U00010000-\U0010ffff]','',i))
                    cd.see(tkinter.END)
                    cd.update()
            except:
                import traceback
                tkinter.messagebox.showinfo('Error',traceback.format_exc())
        nb.after(200, loop_in_tkinter)
    loop_in_tkinter()

    def _exec_javascript(*a):
        from .tab import show_code_log
        show_code_log()
        exec_javascript()

    def js_beautify(*a):
        try:
            import jsbeautifier
            jscode = txt1.get(0.,tkinter.END)
            btjscode = jsbeautifier.beautify(jscode)
            txt1.delete(0.,tkinter.END)
            txt1.insert(0.,btjscode)
        except ImportError as e:
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,e)
        except:
            einfo = traceback.format_exc() + \
            '\n\njs代码美化在一些极端的 eval 函数美化时会出现一些问题' + \
            '\n所以出现错误时可以考虑检查代码的 eval 函数的处理'
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,einfo)

    def save_script_in_desktop(*a):
        name = askstring('脚本名','请输入脚本文件名，尽量小写无空格。')
        if not name: return
        if not name.endswith('.py'): name += '.py'
        desktop_script = os.path.join(os.path.expanduser("~"),'Desktop\\{}'.format(name))
        if not os.path.isfile(desktop_script):
            with open(desktop_script, 'w', encoding='utf-8') as f:
                f.write(txt2.get(0.,tkinter.END))
        else:
            tkinter.messagebox.showwarning('脚本已存在','脚本已存在')

    def save_defusion_desktop():
        try:
            try:
                from .pyjsdefusion import get_node_string
            except:
                from pyjsdefusion import get_node_string
            jscode = get_node_string()
            name = 'babel_defusion.js'
            desktop_script = os.path.join(os.path.expanduser("~"), 'Desktop', name)
            if not os.path.isfile(desktop_script):
                with open(desktop_script, 'w', encoding='utf-8') as f:
                    f.write(jscode)
            else:
                tkinter.messagebox.showwarning('脚本已存在','脚本已存在')
        except:
            e = traceback.format_exc()
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,e)

    def _ast_hook_create(*a):
        try:
            cwd = os.getcwd()
            home = os.environ.get('HOME')
            home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
            hnode = os.path.join(home, '.vrequest_node')
            if not os.path.isdir(hnode): os.mkdir(hnode)
            os.chdir(hnode)
            cmd = 'start cmd /k "{}"'.format('cnpm install @babel/core @babel/types @babel/generator -S')
            import subprocess
            if not shutil.which("cnpm"):
                cmd = 'start cmd /k "{}"'.format('npm install cnpm -g && cnpm install @babel/core @babel/types @babel/generator -S')
            subprocess.Popen(cmd, creationflags=0x8000000, shell=True)
        except:
            e = traceback.format_exc()
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,e)
            os.chdir(cwd)

    def _ast_hook_makejs(*a):
        try:
            cwd = os.getcwd()
            home = os.environ.get('HOME')
            home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
            hnode = os.path.join(home, '.vrequest_node')
            if not os.path.isdir(hnode): os.mkdir(hnode)
            os.chdir(hnode)
            filename = os.path.join(os.path.split(__file__)[0], 'ast_hook_inject.js')
            import execjs
            with open(filename, encoding='utf-8') as f:
                ctx = execjs.compile(f.read(), cwd=hnode)
                jscode = ctx.call('make_inject_hook', txt1.get(0.,tkinter.END))
                txt2.delete(0.,tkinter.END)
                txt2.insert(0.,jscode)
        except:
            e = traceback.format_exc()
            txt2.delete(0.,tkinter.END)
            txt2.insert(0.,e)
            os.chdir(cwd)

    def about_js(*a):
        from .tab import nb
        from .tab import SimpleDialog
        qq = [   
                # [make_js_script,      '用语法树生成代码'],
                [make_js_tree,          '生成语法树'],
                [translate_js_python,   '简单js代码翻译成[python]代码(可能有错误)'],
                [defusion_js_code,      '使用node简单逆混肴代码'],
                [defusion_ob_js_code,   '使用node解密ob混淆'],
                [save_defusion_desktop, '保存node逆混淆单脚本置桌面(用于单独开发)'],
                [js_mod_pack,           '用于打包js代码的一些方式'],
                [_ast_hook_create,      '创建内存漫游项目空间（只用执行一次）'],
                [_ast_hook_makejs,      '生成内存漫游 js 脚本'],
            ]
        q = [i[1] for i in qq]
        d = SimpleDialog(nb,
            text="请选择启动方式",
            buttons=q,
            default=0,
            cancel=-1,
            title="js功能")
        id = d.go()
        if id == -1: return
        qq[id][0]()

    # 查看常用的js解析器的引入状态
    support_modules = ['execjs', 'js2py']
    def get_js_import_stat(support_modules):
        s = []
        def _temp(module):
            try:
                __import__(module)
                s.append('+ Enable Use [{}] js driver.'.format(module))
            except:
                s.append('- Unable Use [{}] js driver.'.format(module))
        for module in support_modules:
            _temp(module)
        return s
    import_stat = get_js_import_stat(support_modules)
    temp_fr0 = Frame(fr)
    temp_fr0.pack(fill=tkinter.X)
    import_modules = [i[i.find('['):i.rfind(']')+1] for i in import_stat if i.startswith('+')]
    if not import_modules:
        einfo = 'unfind any of {} module.'.format(support_modules)
        tkinter.messagebox.showinfo('Error',einfo)
        raise EnvironmentError(einfo)
    cbx = Combobox(temp_fr0,width=13,state='readonly')
    cbx['values'] = import_modules
    cbx.current(0)
    cbx.pack(fill=tkinter.X,side=tkinter.LEFT)
    cbx.bind('<<ComboboxSelected>>', change_module)

    btn_js_beautify = Button(temp_fr0,text='js代码美化',command=js_beautify)
    btn_js_beautify.pack(side=tkinter.LEFT)
    btn_create_python_code = Button(temp_fr0,text='生成python[]代码 [Alt+c]',command=translate_js)
    btn_create_python_code.pack(side=tkinter.LEFT)
    btn_translate_js = Button(temp_fr0,text='翻译成[js2py]代码',command=translate_js_js2py)
    btn_translate_js.pack(side=tkinter.LEFT)

    btn2 = Button(temp_fr0, text='[执行py代码] <Alt+v>', command=_exec_javascript)
    btn2.pack(side=tkinter.RIGHT)
    btn2 = Button(temp_fr0, text='保存脚本到桌面', command=save_script_in_desktop)
    btn2.pack(side=tkinter.RIGHT)
    btn2 = Button(temp_fr0, text='js语言相关', command=about_js)
    btn2.pack(side=tkinter.RIGHT)

    # btn2 = Button(temp_fr0, text='用语法树生成代码', command=make_js_script)
    # btn2.pack(side=tkinter.RIGHT)
    # btn2 = Button(temp_fr0, text='生成语法树', command=make_js_tree)
    # btn2.pack(side=tkinter.RIGHT)
    # btn2 = Button(temp_fr0, text='使用node简单逆混肴代码', command=defusion_js_code)
    # btn2.pack(side=tkinter.RIGHT)
    # btn2 = Button(temp_fr0,text='简单js代码翻译成[python]代码(可能有错误)',command=translate_js_python)
    # btn2.pack(side=tkinter.RIGHT)


    temp_fr0 = Frame(fr)
    temp_fr0.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)
    temp_fr1 = Frame(temp_fr0)
    temp_fr1_1 = Frame(temp_fr1)
    temp_fr1_1.pack(side=tkinter.TOP)
    temp_fr1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.LEFT)
    txt1 = Text(temp_fr1,height=1,width=1,font=ft)
    lab1 = Label(temp_fr1_1,text='js代码')
    lab1.pack(side=tkinter.TOP)
    txt1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)
    temp_fr2 = Frame(temp_fr0)
    temp_fr2_1 = Frame(temp_fr2)
    temp_fr2_1.pack(fill=tkinter.X,side=tkinter.TOP)
    temp_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.RIGHT)
    lab1 = Label(temp_fr2_1,text='python代码')
    lab1.pack(side=tkinter.TOP)
    txt2 = Text(temp_fr2,height=1,width=1,font=ft)
    txt2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)

    temp_fr3 = Frame(fr)
    lab3 = Label(temp_fr3, text='代码结果 [Esc 切换显示状态]')
    lab3.pack(side=tkinter.TOP)
    cd = Text(temp_fr3,font=ft)
    cd.pack(fill=tkinter.BOTH,expand=True)


    test_code = '''
// test_code
function func(a,b){
    return a+b
}

var a = func(1,3);
'''.strip()
    txt1.insert(0.,test_code)


    change_module()
    try:
        from idlelib.colorizer import ColorDelegator
        from idlelib.percolator import Percolator
        p = ColorDelegator()
        Percolator(txt2).insertfilter(p) # txt2 是js2py生成的python代码，需要填色
    except:
        e = traceback.format_exc()
        txt2.delete(0.,tkinter.END)
        txt2.insert(0.,e)




    frame_setting[fr] = {}
    frame_setting[fr]['type'] = 'js'
    frame_setting[fr]['execute_func0'] = translate_js
    frame_setting[fr]['execute_func1'] = translate_js_js2py
    frame_setting[fr]['execute_func'] = exec_javascript
    frame_setting[fr]['import_stat'] = import_stat
    frame_setting[fr]['fr_temp2'] = temp_fr3 # 代码执行框，这里仍需挂钩esc按键显示/关闭该窗口
    return fr








def selenium_test_window(setting=None):
    '''
    快速使用临时的 selenium 启动浏览器并且快速将某些操作自动化处理
    '''
    fr = Frame()
    ft = Font(family='Consolas',size=10)

    def print(*a):
        from .tab import show_code_log
        try:
            show_code_log()
            txt = ' '.join(map(str,a)) + '\n'
            cd.insert(tkinter.END,re.sub('[\uD800-\uDBFF][\uDC00-\uDFFF]|[\U00010000-\U0010ffff]','',txt))
            cd.see(tkinter.END)
            cd.update()
        except:
            pass

    temp_fr0 = Frame(fr)
    temp_fr0.pack(fill=tkinter.X)

    def get_webdriver():
        local = {'get_driver_func':None}
        exec(txt2.get(0.,tkinter.END)+'\nlocal["get_driver_func"] = get_driver', None, {'local':local})
        get_driver_func = local['get_driver_func']
        return get_driver_func()

    driver = None
    def start_selenium(*a):
        nonlocal driver
        def _():
            nonlocal driver
            if driver is None:
                print('预备启动，请等待获取 driver 对象。')
                driver = 'None' # 启动浏览器为耗时操作，这里用了多线程，所以要防启动间隙多次启动
                try:
                    import subprocess
                    _bak_Popen = subprocess.Popen
                    def _Popen(*a, **kw):
                        kw['creationflags'] = 0x08000000
                        return _bak_Popen(*a, **kw)
                    subprocess.Popen = _Popen
                    driver = get_webdriver()
                    print('启动成功，可以在代码窗使用 driver 对象代码。')
                    def hook_close():
                        nonlocal driver
                        while True:
                            try:
                                time.sleep(.1)
                                for i in driver.get_log('driver'):
                                    if 'Unable to evaluate script: disconnected: not connected to DevTools' in i.get('message'):
                                        break
                            except:
                                break
                        print('窗口关闭。')
                        driver = None
                    threading.Thread(target=hook_close).start()
                except:
                    print(traceback.format_exc())
                finally:
                    subprocess.Popen = _bak_Popen
            else:
                tkinter.messagebox.showwarning('警告','浏览器driver已启动，如需重启，先关闭。')
        threading.Thread(target=_).start()
                
    def close_selenium(*a):
        # nonlocal driver
        # def _():
        #     nonlocal driver
        #     if driver is not None and driver != 'None':
        #         _driver = driver
        #         try:
        #             try: print('正在关闭，请等待片刻。')
        #             except: pass
        #             driver = 'None'
        #             _driver.quit()
        #             driver = None
        #             print('关闭成功，代码窗口将不能使用 driver 对象。')
        #         except:
        #             print(traceback.format_exc())
        #     elif driver == 'None':
        #         clear_selenium_driver()
        #     else:
        #         print('警告','不存在已启动的浏览器')
        # threading.Thread(target=_).start()
        clear_selenium_driver()
        print('已关闭进程中所有的 chromedriver 进程。')

    def clear_selenium_driver(*a):
        nonlocal driver
        os.popen('taskkill /f /im chromedriver.exe /t')
        driver = None

    def execute_selenium_code(*a):
        nonlocal print, driver
        code = txt1.get(0., tkinter.END)
        local = {'print':print, 'driver':driver}
        try:
            exec(code, None, local)
        except:
            print(traceback.format_exc())

    def save_script_in_desktop(*a):
        name = askstring('脚本名','请输入脚本文件名，尽量小写无空格。')
        if not name: return
        if not name.endswith('.py'): name += '.py'
        desktop_script = os.path.join(os.path.expanduser("~"),'Desktop\\{}'.format(name))
        if not os.path.isfile(desktop_script):
            with open(desktop_script, 'w', encoding='utf-8') as f:
                script = txt2.get(0.,tkinter.END) + '\ndriver = get_driver()\n'
                script += txt1.get(0.,tkinter.END) + '\ndriver.quit()'
                f.write(script)
        else:
            tkinter.messagebox.showwarning('脚本已存在','脚本已存在')

    def add_script(*a):
        if '常见用法，请求某个网页' not in txt1.get(0., tkinter.END):
            txt1.insert(tkinter.END, '''
# 常见用法，请求某个网页，在某个输入框输入内容，点击提交按钮
driver.get('http://baidu.com')
driver.find_element_by_xpath('//*[@id="kw"]').clear()
driver.find_element_by_xpath('//*[@id="kw"]').send_keys('123123')
driver.find_element_by_xpath('//*[@id="su"]').click()
# driver.find_element_by_xpath('//*[@id="su"]').get_attribute() # 获取属性









# (1) 常用获取组件方式
#     1 find_element_* 直接获取组件对象，如果获取不到直接报错
#       driver.find_element_by_id
#       driver.find_element_by_name
#       driver.find_element_by_xpath
#     2 find_elements_* 获取组件列表对象，如果获取不到不会报错，只会返回空
#       driver.find_elements_by_id
#       driver.find_elements_by_name
#       driver.find_elements_by_xpath
# (2) 获取 window 桌面绝对路径的代码，用于快速保存数据到可见位置
#     desktop = os.path.join(os.path.expanduser("~"),'Desktop')
# (3) 部分智能等待的代码，提高浏览器效率的处理，最好在生成的单独脚本中使用
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.support import expected_conditions as EC
#     from selenium.webdriver.support.wait import WebDriverWait as wbw
#     locator = (By.XPATH, '//img[@class="focus-item-img"]')
#     # wbw(self.webdriver,10).until(EC.presence_of_element_located(locator)) # 判断某个元素是否被加到了dom树里
#     wbw(self.webdriver,10).until(EC.visibility_of_element_located(locator)) # 判断某个元素是否被添加到了dom里并且可见，即宽和高都大于0
# (4) 当你打包脚本时，在 get_driver 函数执行前执行以下代码，打包的后的工具就不会因为 selenium启动服务自动开启黑窗口了
#     import subprocess
#     _bak_Popen = subprocess.Popen
#     def _Popen(*a, **kw):
#         kw['creationflags'] = 0x08000000
#         return _bak_Popen(*a, **kw)
#     subprocess.Popen = _Popen



# mitmproxy调试功能增强
#     功能：使用 mitmproxy 修改浏览器请求返回的数据，用于绕过浏览器返回的js中的某些反调试js代码。
#         使用 fiddler 也能做到，不过那种修改起来比较麻烦
#         使用 mitmproxy 可以使用 python 代码来修改返回信息，对我来说会更加方便一些
#         这样可以更简单的实现更加复杂的替换操作
#         需要安装 mitmproxy： pip install mitmproxy -i https://pypi.douban.com/simple
#         使用该库的命令行工具 mitmdump 来创建一个代理端口
#         mitmdump -q -s change_js.py -p 8888
#             -q 静音模式(仅限制该代码内的打印输出) -s 指定mitm中间件代码(即当前代码脚本) -p 指定端口(默认8080)
# # 以下为 change_js.py 代码脚本中的脚本内容
# # 1将代码揭开注释写入文件，
# # 2然后使用命令行工具 mitmdump 执行代码启动服务，
# # 3最后再用配置好端口的浏览器直接访问正常网页就可以正常修改内容
# import re
# import json
# from mitmproxy.http import flow
# def response(flow: flow):
#     target_url = 'https://www.baidu.com'
#     if  target_url in flow.request.url:
#         jscode = flow.response.get_text()
#         jscode = jscode.replace('debugger', '')
#         flow.response.set_text(jscode)
#         print('changed.', flow.request.url)
''')

    show_xpath_finder = False
    def switch_window(*a):
        nonlocal show_xpath_finder
        if not show_xpath_finder:
            temp_fr2.pack_forget()
            temp_fr3.pack(fill=tkinter.BOTH,expand=True,side=tkinter.RIGHT)
        else:
            temp_fr3.pack_forget()
            temp_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.RIGHT)
        show_xpath_finder = not show_xpath_finder

    class driver_color_changer:
        def __init__(self, driver):
            self.attr = 'style'
            self.driver = driver
            self.default_color = "background:green"
            self.default_func = "arguments[0].setAttribute('style',arguments[1]);"
            self.origin = []
        def highlight_list(self, xpath):
            ls = driver.find_elements_by_xpath(xpath)
            if ls:
                for dr in ls:
                    self.origin.append({'style':dr.get_attribute('style'), 'node':dr})
                    self.driver.execute_script( self.default_func, dr, self.default_color, )
        def clear(self):
            while self.origin:
                d = self.origin.pop()
                try:
                    self.driver.execute_script( self.default_func, d['node'], d['style'], )
                except:
                    pass
                    # import traceback
                    # print(traceback.format_exc())

    dcc = None
    dic = {}
    dis = {}
    def xpath_list_highlight(*a):
        nonlocal print, driver, show_xpath_finder, dcc, dic, dis
        from .util import get_xpath_by_str, get_simple_path_tail
        from lxml import etree
        if driver is None:
            print('no chromedriver opened.')
            return
        content = driver.page_source
        if not show_xpath_finder: switch_window()
        if dcc is None: dcc = driver_color_changer(driver)
        dcc.driver = driver
        q = []
        for xp,strs in get_xpath_by_str("", content):
            q.append((xp, strs))
        p = sorted(q, key=lambda i:len(i[0]))
        lbx3.delete(0, tkinter.END)
        if p:
            for idx, (xp, strs) in enumerate(p):
                lbx3.insert("end", xp)
                dic[xp] = strs
                for j,c in strs:
                    lbx3.insert("end", '    [ content ]: {} {}'.format(j,c))
        else:
            print('no xpath list find.')

    def xpath_highlight(*a):
        nonlocal print, driver, show_xpath_finder, dcc, dic, dis
        from .util import get_xpath_by_str, get_simple_path_tail
        from lxml import etree
        if driver is None:
            print('no chromedriver opened.')
            return
        content = driver.page_source
        if not show_xpath_finder: switch_window()
        if dcc is None: dcc = driver_color_changer(driver)
        dcc.driver = driver
        def normal_etree(e, tags=['script','style','select','noscript','textarea'], rootxpath='//html'):
            q = []
            for it in e.getiterator():
                if it.tag in tags or type(it.tag) is not str:
                    q.append(it)
            for it in q:
                p = it.getparent()
                if p is not None:
                    p.remove(it)
            return e
        e = etree.HTML(re.sub(r'^ *<\?xml[^<>]+\?>', '', content))
        e = normal_etree(e)
        ls = []
        for i in e.xpath('//*'):
            xps = get_simple_path_tail(i) 
            if not xps: continue
            xp, sxp, key = xps
            v = e.xpath('string({})'.format(sxp))
            v = re.sub(r'\s+',' ',v).strip()
            if v and (sxp, v) not in ls:
                ls.append((sxp, v))
        lbx3.delete(0, tkinter.END)
        if ls:
            mxl = 0
            for sxp, v in ls: mxl = len(sxp) if len(sxp) > mxl else mxl
            fmt = '{:<3}[len:{:>4}:{:>2}] {:<' + str(mxl + 3) + '}'
            ls = sorted(ls, key=lambda i:len(i[1]))[::-1]
            for idx, (sxp, v) in enumerate(ls, 1):
                lbx3.insert("end", fmt.format(idx, len(v), mxl, sxp) + (v[:20]+'...'+v[-20:] if len(v) > 40 else v))
        else:
            print('no xpath find.')

    def show_log(*a):
        nonlocal dic, dcc
        try: xp = lbx3.get(lbx3.curselection())
        except: return
        if xp.lstrip().startswith('[ content ]:'): return
        mxl = re.findall(r'\[len: *\d+: *(\d+)\]', xp)
        if mxl:
            mxl = int(mxl[0])
            xp = re.sub(r'\[len: *\d+: *(\d+)\]', '', xp[17:18+mxl].strip()).strip()
        dcc.clear()
        dcc.highlight_list(xp)

    def double_click(*a):
        nonlocal dic, dcc
        try: xp = lbx3.get(lbx3.curselection())
        except: return
        if xp.lstrip().startswith('[ content ]:'): return
        dcc.clear()
        dcc.highlight_list(xp)

    show_code_window = True
    def close_exec_code_window(*a):
        nonlocal show_code_window
        if show_code_window:
            temp_fr1.pack_forget()
        else:
            temp_fr1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.LEFT)
        show_code_window = not show_code_window


    def _mitm_changejs_create(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            mitmcode = r'''
hook_script = r"""
// eval Function Function.constructor 三种执行字符串脚本的挂钩
(function(){
  const handler = { apply: function (target, thisArg, args){
      // debugger;
      console.log("----- eval(*) -----\n" + args);
      return target.apply(thisArg, args) } }
  window.eval = new Proxy(window.eval, handler);
})();
(function(){
  const handler = { apply: function (target, thisArg, args){
      // debugger;
      console.log("----- Function(*) -----\n" + args);
      return target.apply(thisArg, args) } }
  window.Function = new Proxy(window.Function, handler);
})();
Function.prototype.__defineGetter__('constructor', function() { return function(...args) {
    // debugger;
    console.log('----- Function constructor(*) -----\n', ...args); 
    return Function(...args); }; });



// 挂钩 XMLHttpRequest. 设置请求头和发起请求的时机
(function(){
  const handler = { apply: function (target, thisArg, args){
      // debugger;
      console.log("----- XMLHttpRequest_open -----\n", args)
      return target.apply(thisArg, args) } }
  XMLHttpRequest.prototype.open = new Proxy(XMLHttpRequest.prototype.open, handler);
})();
(function(){
  const handler = { apply: function (target, thisArg, args){
      // debugger;
      console.log("----- XMLHttpRequest_setRequestHeader -----\n", args)
      return target.apply(thisArg, args) } }
  XMLHttpRequest.prototype.setRequestHeader = new Proxy(XMLHttpRequest.prototype.setRequestHeader, handler);
})();




// 挂钩生成cookie设置时机，但是这里是有问题的，这里如果挂钩，之后请求时候可能无法使用挂钩后设置的 cookie 键值
(function(){
  var _cookie = document.__lookupSetter__('cookie');
  var _cookie_set = function(c) {
    if (/RM4hZBv0dDon443M/.test(c)){
      // debugger;
    }
    console.log('----- cookie.set -----\n', c);
    _cookie = c;
    return _cookie;
  }
  var mycookie = document.cookie;
  document.__defineSetter__("cookie", _cookie_set);
  document.__defineGetter__("cookie", function() {return _cookie;} );
  Object.getOwnPropertyNames(String.prototype).filter(k => !!String.prototype[k].call).map(function(a){
    if (!/^caller$|^callee$|^arguments$/.test(a)){
      document.cookie[a] = mycookie[a];
    }
  });
  document.cookie.toString = function (){ return mycookie.toString() };
})();



// 挂钩一些对象的参数，特别是该值为列表，也会挂钩该列表对象的push函数
var hook_set = (function(pname, pobject){
  var win_param = pobject.__lookupSetter__(pname);
  var win_param_set = function(c) {
    console.log('----- ' + pname + '.set -----\n', c);
    win_param = c;
    if (win_param instanceof Array){
      (function(){
        const handler = { apply: function (target, thisArg, args){
          // debugger;
          console.log("----- " + pname + " Array.push -----\n", args)
          return target.apply(thisArg, args) } }
        win_param.push = new Proxy(win_param.push, handler);
      })();
    }
    return win_param;
  }
  pobject.__defineSetter__(pname, win_param_set);
  pobject.__defineGetter__(pname, function() {return win_param;} );
});
// hook_set('_$ss', window)
// hook_set('_$pr', window)



// 挂钩打印函数
_console_log = console.log;
console.log = function(...args){
  if (args && args[0] == '有时候控制台输出太多无意义内容会影响性能，可以hook对部分字符串进行不打印'){
    return 
  }
  _console_log(...args);
}
"""












import re
import json
from mitmproxy import ctx
print('start mitmdump in {}'.format(ctx.master.server.address[1]))
print('wanna change proxy? ctl+c and use new command: "mitmdump -q -s mitm_changejs.py -p $newproxy"')
print('该代码将自动设置全局代理，停止 Ctrl+C 或关闭窗口均可自动关闭全局代理，')
print('如果计算机异常关闭，代理可能还处于开启状态，')
print('这时你可以打开 vv 工具，然后右键选择浏览器窗口，点击关闭代理即可。')
def response(flow):
    if 'xxxxxxxxxxxxxxxxxxxxx' in flow.request.url:
        # 针对某个请求返回的结果进行定制修改，在js抵达浏览器之前就被修改
        # 使用下面的 get_text()/set_text(text) 进行获取和修改，
        # 如果是修改二进制数据就用 get_content/set_content 进行获取和修改
        toggle = True
        def rep(e): 
            nonlocal toggle
            ret = e.group(0)
            if toggle and 'src=' not in ret:
                toggle = False
                return e.group(0) + hook_script
            elif toggle:
                toggle = False
                return """<script type="text/javascript">{}</script>""".format(hook_script) + e.group(0)
            else:
                return e.group(0)
        jscode = flow.response.get_text()
        jscode = re.sub('<script[^>]*>', rep, jscode)
        flow.response.set_text(jscode)
    buti_resp_print(flow)

def request(flow):
    if 'xxxxxxxxxxxxxxxxxxxxx' in flow.request.url:
        # 如果想要截断，直接加上 raise 即可截断请求流
        # 对请求流进行截断，可以处理某一些类似于瑞数的重放攻击，
        # 让浏览器加密运算好的请求信息不发送出去，传递给其他请求模块进行请求。
        flow.request.headers['User-Agent'] = 'VILAME'
    buti_req_print(flow)



# 后面的代码不用过多关注，固定不变即可。
import os
import time
import shutil
import threading
def clear_cache():
    # 删除缓存文件，看起来干净点
    while True:
        time.sleep(.3)
        pt = os.path.join(os.path.split(__file__)[0], '__pycache__')
        if os.path.isdir(pt):
            shutil.rmtree(pt)
            break
threading.Thread(target=clear_cache).start()
# 打开全局的代理，让代理自动切换
import ctypes
import winreg
class WindowProxySetting:
    def __init__(self, proxy="127.0.0.1:8888"):
        proxy_path = r'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings'
        self.proxy = proxy
        self.root = winreg.HKEY_CURRENT_USER
        self.hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, proxy_path)
        self.set_proxy = [
            [proxy_path, "ProxyEnable", winreg.REG_DWORD, 1],
            [proxy_path, "ProxyServer", winreg.REG_SZ, self.proxy],
        ]
    def _flash(self):
        try:
            internet_set_option = ctypes.windll.Wininet.InternetSetOptionW    
            internet_set_option(0, 39, 0, 0)
            internet_set_option(0, 37, 0, 0)
        except:pass
    def open(self):
        self.set_proxy[0][3] = 1
        for keypath, value_name, value_type, value in self.set_proxy:
            self.hKey = winreg.CreateKey(self.root, keypath)
            winreg.SetValueEx(self.hKey, value_name, 0, value_type, value)
        self._flash()
    def close(self):
        self.set_proxy[0][3] = 0
        for keypath, value_name, value_type, value in self.set_proxy:
            self.hKey = winreg.CreateKey(self.root, keypath)
            winreg.SetValueEx(self.hKey, value_name, 0, value_type, value)
        self._flash()
    def get_state(self):
        value, type = winreg.QueryValueEx(self.hKey, "ProxyEnable")
        return bool(value)
wproxy = WindowProxySetting(proxy="127.0.0.1:{}".format(ctx.master.server.address[1]))
wproxy.open()
import signal
import sys
def Quit(signum, frame):
    wproxy.close()
    print('proxy close.')
    print('command: "mitmdump -q -s mitm_changejs.py -p $newproxy"')
    sys.exit(0)
signal.signal(signal.SIGINT, Quit)
signal.signal(signal.SIGTERM, Quit)
# 美化 headers 输出
def header_fprint(headers_dict):
    maxklen = len(repr(max(headers_dict,key=len)))
    for keystring in sorted(headers_dict):
        valuestring = headers_dict[keystring]
        if 'cookie' in keystring.lower():
            vlist = sorted(valuestring.split('; '))
            for idx,value in enumerate(vlist):
                endsp = ('; ' if idx != len(vlist)-1 else '')
                lstring = ('{:<'+str(maxklen)+'}:({}').format(repr(keystring), repr(value+endsp)) if idx == 0 else \
                          ('{:<'+str(maxklen)+'}  {}').format('', repr(value+endsp))
                if idx == len(vlist)-1: lstring += '),'
                print(lstring)
        else:
            print(('{:<'+str(maxklen)+'}: {},').format(repr(keystring), repr(valuestring)))
def buti_req_print(flow):
    print('===========\n| request |\n===========')
    print('request method: {}\nrequest url: {}'.format(flow.request.method, flow.request.url))
    print('------------------- request headers ---------------------')
    header_fprint(dict(flow.request.headers))
    print('------------------- request body ------------------------')
    print(flow.request.content, end='\n\n\n')
def buti_resp_print(flow):
    print('============\n| response |\n============')
    print('status: {}\nresponse length: {}\nurl: {}'.format(flow.response.status_code, len(flow.response.get_content()), flow.request.url))
    print('------------------- response headers --------------------')
    header_fprint(dict(flow.response.headers))
    print('------------------- response content[:1000] ----------------')
    print('response content[:1000]:\n {}'.format(flow.response.get_content()[:1000]), end='\n\n\n')
    '''
            f.write(mitmcode)

    def _mitm_changejs_use(filename):
        cwd = os.getcwd()
        desktop = os.path.join(os.path.expanduser("~"),'Desktop')
        os.chdir(desktop)
        import subprocess
        # 挂钩cmd关闭，让强制关闭cmd能够自动关闭掉代理
        close_proxy = '''python -c "x=0;import ctypes;import winreg;v=winreg.CreateKey(winreg.HKEY_CURRENT_USER,r'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings');winreg.SetValueEx(v,'ProxyEnable',0,winreg.REG_DWORD,x);c=ctypes.windll.Wininet.InternetSetOptionW;c(0,39,0,0);c(0,37,0,0)"'''
        # close_proxy = '''python -c "x=0;p='127.0.0.1:8888';import ctypes;import winreg;v=winreg.CreateKey(winreg.HKEY_CURRENT_USER,r'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings');winreg.SetValueEx(v,'ProxyEnable',0,winreg.REG_DWORD,x);winreg.SetValueEx(v,'ProxyServer',0,winreg.REG_SZ,p);c=ctypes.windll.Wininet.InternetSetOptionW;c(0,39,0,0);c(0,37,0,0)"'''
        try:
            assert shutil.which("powershell")
            cmd = 'start /wait powershell -NoExit "{}"'.format('mitmdump -q -s "{}" -p 8888'.format(filename))
            subprocess.Popen(cmd+' && '+close_proxy, creationflags=0x8000000, shell=True)
        except:
            cmd = 'start /wait cmd /k "{}"'.format('mitmdump -q -s "{}" -p 8888'.format(filename))
            subprocess.Popen(cmd+' && '+close_proxy, creationflags=0x8000000, shell=True)
        os.chdir(cwd)

    def start_mitm_in_desktop(*a):
        filename = os.path.join(os.path.expanduser("~"),'Desktop', 'mitm_changejs.py')
        from .tab import nb
        from .tab import SimpleDialog
        q = [   '在桌面覆盖创建新的模板脚本 mitm_changejs.py 并启动',
                '在桌面使用已存在的 mitm_changejs.py 脚本启动', 
            ]
        d = SimpleDialog(nb,
            text="请选择启动方式",
            buttons=q,
            default=0,
            cancel=-1,
            title="启动mitmdump")
        id = d.go()
        if id == -1: return
        if id == 0: _mitm_changejs_create(filename), _mitm_changejs_use(filename)
        if id == 1: _mitm_changejs_use(filename)
        if id == 2:
            pass

    script_v1 = '''
def get_driver():
    from selenium import webdriver
    option = webdriver.ChromeOptions()
    extset = ['enable-automation', 'ignore-certificate-errors']
    ignimg = "profile.managed_default_content_settings.images"
    mobile = {'deviceName':'Galaxy S5'}

    # 需要哪些 driver 功能，请解开对应的代码注释再启动
    option.add_argument("--disable-infobars")                       # 关闭调试信息
    option.add_experimental_option("excludeSwitches", extset)       # 关闭调试信息
    option.add_experimental_option("useAutomationExtension", False) # 关闭调试信息
    option.add_argument('--start-maximized')                        # 最大化
    # option.add_experimental_option('mobileEmulation', mobile)     # 手机模式
    # option.add_experimental_option("prefs", {ignore_image: 2})    # 不加载图片
    # option.add_argument('--headless')                             # 【*】 无界面
    # option.add_argument('--no-sandbox')                           # 【*】 沙箱模式
    # option.add_argument('--disable-dev-shm-usage')                # 【*】 in linux
    # option.add_argument('--window-size=1920,1080')                # 无界面最大化
    # option.add_argument('--disable-gpu')                          # 禁用 gpu 加速
    # option.add_argument("--auto-open-devtools-for-tabs")          # F12
    # option.add_argument("--user-agent=Mozilla/5.0 VILAME")        # 修改 UA
    # option.add_argument('--proxy-server=http://127.0.0.1:8888')   # 代理

    # 处理 document.$cdc_asdjflasutopfhvcZLmcfl_ 参数的指纹的检测
    def check_magic_word(driver_path, rollback=False):
        import shutil
        cpdriver = shutil.which(driver_path)
        with open(cpdriver, 'rb') as f: filebit = f.read()
        a, b = b'$cdc_asdjflasutopfhvcZLmcfl_', b'$pqp_nfqwsynfhgbcsuipMYzpsy_'
        a, b = (b, a) if rollback else (a, b)
        mgc_o, mgc_t = a, b
        if mgc_o in filebit: 
            with open(cpdriver, 'wb') as f: f.write(filebit.replace(mgc_o, mgc_t))
    driver_path = 'chromedriver'
    check_magic_word(driver_path, rollback=False)

    # 启动 webdriver
    webdriver = webdriver.Chrome(options=option, executable_path=driver_path)

    # 指纹相关的处理，能处理部分检测。
    webdriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": """
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, "plugins", { get: () => [1,2,3,4,5] });
      """
    })
    webdriver.execute_cdp_cmd("Network.enable", {})

    # 设置:当你直接关闭浏览器时自动关闭 chromedriver，防止进程残留
    import time, threading
    def hook_close_window():
        chrome_close = False
        while not chrome_close:
            time.sleep(.3) # 每0.3秒检测一次，如果强制关闭浏览器，则自动关闭
            try:    driver_logs = webdriver.get_log('driver')
            except: driver_logs = []
            for i in driver_logs:
                if 'Unable to evaluate script: disconnected: not connected to DevTools' in i.get('message'):
                    chrome_close = True
                    webdriver.quit()
    threading.Thread(target=hook_close_window).start()
    return webdriver
'''.strip()

    script_v2 = r"""
def get_driver():
    def get_win_chrome_path():
        # 注意，要使用非硬盘版安装的 chrome 软件才会在注册表里面留有痕迹，才能使用这个函数快速定位软件地址
        # 通常来说 chrome 的安装一般都是非硬盘版的安装，所以这个函数算是在 windows 系统下获取 chrome.exe 路径的通解。
        import os, winreg
        sub_key = ['SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall', 'SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall']
        def get_install_list(key, root):
            try:
                _key = winreg.OpenKey(root, key, 0, winreg.KEY_ALL_ACCESS)
                for j in range(0, winreg.QueryInfoKey(_key)[0]-1):
                    try:
                        each_key = winreg.OpenKey(root, key + '\\' + winreg.EnumKey(_key, j), 0, winreg.KEY_ALL_ACCESS)
                        displayname, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayName')
                        install_loc, REG_SZ = winreg.QueryValueEx(each_key, 'InstallLocation')
                        display_var, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayVersion')
                        yield displayname, install_loc, display_var
                    except WindowsError:
                        pass
            except:
                pass
        for key in sub_key:
            for root in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
                for name, local, var in get_install_list(key, root):
                    if name == 'Google Chrome':
                        return os.path.join(local, 'chrome.exe')
    chrome = get_win_chrome_path() # 尝试自动获取 chrome.exe 的地址
    driver = None # 如果有设置 chromedriver.exe 的环境变量，这里可以不用主动设置
    # driver = r'D:/Python/Python36/Scripts/chromedriver.exe'
    remote_port = 9223
    proxy_port = None # 8888 # 使用代理调试则将这里设置成代理端口既可，方便 mitmdump 等工具使用

    import os, shutil, subprocess
    chrome_path = shutil.which('chrome')       if not chrome else chrome # 在环境变量里面找文件的绝对地址
    driver_path = shutil.which('chromedriver') if not driver else driver # 在环境变量里面找文件的绝对地址
    assert chrome_path, "pls set chrome.exe path in env or set chrome=$abs_path(chrome.exe)."
    assert driver_path, "pls set chromedriver.exe path in env or set driver=$abs_path(chromedriver.exe)."

    # 临时 chrome 配置文件存放地址，防止破环日常使用的 chrome 配置
    # 另外，经过测试，如果删除掉旧的临时配置文件的地址，启动会块很多很多
    home = os.environ.get('HOME')
    home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
    home = os.path.join(home, 'auto_selenium', 'AutomationProfile')
    cache_path = os.path.split(home)[0]
    if os.path.isdir(cache_path):
        # print('cache_path clear: {}'.format(cache_path))
        shutil.rmtree(cache_path)
    # 如果想要使用代理
    if proxy_port: chrome_exe = '''"{}" --remote-debugging-port={} --user-data-dir="{}" --proxy-server=http://127.0.0.1:{}'''.format(chrome_path, remote_port, home, proxy_port)
    else:          chrome_exe = '''"{}" --remote-debugging-port={} --user-data-dir="{}"'''.format(chrome_path, remote_port, home)
    subprocess.Popen(chrome_exe)
    # print('driver_path: {}'.format(driver_path))
    # print('chrome_path: {}'.format(chrome_path))
    # print('chrome_exe: {}'.format(chrome_exe))

    import selenium
    from selenium import webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{}".format(remote_port))

    # 处理 document.$cdc_asdjflasutopfhvcZLmcfl_ 参数的指纹的检测
    def check_magic_word(driver_path, rollback=False):
        with open(driver_path, 'rb') as f: filebit = f.read()
        a, b = b'$cdc_asdjflasutopfhvcZLmcfl_', b'$pqp_nfqwsynfhgbcsuipMYzpsy_'
        a, b = (b, a) if rollback else (a, b)
        mgc_o, mgc_t = a, b
        if mgc_o in filebit: 
            with open(driver_path, 'wb') as f: f.write(filebit.replace(mgc_o, mgc_t))
    check_magic_word(driver_path, rollback=False)

    # 启动 webdriver
    webdriver = webdriver.Chrome(options=chrome_options, executable_path=driver_path)
    webdriver.set_page_load_timeout(5) # 让所有的 get 网页的加载都限制在 n秒钟内，防止无限加载的问题。
    _bak_get = webdriver.get
    def get(url):
        try:
            _bak_get(url)
        except selenium.common.exceptions.TimeoutException:
            print('selenium.common.exceptions.TimeoutException: {}'.format(url))
            get(url)
    webdriver.get = get

    # 设置:当你直接关闭浏览器时自动关闭 chromedriver.exe，防止进程残留
    import time, threading
    def hook_close_window():
        chrome_close = False
        while not chrome_close:
            time.sleep(.3) # 每0.3秒检测一次，如果强制关闭浏览器，则自动关闭 chromedriver.exe
            try:    driver_logs = webdriver.get_log('driver')
            except: driver_logs = []
            for i in driver_logs:
                if 'Unable to evaluate script: disconnected: not connected to DevTools' in i.get('message'):
                    chrome_close = True
                    webdriver.quit()
    threading.Thread(target=hook_close_window).start()
    return webdriver
""".strip()

    from itertools import cycle
    scripts_get_driver = {}
    scripts_get_driver['v1'] = script_v1
    scripts_get_driver['v2'] = script_v2
    scripts_get_driver_curr = 'v1'
    scripts_get_driver_loop = cycle(list(scripts_get_driver))
    next(scripts_get_driver_loop)

    def switch_script_get_driver(*a):
        nonlocal scripts_get_driver_curr
        curr_s = scripts_get_driver_curr
        next_s = next(scripts_get_driver_loop)
        scripts_get_driver_curr = next_s
        scripts_get_driver[curr_s] = txt2.get(0.,tkinter.END).strip()
        txt2.delete(0., tkinter.END)
        txt2.insert(tkinter.END, scripts_get_driver[next_s])

    def reset_proxy_state(*a):
        try:
            from .pywindowproxy import WindowProxySetting
            wproxy = WindowProxySetting()
            if wproxy.get_state():
                tkinter.messagebox.showinfo(title='Hi', message='关闭已经打开的代理！\n{}'.format(wproxy.get_server()))
                wproxy.close()
            else:
                tkinter.messagebox.showinfo(title='Hi', message='代理已关闭')
        except:
            print('reset_proxy_state error.')

    # 这几个功能感觉不太好用，基本上没有用到过，注释掉
    # btn2 = Button(temp_fr0, text='xpath列表高亮显示', command=xpath_list_highlight)
    # btn2.pack(side=tkinter.RIGHT)
    # btn2 = Button(temp_fr0, text='xpath高亮显示', command=xpath_highlight)
    # btn2.pack(side=tkinter.RIGHT)
    # btn2 = Button(temp_fr0, text='【切换：xpath选择器/driver启动代码】', command=switch_window)
    # btn2.pack(side=tkinter.RIGHT)

    btn2 = Button(temp_fr0, text='切换remote启动器脚本', command=switch_script_get_driver)
    btn2.pack(side=tkinter.RIGHT)
    btn2 = Button(temp_fr0, text='保存脚本到桌面', command=save_script_in_desktop)
    btn2.pack(side=tkinter.RIGHT)
    btn2 = Button(temp_fr0, text='[启动浏览器driver] <Alt+c>', command=start_selenium)
    btn2.pack(side=tkinter.LEFT)
    btn2 = Button(temp_fr0, text='[执行代码] <Alt+v>', command=execute_selenium_code)
    btn2.pack(side=tkinter.LEFT)
    btn2 = Button(temp_fr0, text='[开启/关闭执行代码窗口]', command=close_exec_code_window)
    btn2.pack(side=tkinter.LEFT)
    btn2 = Button(temp_fr0, text='[关闭浏览器driver]', command=close_selenium)
    btn2.pack(side=tkinter.LEFT)
    btn2 = Button(temp_fr0, text='启动mitmdump', command=start_mitm_in_desktop)
    btn2.pack(side=tkinter.RIGHT)
    btn2 = Button(temp_fr0, text='关闭代理', command=reset_proxy_state)
    btn2.pack(side=tkinter.RIGHT)
    btn2 = Button(temp_fr0, text='添加常用代码模板', command=add_script)
    btn2.pack(side=tkinter.RIGHT)

    temp_fr0 = Frame(fr)
    temp_fr0.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)
    temp_fr1 = Frame(temp_fr0)
    temp_fr1_1 = Frame(temp_fr1)
    temp_fr1_1.pack(side=tkinter.TOP)
    temp_fr1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.LEFT)
    txt1 = Text(temp_fr1,height=1,width=1,font=ft)
    lab1 = Label(temp_fr1_1,text='可执行 python 代码')
    lab1.pack(side=tkinter.TOP)
    txt1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)
    temp_fr2 = Frame(temp_fr0)
    temp_fr2_1 = Frame(temp_fr2)
    temp_fr2_1.pack(fill=tkinter.X,side=tkinter.TOP)
    temp_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.RIGHT)
    lab2 = Label(temp_fr2_1,text='启动 driver 的 python 代码')
    lab2.pack(side=tkinter.TOP)
    txt2 = Text(temp_fr2,height=1,width=1,font=ft)
    txt2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)

    temp_fr3 = Frame(temp_fr0)
    temp_fr3_1 = Frame(temp_fr3)
    temp_fr3_1.pack(fill=tkinter.X,side=tkinter.TOP)
    # temp_fr3.pack(fill=tkinter.BOTH,expand=True,side=tkinter.RIGHT)
    lab3 = Label(temp_fr3_1,text='xpath 选择器窗口(单击着色/双击添加代码)')
    lab3.pack(side=tkinter.TOP)
    lbx3 = Listbox(temp_fr3,height=1,width=1,font=ft)
    lbx3.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)
    lbx3.bind("<<ListboxSelect>>", show_log)
    lbx3.bind('<Double-Button-1>', double_click)

    txt1.insert(tkinter.END, '''
print(driver)
'''.strip())

    txt2.insert(tkinter.END, scripts_get_driver[scripts_get_driver_curr])

    temp_fr4 = Frame(fr)
    lab3 = Label(temp_fr4, text='代码结果 [Esc 切换显示状态]')
    lab3.pack(side=tkinter.TOP)
    cd = Text(temp_fr4,font=ft)
    cd.pack(fill=tkinter.BOTH,expand=True)


    try:
        from idlelib.colorizer import ColorDelegator
        from idlelib.percolator import Percolator
        p = ColorDelegator()
        Percolator(txt1).insertfilter(p)
    except:
        e = traceback.format_exc()
        txt1.delete(0.,tkinter.END)
        txt1.insert(0.,e)
    try:
        from idlelib.colorizer import ColorDelegator
        from idlelib.percolator import Percolator
        p = ColorDelegator()
        Percolator(txt2).insertfilter(p)
    except:
        e = traceback.format_exc()
        txt2.delete(0.,tkinter.END)
        txt2.insert(0.,e)

    # 确保强制退出时能关闭 webdriver 进程，防止幽灵进程
    from .root import tails
    # tails.append(clear_selenium_driver) 
    # 后续发现这种方式有点问题，暂时不考虑使用，不过 tails 的功能保留。

    frame_setting[fr] = {}
    frame_setting[fr]['type'] = 'selenium'
    frame_setting[fr]['execute_func'] = execute_selenium_code
    frame_setting[fr]['start_selenium'] = start_selenium
    frame_setting[fr]['fr_temp2'] = temp_fr4 # 代码执行框，这里仍需挂钩esc按键显示/关闭该窗口
    return fr













def encode_window(setting=None):
    '''
    处理简单的加密编码对比
    '''
    fr = tkinter.Toplevel()
    fr.title('命令行输入 ee 则可快速打开便捷加密窗口(为防冲突，输入vv e也可以打开), 组合快捷键 Alt+` 快速打开IDLE')
    fr.resizable(False, False)
    try:
        try:
            from .tab import create_temp_idle
        except:
            from tab import create_temp_idle
        fr.bind('<Alt-`>',lambda *a:create_temp_idle())
    except:
        pass

    enb = ttk.Notebook(fr)
    enb_names = {} 

    _fr = Frame(fr)
    enb.add(_fr, text='hash')
    enb.pack()
    enb_names[_fr._name] = 'hash'


    f0 = Frame(_fr)
    f0.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)

    f0_ = Frame(_fr)
    f0_.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)

    f1 = Frame(f0)
    f2 = Frame(f0)
    f1.pack(fill=tkinter.BOTH,expand=True)
    f2.pack(fill=tkinter.BOTH,expand=True)

    algorithms = hashlib.algorithms_available
    algorithms.add('md2')
    try:
        from . import pymd2
    except:
        import pymd2

    ipadx   = 0
    ipady   = 0
    padx    = 1
    pady    = 1
    width   = 60
    sticky  = 'NESW'
    ft = Font(family='Consolas',size=10)

    crow = 0
    ls = []
    di = {}
    dh = {}
    allow = [
        'blake2b',
        'blake2s',
        'md2',
        'md4',
        'md5',
        'ripemd160',
        'sha',
        'sha1',
        'sha224',
        'sha256',
        'sha384',
        'sha3_224',
        'sha3_256',
        'sha3_384',
        'sha3_512',
        'sha512',
        'whirlpool'
    ]
    for idx,name in enumerate(sorted(algorithms)+sorted(algorithms)):
        if name in allow and idx < len(algorithms):
            if name == 'md2': 
                hlen = 32
            else:
                hlen = len(hmac.new(b'',b'',name).hexdigest())
            l,e = Label(f2,text='[*]'+name+'[len:{}]'.format(str(hlen)),font=ft),Entry(f2,width=width,font=ft)
            dh[name] = e
            l.grid(row=idx,column=0,ipadx=ipadx,ipady=ipady,padx=padx,pady=pady,sticky=sticky)
            e.grid(row=idx,column=1,ipadx=ipadx,ipady=ipady,padx=padx,pady=pady,sticky=sticky)
        if name in allow and idx >= len(algorithms):
            if name == 'md2': 
                continue
            else:
                hlen = len(hmac.new(b'',b'',name).hexdigest())
            l,e = Label(f2,text='[hmac]'+name+'[len:{}]'.format(str(hlen)),font=ft),Entry(f2,width=width,font=ft)
            di[name] = e
            l.grid(row=idx,column=0,ipadx=ipadx,ipady=ipady,padx=padx,pady=pady,sticky=sticky)
            e.grid(row=idx,column=1,ipadx=ipadx,ipady=ipady,padx=padx,pady=pady,sticky=sticky)

    def func(*a):
        def _show(*a, stat='show'):
            try:
                if stat == 'show': ss.pack(side=tkinter.LEFT)
                if stat == 'hide': ss.pack_forget()
            except:
                pass
        _show(stat='show') if va.get() else _show(stat='hide')

    f11 = Frame(f1)
    f11.pack(fill=tkinter.X)

    def _switch_case(*a):
        for name,ge in di.items():
            try:
                v = ge.get().upper() if ca.get() else ge.get().lower()
                ge.delete(0,tkinter.END)
                ge.insert(0,v)
            except:
                import traceback; traceback.print_exc()
                print('error',name)
        for name,ge in dh.items():
            try:
                v = ge.get().upper() if ca.get() else ge.get().lower()
                ge.delete(0,tkinter.END)
                ge.insert(0,v)
            except:
                import traceback; traceback.print_exc()
                print('error',name)

    def _swich_encd(*a):
        s = en.get().strip()
        if s == 'utf-8':
            en.delete(0,tkinter.END)
            en.insert(0,'gbk')
        elif s == 'gbk':
            en.delete(0,tkinter.END)
            en.insert(0,'utf-8')
        else:
            en.delete(0,tkinter.END)
            en.insert(0,'utf-8')

    ca = tkinter.IntVar()
    rb = Checkbutton(f11,text='hash编码是否大写',variable=ca,command=_switch_case)
    rb.pack(side=tkinter.RIGHT)
    rb.deselect()

    en = Entry(f11, width=6, font=ft)
    en.insert(0,'utf-8')
    en.pack(side=tkinter.RIGHT)
    Button(f11,text='编码方式',command=_swich_encd).pack(side=tkinter.RIGHT,padx=2)

    ss = Entry(f11)
    va = tkinter.IntVar()
    rb = Checkbutton(f11,text='添加密盐参数',variable=va,command=func)
    rb.pack(side=tkinter.LEFT,padx=10)

    Label(f1,text='加密或编解码文本').pack(side=tkinter.LEFT,padx=10)
    ee = Entry(f1)
    ee.pack(side=tkinter.LEFT)

    def _encode_all(*a):
        encd = en.get().strip()
        salt = ss.get().encode(encd) if va.get() else b''
        text = ee.get().encode(encd)
        for name,ge in di.items():
            try:
                # if name == 'md2': name = pymd2.md2
                v = hmac.new(salt,text,name).hexdigest()
                v = v.upper() if ca.get() else v.lower()
                ge.delete(0,tkinter.END)
                ge.insert(0,v)
            except:
                import traceback; traceback.print_exc()
                print('error',name)

    def _encode_hash(*a):
        encd = en.get().strip()
        salt = ss.get().encode(encd) if va.get() else b''
        text = ee.get().encode(encd)
        for name,ge in dh.items():
            try:
                if name == 'md2':
                    v = pymd2.md2(text)
                else:
                    v = hashlib.new(name,text).hexdigest()
                v = v.upper() if ca.get() else v.lower()
                ge.delete(0,tkinter.END)
                ge.insert(0,v)
            except:
                import traceback; traceback.print_exc()
                print('error',name)
    
    Button(f1, text='hmac',command=_encode_all,width=5).pack(side=tkinter.RIGHT)
    Button(f1, text='hash',command=_encode_hash,width=5).pack(side=tkinter.RIGHT)

    f1_ = Frame(f0_)
    f1_.pack(fill=tkinter.BOTH)
    f2_ = Frame(f0_)
    f2_.pack(fill=tkinter.BOTH,expand=True)

    lb_ = Label(f1_,text='compare(对比字符串)')
    lb_.pack(side=tkinter.LEFT,padx=10,pady=pady)
    et_ = Entry(f1_,width=30)
    et_.pack(side=tkinter.LEFT,padx=padx,pady=pady)

    import difflib
    def _diff_log(a, b):
        d = difflib.Differ()
        s = d.compare(a.splitlines(), b.splitlines())
        for i in s:
            print(i)

    def print(*a, end='\n'):
        # import pprint
        # pprint.pprint(enb_names)
        name = enb.select().rsplit('.')[-1]
        if enb_names[name] == 'hash':
            txt.insert(tkinter.END,' '.join(map(str,a)) + end)
        elif enb_names[name] == '算法加解密':
            ftxt.insert(tkinter.END,' '.join(map(str,a)) + end)
        elif enb_names[name] == '依赖库加解密':
            ctxt.insert(tkinter.END,' '.join(map(str,a)) + end)
        elif enb_names[name] == '通用解密':
            bbtxt.insert(tkinter.END,' '.join(map(str,a)) + end)
        elif enb_names[name] == '爆破;RSA;二维码':
            fsstxt.insert(tkinter.END,' '.join(map(str,a)) + end)
        elif enb_names[name] == '图片相关':
            fpictxt.insert(tkinter.END,' '.join(map(str,a)) + end)
        fpictxt.update()

    def _analysis_diff(*a):
        txt.delete(0.,tkinter.END)
        it = []
        for name,ge in list(dh.items()):
            try:
                a, b = et_.get(), ge.get()
                s = difflib.SequenceMatcher(None, a.upper(), b.upper())
                q = s.find_longest_match(0, len(a), 0, len(b))
                if q.size>0:
                    it.append([name, a, b, q.size])
            except:
                import traceback; traceback.print_exc()
                print('error',name)
        for name,ge in list(di.items()):
            try:
                a, b = et_.get(), ge.get()
                s = difflib.SequenceMatcher(None, a.upper(), b.upper())
                q = s.find_longest_match(0, len(a), 0, len(b))
                if q.size>0:
                    it.append(['[hmac]'+name, a, b, q.size])
            except:
                import traceback; traceback.print_exc()
                print('error',name)

        cnt = 0
        for name,a,b,max_match in sorted(it,key=lambda max_match:-max_match[3])[:5]:
            cnt += 1
            s = difflib.SequenceMatcher(None, a.upper(), b.upper())
            print('max_match_len:{}'.format(max_match))
            print('len[compare]:{}'.format(len(a), ))
            print('len[{}]:{}'.format(name, len(b)))
            matchcnt = 0
            for match in sorted(s.get_matching_blocks(),key=lambda i:-i.size):
                if match.size:
                    v = a[match.a:match.a+match.size]
                    matchcnt += match.size
                    print('    [match.size:{}]  {}'.format(match.size, v))
            print('    [match.count:{}]'.format(matchcnt))
            print('---------------')
        if not cnt:
            print('not match.')

    def _creat_code(*a):
        import pprint
        txt.delete(0.,tkinter.END)
        salt = ss.get().strip() if va.get() else ''
        text = ee.get().strip()
        compare_str = et_.get().strip()
        code = '''
import hmac
import hashlib

# md2 算法
def _hash(message, printdebug=False):
    assert isinstance(message, list)
    msg = list(message)
    if printdebug: print("md2.hash(message = {} bytes)".format(len(message)))
    padlen = _BLOCK_SIZE - (len(msg) % _BLOCK_SIZE)
    msg.extend([padlen] * padlen)
    state    = tuple([0] * 48)
    checksum = tuple([0] * 16)
    assert len(msg) % _BLOCK_SIZE == 0
    for i in range(len(msg) // _BLOCK_SIZE):
        block = tuple(msg[i * _BLOCK_SIZE : (i + 1) * _BLOCK_SIZE])
        state, checksum = _compress(block, state, checksum, printdebug)
    state, checksum = _compress(checksum, state, checksum, printdebug)
    return list(state[ : 16])
def _compress(block, state, checksum, printdebug):
    assert isinstance(block, tuple) and len(block) == _BLOCK_SIZE
    assert isinstance(state, tuple) and len(state) == 48
    assert isinstance(checksum, tuple) and len(checksum) == 16
    newstate = list(state)
    for i in range(16):
        b = block[i]
        assert 0 <= b <= 0xFF
        newstate[i + 16] = b
        newstate[i + 32] = b ^ newstate[i]
    t = 0
    for i in range(18):
        for j in range(len(newstate)):
            newstate[j] ^= _SBOX[t]
            t = newstate[j]
        t = (t + i) & 0xFF
    newchecksum = list(checksum)
    l = newchecksum[-1]
    for i in range(16):
        l = newchecksum[i] ^ _SBOX[block[i] ^ l]
        newchecksum[i] = l
    return (tuple(newstate), tuple(newchecksum))
_BLOCK_SIZE = 16  # In bytes
_SBOX = [  # A permutation of the 256 byte values, from 0x00 to 0xFF
    0x29, 0x2E, 0x43, 0xC9, 0xA2, 0xD8, 0x7C, 0x01, 0x3D, 0x36, 0x54, 0xA1, 0xEC, 0xF0, 0x06, 0x13,
    0x62, 0xA7, 0x05, 0xF3, 0xC0, 0xC7, 0x73, 0x8C, 0x98, 0x93, 0x2B, 0xD9, 0xBC, 0x4C, 0x82, 0xCA,
    0x1E, 0x9B, 0x57, 0x3C, 0xFD, 0xD4, 0xE0, 0x16, 0x67, 0x42, 0x6F, 0x18, 0x8A, 0x17, 0xE5, 0x12,
    0xBE, 0x4E, 0xC4, 0xD6, 0xDA, 0x9E, 0xDE, 0x49, 0xA0, 0xFB, 0xF5, 0x8E, 0xBB, 0x2F, 0xEE, 0x7A,
    0xA9, 0x68, 0x79, 0x91, 0x15, 0xB2, 0x07, 0x3F, 0x94, 0xC2, 0x10, 0x89, 0x0B, 0x22, 0x5F, 0x21,
    0x80, 0x7F, 0x5D, 0x9A, 0x5A, 0x90, 0x32, 0x27, 0x35, 0x3E, 0xCC, 0xE7, 0xBF, 0xF7, 0x97, 0x03,
    0xFF, 0x19, 0x30, 0xB3, 0x48, 0xA5, 0xB5, 0xD1, 0xD7, 0x5E, 0x92, 0x2A, 0xAC, 0x56, 0xAA, 0xC6,
    0x4F, 0xB8, 0x38, 0xD2, 0x96, 0xA4, 0x7D, 0xB6, 0x76, 0xFC, 0x6B, 0xE2, 0x9C, 0x74, 0x04, 0xF1,
    0x45, 0x9D, 0x70, 0x59, 0x64, 0x71, 0x87, 0x20, 0x86, 0x5B, 0xCF, 0x65, 0xE6, 0x2D, 0xA8, 0x02,
    0x1B, 0x60, 0x25, 0xAD, 0xAE, 0xB0, 0xB9, 0xF6, 0x1C, 0x46, 0x61, 0x69, 0x34, 0x40, 0x7E, 0x0F,
    0x55, 0x47, 0xA3, 0x23, 0xDD, 0x51, 0xAF, 0x3A, 0xC3, 0x5C, 0xF9, 0xCE, 0xBA, 0xC5, 0xEA, 0x26,
    0x2C, 0x53, 0x0D, 0x6E, 0x85, 0x28, 0x84, 0x09, 0xD3, 0xDF, 0xCD, 0xF4, 0x41, 0x81, 0x4D, 0x52,
    0x6A, 0xDC, 0x37, 0xC8, 0x6C, 0xC1, 0xAB, 0xFA, 0x24, 0xE1, 0x7B, 0x08, 0x0C, 0xBD, 0xB1, 0x4A,
    0x78, 0x88, 0x95, 0x8B, 0xE3, 0x63, 0xE8, 0x6D, 0xE9, 0xCB, 0xD5, 0xFE, 0x3B, 0x00, 0x1D, 0x39,
    0xF2, 0xEF, 0xB7, 0x0E, 0x66, 0x58, 0xD0, 0xE4, 0xA6, 0x77, 0x72, 0xF8, 0xEB, 0x75, 0x4B, 0x0A,
    0x31, 0x44, 0x50, 0xB4, 0x8F, 0xED, 0x1F, 0x1A, 0xDB, 0x99, 0x8D, 0x33, 0x9F, 0x11, 0x83, 0x14,
]
def md2hex(message:bytes):
    s = _hash(list(message))
    v = 0
    for idx,i in enumerate(s[::-1]):
        v += i << idx*8
    return hex(v)[2:]

def encode_all(text,debug=False):
    text = text.encode() if type(text) == str else text
    ret = {}
    for name in allow:
        v = md2hex(text) if name == 'md2' else hashlib.new(name, text).hexdigest()
        v = v.upper() if upper else v.lower()
        ret[name] = v
        if debug: print('[*]{:<10}{}'.format(name, v))
    return ret

def encode_all_withsalt(salt,text,debug=False):
    salt = salt.encode() if type(salt) == str else salt
    text = text.encode() if type(text) == str else text
    ret = {}
    for name in allow:
        if name == 'md2':continue
        v = hmac.new(salt,text,name).hexdigest()
        v = v.upper() if upper else v.lower()
        ret[name] = v
        if debug: print('[hmac]{:<10}{}'.format(name, v))
    return ret

allow = \
$allow
upper = True  # 是否使用大写

if __name__ == '__main__':
    salt = '$salt' # 字符串/byte类型  盐（默认空）
    text = '$text' # 字符串/byte类型  需要被加密的数据
    import pprint
    v = encode_all(text)
    print('[*]')
    pprint.pprint(v)
    print()
    
    print('[hmac]')
    v = encode_all_withsalt(salt,text)
    pprint.pprint(v)
        '''.strip()
        code = code.replace('$allow', pprint.pformat(allow))
        code = code.replace('$compare_str', compare_str)
        code = code.replace('$salt', salt)
        code = code.replace('$text', text)
        print(code)

    bt_ = Button(f1_,text='分析对比[忽略大小写]',command=_analysis_diff)
    bt_.pack(side=tkinter.LEFT,padx=padx,pady=pady,)
    bt2_ = Button(f1_,text='测用代码',command=_creat_code)
    bt2_.pack(side=tkinter.LEFT,padx=padx,pady=pady,)

    txt = Text(f2_,font=ft)
    txt.pack(padx=padx,pady=pady,fill=tkinter.BOTH,expand=True)





    basehp = r'''
            通用加解密（请将需要加/解密的数据输入右侧窗口）
    base加密：
        [-] 这种类型只能对数字进行加解密
        [*] 这种类型能对一般数据流进行加解密
        [/] 这种类型通过正则切分并针对字符串内的数字进行 bytes 转换
           base_8  RegExp:[0-7]{1,3}    : r"\o123\o123" => bytes([0o123, 0o123])
                                          r"123123"     => bytes([0o123, 0o123])
           base_10 RegExp:[0-9]{1,3}    : r"\123\123"   => bytes([123, 123])
                                          r"123123"     => bytes([123, 123])
           base_16 RegExp:[0-9a-fA-F]{2}: r"\xbe\xac"   => bytes([0xbe, 0xac])
                                          r"beac"       => bytes([0xbe, 0xac])
           (由于输出框不显示无法解码数据，如需 bit 类型数据请直接使用"其他算法")
    注意：
        左边 Entry 控件在单行文书输入过长时会有卡顿甚至卡死
        右边 Text 控件虽然也有相同的问题，但能接受更长的单行文本(行数不限)
        所以长字符串的加解密，请使用单独的加解密按钮实现
        全部加解密：
            [input]  使用右边->窗口为输入  [output] 使用左边<-窗口为输出
        单独加解密：
            [input]  使用右边->窗口为输入  [output] 使用右边->窗口为输出
'''.strip('\n')

    _fr = Frame(fr)
    enb.add(_fr, text='通用解密')
    enb.pack()
    enb_names[_fr._name] = '通用解密'

    f3 = Frame(_fr)
    f3.pack(side=tkinter.LEFT,fill=tkinter.BOTH)

    f3_ = Frame(_fr)
    f3_.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)

    f4 = Frame(f3)
    f5 = Frame(f3)
    f4.pack(fill=tkinter.BOTH)
    f5.pack(fill=tkinter.BOTH,expand=True)

    base_algos = [
        'base36', # 貌似仅用于数字映射
        'base62', # 貌似仅用于数字映射
        'base16',
        'base32',
        'base58',
        'base64',
        'urlsafe_b64',
        'base85',
        'base91',
    ]
    bs = {}
    html_quote = [
        'base_2',
        'base_8',
        'base_10',
        'base_16',
        'quote',
        'urlquote',
        'escape',
        'unicode',
    ]
    for idx,name in enumerate(base_algos+html_quote):
        if name in base_algos:
            t = '[*]' if name not in ('base36', 'base62') else '[-]'
            l,e = Label(f5,text=t+name,font=ft),Entry(f5,width=width,font=ft)
            b1,b2 = Button(f5,text='加',width=3), Button(f5,text='解',width=3)
            b2.grid(row=idx,column=3,ipadx=0,ipady=0,padx=0,pady=0,sticky=sticky)
            b1.grid(row=idx,column=2,ipadx=0,ipady=0,padx=0,pady=0,sticky=sticky)
            bs[name] = e,b1,b2
            e.grid(row=idx,column=1,ipadx=ipadx,ipady=ipady,padx=padx,pady=pady,sticky=sticky)
            l.grid(row=idx,column=0,ipadx=ipadx,ipady=ipady,padx=padx,pady=pady,sticky=sticky)
        if name in html_quote:
            if name.startswith('base_'): name = '[/]' + name
            l,e = Label(f5,text=name,font=ft),Entry(f5,width=width,font=ft)
            b1,b2 = Button(f5,text='加',width=3), Button(f5,text='解',width=3)
            b2.grid(row=idx,column=3,ipadx=0,ipady=0,padx=0,pady=0,sticky=sticky)
            b1.grid(row=idx,column=2,ipadx=0,ipady=0,padx=0,pady=0,sticky=sticky)
            bs[name] = e,b1,b2
            e.grid(row=idx,column=1,ipadx=ipadx,ipady=ipady,padx=padx,pady=pady,sticky=sticky)
            l.grid(row=idx,column=0,ipadx=ipadx,ipady=ipady,padx=padx,pady=pady,sticky=sticky)

    def _b_encode(*a):
        encd = bben.get().strip()
        text = bbtxt.get(0.,tkinter.END).strip('\n').encode(encd)
        limit = 1000
        if len(text) > limit:
            print('error ! 由于Entry组件性能问题，全部加密解密模式只能在右侧窗口直接使用[单独加解进行]')
            print('当前加密字符串的长度为{}，超过限制{}'.format(len(text), limit))
            print('\n'*10)
            bbtxt.see(tkinter.END)
            return
        try:
            from . import pybase, pyplus
        except:
            import pybase, pyplus
        for name,(ge,gb1,gb2) in bs.items():
            ge.delete(0,tkinter.END)
            try:
                if name in base_algos:
                    base_encode, base_decode = pybase.base_algos[name]
                    ge.insert(0,base_encode(text))
                name = name.strip('[/]')
                if name in html_quote:
                    plus_encode, plus_decode = pyplus.html_quote[name]
                    ge.insert(0,plus_encode(text, encd))
            except:
                import traceback; traceback.print_exc()
                ge.insert(0,'error.!')
                if name in ('base36', 'base62'):
                    ge.insert(tkinter.END,'{} can only parse int type.'.format(name))

    def _b_decode(*a):
        encd = bben.get().strip()
        text = bbtxt.get(0.,tkinter.END).strip('\n').encode()
        limit = 1000
        if len(text) > limit:
            print('error ! 由于Entry组件性能问题，全部加密解密模式只能在右侧窗口直接使用[单独加解进行]')
            print('当前加密字符串的长度为{}，超过限制{}'.format(len(text), limit))
            print('\n'*10)
            bbtxt.see(tkinter.END)
            return
        try:
            from . import pybase, pyplus
        except:
            import pybase, pyplus
        for name,(ge,gb1,gb2) in bs.items():
            ge.delete(0,tkinter.END)
            try:
                if name in base_algos:
                    base_encode, base_decode = pybase.base_algos[name]
                    ge.insert(0,base_decode(text).decode(encd))
                name = name.strip('[/]')
                if name in html_quote:
                    plus_encode, plus_decode = pyplus.html_quote[name]
                    ge.insert(0,plus_decode(text.decode(), encoding=encd))
            except:
                import traceback; traceback.print_exc()
                ge.insert(0,'error')

    def _pybase_code(*a):
        try:
            from . import pybase
        except:
            import pybase
        bbtxt.delete(0.,tkinter.END)
        with open(pybase.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    def _pyplus_code(*a):
        try:
            from . import pyplus
        except:
            import pyplus
        bbtxt.delete(0.,tkinter.END)
        with open(pyplus.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    def pack_button(name):
        def do():
            nonlocal name
            encd = bben.get().strip()
            text = bbtxt.get(0.,tkinter.END).strip('\n').encode(encd)
            bbtxt.delete(0.,tkinter.END)
            try:
                from . import pybase, pyplus
            except:
                import pybase, pyplus
            try:
                if name in base_algos:
                    base_encode, base_decode = pybase.base_algos[name]
                    v = base_encode(text)
                    v = v.decode() if isinstance(v, bytes) else v
                    print(v)
                name = name.strip('[/]')
                if name in html_quote:
                    plus_encode, plus_decode = pyplus.html_quote[name]
                    print(plus_encode(text, encd))
            except:
                import traceback
                print(traceback.format_exc())
        def undo():
            nonlocal name
            encd = bben.get().strip()
            text = bbtxt.get(0.,tkinter.END).strip('\n').encode()
            bbtxt.delete(0.,tkinter.END)
            try:
                from . import pybase, pyplus
            except:
                import pybase, pyplus
            try:
                if name in base_algos:
                    base_encode, base_decode = pybase.base_algos[name]
                    print(base_decode(text).decode(encd))
                name = name.strip('[/]')
                if name in html_quote:
                    plus_encode, plus_decode = pyplus.html_quote[name]
                    print(plus_decode(text.decode(), encoding=encd))
            except:
                import traceback
                print(traceback.format_exc())
        class d:pass
        d.do = do
        d.undo = undo
        return d

    Label(f4,text=basehp,font=ft).pack(side=tkinter.TOP,padx=6)
    Button(f4,text='其他算法',width=8,command=_pyplus_code).pack(side=tkinter.RIGHT)
    Button(f4,text='base算法',width=8,command=_pybase_code).pack(side=tkinter.RIGHT)
    Button(f4,text='全部解密',width=8,command=_b_decode).pack(side=tkinter.RIGHT)
    Button(f4,text='全部加密',width=8,command=_b_encode).pack(side=tkinter.RIGHT)
    def _swich_bben(*a):
        s = bben.get().strip()
        if s == 'utf-8':
            bben.delete(0,tkinter.END)
            bben.insert(0,'gbk')
        elif s == 'gbk':
            bben.delete(0,tkinter.END)
            bben.insert(0,'utf-8')
        else:
            bben.delete(0,tkinter.END)
            bben.insert(0,'utf-8')
    

    f4_ = Frame(f3_)
    f4_.pack(fill=tkinter.BOTH)
    f5_ = Frame(f3_)
    f5_.pack(fill=tkinter.BOTH,expand=True)
    Button(f4_, text='编码',command=_swich_bben,width=6).pack(side=tkinter.LEFT)
    bben = Entry(f4_,width=5)
    bben.insert(0,'utf-8')
    bben.pack(side=tkinter.LEFT)

    bbtxt = Text(f5_,font=ft)
    bbtxt.pack(padx=padx,pady=pady,fill=tkinter.BOTH,expand=True)

    for name,(ge,gb1,gb2) in bs.items():
        d = pack_button(name)
        gb1['command'] = d.do
        gb2['command'] = d.undo










    _fr0 = Frame(fr)
    enb.add(_fr0, text='算法加解密')
    enb.pack()
    enb_names[_fr0._name] = '算法加解密'

    ff0 = Frame(_fr0)
    ff0.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)

    ff0_ = Frame(_fr0)
    ff0_.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)

    def _my_encode(*a):
        estr = ftxt.get(0.,tkinter.END).strip('\n')
        ftxt.delete(0.,tkinter.END)
        _ack = ent22.get().strip() if aa.get() else ''
        base = cbx.get()
        try:
            from . import pyzlibaes
        except:
            import pyzlibaes
        c = pyzlibaes.crypter(_ack, base=base)
        print(c.zencrypt(estr))


    def _my_decode(*a):
        dstr = ftxt.get(0.,tkinter.END).strip('\n')
        _ack = ent22.get().strip() if aa.get() else ''
        base = cbx.get()
        try:
            from . import pyzlibaes
        except:
            import pyzlibaes
        c = pyzlibaes.crypter(_ack, base=base)
        try:
            s = c.zdecrypt(dstr)
            ftxt.delete(0.,tkinter.END)
            print(s)
        except:
            tkinter.messagebox.showinfo('Error','密码或解密文本错误.\n\n'+traceback.format_exc())

    def _my_code(*a):
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyzlibaes
        except:
            import pyzlibaes
        ftxt.delete(0.,tkinter.END)
        with open(pyzlibaes.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    pure_python_encrypthelp = '''
            纯 python 实现的加解密算法
    该处大部分算法均为从各个地方收集而来的、或是我自己写的纯 python 实现的加解密算法，
    如果没有特别苛刻的环境要求，请还是尽量使用成熟的加解密函数库来实现
'''.strip('\n')

    f20 = Frame(ff0)
    f20.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f20, text=pure_python_encrypthelp,font=ft).pack(fill=tkinter.X,expand=True)
    f21 = Frame(ff0)
    f21.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f21, text='     以下算法为个人私用。应对 python 压缩的、无外部依赖库的、混合AES的、字符串加解密。').pack(fill=tkinter.X,expand=True)

    f22 = Frame(ff0)
    f22.pack(side=tkinter.TOP,fill=tkinter.X)
    ent22 = Entry(f22,width=10)
    def _switch_ack(*a):
        def _show(*a, stat='show'):
            try:
                if stat == 'show': ent22.pack(side=tkinter.LEFT)
                if stat == 'hide': ent22.pack_forget()
            except:
                pass
        _show(stat='show') if aa.get() else _show(stat='hide')
    aa = tkinter.IntVar()
    ab = Checkbutton(f22,text='密码',variable=aa,command=_switch_ack)
    ab.pack(side=tkinter.LEFT)
    ab.deselect()

    cbx = Combobox(f22,width=4,state='readonly')
    cbx['values'] = base64enc = ['b16','b32','b64','b85',]
    cbx.current(3)
    cbx.pack(side=tkinter.RIGHT)
    Label(f22, text='编码',width=4).pack(side=tkinter.RIGHT,padx=5)
    Button(f22, text='[算法]',command=_my_code,width=5).pack(side=tkinter.RIGHT)
    Button(f22, text='解密',command=_my_decode,width=5).pack(side=tkinter.RIGHT)
    Button(f22, text='加密',command=_my_encode,width=5).pack(side=tkinter.RIGHT)
    txttitlefr = Frame(ff0_)
    txttitlefr.pack(side=tkinter.TOP)
    Label(txttitlefr, text='使用以下文本框进行加解密 [仅忽略文本前后换行符,空格不忽略]，显示限制字符数：').pack(side=tkinter.LEFT,padx=10)
    entlimit = Entry(txttitlefr, width=10)
    entlimit.pack(side=tkinter.LEFT)
    entlimit.insert(0,'10000')
    ftxt = Text(ff0_,font=ft)
    ftxt.pack(padx=padx,pady=pady,fill=tkinter.BOTH,expand=True)

    def change_cbit_1(*content):
        if content:
            encd = fent1.get().strip()
            blen = len(content[0].encode(encd))*8
            cbit1['text'] = str(blen)+'bit'
            return True
    def change_cbit_2(*content):
        if content:
            encd = fent1.get().strip()
            blen = len(content[0].encode(encd))*8
            cbit2['text'] = str(blen)+'bit'
            return True

    change_cbit1 = root.register(change_cbit_1)
    change_cbit2 = root.register(change_cbit_2)

    # 这里后续需要考虑增加各种各样的加密解密以及代码的记录
    # 光是aes就有5种加解密方式
    f23 = Frame(ff0)
    f23.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f23, text='     以下算法为 AES 加解密算法 [密码长度需注意:128bit,192bit,256bit] [iv长度需注意:128bit]。').pack(fill=tkinter.X,expand=True)
    f24 = Frame(ff0)
    f24.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f24, text='密码',width=4).pack(side=tkinter.LEFT,padx=2)
    ent23 = Entry(f24,width=17,validate='key',validatecommand=(change_cbit1, '%P'))
    ent23.pack(side=tkinter.LEFT)
    ent23.bind('<Key>', change_cbit1)
    cbit1 = Label(f24, text='0bit',width=6)
    cbit1.pack(side=tkinter.LEFT,padx=6)
    cbx1 = Combobox(f24,width=4,state='readonly')
    cbx1['values'] = ['b16','b32','b64','b85']
    cbx1.current(2)
    cbx1.pack(side=tkinter.RIGHT)
    Label(f24, text='编码',width=4).pack(side=tkinter.RIGHT,padx=5)
    def _swich_encd1(*a):
        s = fent1.get().strip()
        if s == 'utf-8':
            fent1.delete(0,tkinter.END)
            fent1.insert(0,'gbk')
        elif s == 'gbk':
            fent1.delete(0,tkinter.END)
            fent1.insert(0,'utf-8')
        else:
            fent1.delete(0,tkinter.END)
            fent1.insert(0,'utf-8')
        change_cbit_1(ent23.get().strip())
        change_cbit_2(ent24.get().strip())
    fent1 = Entry(f24,width=5)
    fent1.insert(0,'utf-8')
    fent1.pack(side=tkinter.RIGHT)
    Button(f24, text='密码/iv/数据编码格式',command=_swich_encd1).pack(side=tkinter.RIGHT)
    cbx2 = Combobox(f24,width=4,state='readonly')
    cbx2['values'] = ['cbc','cfb','ofb','ctr','ecb',]
    cbx2.current(0)
    cbx2.pack(side=tkinter.RIGHT)
    Label(f24, text='模式',width=4).pack(side=tkinter.RIGHT,padx=5)
    f25 = Frame(ff0)
    f25.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f25, text='iv',width=4).pack(side=tkinter.LEFT,padx=2)
    ent24 = Entry(f25,width=17,validate='key',validatecommand=(change_cbit2, '%P'))
    ent24.pack(side=tkinter.LEFT)
    
    cbit2 = Label(f25, text='128:bit',width=6)
    cbit2.pack(side=tkinter.LEFT,padx=6)
    ent24.insert(0,'1234567890123456')
    Label(f25, text='ecb模式：iv无效；ctr模式：iv长度不限制',).pack(side=tkinter.LEFT,padx=6)

    def _aes_encode(*a):
        encd = fent1.get().strip()
        mode = cbx2.get().strip()
        eout = cbx1.get().strip()
        key  = ent23.get().strip().encode(encd)
        iv   = ent24.get().strip().encode(encd)
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

    def _aes_decode(*a):
        encd = fent1.get().strip()
        mode = cbx2.get().strip()
        eout = cbx1.get().strip()
        key  = ent23.get().strip().encode(encd)
        iv   = ent24.get().strip().encode(encd)
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

    def _aes_code(*a):
        try:
            from . import pyaes
        except:
            import pyaes
        ftxt.delete(0.,tkinter.END)
        with open(pyaes.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(f25, text='[算法]',command=_aes_code,width=5).pack(side=tkinter.RIGHT)
    Button(f25, text='解密',command=_aes_decode,width=5).pack(side=tkinter.RIGHT)
    Button(f25, text='加密',command=_aes_encode,width=5).pack(side=tkinter.RIGHT)




    # 这部分是后续增加的纯 python 的des解密
    def change_cbit_3(*content):
        if content:
            encd = fent2.get().strip()
            blen = len(content[0].encode(encd))*8
            cbit3['text'] = str(blen)+'bit'
            return True
    def change_cbit_4(*content):
        if content:
            encd = fent2.get().strip()
            blen = len(content[0].encode(encd))*8
            cbit4['text'] = str(blen)+'bit'
            return True

    change_cbit3 = root.register(change_cbit_3)
    change_cbit4 = root.register(change_cbit_4)

    f23 = Frame(ff0)
    f23.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f23, text='     以下算法为 DES/3DES 加解密算法 [密码长度:64bit(DES),128bit(3DES),192bit(3DES)] [iv长度:64bit]。').pack(fill=tkinter.X,expand=True)
    f24 = Frame(ff0)
    f24.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f24, text='密码',width=4).pack(side=tkinter.LEFT,padx=2)
    ent25 = Entry(f24,width=17,validate='key',validatecommand=(change_cbit3, '%P'))
    ent25.pack(side=tkinter.LEFT)
    ent25.bind('<Key>', change_cbit3)
    cbit3 = Label(f24, text='0bit',width=6)
    cbit3.pack(side=tkinter.LEFT,padx=6)
    cbx3 = Combobox(f24,width=4,state='readonly')
    cbx3['values'] = ['b16','b32','b64','b85']
    cbx3.current(2)
    cbx3.pack(side=tkinter.RIGHT)
    Label(f24, text='编码',width=4).pack(side=tkinter.RIGHT,padx=5)
    def _swich_encd2(*a):
        s = fent2.get().strip()
        if s == 'utf-8':
            fent2.delete(0,tkinter.END)
            fent2.insert(0,'gbk')
        elif s == 'gbk':
            fent2.delete(0,tkinter.END)
            fent2.insert(0,'utf-8')
        else:
            fent2.delete(0,tkinter.END)
            fent2.insert(0,'utf-8')
        change_cbit_3(ent25.get().strip())
        change_cbit_4(ent26.get().strip())
    fent2 = Entry(f24,width=5)
    fent2.insert(0,'utf-8')
    fent2.pack(side=tkinter.RIGHT)
    Button(f24, text='密码/iv/数据编码格式',command=_swich_encd2).pack(side=tkinter.RIGHT)
    cbx4 = Combobox(f24,width=4,state='readonly')
    cbx4['values'] = ['cbc','ecb',]
    cbx4.current(0)
    cbx4.pack(side=tkinter.RIGHT)
    Label(f24, text='模式',width=4).pack(side=tkinter.RIGHT,padx=5)
    f25 = Frame(ff0)
    f25.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f25, text='iv',width=4).pack(side=tkinter.LEFT,padx=2)
    ent26 = Entry(f25,width=17,validate='key',validatecommand=(change_cbit4, '%P'))
    ent26.pack(side=tkinter.LEFT)
    
    cbit4 = Label(f25, text='128:bit',width=6)
    cbit4.pack(side=tkinter.LEFT,padx=6)
    ent26.insert(0,'12345678')
    Label(f25, text='ecb模式：iv无效；ctr模式：iv长度不限制',).pack(side=tkinter.LEFT,padx=6)

    def _des_encode(*a):
        encd = fent2.get().strip()
        mode = cbx4.get().strip()
        eout = cbx3.get().strip()
        key  = ent25.get().strip().encode(encd)
        iv   = ent26.get().strip().encode(encd)
        data = ftxt.get(0.,tkinter.END).strip('\n').encode(encd)
        limitnum = int(entlimit.get().strip())
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pydes
        except:
            # 请勿在本脚本测试时安装了 pyaes，pyaes的源码部分有问题
            import pydes
        if eout == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if eout == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if eout == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if eout == 'b85':_encode = base64.b85encode; _decode = base64.b85decode
        if len(key) not in [8,16,24]:
            print('error. len(key) must in [64bit,128bit,192bit]. now is {}.'.format(len(key)*8))
            return
        try:
            if mode in 'ecb': mode = pydes.ECB
            elif mode == 'cbc': mode = pydes.CBC
            else:
                print('error mode:{}, mode must in [ecb cbc]'.format(mode))
            if len(key) == 8:
                d = pydes.des(key, mode, iv, padmode=pydes.PAD_PKCS5)
            else:
                d = pydes.triple_des(key, mode, iv, padmode=pydes.PAD_PKCS5)
            en = _encode(d.encrypt(data)).decode(encd)
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

    def _des_decode(*a):
        encd = fent2.get().strip()
        mode = cbx4.get().strip()
        eout = cbx3.get().strip()
        key  = ent25.get().strip().encode(encd)
        iv   = ent26.get().strip().encode(encd)
        data = ftxt.get(0.,tkinter.END).strip('\n').encode(encd)
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pydes
        except:
            # 请勿在本脚本测试时安装了 pyaes，pyaes的源码部分有问题
            import pydes
        if eout == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if eout == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if eout == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if eout == 'b85':_encode = base64.b85encode; _decode = base64.b85decode
        if len(key) not in [8,16,24]:
            print('error. len(key) must in [64bit,128bit,192bit]. now is {}.'.format(len(key)*8))
            return
        try:
            if mode in 'ecb': mode = pydes.ECB
            elif mode == 'cbc': mode = pydes.CBC
            else:
                print('error mode:{}, mode must in [ecb cbc]'.format(mode))
            if len(key) == 8:
                d = pydes.des(key, mode, iv, padmode=pydes.PAD_PKCS5)
            else:
                d = pydes.triple_des(key, mode, iv, padmode=pydes.PAD_PKCS5)
            dc = d.decrypt(_decode(data)).decode(encd)
            print(dc)
        except:
            print(traceback.format_exc())

    def _des_code(*a):
        try:
            from . import pydes
        except:
            import pydes
        ftxt.delete(0.,tkinter.END)
        with open(pydes.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(f25, text='[算法]',command=_des_code,width=5).pack(side=tkinter.RIGHT)
    Button(f25, text='解密',command=_des_decode,width=5).pack(side=tkinter.RIGHT)
    Button(f25, text='加密',command=_des_encode,width=5).pack(side=tkinter.RIGHT)









    # 这里是 blowfish 算法的部分
    def f100_change_cbit_1(*content):
        if content:
            encd = f1001_fent1.get().strip()
            blen = len(content[0].encode(encd))*8
            f1001_cbit1['text'] = str(blen)+'bit'
            return True
    def f100_change_cbit_2(*content):
        if content:
            encd = f1001_fent1.get().strip()
            blen = len(content[0].encode(encd))*8
            f1002_cbit2['text'] = str(blen)+'bit'
            return True

    f100_change_cbit1 = root.register(f100_change_cbit_1)
    f100_change_cbit2 = root.register(f100_change_cbit_2)
    f1000 = Frame(ff0)
    f1000.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f1000, text='     以下算法为 Blowfish 加解密算法 [密码长度区间:32-448bit] [iv长度需注意:64bit]。').pack(fill=tkinter.X,expand=True)
    f1001 = Frame(ff0)
    f1001.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f1001, text='密码',width=4).pack(side=tkinter.LEFT,padx=2)
    f1001_ent1 = Entry(f1001,width=17,validate='key',validatecommand=(f100_change_cbit1, '%P'))
    f1001_ent1.pack(side=tkinter.LEFT)
    f1001_ent1.bind('<Key>', f100_change_cbit1)
    f1001_cbit1 = Label(f1001, text='0bit',width=6)
    f1001_cbit1.pack(side=tkinter.LEFT,padx=6)
    f1001_mode1 = Combobox(f1001,width=4,state='readonly')
    f1001_mode1['values'] = ['b16','b32','b64','b85']
    f1001_mode1.current(2)
    f1001_mode1.pack(side=tkinter.RIGHT)
    Label(f1001, text='编码',width=4).pack(side=tkinter.RIGHT,padx=5)
    def _f100swich_encd1(*a):
        s = f1001_fent1.get().strip()
        if s == 'utf-8':
            f1001_fent1.delete(0,tkinter.END)
            f1001_fent1.insert(0,'gbk')
        elif s == 'gbk':
            f1001_fent1.delete(0,tkinter.END)
            f1001_fent1.insert(0,'utf-8')
        else:
            f1001_fent1.delete(0,tkinter.END)
            f1001_fent1.insert(0,'utf-8')
        f100_change_cbit_1(f1001_ent1.get().strip())
        f100_change_cbit_2(f1002_ent2.get().strip())
    f1001_fent1 = Entry(f1001,width=5)
    f1001_fent1.insert(0,'utf-8')
    f1001_fent1.pack(side=tkinter.RIGHT)
    Button(f1001, text='密码/iv/数据编码格式',command=_f100swich_encd1).pack(side=tkinter.RIGHT)
    f1001_mode2 = Combobox(f1001,width=4,state='readonly')
    f1001_mode2['values'] = ['ecb', 'ecb_cts', 'cbc', 'cbc_cts', 'pcbc', 'cfb', 'ofb', 'ctr']
    f1001_mode2.current(0)
    f1001_mode2.pack(side=tkinter.RIGHT)
    Label(f1001, text='模式',width=4).pack(side=tkinter.RIGHT,padx=5)
    f1002 = Frame(ff0)
    f1002.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f1002, text='iv',width=4).pack(side=tkinter.LEFT,padx=2)
    f1002_ent2 = Entry(f1002,width=17,validate='key',validatecommand=(f100_change_cbit2, '%P'))
    f1002_ent2.pack(side=tkinter.LEFT)
    
    f1002_cbit2 = Label(f1002, text='128:bit',width=6)
    f1002_cbit2.pack(side=tkinter.LEFT,padx=6)
    f1002_ent2.insert(0,'12345678')
    Label(f1002, text='ecb模式：iv无效；ctr模式：iv长度不限制',).pack(side=tkinter.LEFT,padx=6)

    def _blowfish_encode(*a):
        encd = f1001_fent1.get().strip()
        mode = f1001_mode2.get().strip()
        eout = f1001_mode1.get().strip()
        key  = f1001_ent1.get().strip().encode(encd)
        iv   = f1002_ent2.get().strip().encode(encd)
        data = ftxt.get(0.,tkinter.END).strip('\n').encode(encd)
        limitnum = int(entlimit.get().strip())
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyblowfish
        except:
            import pyblowfish
        if eout == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if eout == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if eout == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if eout == 'b85':_encode = base64.b85encode; _decode = base64.b85decode

        try:
            en = pyblowfish.encrypt(key, data, iv, mode, enfunc=_encode).decode(encd)
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

    def _blowfish_decode(*a):
        encd = f1001_fent1.get().strip()
        mode = f1001_mode2.get().strip()
        eout = f1001_mode1.get().strip()
        key  = f1001_ent1.get().strip().encode(encd)
        iv   = f1002_ent2.get().strip().encode(encd)
        data = ftxt.get(0.,tkinter.END).strip('\n').encode(encd)
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyblowfish
        except:
            import pyblowfish
        if eout == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if eout == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if eout == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if eout == 'b85':_encode = base64.b85encode; _decode = base64.b85decode

        try:
            dc = pyblowfish.decrypt(key, data, iv, mode, defunc=_decode).decode(encd)
            print(dc)
        except:
            print(traceback.format_exc())

    def _blowfish_code(*a):
        try:
            from . import pyblowfish
        except:
            import pyblowfish
        ftxt.delete(0.,tkinter.END)
        with open(pyblowfish.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(f1002, text='[算法]',command=_blowfish_code,width=5).pack(side=tkinter.RIGHT)
    Button(f1002, text='解密',command=_blowfish_decode,width=5).pack(side=tkinter.RIGHT)
    Button(f1002, text='加密',command=_blowfish_encode,width=5).pack(side=tkinter.RIGHT)






    # 这里是 serpent 算法的部分
    def f200_change_cbit_1(*content):
        if content:
            encd = f2001_fent1.get().strip()
            blen = len(content[0].encode(encd))*8
            f2001_cbit1['text'] = str(blen)+'bit'
            return True
    def f200_change_cbit_2(*content):
        if content:
            encd = f2001_fent1.get().strip()
            blen = len(content[0].encode(encd))*8
            f2002_cbit2['text'] = str(blen)+'bit'
            return True

    f200_change_cbit1 = root.register(f200_change_cbit_1)
    f200_change_cbit2 = root.register(f200_change_cbit_2)
    f2000 = Frame(ff0)
    f2000.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f2000, text='     以下算法为 Serpent 加解密算法 [密码长度区间:32-256bit] [iv长度需注意:128bit]。').pack(fill=tkinter.X,expand=True)
    f2001 = Frame(ff0)
    f2001.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f2001, text='密码',width=4).pack(side=tkinter.LEFT,padx=2)
    f2001_ent1 = Entry(f2001,width=17,validate='key',validatecommand=(f200_change_cbit1, '%P'))
    f2001_ent1.pack(side=tkinter.LEFT)
    f2001_ent1.bind('<Key>', f200_change_cbit1)
    f2001_cbit1 = Label(f2001, text='0bit',width=6)
    f2001_cbit1.pack(side=tkinter.LEFT,padx=6)
    f2001_mode1 = Combobox(f2001,width=4,state='readonly')
    f2001_mode1['values'] = ['b16','b32','b64','b85']
    f2001_mode1.current(2)
    f2001_mode1.pack(side=tkinter.RIGHT)
    Label(f2001, text='编码',width=4).pack(side=tkinter.RIGHT,padx=5)
    def _f200swich_encd1(*a):
        s = f2001_fent1.get().strip()
        if s == 'utf-8':
            f2001_fent1.delete(0,tkinter.END)
            f2001_fent1.insert(0,'gbk')
        elif s == 'gbk':
            f2001_fent1.delete(0,tkinter.END)
            f2001_fent1.insert(0,'utf-8')
        else:
            f2001_fent1.delete(0,tkinter.END)
            f2001_fent1.insert(0,'utf-8')
        f200_change_cbit_1(f2001_ent1.get().strip())
        f200_change_cbit_2(f2002_ent2.get().strip())
    f2001_fent1 = Entry(f2001,width=5)
    f2001_fent1.insert(0,'utf-8')
    f2001_fent1.pack(side=tkinter.RIGHT)
    Button(f2001, text='密码/iv/数据编码格式',command=_f200swich_encd1).pack(side=tkinter.RIGHT)
    f2001_mode2 = Combobox(f2001,width=4,state='readonly')
    f2001_mode2['values'] = ['cbc', 'ecb',]
    f2001_mode2.current(0)
    f2001_mode2.pack(side=tkinter.RIGHT)
    Label(f2001, text='模式',width=4).pack(side=tkinter.RIGHT,padx=5)
    f2002 = Frame(ff0)
    f2002.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f2002, text='iv',width=4).pack(side=tkinter.LEFT,padx=2)
    f2002_ent2 = Entry(f2002,width=17,validate='key',validatecommand=(f200_change_cbit2, '%P'))
    f2002_ent2.pack(side=tkinter.LEFT)
    
    f2002_cbit2 = Label(f2002, text='128:bit',width=6)
    f2002_cbit2.pack(side=tkinter.LEFT,padx=6)
    f2002_ent2.insert(0,'1234567890123456')
    Label(f2002, text='ecb模式：iv无效；ctr模式：iv长度不限制',).pack(side=tkinter.LEFT,padx=6)

    def _serpent_encode(*a):
        encd = f2001_fent1.get().strip()
        mode = f2001_mode2.get().strip()
        eout = f2001_mode1.get().strip()
        key  = f2001_ent1.get().strip().encode(encd)
        iv   = f2002_ent2.get().strip().encode(encd)
        data = ftxt.get(0.,tkinter.END).strip('\n').encode(encd)
        limitnum = int(entlimit.get().strip())
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyserpent
        except:
            import pyserpent
        if eout == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if eout == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if eout == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if eout == 'b85':_encode = base64.b85encode; _decode = base64.b85decode
        try:
            en = pyserpent.serpent_encrypt(key, data, iv=iv, mode=mode, enfunc=_encode).decode(encd)
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

    def _serpent_decode(*a):
        encd = f2001_fent1.get().strip()
        mode = f2001_mode2.get().strip()
        eout = f2001_mode1.get().strip()
        key  = f2001_ent1.get().strip().encode(encd)
        iv   = f2002_ent2.get().strip().encode(encd)
        data = ftxt.get(0.,tkinter.END).strip('\n').encode(encd)
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyserpent
        except:
            import pyserpent
        if eout == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if eout == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if eout == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if eout == 'b85':_encode = base64.b85encode; _decode = base64.b85decode

        try:
            dc = pyserpent.serpent_decrypt(key, data, iv=iv, mode=mode, defunc=_decode).decode(encd)
            print(dc)
        except:
            print(traceback.format_exc())

    def _serpent_code(*a):
        try:
            from . import pyserpent
        except:
            import pyserpent
        ftxt.delete(0.,tkinter.END)
        with open(pyserpent.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(f2002, text='[算法]',command=_serpent_code,width=5).pack(side=tkinter.RIGHT)
    Button(f2002, text='解密',command=_serpent_decode,width=5).pack(side=tkinter.RIGHT)
    Button(f2002, text='加密',command=_serpent_encode,width=5).pack(side=tkinter.RIGHT)







    # 这里是 twofish 算法的部分
    def f300_change_cbit_1(*content):
        if content:
            encd = f3001_fent1.get().strip()
            blen = len(content[0].encode(encd))*8
            f3001_cbit1['text'] = str(blen)+'bit'
            return True
    def f300_change_cbit_2(*content):
        if content:
            encd = f3001_fent1.get().strip()
            blen = len(content[0].encode(encd))*8
            f3002_cbit2['text'] = str(blen)+'bit'
            return True

    f300_change_cbit1 = root.register(f300_change_cbit_1)
    f300_change_cbit2 = root.register(f300_change_cbit_2)
    f3000 = Frame(ff0)
    f3000.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f3000, text='     以下算法为 Twofish 加解密算法 [密码长度需注意:128bit,192bit,256bit] [iv长度需注意:128bit]。').pack(fill=tkinter.X,expand=True)
    f3001 = Frame(ff0)
    f3001.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f3001, text='密码',width=4).pack(side=tkinter.LEFT,padx=2)
    f3001_ent1 = Entry(f3001,width=17,validate='key',validatecommand=(f300_change_cbit1, '%P'))
    f3001_ent1.pack(side=tkinter.LEFT)
    f3001_ent1.bind('<Key>', f300_change_cbit1)
    f3001_cbit1 = Label(f3001, text='0bit',width=6)
    f3001_cbit1.pack(side=tkinter.LEFT,padx=6)
    f3001_mode1 = Combobox(f3001,width=4,state='readonly')
    f3001_mode1['values'] = ['b16','b32','b64','b85']
    f3001_mode1.current(2)
    f3001_mode1.pack(side=tkinter.RIGHT)
    Label(f3001, text='编码',width=4).pack(side=tkinter.RIGHT,padx=5)
    def _f300swich_encd1(*a):
        s = f3001_fent1.get().strip()
        if s == 'utf-8':
            f3001_fent1.delete(0,tkinter.END)
            f3001_fent1.insert(0,'gbk')
        elif s == 'gbk':
            f3001_fent1.delete(0,tkinter.END)
            f3001_fent1.insert(0,'utf-8')
        else:
            f3001_fent1.delete(0,tkinter.END)
            f3001_fent1.insert(0,'utf-8')
        f300_change_cbit_1(f3001_ent1.get().strip())
        f300_change_cbit_2(f3002_ent2.get().strip())
    f3001_fent1 = Entry(f3001,width=5)
    f3001_fent1.insert(0,'utf-8')
    f3001_fent1.pack(side=tkinter.RIGHT)
    Button(f3001, text='密码/iv/数据编码格式',command=_f300swich_encd1).pack(side=tkinter.RIGHT)
    f3001_mode2 = Combobox(f3001,width=4,state='readonly')
    f3001_mode2['values'] = ['cbc', 'ecb',]
    f3001_mode2.current(0)
    f3001_mode2.pack(side=tkinter.RIGHT)
    Label(f3001, text='模式',width=4).pack(side=tkinter.RIGHT,padx=5)
    f3002 = Frame(ff0)
    f3002.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f3002, text='iv',width=4).pack(side=tkinter.LEFT,padx=2)
    f3002_ent2 = Entry(f3002,width=17,validate='key',validatecommand=(f300_change_cbit2, '%P'))
    f3002_ent2.pack(side=tkinter.LEFT)
    
    f3002_cbit2 = Label(f3002, text='128:bit',width=6)
    f3002_cbit2.pack(side=tkinter.LEFT,padx=6)
    f3002_ent2.insert(0,'1234567890123456')
    Label(f3002, text='ecb模式：iv无效；ctr模式：iv长度不限制',).pack(side=tkinter.LEFT,padx=6)

    def _twofish_encode(*a):
        encd = f3001_fent1.get().strip()
        mode = f3001_mode2.get().strip()
        eout = f3001_mode1.get().strip()
        key  = f3001_ent1.get().strip().encode(encd)
        iv   = f3002_ent2.get().strip().encode(encd)
        data = ftxt.get(0.,tkinter.END).strip('\n').encode(encd)
        limitnum = int(entlimit.get().strip())
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pytwofish
        except:
            import pytwofish
        if eout == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if eout == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if eout == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if eout == 'b85':_encode = base64.b85encode; _decode = base64.b85decode
        try:
            en = pytwofish.twofish_encrypt(key, data, iv=iv, mode=mode, enfunc=_encode).decode(encd)
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

    def _twofish_decode(*a):
        encd = f3001_fent1.get().strip()
        mode = f3001_mode2.get().strip()
        eout = f3001_mode1.get().strip()
        key  = f3001_ent1.get().strip().encode(encd)
        iv   = f3002_ent2.get().strip().encode(encd)
        data = ftxt.get(0.,tkinter.END).strip('\n').encode(encd)
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pytwofish
        except:
            import pytwofish
        if eout == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if eout == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if eout == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if eout == 'b85':_encode = base64.b85encode; _decode = base64.b85decode

        try:
            dc = pytwofish.twofish_decrypt(key, data, iv=iv, mode=mode, defunc=_decode).decode(encd)
            print(dc)
        except:
            print(traceback.format_exc())

    def _twofish_code(*a):
        try:
            from . import pytwofish
        except:
            import pytwofish
        ftxt.delete(0.,tkinter.END)
        with open(pytwofish.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(f3002, text='[算法]',command=_twofish_code,width=5).pack(side=tkinter.RIGHT)
    Button(f3002, text='解密',command=_twofish_decode,width=5).pack(side=tkinter.RIGHT)
    Button(f3002, text='加密',command=_twofish_encode,width=5).pack(side=tkinter.RIGHT)





    f200 = Frame(ff0)
    f200.pack(side=tkinter.TOP,fill=tkinter.X)
    f201 = Frame(f200)
    f202 = Frame(f200)
    f201.pack(side=tkinter.TOP,fill=tkinter.X)
    f202.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f201, text='     以下算法为 rc4 解密算法').pack(fill=tkinter.X,expand=True)

    def _rc4_encode(*a):
        data = ftxt.get(0.,tkinter.END).strip('\n')
        ftxt.delete(0.,tkinter.END)
        encd = k201.get().strip('\n')
        key = k200.get().strip('\n').encode(encd)
        data = data.encode(encd)
        mode = cbx201.get().strip()
        try:
            from . import pyrc4
        except:
            import pyrc4
        if mode == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if mode == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if mode == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if mode == 'b85':_encode = base64.b85encode; _decode = base64.b85decode
        try:
            f = pyrc4.rc4(data, key, mode="encode", enfunc=_encode, defunc=_decode)
            print(f.decode(encd))
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error encoding!!! check input data.')

    def _rc4_decode(*a):
        data = ftxt.get(0.,tkinter.END).strip('\n')
        ftxt.delete(0.,tkinter.END)
        encd = k201.get().strip('\n')
        key = k200.get().strip('\n').encode(encd)
        data = data.encode(encd)
        mode = cbx201.get().strip()
        try:
            from . import pyrc4
        except:
            import pyrc4
        if mode == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if mode == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if mode == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if mode == 'b85':_encode = base64.b85encode; _decode = base64.b85decode
        try:
            f = pyrc4.rc4(data, key, mode="decode", enfunc=_encode, defunc=_decode)
            print(f.decode(encd))
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _rc4_code(*a):
        try:
            from . import pyrc4
        except:
            import pyrc4
        ftxt.delete(0.,tkinter.END)
        with open(pyrc4.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    def _swich_rc4_encd(*a):
        s = k201.get().strip()
        if s == 'utf-8':
            k201.delete(0,tkinter.END)
            k201.insert(0,'gbk')
        elif s == 'gbk':
            k201.delete(0,tkinter.END)
            k201.insert(0,'utf-8')
        else:
            k201.delete(0,tkinter.END)
            k201.insert(0,'utf-8')

    cbx201 = Combobox(f202,width=4,state='readonly')
    cbx201['values'] = ['b16','b32','b64','b85']
    cbx201.current(2)
    cbx201.pack(side=tkinter.RIGHT)
    Label(f202, text='密码',width=4).pack(side=tkinter.LEFT,padx=5)
    k200 = Entry(f202, width=17)
    k200.pack(side=tkinter.LEFT)
    Button(f202, text='[算法]',command=_rc4_code,width=5).pack(side=tkinter.RIGHT)
    Button(f202, text='解密',command=_rc4_decode,width=5).pack(side=tkinter.RIGHT)
    Button(f202, text='加密',command=_rc4_encode,width=5).pack(side=tkinter.RIGHT)
    k201 = Entry(f202, width=5)
    k201.pack(side=tkinter.RIGHT)
    k201.insert(0,'utf-8')
    Button(f202, text='密码/数据编码格式',command=_swich_rc4_encd).pack(side=tkinter.RIGHT)








    # jsfuck 的解密
    fxpy0010 = Frame(ff0)
    fxpy0010.pack(side=tkinter.TOP,fill=tkinter.X)
    fxpy0012 = Frame(fxpy0010)
    fxpy0012.pack(side=tkinter.TOP,fill=tkinter.X)
    def _jsfuck_decode(*a):
        data = ftxt.get(0.,tkinter.END).strip('\n')
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyjsfuck
        except:
            import pyjsfuck
        try:
            if cbxejsfuck.get().strip() == '显示解密过程':
                debuglevel = 1
            else:
                debuglevel = 0
            f = pyjsfuck.unjsfuck(data, debuglevel=debuglevel, logger=print)
            print()
            print('[ result ]:')
            print(f)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _jsfuck_code(*a):
        try:
            from . import pyjsfuck
        except:
            import pyjsfuck
        ftxt.delete(0.,tkinter.END)
        with open(pyjsfuck.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(fxpy0012, text='[算法]',command=_jsfuck_code,width=5).pack(side=tkinter.LEFT)
    Label(fxpy0012, text=' 这里为 jsfuck 算法解密。').pack(side=tkinter.LEFT)
    Button(fxpy0012, text='解密',command=_jsfuck_decode,width=5).pack(side=tkinter.RIGHT)
    cbxejsfuck = Combobox(fxpy0012,width=11,state='readonly')
    cbxejsfuck['values'] = ['显示解密过程', '不显示过程']
    cbxejsfuck.current(0)
    cbxejsfuck.pack(fill=tkinter.X,side=tkinter.RIGHT)

    # brainfuck 的解密
    fxpy0070 = Frame(ff0)
    fxpy0070.pack(side=tkinter.TOP,fill=tkinter.X)
    fxpy0072 = Frame(fxpy0070)
    fxpy0072.pack(side=tkinter.TOP,fill=tkinter.X)
    def _brainfuck_decode(*a):
        data = ftxt.get(0.,tkinter.END).strip('\n')
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pybrainfuck
        except:
            import pybrainfuck
        try:
            v = pybrainfuck.evaluate(data)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _brainfuck_code(*a):
        try:
            from . import pybrainfuck
        except:
            import pybrainfuck
        ftxt.delete(0.,tkinter.END)
        with open(pybrainfuck.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(fxpy0072, text='[算法]',command=_brainfuck_code,width=5).pack(side=tkinter.LEFT)
    Label(fxpy0072, text=' 这里为 brainfuck 算法解密。').pack(side=tkinter.LEFT)
    Button(fxpy0072, text='brainfuck解密',command=_brainfuck_decode,width=12).pack(side=tkinter.RIGHT)

    # ook 的解密
    fxpy0080 = Frame(ff0)
    fxpy0080.pack(side=tkinter.TOP,fill=tkinter.X)
    fxpy0082 = Frame(fxpy0080)
    fxpy0082.pack(side=tkinter.TOP,fill=tkinter.X)
    def _brainfuckook_decode(*a):
        data = ftxt.get(0.,tkinter.END).strip('\n')
        a = brainfuckook_a.get().strip()
        b = brainfuckook_b.get().strip()
        c = brainfuckook_c.get().strip()
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pybrainfuck
        except:
            import pybrainfuck
        try:
            data = pybrainfuck.parse_ook_to_brainfuckmap(data, abc = (a,b,c))
            v = pybrainfuck.evaluate(data)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _brainfuck_code(*a):
        try:
            from . import pybrainfuck
        except:
            import pybrainfuck
        ftxt.delete(0.,tkinter.END)
        with open(pybrainfuck.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(fxpy0082, text='[算法]',command=_brainfuck_code,width=5).pack(side=tkinter.LEFT)
    Label(fxpy0082, text=' 这里为 Ook! 算法解密。').pack(side=tkinter.LEFT)
    Button(fxpy0082, text='Ook!解密',command=_brainfuckook_decode,width=8).pack(side=tkinter.RIGHT)
    brainfuckook_c = Entry(fxpy0082, width=2)
    brainfuckook_c.insert(0, '.')
    brainfuckook_c.pack(side=tkinter.RIGHT)
    Label(fxpy0082, text='c').pack(side=tkinter.RIGHT)
    brainfuckook_b = Entry(fxpy0082, width=2)
    brainfuckook_b.insert(0, '?')
    brainfuckook_b.pack(side=tkinter.RIGHT)
    Label(fxpy0082, text='b').pack(side=tkinter.RIGHT)
    brainfuckook_a = Entry(fxpy0082, width=2)
    brainfuckook_a.insert(0, '!')
    brainfuckook_a.pack(side=tkinter.RIGHT)
    Label(fxpy0082, text='a').pack(side=tkinter.RIGHT)


    # 凯撒解密
    fxpy0020 = Frame(ff0)
    fxpy0020.pack(side=tkinter.TOP,fill=tkinter.X)
    fxpy0022 = Frame(fxpy0020)
    fxpy0022.pack(side=tkinter.TOP,fill=tkinter.X)
    def _caesar_enum(*a):
        data = ftxt.get(0.,tkinter.END).strip('\n')
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pycaesar
        except:
            import pycaesar
        try:
            if len(data) > 1000:
                print('注意，使用超过1000长度的的凯撒遍历处理时，请直接使用代码在 IDE 里面自行处理。')
            for i in range(-13, 13, 1):
                v = pycaesar.caesar(data, i)
                if i == 0:print()
                print('{:>3} --- {} '.format(i, v))
                if i == 0:print()
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _caesar_encode():
        data = ftxt.get(0.,tkinter.END).strip('\n')
        deviation = fxpy0022ent.get().strip()
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pycaesar
        except:
            import pycaesar
        try:
            deviation = int(deviation)
            v = pycaesar.caesar(data, deviation)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _caesar_decode():
        data = ftxt.get(0.,tkinter.END).strip('\n')
        deviation = fxpy0022ent.get().strip()
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pycaesar
        except:
            import pycaesar
        try:
            deviation = int(deviation)
            v = pycaesar.caesar(data, -deviation)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _caesar_code(*a):
        try:
            from . import pycaesar
        except:
            import pycaesar
        ftxt.delete(0.,tkinter.END)
        with open(pycaesar.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)
    
    Button(fxpy0022, text='[算法]',command=_caesar_code,width=5).pack(side=tkinter.LEFT)
    Label(fxpy0022, text=' 这里为 凯撒密码 算法加解密。').pack(side=tkinter.LEFT)
    Button(fxpy0022, text='遍历',command=_caesar_enum,width=5).pack(side=tkinter.RIGHT)
    Button(fxpy0022, text='解密',command=_caesar_decode,width=5).pack(side=tkinter.RIGHT)
    Button(fxpy0022, text='加密',command=_caesar_encode,width=5).pack(side=tkinter.RIGHT)
    fxpy0022ent = Entry(fxpy0022, width=3)
    fxpy0022ent.pack(side=tkinter.RIGHT)
    fxpy0022ent.insert(0, '3')
    Label(fxpy0022, text='偏移').pack(side=tkinter.RIGHT)

    # ascii偏移解密
    fxpy0060 = Frame(ff0)
    fxpy0060.pack(side=tkinter.TOP,fill=tkinter.X)
    fxpy0062 = Frame(fxpy0060)
    fxpy0062.pack(side=tkinter.TOP,fill=tkinter.X)
    def _caesar_enum(*a):
        data = ftxt.get(0.,tkinter.END).strip('\n')
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyascii_deviation
        except:
            import pyascii_deviation
        try:
            if len(data) > 1000:
                print('注意，使用超过1000长度的的凯撒遍历处理时，请直接使用代码在 IDE 里面自行处理。')
            for i in range(-20, 20, 1):
                v = pyascii_deviation.ascii_deviation(data, i)
                if i == 0:print()
                print('{:>3} --- {} '.format(i, v))
                if i == 0:print()
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _caesar_encode():
        data = ftxt.get(0.,tkinter.END).strip('\n')
        deviation = fxpy0062ent.get().strip()
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyascii_deviation
        except:
            import pyascii_deviation
        try:
            deviation = int(deviation)
            v = pyascii_deviation.ascii_deviation(data, deviation)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _caesar_decode():
        data = ftxt.get(0.,tkinter.END).strip('\n')
        deviation = fxpy0062ent.get().strip()
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyascii_deviation
        except:
            import pyascii_deviation
        try:
            deviation = int(deviation)
            v = pyascii_deviation.ascii_deviation(data, -deviation)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _caesar_code(*a):
        try:
            from . import pyascii_deviation
        except:
            import pyascii_deviation
        ftxt.delete(0.,tkinter.END)
        with open(pyascii_deviation.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(fxpy0062, text='[算法]',command=_caesar_code,width=5).pack(side=tkinter.LEFT)
    Label(fxpy0062, text=' 这里为 ascii偏移 算法加解密。').pack(side=tkinter.LEFT)
    Button(fxpy0062, text='遍历',command=_caesar_enum,width=5).pack(side=tkinter.RIGHT)
    Button(fxpy0062, text='解密',command=_caesar_decode,width=5).pack(side=tkinter.RIGHT)
    Button(fxpy0062, text='加密',command=_caesar_encode,width=5).pack(side=tkinter.RIGHT)
    fxpy0062ent = Entry(fxpy0062, width=3)
    fxpy0062ent.pack(side=tkinter.RIGHT)
    fxpy0062ent.insert(0, '3')
    Label(fxpy0062, text='偏移').pack(side=tkinter.RIGHT)


    # 莫斯解密
    fxpy0030 = Frame(ff0)
    fxpy0030.pack(side=tkinter.TOP,fill=tkinter.X)
    fxpy0032 = Frame(fxpy0030)
    fxpy0032.pack(side=tkinter.TOP,fill=tkinter.X)
    def _morse_encode(*a):
        data = ftxt.get(0.,tkinter.END).strip('\n')
        point = morse_point.get().strip()
        line  = morse_line.get().strip()
        space = morse_space.get().strip('\n')
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pymorse
        except:
            import pymorse
        try:
            v = pymorse.morse_enc(data, point, line, space)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _morse_decode(*a):
        data = ftxt.get(0.,tkinter.END).strip('\n')
        point = morse_point.get().strip()
        line  = morse_line.get().strip()
        space = morse_space.get().strip('\n')
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pymorse
        except:
            import pymorse
        try:
            v = pymorse.morse_dec(data, point, line, space)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _morse_code(*a):
        try:
            from . import pymorse
        except:
            import pymorse
        ftxt.delete(0.,tkinter.END)
        with open(pymorse.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(fxpy0032, text='[算法]',command=_morse_code,width=5).pack(side=tkinter.LEFT)
    Label(fxpy0032, text=' 这里为 莫斯密码 算法加解密。').pack(side=tkinter.LEFT)
    Button(fxpy0032, text='解密',command=_morse_decode,width=5).pack(side=tkinter.RIGHT)
    Button(fxpy0032, text='加密',command=_morse_encode,width=5).pack(side=tkinter.RIGHT)
    morse_space = Entry(fxpy0032, width=2)
    morse_space.insert(0, ' ')
    morse_space.pack(side=tkinter.RIGHT)
    Label(fxpy0032, text='空格').pack(side=tkinter.RIGHT)
    morse_line = Entry(fxpy0032, width=2)
    morse_line.insert(0, '-')
    morse_line.pack(side=tkinter.RIGHT)
    Label(fxpy0032, text='线').pack(side=tkinter.RIGHT)
    morse_point = Entry(fxpy0032, width=2)
    morse_point.insert(0, '.')
    morse_point.pack(side=tkinter.RIGHT)
    Label(fxpy0032, text='点').pack(side=tkinter.RIGHT)
    


    # rot 加解密
    fxpy0040 = Frame(ff0)
    fxpy0040.pack(side=tkinter.TOP,fill=tkinter.X)
    fxpy0042 = Frame(fxpy0040)
    fxpy0042.pack(side=tkinter.TOP,fill=tkinter.X)
    def _rots_encode_decode(*a):
        data = ftxt.get(0.,tkinter.END).strip('\n')
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyrots
        except:
            import pyrots
        try:
            if cbxrots.get().strip() == 'rot5':  encdec = pyrots.rot5
            if cbxrots.get().strip() == 'rot13': encdec = pyrots.rot13
            if cbxrots.get().strip() == 'rot18': encdec = pyrots.rot18
            if cbxrots.get().strip() == 'rot47': encdec = pyrots.rot47
            v = encdec(data)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _rots_encode_decode_all(*a):
        data = ftxt.get(0.,tkinter.END).strip('\n')
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyrots
        except:
            import pyrots
        try:
            v = pyrots.morse_enc(data, point, line, space)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _morse_code(*a):
        try:
            from . import pyrots
        except:
            import pyrots
        ftxt.delete(0.,tkinter.END)
        with open(pyrots.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(fxpy0042, text='[算法]',command=_morse_code,width=5).pack(side=tkinter.LEFT)
    Label(fxpy0042, text=' 这里为 rot* 算法加解密。(rot18,rot47 部分加密数据的大小写无法还原)').pack(side=tkinter.LEFT)
    Button(fxpy0042, text='加解密',command=_rots_encode_decode,width=5).pack(side=tkinter.RIGHT)
    cbxrots = Combobox(fxpy0042,width=5,state='readonly')
    cbxrots['values'] = ['rot5', 'rot13','rot18','rot47']
    cbxrots.current(0)
    cbxrots.pack(fill=tkinter.X,side=tkinter.RIGHT)



    # 培根加解密
    fxpy0050 = Frame(ff0)
    fxpy0050.pack(side=tkinter.TOP,fill=tkinter.X)
    fxpy0052 = Frame(fxpy0050)
    fxpy0052.pack(side=tkinter.TOP,fill=tkinter.X)
    def _bacon_encode(*a):
        data = ftxt.get(0.,tkinter.END).strip()
        a = bacon_a.get().strip()
        b = bacon_b.get().strip()
        ver = cbxbaconver.get().strip()
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pybacon
        except:
            import pybacon
        try:
            v = pybacon.bacon_enc(data, a, b, ver)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _bacon_decode(*a):
        data = ftxt.get(0.,tkinter.END).strip()
        a = bacon_a.get().strip()
        b = bacon_b.get().strip()
        ver = cbxbaconver.get().strip()
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pybacon
        except:
            import pybacon
        try:
            v = pybacon.bacon_dec(data, a, b, ver)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _bacon_code(*a):
        try:
            from . import pybacon
        except:
            import pybacon
        ftxt.delete(0.,tkinter.END)
        with open(pybacon.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(fxpy0052, text='[算法]',command=_bacon_code,width=5).pack(side=tkinter.LEFT)
    Label(fxpy0052, text=' 这里为 培根密码 算法加解密。').pack(side=tkinter.LEFT)
    Button(fxpy0052, text='解密',command=_bacon_decode,width=5).pack(side=tkinter.RIGHT)
    Button(fxpy0052, text='加密',command=_bacon_encode,width=5).pack(side=tkinter.RIGHT)
    bacon_b = Entry(fxpy0052, width=2)
    bacon_b.insert(0, 'b')
    bacon_b.pack(side=tkinter.RIGHT)
    Label(fxpy0052, text='b').pack(side=tkinter.RIGHT)
    bacon_a = Entry(fxpy0052, width=2)
    bacon_a.insert(0, 'a')
    bacon_a.pack(side=tkinter.RIGHT)
    Label(fxpy0052, text='a').pack(side=tkinter.RIGHT)
    cbxbaconver = Combobox(fxpy0052,width=3,state='readonly')
    cbxbaconver['values'] = ['v1', 'v2']
    cbxbaconver.current(0)
    cbxbaconver.pack(fill=tkinter.X,side=tkinter.RIGHT)


    # 栅栏加解密
    fxpy0090 = Frame(ff0)
    fxpy0090.pack(side=tkinter.TOP,fill=tkinter.X)
    fxpy0092 = Frame(fxpy0090)
    fxpy0092.pack(side=tkinter.TOP,fill=tkinter.X)
    def _rail_fence_encode(*a):
        data = ftxt.get(0.,tkinter.END).strip()
        _num = rail_num.get().strip()
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyrail_fence
        except:
            import pyrail_fence
        try:
            _num = int(_num)
            v, _ = pyrail_fence.rail_fence_enc(data, _num)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _rail_fence_decode(*a):
        data = ftxt.get(0.,tkinter.END).strip()
        _num = rail_num.get().strip()
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyrail_fence
        except:
            import pyrail_fence
        try:
            _num = int(_num)
            v = pyrail_fence.rail_fence_dec(data, _num)
            print(v)
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _rail_fence_enum(*a):
        data = ftxt.get(0.,tkinter.END).strip()
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyrail_fence
        except:
            import pyrail_fence
        try:
            v = pyrail_fence.rail_fence_enum(data)
            if not v:
                print('cannot factorize. by len(string):{}'.format(len(data)))
                return
            for a,b,r in v:
                print('{:>2} --- {}'.format(a, r))
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _rail_fence_enummatrix(*a):
        data = ftxt.get(0.,tkinter.END).strip()
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyrail_fence
        except:
            import pyrail_fence
        try:
            v = pyrail_fence.rail_fence_enum(data, return_matrix=True)
            if not v:
                print('cannot factorize. by len(string):{}'.format(len(data)))
                return
            for a,b,i in v:
                print('--- {}x{} ---'.format(a,b))
                for j in i:
                    r = ''
                    for k in list(j):
                        r += k + ' '
                    print(r.strip())
                    # re.sub("''")
        except:
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _rail_fence_code(*a):
        try:
            from . import pyrail_fence
        except:
            import pyrail_fence
        ftxt.delete(0.,tkinter.END)
        with open(pyrail_fence.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(fxpy0092, text='[算法]',command=_rail_fence_code,width=5).pack(side=tkinter.LEFT)
    Label(fxpy0092, text=' 这里为 栅栏密码 算法加解密。').pack(side=tkinter.LEFT)
    Button(fxpy0092, text='遍历矩阵',command=_rail_fence_enummatrix,width=8).pack(side=tkinter.RIGHT)
    Button(fxpy0092, text='遍历',command=_rail_fence_enum,width=5).pack(side=tkinter.RIGHT)
    Button(fxpy0092, text='解密',command=_rail_fence_decode,width=5).pack(side=tkinter.RIGHT)
    Button(fxpy0092, text='加密',command=_rail_fence_encode,width=5).pack(side=tkinter.RIGHT)
    rail_num = Entry(fxpy0092, width=2)
    rail_num.insert(0, '2')
    rail_num.pack(side=tkinter.RIGHT)
    Label(fxpy0092, text='栅栏数').pack(side=tkinter.RIGHT)





    _fr1 = Frame(fr)
    enb.add(_fr1, text='依赖库加解密')
    enb.pack()
    enb_names[_fr1._name] = '依赖库加解密'


    ff1 = Frame(_fr1)
    ff1.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)

    ff1_ = Frame(_fr1)
    ff1_.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)
    txttitlefr = Frame(ff1_)
    txttitlefr.pack(side=tkinter.TOP)
    Label(txttitlefr, text='使用以下文本框进行加解密 [仅忽略文本前后换行符,空格不忽略]，显示限制字符数：').pack(side=tkinter.LEFT,padx=10)
    entlimit2 = Entry(txttitlefr, width=10)
    entlimit2.pack(side=tkinter.LEFT)
    entlimit2.insert(0,'10000')
    ctxt = Text(ff1_,font=ft)
    ctxt.pack(padx=padx,pady=pady,fill=tkinter.BOTH,expand=True)

    # 这里依赖于 cryptography 库的加解密算法，这里会比以上从各种地方收集来的纯py代码要更加保险
    cryptographyhelps = '''
            以下算法为依赖于 cryptography 库
    由于使用了一个比较成熟的加密函数库，所以基本包含了常用的加解密算法
    如有安装该加密库，则请尽量使用该库的算法实现。
    不过还是有部分例如 twofish 以及 serpent 这里没有，在纯py算法中有实现。

    #[*] AES       len(key) [128, 192, 256, 512]  len(iv) 128
    #[*] Camellia  len(key) [128, 192, 256]       len(iv) 128
    #[*] SEED      len(key) [128]                 len(iv) 128
    #    ChaCha20  len(key) [256]                 len(iv) 128 (nonce)
    #[*] Blowfish  len(key) range(32, 449, 8)     len(iv) 64
    #[*] CAST5     len(key) range(40, 129, 8)     len(iv) 64
    #[*] IDEA      len(key) [128]                 len(iv) 64
    #[*] TripleDES len(key) [64, 128, 192]        len(iv) 64
    #[*] DES       len(key) [64, 128, 192]        len(iv) 64
    #    ARC4      len(key) [40, 56, 64, 80, 128, 160, 192, 256] # 不使用iv

    带有 [*] 的可以有不同的加密模式(cbc,ecb...)，没有的，则该选项无效。
'''.strip('\n')

    def f900_change_cbit_1(*content):
        if content:
            encd = f9001_fent1.get().strip()
            blen = len(content[0].encode(encd))*8
            f9001_cbit1['text'] = str(blen)+'bit'
            return True
    def f900_change_cbit_2(*content):
        if content:
            encd = f9001_fent1.get().strip()
            blen = len(content[0].encode(encd))*8
            f9002_cbit2['text'] = str(blen)+'bit'
            return True

    f900_change_cbit1 = root.register(f900_change_cbit_1)
    f900_change_cbit2 = root.register(f900_change_cbit_2)
    f9000 = Frame(ff1)
    f9000.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f9000, text=cryptographyhelps,font=ft).pack(fill=tkinter.X,expand=True)
    f9001 = Frame(ff1)
    f9001.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f9001, text='密码',width=4).pack(side=tkinter.LEFT,padx=2)
    f90001_ent1 = Entry(f9001,width=17,validate='key',validatecommand=(f900_change_cbit1, '%P'))
    f90001_ent1.pack(side=tkinter.LEFT)
    f90001_ent1.bind('<Key>', f900_change_cbit1)
    f9001_cbit1 = Label(f9001, text='0bit',width=6)
    f9001_cbit1.pack(side=tkinter.LEFT,padx=6)
    f9001_mode1 = Combobox(f9001,width=4,state='readonly')
    f9001_mode1['values'] = ['b16','b32','b64','b85']
    f9001_mode1.current(2)
    f9001_mode1.pack(side=tkinter.RIGHT)
    Label(f9001, text='编码',width=4).pack(side=tkinter.RIGHT,padx=5)
    def _f900swich_encd1(*a):
        s = f9001_fent1.get().strip()
        if s == 'utf-8':
            f9001_fent1.delete(0,tkinter.END)
            f9001_fent1.insert(0,'gbk')
        elif s == 'gbk':
            f9001_fent1.delete(0,tkinter.END)
            f9001_fent1.insert(0,'utf-8')
        else:
            f9001_fent1.delete(0,tkinter.END)
            f9001_fent1.insert(0,'utf-8')
        f900_change_cbit_1(f90001_ent1.get().strip())
        f900_change_cbit_2(f90002_ent2.get().strip())
    f9001_fent1 = Entry(f9001,width=5)
    f9001_fent1.insert(0,'utf-8')
    f9001_fent1.pack(side=tkinter.RIGHT)
    Button(f9001, text='编码格式',command=_f900swich_encd1, width=7).pack(side=tkinter.RIGHT)
    f9001_mode2 = Combobox(f9001,width=4,state='readonly')
    f9001_mode2['values'] = ['cbc','cfb','ofb','ctr','ecb',]
    f9001_mode2.current(0)
    f9001_mode2.pack(side=tkinter.RIGHT)
    Label(f9001, text='模式',width=4).pack(side=tkinter.RIGHT,padx=5)
    Label(f9001, text='加密',).pack(side=tkinter.LEFT,padx=2)
    f9001_mode3 = Combobox(f9001,width=6,state='readonly')
    f9001_mode3['values'] = ['AES', 'ARC4', 'Blowfish', 'CAST5', 'Camellia', 'ChaCha20', 'IDEA', 'SEED', 'TripleDES', 'DES']
    f9001_mode3.current(0)
    f9001_mode3.pack(side=tkinter.LEFT)
    f9002 = Frame(ff1)
    f9002.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f9002, text='iv',width=4).pack(side=tkinter.LEFT,padx=2)
    f90002_ent2 = Entry(f9002,width=17,validate='key',validatecommand=(f900_change_cbit2, '%P'))
    f90002_ent2.pack(side=tkinter.LEFT)
    f9002_cbit2 = Label(f9002, text='128:bit',width=6)
    f9002_cbit2.pack(side=tkinter.LEFT,padx=6)
    f90002_ent2.insert(0,'1234567890123456')
    Label(f9002, text='PADDING',).pack(side=tkinter.LEFT,padx=2)
    f9002_mode4 = Combobox(f9002,width=7,state='readonly')
    f9002_mode4['values'] = ['PKCS7', 'ANSIX923', 'None',]
    f9002_mode4.current(0)
    f9002_mode4.pack(side=tkinter.LEFT)

    def _pymultialgo_encode(*a):
        encd = f9001_fent1.get().strip()
        mode = f9001_mode2.get().strip()
        eout = f9001_mode1.get().strip()
        key  = f90001_ent1.get().strip().encode(encd)
        iv   = f90002_ent2.get().strip().encode(encd)
        algo = f9001_mode3.get().strip()
        padd = f9002_mode4.get().strip()
        data = ctxt.get(0.,tkinter.END).strip('\n').encode(encd)
        limitnum = int(entlimit2.get().strip())
        ctxt.delete(0.,tkinter.END)
        try:
            from . import pymultialgo
        except:
            # 请勿在本脚本测试时安装了 pyaes，pyaes的源码部分有问题
            import pymultialgo
        if eout == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if eout == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if eout == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if eout == 'b85':_encode = base64.b85encode; _decode = base64.b85decode

        try:
            encryptor = pymultialgo.get_encryptor(algo, key, iv, mode, padd)
            edata = encryptor.encrypt(data)
            en = _encode(edata).decode(encd)
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

    def _pymultialgo_decode(*a):
        encd = f9001_fent1.get().strip()
        mode = f9001_mode2.get().strip()
        eout = f9001_mode1.get().strip()
        key  = f90001_ent1.get().strip().encode(encd)
        iv   = f90002_ent2.get().strip().encode(encd)
        algo = f9001_mode3.get().strip()
        padd = f9002_mode4.get().strip()
        data = ctxt.get(0.,tkinter.END).strip('\n').encode(encd)
        ctxt.delete(0.,tkinter.END)
        try:
            from . import pymultialgo
        except:
            # 请勿在本脚本测试时安装了 pyaes，pyaes的源码部分有问题
            import pymultialgo
        if eout == 'b16':_encode = base64.b16encode; _decode = base64.b16decode
        if eout == 'b32':_encode = base64.b32encode; _decode = base64.b32decode
        if eout == 'b64':_encode = base64.b64encode; _decode = base64.b64decode
        if eout == 'b85':_encode = base64.b85encode; _decode = base64.b85decode
        try:
            encryptor = pymultialgo.get_encryptor(algo, key, iv, mode, padd)
            dc = encryptor.decrypt(_decode(data)).decode(encd)
            print(dc)
        except:
            print(traceback.format_exc())

    def _pymultialgo_code(*a):
        try:
            from . import pymultialgo
        except:
            import pymultialgo
        ctxt.delete(0.,tkinter.END)
        with open(pymultialgo.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(f9002, text='[算法]',command=_pymultialgo_code,width=5).pack(side=tkinter.RIGHT)
    Button(f9002, text='解密',command=_pymultialgo_decode,width=5).pack(side=tkinter.RIGHT)
    Button(f9002, text='加密',command=_pymultialgo_encode,width=5).pack(side=tkinter.RIGHT)


    fevpkdflab = '''
            以 U2FsdGVkX1 开头的加密数据相关
    该种类的加密方式为 cryptojs 的默认加密方式，在某种程度上只需要密码即可解密
    但是实际上使用的却是 CBC 模式（该模式需要设置偏移 iv参数）。
    并且每次加密都能加密出不同的密文数据，但是却用密码都能解密出相同的原始数据，
    目前这里暂时只提供了加解密算法代码。
    加密算法伪代码：
        salt        <= os.urandom(8)
        key,iv      <= EvpKDF(realkey, salt)        # 这里有简化，详细请看代码
        encodedata  <= encrypt(key, iv, CBC, data)  # 通常为 cbc/pkcs7
        result      <= base64('Salted__' + salt + encodedata)
        1) 生成随机盐
        2) 通过真实 key 与盐算出固定加密用的 key,iv
        3) 使用加密算法加密数据
        4) 将标识头（Salted__）、盐和加密数据打包并进行 base64 就是加密数据，
            因为标识头都是一样的，所以一般都是以 U2FsdGVkX1 开头的加密数据
'''.rstrip('\n')
    fevpkdf0 = Frame(ff1)
    fevpkdf0.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fevpkdf0, text=fevpkdflab,font=ft).pack(fill=tkinter.X,expand=True)
    fevpkdf1 = Frame(ff1)
    fevpkdf1.pack(side=tkinter.TOP,fill=tkinter.X)
    fevpkdf2 = Frame(fevpkdf1)
    fevpkdf2.pack(side=tkinter.TOP,fill=tkinter.X)
    def _evpkdf_code(*a):
        try:
            from . import pyevpkdf
        except:
            import pyevpkdf
        ctxt.delete(0.,tkinter.END)
        with open(pyevpkdf.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)
    Button(fevpkdf2, text='[算法]',command=_evpkdf_code,width=5).pack(side=tkinter.RIGHT)










    _fss1 = Frame(fr)
    enb.add(_fss1, text='爆破;RSA;二维码')
    enb.pack()
    enb_names[_fss1._name] = '爆破;RSA;二维码'
    fss1 = Frame(_fss1)
    fss1.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)
    fss1_ = Frame(_fss1)
    fss1_.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)
    txttitlefss = Frame(fss1_)
    txttitlefss.pack(side=tkinter.TOP)
    Label(txttitlefss, text='使用以下文本框进行输出').pack(side=tkinter.LEFT,padx=10)
    fssentlimit2 = Entry(txttitlefss, width=10)
    fssentlimit2.pack(side=tkinter.LEFT)
    fssentlimit2.insert(0,'10000')
    fsstxt = Text(fss1_,font=ft)
    fsstxt.pack(padx=padx,pady=pady,fill=tkinter.BOTH,expand=True)

    bhashhelp = '''
            hash 爆破
    该算法会自动使用一定程度的黑客语(leetspeak)对密码进行膨胀处理，详细的处理请参考算法。
    若想使用自己的字典，可以直接将字典内容粘贴到右侧窗口中，点击[自定义爆破]即可
    会自动使用选择的算法进行 hash 的对比。
    另外，算法内还有名字前缀以及日期的组合，没有放在该功能中，如果有更详细的需求
    请直接点开算法，使用别的ide进行更丰富的爆破处理。
'''.rstrip('\n')
    # 这里是 twofish 算法的部分
    def fbx_change_cbit_1(*content):
        if content:
            blen = len(content[0])
            fbx_cbit1['text'] = str(blen)
            return True

    fbx_change_cbit1 = root.register(fbx_change_cbit_1)
    fbx100 = Frame(fss1)
    fbx100.pack(side=tkinter.TOP,fill=tkinter.X)
    fbx101 = Frame(fbx100)
    fbx102 = Frame(fbx100)
    fbx103 = Frame(fbx100)
    fbx101.pack(side=tkinter.TOP,fill=tkinter.X)
    fbx102.pack(side=tkinter.TOP,fill=tkinter.X)
    fbx103.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fbx101, text=bhashhelp, font=ft).pack(fill=tkinter.X,expand=True)
    def _pymapmd5_decode(*a):
        _hash = fbxent.get().strip()
        _mode = fbx1_mode1.get()
        fsstxt.delete(0.,tkinter.END)
        try:
            from . import pymapmd5, pymd2
        except:
            import pymapmd5, pymd2
        try:
            if _mode == 'md2':
                hfunc = pymd2.md2
            else:
                hfunc = lambda i:hashlib.new(_mode, i).hexdigest()
            emptyhash = hfunc(b'')
            if len(_hash) != len(emptyhash):
                print('非法的hash长度')
                print(_mode,'需要的长度为',len(emptyhash))
                return
            if _hash == emptyhash:
                print('空参数的hash。')
                return
            ctime = time.time()
            mk_map_passleet = pymapmd5.mk_map_passleet
            zpasslist       = mk_map_passleet(pymapmd5.zpasslist)
            map_namehead_times = pymapmd5.map_namehead_times
            findkey = False
            for i in itertools.chain(zpasslist, map_namehead_times()):
                v = hfunc(i.encode())
                if v == _hash:
                    findkey = (v, i)
                    break
            if findkey:
                print('发现密码：')
                print('password:',i)
                print('hash:',v)
            else:
                print('未找到密码')
            print('使用时间：',time.time()-ctime)
        except:
            fsstxt.delete(0.,tkinter.END)
            print(traceback.format_exc())

    def _inputdict_map(*a):
        _hash = fbxent.get().strip()
        _mode = fbx1_mode1.get()
        _list = fsstxt.get(0.,tkinter.END).strip('\n').splitlines()
        fsstxt.delete(0.,tkinter.END)
        try:
            from . import pymapmd5, pymd2
        except:
            import pymapmd5, pymd2
        try:
            if _mode == 'md2':
                hfunc = pymd2.md2
            else:
                hfunc = lambda i:hashlib.new(_mode, i).hexdigest()
            emptyhash = hfunc(b'')
            mk_map_passleet = pymapmd5.mk_map_passleet
            if len(_hash) != len(emptyhash):
                print('非法的hash长度')
                print(_mode,'需要的长度为',len(emptyhash))
                return
            if _hash == emptyhash:
                print('空参数的hash。')
                return
            ctime = time.time()
            findkey = False
            for i in mk_map_passleet(_list):
                v = hfunc(i.encode())
                if v == _hash:
                    findkey = (v, i)
                    break
            if findkey:
                print('发现密码：')
                print('password:',i)
                print('hash:',v)
            else:
                print('未找到密码')
            print('使用时间：',time.time()-ctime)
        except:
            fsstxt.delete(0.,tkinter.END)
            print(traceback.format_exc())

    def _pymapmd5_code(*a):
        try:
            from . import pymapmd5
        except:
            import pymapmd5
        fsstxt.delete(0.,tkinter.END)
        with open(pymapmd5.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Label(fbx102, text='参数',width=4).pack(side=tkinter.LEFT,padx=5)
    fbxent = Entry(fbx102, width=41,validate='key',validatecommand=(fbx_change_cbit1, '%P'))
    fbxent.pack(side=tkinter.LEFT)
    fbxent.bind('<Key>', fbx_change_cbit1)
    # fbxent.pack(side=tkinter.LEFT)
    fbx1_mode1 = Combobox(fbx102,width=12,state='readonly')
    fbx1_mode1['values'] = ['md5', 'sha1', 'blake2b', 'blake2s', 'md2', 'md4', 'ripemd160', 'sha', \
                            'sha224', 'sha256', 'sha384', 'sha3_224', 'sha3_256', 'sha3_384', \
                            'sha3_512', 'sha512', 'whirlpool']
    fbx1_mode1.current(0)
    fbx1_mode1.pack(side=tkinter.RIGHT)
    fbx_cbit1 = Label(fbx102, text='0',width=4)
    fbx_cbit1.pack(side=tkinter.LEFT,padx=5)
    Label(fbx102, text='hash',width=4).pack(side=tkinter.RIGHT,padx=5)
    Button(fbx103, text='[算法]',command=_pymapmd5_code,width=5).pack(side=tkinter.RIGHT)
    Button(fbx103, text='快速爆破',command=_pymapmd5_decode,width=8).pack(side=tkinter.RIGHT)
    Button(fbx103, text='自定义爆破',command=_inputdict_map,width=10).pack(side=tkinter.RIGHT)






    sshelp = '''
            一些关于素数的内容
    以下一开始就在输入框的的内容均是测试内容
    e=65537=0x10001 是常用的的 rsa 加密标准的通用初始值，
    如果有需要自定义，请自行填入一个素数
'''.strip('\n')
    fss001 = Frame(fss1)
    fss001.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss001, text=sshelp,font=ft).pack(fill=tkinter.X,expand=True)

    def css002(*a):
        try:
            from . import pyprime
        except:
            import pyprime
        fsstxt.delete(0.,tkinter.END)
        try:
            num = int(ess002.get())
            if num > 1030:
                print('目前不支持生成超过 1030bit 位的素数。')
                return
            en = str(pyprime.get_prime(num))
            print(en)
        except:
            print(traceback.format_exc())

    fss002 = Frame(fss1)
    fss002.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss002,text='bit位',font=ft,width=6).pack(side=tkinter.LEFT)
    ess002 = Entry(fss002,width=40)
    ess002.pack(side=tkinter.LEFT)
    ess002.insert(0, '30')
    bss002 = Button(fss002,text='生成 n bit位素数',command=css002)
    bss002.pack(side=tkinter.LEFT,padx=2)

    def css002_1(*a):
        try:
            from . import pyprime
        except:
            import pyprime
        fsstxt.delete(0.,tkinter.END)
        try:
            num = int(ess002_1.get())
            if pyprime.isprime_mr(num):
                print('{} 是素数。'.format(num))
            else:
                print('{} 不是素数。'.format(num))
        except:
            print(traceback.format_exc())

    fss002_1 = Frame(fss1)
    fss002_1.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss002_1,text='数字',font=ft,width=6).pack(side=tkinter.LEFT)
    ess002_1 = Entry(fss002_1,width=40)
    ess002_1.pack(side=tkinter.LEFT)
    ess002_1.insert(0, '30')
    bss002_1 = Button(fss002_1,text='素性检测',command=css002_1)
    bss002_1.pack(side=tkinter.LEFT,padx=2)

    def css003(*a):
        fsstxt.delete(0.,tkinter.END)
        try:
            print(hex(int(ess003.get()))[2:].upper())
        except:
            print(traceback.format_exc())

    fss003 = Frame(fss1)
    fss003.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss003,text='数字',font=ft,width=6).pack(side=tkinter.LEFT)
    ess003 = Entry(fss003,width=40)
    ess003.pack(side=tkinter.LEFT)
    ess003.insert(0, '123456789012345678901234567890')
    bss003 = Button(fss003,text='数字转字符串',command=css003)
    bss003.pack(side=tkinter.LEFT,padx=2)

    def css004(*a):
        fsstxt.delete(0.,tkinter.END)
        try:
            print(int(ess004.get(),16))
        except:
            print(traceback.format_exc())

    fss004 = Frame(fss1)
    fss004.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss004,text='字符串',font=ft,width=6).pack(side=tkinter.LEFT)
    ess004 = Entry(fss004,width=40)
    ess004.pack(side=tkinter.LEFT)
    ess004.insert(0, '16704F4FAB27EC51A071C71C7')
    bss004 = Button(fss004,text='字符串转数字',command=css004)
    bss004.pack(side=tkinter.LEFT,padx=2)

    def css005(*a):
        try:
            from . import pyprime
        except:
            import pyprime
        fsstxt.delete(0.,tkinter.END)
        try:
            num = int(ess005.get())
            if not pyprime.isprime_mr(num):
                print('e 必须是一个素数。')
                return
            num2 = int(ess005_2.get())
            if num2 > 2050:
                print('当前的密钥 n bit长度不能超过2050.')
                return
            e,d,n = pyprime.create_rsa_key(num2, num)
            ess006.delete(0,tkinter.END)
            ess006.insert(0,str(n))
            ess007.delete(0,tkinter.END)
            ess007.insert(0,str(d))
            print('e:',e)
            print('d:',d)
            print('n:',n)
            print()
            print('密钥n bit位长度：',len(bin(n)[2:]))
            print('e,n 就是公钥')
            print('d,n 就是私钥')
        except:
            print(traceback.format_exc())

    fss005 = Frame(fss1)
    fss005.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss005,text='e',font=ft,width=6).pack(side=tkinter.LEFT)
    ess005 = Entry(fss005,width=40)
    ess005.pack(side=tkinter.LEFT)
    ess005.insert(0,'65537')
    bss005 = Button(fss005,text='生成rsa密钥对，密钥n的bit位：',command=css005)
    bss005.pack(side=tkinter.LEFT,padx=2)
    ess005_2 = Entry(fss005,width=5)
    ess005_2.pack(side=tkinter.LEFT)
    ess005_2.insert(0,'1024')

    def css006(*a):
        try:
            from . import pyprime
        except:
            import pyprime
        try:
            dataint = int(fsstxt.get(0.,tkinter.END))
            fsstxt.delete(0.,tkinter.END)
            e = int(ess005.get())
            n = int(ess006.get())
            print(pow(dataint, e, n))
        except:
            print(traceback.format_exc())

    fss006 = Frame(fss1)
    fss006.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss006,text='n',font=ft,width=6).pack(side=tkinter.LEFT)
    ess006 = Entry(fss006,width=40)
    ess006.pack(side=tkinter.LEFT)
    bss006 = Button(fss006,text='使用e,n对右侧数字进行rsa加密',command=css006)
    bss006.pack(side=tkinter.LEFT,padx=2)

    def css007(*a):
        try:
            from . import pyprime
        except:
            import pyprime
        try:
            dataint = int(fsstxt.get(0.,tkinter.END))
            fsstxt.delete(0.,tkinter.END)
            d = int(ess007.get())
            n = int(ess006.get())
            print(pow(dataint, d, n))
        except:
            print(traceback.format_exc())

    fss007 = Frame(fss1)
    fss007.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss007,text='d',font=ft,width=6).pack(side=tkinter.LEFT)
    ess007 = Entry(fss007,width=40)
    ess007.pack(side=tkinter.LEFT)
    bss007 = Button(fss007,text='使用d,n对右侧数字进行rsa解密',command=css007)
    bss007.pack(side=tkinter.LEFT,padx=2)

    def css009(*a):
        try:
            from . import pyprime
        except:
            import pyprime
        fsstxt.delete(0.,tkinter.END)
        try:
            num = int(ess009.get())
            plist = pyprime.prime_list_rho(num)
            print(plist)
            r = 1
            for i in plist:
                r *= i
            print('原始数据：',num)
            print('验算结果：',str(r))

        except:
            print(traceback.format_exc())

    fss009 = Frame(fss1)
    fss009.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss009,text='数字',font=ft,width=6).pack(side=tkinter.LEFT)
    ess009 = Entry(fss009,width=40)
    ess009.pack(side=tkinter.LEFT)
    bss009 = Button(fss009,text='质因数分解',command=css009)
    bss009.pack(side=tkinter.LEFT,padx=2)

    def css0014(*a):
        try:
            from . import pyprime
        except:
            import pyprime
        fsstxt.delete(0.,tkinter.END)
        try:
            e = int(ess005.get())
            n = int(ess006.get())
            print('注意：p,q 中的最小值的 bit 长度应大约小于40（经验判断），否则程序卡死。')
            fsstxt.update()
            d, p, q = pyprime.get_d_from_e_n(e, n)
            print('p:',p)
            print('q:',q)
            print()
            print('计算结果d:', d)
            ess007.delete(0,tkinter.END)
            ess007.insert(0,str(d))
        except:
            print(traceback.format_exc())

    fss0014 = Frame(fss1)
    fss0014.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss0014,text='n因式分解条件：n==p*q; min(p,q)的bit长度大约在40或更小，否则程序卡死',font=ft).pack(side=tkinter.LEFT)
    bss0014 = Button(fss0014,text='通过e,n直接解出参数d',command=css0014)
    bss0014.pack(side=tkinter.RIGHT,padx=2)

    def css008(*a):
        try:
            from . import pywiener_attack
        except:
            import pywiener_attack
        fsstxt.delete(0.,tkinter.END)
        try:
            e = int(ess005.get())
            n = int(ess006.get())
            v = str(pywiener_attack.wiener_attack(e, n))
            if v.startswith('Error'):
                print('使用的e参数：',e)
                print('使用的n参数：',n)
                print()
                print('wiener attack 算法攻击未成功。')
            else:
                print('使用的e参数：',e)
                print('使用的n参数：',n)
                print()
                print('wiener attack 算法攻击成功。')
                print('算出的 d 参数为：',v)
        except:
            print(traceback.format_exc())

    fss008 = Frame(fss1)
    fss008.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss008,text='当e很大，且d很小，这时可通过 wiener-attack 算法用e,n解密出d',font=ft).pack(side=tkinter.LEFT)
    bss008 = Button(fss008,text='使用e,n进行算法攻击',command=css008)
    bss008.pack(side=tkinter.RIGHT,padx=2)

    def _pyprime_code(*a):
        try:
            from . import pyprime
        except:
            import pyprime
        fsstxt.delete(0.,tkinter.END)
        with open(pyprime.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)
    def _pywiener_attck_code(*a):
        try:
            from . import pywiener_attack
        except:
            import pywiener_attack
        fsstxt.delete(0.,tkinter.END)
        with open(pywiener_attack.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    fss0010 = Frame(fss1)
    fss0010.pack(side=tkinter.TOP,fill=tkinter.X)
    bss0010 = Button(fss0010,text='素数与rsa相关算法',command=_pyprime_code)
    bss0010.pack(side=tkinter.RIGHT,padx=2)
    bss0010_2 = Button(fss0010,text='wiener-attack算法',command=_pywiener_attck_code)
    bss0010_2.pack(side=tkinter.RIGHT,padx=2)






    sshelp = '''
            关于二维码的加解密
    解密：
        使用解密时，需要将图片打开，解密功能会自动将桌面截图，
        也可以直接使用截图解密，这样可以更加精准的定位数据。
        當然，你可以选择使用脚本进行自定义的处理。
    加密：
        在加密中中文的加密有时会因为zbar的问题解码成无意义的日文或乱码。
        请确认解码的正常后再使用加密的二维码，
        解决方式可以尝试微调一下加密数据。
'''.strip('\n')

    fss0011 = Frame(fss1)
    fss0011.pack(side=tkinter.TOP,fill=tkinter.X)        
    Label(fss0011, text=sshelp,font=ft).pack(fill=tkinter.X,expand=True)
    def css0012(*a):
        try:
            from . import pypyzbar
        except:
            import pypyzbar
        fsstxt.delete(0.,tkinter.END)
        try:
            screenshot_bit = pypyzbar.screenshot()
            pixbytes, w, h = pypyzbar.create_png_pixel_tobytes(screenshot_bit)
            deco = pypyzbar.decode((pixbytes, w, h))
            print(time.ctime())
            print('开始识别')
            if deco:
                print('发现{}个二维码并解密：'.format(len(deco)))
                print(' <注意：含有中文解密若是在解码中出现乱码问题则该bytes类型数据就已经不可信了>')
                for idx,i in enumerate(deco):
                    print('[ {} ]'.format(idx))
                    print('    bytes类型展示')
                    print('        ',i.data)
                    print('    尝试简单解码')
                    try:
                        print('        ',i.data.decode('utf-8'))
                    except:
                        print('        ',i.data.decode('gbk'))
            else:
                print('未定位到二维码。')
            print('识别结束')
        except:
            print(traceback.format_exc())

    def css0012_1(*a):
        try:
            from . import pypyzbar
        except:
            import pypyzbar
        try:
            pixbytes, w, h = pypyzbar.screenshot_rect(root)
            deco = pypyzbar.decode((pixbytes, w, h))
            fsstxt.delete(0.,tkinter.END)
            print(time.ctime())
            print('开始识别')
            if deco:
                print('发现{}个二维码并解密：'.format(len(deco)))
                print(' <注意：含有中文解密若是在解码中出现问题则该bytes类型数据就已经不可信了>')
                for idx,i in enumerate(deco):
                    print('[ {} ]'.format(idx))
                    print('    bytes类型展示')
                    print('        ',i.data)
                    print('    尝试简单解码')
                    try:
                        print('        ',i.data.decode('utf-8'))
                    except:
                        print('        ',i.data.decode('gbk'))
            else:
                print('未定位到二维码。')
            print('识别结束')
        except:
            print(traceback.format_exc())

    def css0013(*a):
        try:
            from . import pyqrcode
        except:
            import pyqrcode
        fsstxt.delete(0.,tkinter.END)
        try:
            enctxt = ess0012.get().strip()
            encdlv = cbx_0013.get().strip()
            if encdlv ==  '7%': encdlv = pyqrcode.ERROR_CORRECT_L
            if encdlv == '15%': encdlv = pyqrcode.ERROR_CORRECT_M
            if encdlv == '25%': encdlv = pyqrcode.ERROR_CORRECT_Q
            if encdlv == '30%': encdlv = pyqrcode.ERROR_CORRECT_H
            s = pyqrcode.QRCode(error_correction=encdlv)
            s.add_data(enctxt.encode('utf-8'))
            for i in s.get_matrix():
                black = '██'
                white = '  '
                v = ''.join([black if j else white for j in i])
                print(v)
        except:
            print(traceback.format_exc())

    fss0012 = Frame(fss1)
    fss0012.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss0012,text='加密',font=ft,width=6).pack(side=tkinter.LEFT)
    ess0012 = Entry(fss0012,width=50)
    ess0012.pack(side=tkinter.LEFT)

    fss0013 = Frame(fss1)
    fss0013.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss0013,text='等级',font=ft,width=6).pack(side=tkinter.LEFT)
    cbx_0013 = Combobox(fss0013,width=6,state='readonly')
    cbx_0013['values'] = ['7%', '15%', '25%', '30%']
    cbx_0013.current(1)
    cbx_0013.pack(side=tkinter.LEFT)
    bss0013_3 = Button(fss0013,text='截图解密',command=css0012_1,width=9)
    bss0013_3.pack(side=tkinter.RIGHT,padx=1)
    bss0013_2 = Button(fss0013,text='全屏解密',command=css0012,width=9)
    bss0013_2.pack(side=tkinter.RIGHT,padx=1)
    bss0013 = Button(fss0013,text='二维码加密',command=css0013,width=9)
    bss0013.pack(side=tkinter.RIGHT,padx=1)
    def _pyqrcode_code(*a):
        try:
            from . import pyqrcode
        except:
            import pyqrcode
        fsstxt.delete(0.,tkinter.END)
        with open(pyqrcode.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)
    def _pypyzbar_code(*a):
        try:
            from . import pypyzbar
        except:
            import pypyzbar
        fsstxt.delete(0.,tkinter.END)
        with open(pypyzbar.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)
    def _donate_code(*a):
        try:
            from . import pyqrcode
        except:
            import pyqrcode
        fsstxt.delete(0.,tkinter.END)
        try:
            encdlv = pyqrcode.ERROR_CORRECT_L
            print('支付宝扫码赞助：')
            enctxt = 'HTTPS://QR.ALIPAY.COM/FKX07500WBJ0OXZUXJLUCF'
            s = pyqrcode.QRCode(error_correction=encdlv)
            s.add_data(enctxt.encode('utf-8'))
            for i in s.get_matrix()[3:]:
                black = '██'
                white = '  '
                v = ''.join([black if j else white for j in i])
                print(v)
            print('微信扫码赞助：')
            enctxt = 'wxp://f2f0xF3d1egb-YtPxHm0AZHw0gdJByCgZeLz'
            s = pyqrcode.QRCode(error_correction=encdlv)
            s.add_data(enctxt.encode('utf-8'))
            for i in s.get_matrix()[3:]:
                black = '██'
                white = '  '
                v = ''.join([black if j else white for j in i])
                print(v)
        except:
            print(traceback.format_exc())
    style = ttk.Style()
    style.map("TEST.TButton",
        foreground=[('!focus', '#EE6363')],
    )
    bss0013_5 = Button(fss0013,text='赞助作者',command=_donate_code,width=7,style='TEST.TButton')
    bss0013_5.pack(side=tkinter.LEFT)
    bss0013_4 = Button(fss0013,text='加密[算法]',command=_pyqrcode_code,width=9)
    bss0013_4.pack(side=tkinter.LEFT)
    bss0013_3 = Button(fss0013,text='解密[算法]',command=_pypyzbar_code,width=9)
    bss0013_3.pack(side=tkinter.LEFT)



    zfcys = r'''
            字符串或二进制的简单压缩，嵌入代码
    使用有边框进行字符串的压缩处理并输出代码化的脚本
    便于让二进制数据能更好更快的嵌入脚本之中（下面压缩算法均为py自带）
'''.strip('\n')
    zfcys = '\n' + zfcys
    fss0015 = Frame(fss1)
    fss0015.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fss0015, text=zfcys, font=ft).pack(fill=tkinter.X,expand=True)

    def _zipstring(*a):
        try:
            from . import pycompress
        except:
            import pycompress
        w = int(eny0015.get())
        b = cbx0015_1.get()
        z = cbx0015_2.get()
        e = cbx0015_3.get()
        f = ibx0015.get()
        string = fsstxt.get(0.,tkinter.END).strip('\n')
        if f:
            v = pycompress.format_compress_file(b, z, w, e)
        else:
            v = pycompress.format_compress_string(string, b, z, w, e)
        fsstxt.delete(0.,tkinter.END)
        print(v)
    Label(fss0015, text='脚本宽度', font=ft).pack(side=tkinter.LEFT)
    eny0015 = Entry(fss0015,width=4)
    eny0015.pack(side=tkinter.LEFT)
    eny0015.insert(0,'70')
    Label(fss0015, text='base模式', font=ft).pack(side=tkinter.LEFT)
    cbx0015_1 = Combobox(fss0015,width=6,state='readonly')
    cbx0015_1['values'] = ['base64', 'base85']
    cbx0015_1.pack(side=tkinter.LEFT)
    cbx0015_1.current(0)
    Label(fss0015, text='压缩方式', font=ft).pack(side=tkinter.LEFT)
    cbx0015_2 = Combobox(fss0015,width=4,state='readonly')
    cbx0015_2['values'] = ['zlib', 'lzma', 'gzip', 'None']
    cbx0015_2.pack(side=tkinter.LEFT)
    cbx0015_2.current(0)
    Label(fss0015, text='编码', font=ft).pack(side=tkinter.LEFT)
    cbx0015_3 = Combobox(fss0015,width=6,state='readonly')
    cbx0015_3['values'] = ['utf-8', 'gbk']
    cbx0015_3.pack(side=tkinter.LEFT)
    cbx0015_3.current(0)
    ibx0015 = tkinter.IntVar()
    kbx0015 = Checkbutton(fss0015,text='压缩文件', variable=ibx0015, width=6)
    kbx0015.pack(side=tkinter.LEFT)
    bss0015_1 = Button(fss0015,text='开始压缩',command=_zipstring, width=9)
    bss0015_1.pack(side=tkinter.RIGHT)



    _fpic = Frame(fr)
    enb.add(_fpic, text='图片相关')
    enb.pack()
    enb_names[_fpic._name] = '图片相关'
    fpic1 = Frame(_fpic)
    fpic1.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)
    fpic1_ = Frame(_fpic)
    fpic1_.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)
    txttitlefpic = Frame(fpic1_)
    txttitlefpic.pack(side=tkinter.TOP)
    Label(txttitlefpic, text='使用以下文本框进行输出').pack(side=tkinter.LEFT,padx=10)
    fpicentlimit2 = Entry(txttitlefpic, width=10)
    fpicentlimit2.pack(side=tkinter.LEFT)
    fpicentlimit2.insert(0,'10000')
    fpictxt = Text(fpic1_,font=ft)
    fpictxt.pack(padx=padx,pady=pady,fill=tkinter.BOTH,expand=True)

    fpic0010 = Frame(fpic1)
    fpic0010.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0012 = Frame(fpic0010)
    fpic0012.pack(side=tkinter.TOP,fill=tkinter.X)
    def _find_desktop_gif(*a):
        data = fpictxt.get(0.,tkinter.END).strip('\n')
        fpictxt.delete(0.,tkinter.END)
        try:
            from . import pyfinddesktopfile
            from . import pygif
        except:
            import pyfinddesktopfile
            import pygif
        try:
            finddesktop      = pyfinddesktopfile.finddesktop
            findfile_desktop = pyfinddesktopfile.findfile_desktop
            SimpleDialog     = pyfinddesktopfile.SimpleDialog
            gifs = findfile_desktop('gif')
            d = finddesktop()
            s = SimpleDialog(fr,buttons=gifs)
            v = os.path.join(d, gifs[s.go()])
            print('为了提高压缩率，gif图片格式增加了一些透明通道,')
            print('所以一些图片出现白色脏点是正常的。')
            print('正在解析图片...')
            fpictxt.update()
            phlist = pygif.mk_phlist(v)
            for i in phlist:
                fpictxt.image_create(tkinter.END, image=i)
        except:
            fpictxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _pygif_code(*a):
        try:
            from . import pygif
        except:
            import pygif
        fpictxt.delete(0.,tkinter.END)
        with open(pygif.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    pichelp1 = '''图片相关的处理部分'''
    Label(fpic0012, text=pichelp1).pack(side=tkinter.TOP,padx=10)
    Button(fpic0012, text='[算法]',command=_pygif_code,width=5).pack(side=tkinter.LEFT)
    Label(fpic0012, text=' 这里为 gif 图片切分显示。').pack(side=tkinter.LEFT)
    Button(fpic0012, text='从桌面获取gif解析',command=_find_desktop_gif,width=16).pack(side=tkinter.RIGHT)

    fpic0020 = Frame(fpic1)
    fpic0020.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0022 = Frame(fpic0020)
    fpic0022.pack(side=tkinter.TOP,fill=tkinter.X)
    def _pyscreenshot(*a):
        data = fpictxt.get(0.,tkinter.END).strip('\n')
        fpictxt.delete(0.,tkinter.END)
        try:
            from . import pyfinddesktopfile
            from . import pyscreenshot
        except:
            import pyfinddesktopfile
            import pyscreenshot
        try:
            finddesktop      = pyfinddesktopfile.finddesktop
            screenshot_rect  = pyscreenshot.screenshot_rect
            dfile  = os.path.join(finddesktop(), fpic002ent.get().strip())
            bitpng = screenshot_rect(root)
            with open(dfile, 'wb') as f:
                f.write(bitpng)
                print('write in:{}'.format(dfile))
        except:
            fpictxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _pyscreenshot_code(*a):
        try:
            from . import pyscreenshot
        except:
            import pyscreenshot
        fpictxt.delete(0.,tkinter.END)
        with open(pyscreenshot.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(fpic0022, text='[算法]',command=_pyscreenshot_code,width=5).pack(side=tkinter.LEFT)
    Label(fpic0022, text=' 截图并存放到桌面，文件名字：').pack(side=tkinter.LEFT)
    fpic002ent = Entry(fpic0022,width=10)
    fpic002ent.pack(side=tkinter.LEFT)
    fpic002ent.insert(0,'_temp.png')
    Button(fpic0022, text='截图存放至桌面',command=_pyscreenshot,width=16).pack(side=tkinter.RIGHT)


    fpic0030 = Frame(fpic1)
    fpic0030.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0032 = Frame(fpic0030)
    fpic0032.pack(side=tkinter.TOP,fill=tkinter.X)
    def _pyscreenshot_video_local(*a):
        data = fpictxt.get(0.,tkinter.END).strip('\n')
        fpictxt.delete(0.,tkinter.END)
        try:
            from . import pyfinddesktopfile
            from . import pyscreenshot
        except:
            import pyfinddesktopfile
            import pyscreenshot
        try:
            finddesktop         = pyfinddesktopfile.finddesktop
            screenshot_rect_int = pyscreenshot.screenshot_rect_int
            dfile  = os.path.join(finddesktop(), fpic003ent.get().strip())
            left,top,w,h = screenshot_rect_int(root)
            fpic003ent1.delete(0,tkinter.END)
            fpic003ent2.delete(0,tkinter.END)
            fpic003ent3.delete(0,tkinter.END)
            fpic003ent4.delete(0,tkinter.END)
            fpic003ent1.insert(0,str(left))
            fpic003ent2.insert(0,str(top))
            fpic003ent3.insert(0,str(w))
            fpic003ent4.insert(0,str(h))
        except:
            fpictxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    fpic003toggle = True
    def _pyscreenshot_video(*a):
        data = fpictxt.get(0.,tkinter.END).strip('\n')
        fpictxt.delete(0.,tkinter.END)
        try:
            from . import pyfinddesktopfile
            from . import pyscreenshot
        except:
            import pyfinddesktopfile
            import pyscreenshot
        try:
            finddesktop = pyfinddesktopfile.finddesktop
            _start_video = pyscreenshot._start_video
            _stop_video  = pyscreenshot._stop_video
            nonlocal fpic003toggle
            if fpic003toggle:
                fpic003btn1['text'] = '录制图片[已开启]'
                fpic003toggle = False
                try:
                    left = int(fpic003ent1.get().strip())
                    top  = int(fpic003ent2.get().strip())
                    w    = int(fpic003ent3.get().strip())
                    h    = int(fpic003ent4.get().strip())
                    rect = (left,top,w,h)
                except:
                    print('error left,top,w,h. use fill desktop.')
                    rect = pyscreenshot.desktop_ltwh()
                _start_video(finddesktop(), rect, fpic003ent.get().strip(), print)
            elif not fpic003toggle:
                fpic003btn1['text'] = '录制图片[已关闭]'
                fpic003toggle = True
                _stop_video()

        except:
            fpictxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _pyscreenshot_video_code(*a):
        try:
            from . import pyscreenshot
        except:
            import pyscreenshot
        fpictxt.delete(0.,tkinter.END)
        with open(pyscreenshot.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(fpic0032, text='[算法]',command=_pyscreenshot_video_code,width=5).pack(side=tkinter.LEFT)
    Label(fpic0032, text=' 文件夹：').pack(side=tkinter.LEFT)
    fpic003ent = Entry(fpic0032,width=6)
    fpic003ent.pack(side=tkinter.LEFT)
    fpic003ent.insert(0,'_temp')
    Label(fpic0032, text='left').pack(side=tkinter.LEFT)
    fpic003ent1 = Entry(fpic0032,width=4)
    fpic003ent1.pack(side=tkinter.LEFT)
    Label(fpic0032, text='top').pack(side=tkinter.LEFT)
    fpic003ent2 = Entry(fpic0032,width=4)
    fpic003ent2.pack(side=tkinter.LEFT)
    Label(fpic0032, text='w').pack(side=tkinter.LEFT)
    fpic003ent3 = Entry(fpic0032,width=4)
    fpic003ent3.pack(side=tkinter.LEFT)
    Label(fpic0032, text='h').pack(side=tkinter.LEFT)
    fpic003ent4 = Entry(fpic0032,width=4)
    fpic003ent4.pack(side=tkinter.LEFT)
    fpic003btn1 = Button(fpic0032, text='录制图片[已关闭]',command=_pyscreenshot_video,width=16)
    fpic003btn1.pack(side=tkinter.RIGHT)
    fpic003btn2 = Button(fpic0032, text='定位',command=_pyscreenshot_video_local,width=5)
    fpic003btn2.pack(side=tkinter.RIGHT)

    fpic0040 = Frame(fpic1)
    fpic0040.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0042 = Frame(fpic0040)
    fpic0042.pack(side=tkinter.TOP,fill=tkinter.X)
    def _pypng2gif(*a):
        data = fpictxt.get(0.,tkinter.END).strip('\n')
        fpictxt.delete(0.,tkinter.END)
        try:
            from . import pyfinddesktopfile
            from . import pypng2gif
        except:
            import pyfinddesktopfile
            import pypng2gif
        try:
            finddesktop = pyfinddesktopfile.finddesktop
            create_gif  = pypng2gif.create_gif
            filedir  = os.path.join(finddesktop(), fpic003ent.get().strip())
            filepathname = os.path.join(finddesktop(), fpic004ent1.get().strip())
            step = int(fpic004ent2.get().strip())
            try:
                scale = float(fpic004ent3.get().strip())
            except:
                scale = None
            try:
                size_w = int(fpic004ent4.get().strip())
                size_h = int(fpic004ent5.get().strip())
                size = size_w, size_h
            except:
                size = None
            print('step: ',step)
            print('size: ',size)
            print('scale:',scale)
            realwh = create_gif(filepathname,filedir,size=size,scale=1/scale if scale else None,step=step)
            print('write in:{}'.format(filepathname))
            print('gif-> wh:{}'.format(realwh))
        except:
            fpictxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _pypng2gif_code(*a):
        try:
            from . import pypng2gif
        except:
            import pypng2gif
        fpictxt.delete(0.,tkinter.END)
        with open(pypng2gif.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    pichelp2 = '''    以下部分需要使用到第三方库 Pillow (py3)
通过桌面录制的 png 文件生成 gif 文件
鼓励前后部分多录制，因为下面合并 png 的步骤前
可以直接删除部分 png 图片文件来调节 gif 文件前后溢出位。
    step    : 间隔几张图片
    scale   : 等比缩放（建议使用）
    size_w  : 自定义尺寸（不建议使用）
    size_h  : 自定义尺寸（不建议使用）
（size，scale 最多只有一个有效，不编辑则使用默认）
'''
    Label(fpic0042, text=pichelp2).pack(side=tkinter.TOP)
    Button(fpic0042, text='[算法]',command=_pypng2gif_code,width=5).pack(side=tkinter.LEFT)
    Label(fpic0042, text='生成文件名：').pack(side=tkinter.LEFT)
    fpic004ent1 = Entry(fpic0042,width=8)
    fpic004ent1.pack(side=tkinter.LEFT)
    fpic004ent1.insert(0,'_temp.gif')
    Label(fpic0042, text='step').pack(side=tkinter.LEFT)
    fpic004ent2 = Entry(fpic0042,width=4)
    fpic004ent2.pack(side=tkinter.LEFT)
    fpic004ent2.insert(0,'2')
    Label(fpic0042, text='scale').pack(side=tkinter.LEFT)
    fpic004ent3 = Entry(fpic0042,width=4)
    fpic004ent3.pack(side=tkinter.LEFT)
    Label(fpic0042, text='size_w').pack(side=tkinter.LEFT)
    fpic004ent4 = Entry(fpic0042,width=4)
    fpic004ent4.pack(side=tkinter.LEFT)
    Label(fpic0042, text='size_h').pack(side=tkinter.LEFT)
    fpic004ent5 = Entry(fpic0042,width=4)
    fpic004ent5.pack(side=tkinter.LEFT)
    Button(fpic0042, text='生成 gif 到桌面',command=_pypng2gif,width=16).pack(side=tkinter.RIGHT)





    # opencv
    fpic0050 = Frame(fpic1)
    fpic0050.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0052 = Frame(fpic0050)
    fpic0052.pack(side=tkinter.TOP,fill=tkinter.X)
    def _opencv_canny(*a):
        data = fpictxt.get(0.,tkinter.END).strip('\n')
        fpictxt.delete(0.,tkinter.END)
        try:
            from . import pycv2
            from . import pyfinddesktopfile
        except:
            import pycv2
            import pyfinddesktopfile
        try:
            finddesktop      = pyfinddesktopfile.finddesktop
            findfile_desktop = pyfinddesktopfile.findfile_desktop
            SimpleDialog     = pyfinddesktopfile.SimpleDialog
            gifs = findfile_desktop()
            gifs = [i for i in gifs if any([i.lower().endswith(j) for j in pycv2.canread])]
            if not gifs: return
            d = finddesktop()
            s = SimpleDialog(fr,buttons=gifs,default=0,cancel=-1,).go()
            if s != -1:
                v = os.path.join(d, gifs[s])
                left  = int(fpic005ent1.get().strip())
                right = int(fpic005ent2.get().strip())
                v = pycv2.canny(v, left, right)
                print('shape[h,w] -> {}'.format(v.shape))
        except:
            fpictxt.delete(0.,tkinter.END)
            print(traceback.format_exc())
            print('error decoding!!! check input data.')

    def _pycv2_code(*a):
        try:
            from . import pycv2
        except:
            import pycv2
        fpictxt.delete(0.,tkinter.END)
        with open(pycv2.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)
    pichelp1 = '''以下部分需要使用到第三方库 opencv [pip install opencv-python (py3)]'''
    Label(fpic0052, text=pichelp1).pack(side=tkinter.TOP,padx=10)
    Button(fpic0052, text='[算法]',command=_pycv2_code,width=5).pack(side=tkinter.LEFT)
    Label(fpic0052, text=' Canny').pack(side=tkinter.LEFT)
    Button(fpic0052, text='Canny',command=_opencv_canny,width=16).pack(side=tkinter.RIGHT)
    Label(fpic0052, text=' 后两项取值范围[0-255]，通常默认即可: left').pack(side=tkinter.LEFT)
    fpic005ent1 = Entry(fpic0052,width=4)
    fpic005ent1.pack(side=tkinter.LEFT)
    fpic005ent1.insert(0,'70')
    Label(fpic0052, text='right').pack(side=tkinter.LEFT)
    fpic005ent2 = Entry(fpic0052,width=4)
    fpic005ent2.pack(side=tkinter.LEFT)
    fpic005ent2.insert(0,'140')

    fpic0060 = Frame(fpic1)
    fpic0060.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0062 = Frame(fpic0060)
    fpic0062.pack(side=tkinter.TOP,fill=tkinter.X)
    def _opencv_laplacian(*a):
        data = fpictxt.get(0.,tkinter.END).strip('\n')
        fpictxt.delete(0.,tkinter.END)
        try:
            from . import pycv2
            from . import pyfinddesktopfile
        except:
            import pycv2
            import pyfinddesktopfile
        try:
            finddesktop      = pyfinddesktopfile.finddesktop
            findfile_desktop = pyfinddesktopfile.findfile_desktop
            SimpleDialog     = pyfinddesktopfile.SimpleDialog
            gifs = findfile_desktop()
            gifs = [i for i in gifs if any([i.lower().endswith(j) for j in pycv2.canread])]
            if not gifs: return
            d = finddesktop()
            s = SimpleDialog(fr,buttons=gifs,default=0,cancel=-1,).go()
            if s != -1:
                v = os.path.join(d, gifs[s])
                v = pycv2.laplacian(v)
                print('shape[h,w] -> {}'.format(v.shape))
        except:
            fpictxt.delete(0.,tkinter.END)
            print(traceback.format_exc())

    def _pycv2_code(*a):
        try:
            from . import pycv2
        except:
            import pycv2
        fpictxt.delete(0.,tkinter.END)
        with open(pycv2.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(fpic0062, text='[算法]',command=_pycv2_code,width=5).pack(side=tkinter.LEFT)
    Label(fpic0062, text=' Laplacian').pack(side=tkinter.LEFT)
    Button(fpic0062, text='Laplacian',command=_opencv_laplacian,width=16).pack(side=tkinter.RIGHT)

    fpic0070 = Frame(fpic1)
    fpic0070.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0072 = Frame(fpic0070)
    fpic0072.pack(side=tkinter.TOP,fill=tkinter.X)
    def _opencv_sobel(*a):
        data = fpictxt.get(0.,tkinter.END).strip('\n')
        fpictxt.delete(0.,tkinter.END)
        try:
            from . import pycv2
            from . import pyfinddesktopfile
        except:
            import pycv2
            import pyfinddesktopfile
        try:
            finddesktop      = pyfinddesktopfile.finddesktop
            findfile_desktop = pyfinddesktopfile.findfile_desktop
            SimpleDialog     = pyfinddesktopfile.SimpleDialog
            gifs = findfile_desktop()
            gifs = [i for i in gifs if any([i.lower().endswith(j) for j in pycv2.canread])]
            if not gifs: return
            d = finddesktop()
            s = SimpleDialog(fr,buttons=gifs,default=0,cancel=-1,).go()
            if s != -1:
                v = os.path.join(d, gifs[s])
                v = pycv2.sobel(v)
                print('shape[h,w] -> {}'.format(v.shape))
        except:
            fpictxt.delete(0.,tkinter.END)
            print(traceback.format_exc())

    def _pycv2_code(*a):
        try:
            from . import pycv2
        except:
            import pycv2
        fpictxt.delete(0.,tkinter.END)
        with open(pycv2.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(fpic0072, text='[算法]',command=_pycv2_code,width=5).pack(side=tkinter.LEFT)
    Label(fpic0072, text=' Sobel').pack(side=tkinter.LEFT)
    Button(fpic0072, text='Sobel',command=_opencv_sobel,width=16).pack(side=tkinter.RIGHT)

    fpic0080 = Frame(fpic1)
    fpic0080.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0082 = Frame(fpic0080)
    fpic0082.pack(side=tkinter.TOP,fill=tkinter.X)
    def _opencv_matchtemplate(*a):
        data = fpictxt.get(0.,tkinter.END).strip('\n')
        fpictxt.delete(0.,tkinter.END)
        try:
            from . import pycv2
            from . import pyfinddesktopfile
            from . import pyscreenshot
        except:
            import pycv2
            import pyfinddesktopfile
            import pyscreenshot
        try:
            finddesktop      = pyfinddesktopfile.finddesktop
            findfile_desktop = pyfinddesktopfile.findfile_desktop
            SimpleDialog     = pyfinddesktopfile.SimpleDialog
            gifs = findfile_desktop()
            gifs = [i for i in gifs if any([i.lower().endswith(j) for j in pycv2.canread])]
            d = finddesktop()
            s = SimpleDialog(fr,buttons=gifs,default=0,cancel=-1,).go()
            if s != -1:
                v = os.path.join(d, gifs[s])
                t = fpic008ent1.get().strip()
                f = tempfile.mkdtemp()
                if t and os.path.isfile(os.path.join(d, t)):
                    t = os.path.join(d, t)
                else:
                    t = os.path.join(f, '_desktop_png.png')
                    with open(t, 'wb') as f: 
                        f.write(pyscreenshot.screenshot())
                v = pycv2.findmatchtemplate(v, t)
                print('top,left,w,h -> {}'.format(v))
        except:
            fpictxt.delete(0.,tkinter.END)
            print(traceback.format_exc())

    def _pycv2_code(*a):
        try:
            from . import pycv2
        except:
            import pycv2
        fpictxt.delete(0.,tkinter.END)
        with open(pycv2.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    Button(fpic0082, text='[算法]',command=_pycv2_code,width=5).pack(side=tkinter.LEFT)
    Label(fpic0082, text=' MatchTemplate').pack(side=tkinter.LEFT)
    Button(fpic0082, text='MatchTemplate',command=_opencv_matchtemplate,width=16).pack(side=tkinter.RIGHT)
    Label(fpic0082, text=' 背景图片，不填则默认桌面').pack(side=tkinter.LEFT)
    fpic008ent1 = Entry(fpic0082,width=10)
    fpic008ent1.pack(side=tkinter.LEFT)


    fpic0090 = Frame(fpic1)
    fpic0090.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0092 = Frame(fpic0090)
    fpic0093 = Frame(fpic0090)
    fpic0094 = Frame(fpic0090)
    fpic0095 = Frame(fpic0090)
    fpic0096 = Frame(fpic0090)
    fpic0097 = Frame(fpic0090)
    pichelp1 = '''
 
    使用 pytorch 的模型快速训练简单的目标点选
以下部分需要使用到两个第三方库 opencv，以及 pytorch 。
之所以目前仅使用 voc 数据集是因为 labelimg 默认生成这种格式
并且 voc 格式在多标注方面用起来会很方便，这种格式的数据也会很清晰

* 注意，voc数据的图片文件路径请尽量和 voc标注数据的xml文件路径保持一致
  因为代码在xml文件的path找不到图片就会在xml相同地址下找同名图片文件。
  这样会很方便你剪贴训练数据集在不同地址进行训练。
* 注意，该工具内直接使用的训练模型是固定的，如果想要进行更高的自定义
  请直接点击 “算法” 按钮，获取训练+测试脚本。
* 默认每个 epoch 保存一次模型文件，默认支持中断继续训练。
'''.strip('\n')
    Label(fpic0092, text=pichelp1).pack(side=tkinter.TOP,padx=10)
    fpic0092.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0093.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0094.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0095.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0096.pack(side=tkinter.TOP,fill=tkinter.X)
    fpic0097.pack(side=tkinter.TOP,fill=tkinter.X)

    train_data, imginfos, class_types, anchors = None, None, None, None
    def _load_voc_data(*a):
        def load_voc_data(xmlpath, anchors):
            files = [os.path.join(xmlpath, path) for path in os.listdir(xmlpath) if path.endswith('.xml')]
            imginfos = []
            print('use anchors:', anchors)
            print('load xml file number:{}, start.'.format(len(files)))
            for idx, file in enumerate(files, 1):
                if idx % 1000 == 0: print('loading {}/{}'.format(idx, len(files)))
                imginfos.extend(pymini_yolo.read_voc_xml(file, islist=True))
            if idx % 1000 != 0: print('loading {}/{}'.format(idx, len(files)))
            # 注意这里加载数据的方式是小批量加载处理，所以自动生成 class_types
            # 如果有大量数据想要进行多批次训练，那么就需要注意 class_types 的生成。
            class_types = [imginfo.get('cate') for imginfo in imginfos]
            class_types = {typ:idx for idx,typ in enumerate(sorted(list(set(class_types))))}
            print('class_types:', class_types)
            train_data = []
            print('make x_true,y_true. start.')
            for idx, imginfo in enumerate(imginfos, 1):
                if idx % 1000 == 0: print('makeing x_true,y_true. {}/{}'.format(idx, len(imginfos)))
                x_true = pymini_yolo.torch.FloatTensor(imginfo['numpy'])
                y_true = pymini_yolo.make_y_true(imginfo, 13, anchors, class_types)
                train_data.append([x_true, y_true])
            if idx % 1000 != 0: print('makeing x_true,y_true. {}/{}'.format(idx, len(imginfos)))
            print('make x_true,y_true. ok.')
            return train_data, imginfos, class_types
        try:
            xmlpath = fpic009ent1.get().strip()
            if not os.path.isdir(xmlpath):
                print('无效的 voc 文件地址。')
                return
            print('importing pytorch, opencv.')
            try:
                from . import pymini_yolo
            except:
                import pymini_yolo
            print('import ok.')
            nonlocal train_data, imginfos, class_types, anchors
            anchors = [[60, 60]]
            train_data, imginfos, class_types = load_voc_data(xmlpath, anchors)
        except:
            print(traceback.format_exc())
        fpictxt.see(tkinter.END)

    def _pymini_yolo_code(*a):
        fpictxt.delete(0.,tkinter.END)
        path = os.path.join(os.path.split(__file__)[0], 'pymini_yolo.py')
        with open(path, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    def _set_train_file_dir(*a):
        import tkinter.filedialog
        dirpath = tkinter.filedialog.askdirectory()
        print(dirpath)
        fpic009ent1.delete(0,tkinter.END)
        fpic009ent1.insert(tkinter.END, dirpath)
        if not fpic0095ent1.get().strip():
            fpic0095ent1.insert(tkinter.END, dirpath)

    def _save_train_model_dir(*a):
        import tkinter.filedialog
        dirpath = tkinter.filedialog.askdirectory()
        print(dirpath)
        fpic0094ent1.delete(0,tkinter.END)
        fpic0094ent1.insert(tkinter.END, dirpath)

    def _save_test_model_dir(*a):
        import tkinter.filedialog
        dirpath = tkinter.filedialog.askdirectory()
        print(dirpath)
        fpic0095ent1.delete(0,tkinter.END)
        fpic0095ent1.insert(tkinter.END, dirpath)

    stop = True
    def _pystoptrain_mini_yolo(*a):
        nonlocal stop
        print(stop)
        stop = True

    def _pytrain_mini_yolo(*a):
        nonlocal train_data, class_types
        if train_data is None:
            print('没有加载训练数据。')
            return
        print('importing pytorch, opencv.')
        try:
            from . import pymini_yolo
        except:
            import pymini_yolo
        print('import ok.')
        nonlocal stop
        if stop == True:
            stop = False
        else:
            print('正在训练')
            return 
        def train(train_data, anchors, class_types):
            nonlocal stop
            train_loader = pymini_yolo.Data.DataLoader(
                dataset    = train_data,
                batch_size = BATCH_SIZE,
                shuffle    = True,
            )
            modelfilepath = os.path.join(fpic0094ent1.get().strip(), 'net.pkl')
            try:
                state = pymini_yolo.torch.load(modelfilepath)
                net = pymini_yolo.Mini(anchors, class_types)
                net.load_state_dict(state['net'])
                net.to(pymini_yolo.DEVICE)
                optimizer = state['optimizer']
                epoch = state['epoch']
                print('load train.')
            except:
                excp = traceback.format_exc()
                if 'FileNotFoundError' not in excp:
                    print(excp)
                net = pymini_yolo.Mini(anchors, class_types)
                net.to(pymini_yolo.DEVICE)
                optimizer = pymini_yolo.torch.optim.Adam(net.parameters(), lr=LR)
                epoch = 0
                print('new train.')
            yloss = pymini_yolo.yoloLoss(13, anchors=anchors, class_types=class_types, )
            net.train()
            for epoch in range(epoch, epoch+EPOCH):
                print('epoch', epoch)
                for step, (x_true_, y_true_) in enumerate(train_loader):
                    print('[{:<3}]'.format(step), end='')
                    x_true = pymini_yolo.Variable(x_true_).to(pymini_yolo.DEVICE)
                    y_true = pymini_yolo.Variable(y_true_).to(pymini_yolo.DEVICE)
                    output = net(x_true)
                    loss = yloss(output, y_true, print)
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    if stop: break
                    fpictxt.see(tkinter.END)
                if stop: break
                state = {'net':net.state_dict(), 'optimizer':optimizer, 'epoch':epoch+1, 
                         'anchors':anchors, 'class_types':class_types}
                pymini_yolo.torch.save(state, modelfilepath)
                print('save.')
            print('end.')
        try:
            EPOCH = int(fpic0092ent1.get().strip())
            BATCH_SIZE = int(fpic0092ent2.get().strip())
            LR = float(fpic0092ent3.get().strip())
            anchors = eval(fpic0092ent4.get().strip())
            print('EPOCH:{}, BATCH_SIZE:{}, LR:{}, anchors:{}.'.format(EPOCH,BATCH_SIZE,LR,anchors))
            threading.Thread(target=train, args=(train_data, anchors, class_types)).start()
        except:
            print(traceback.format_exc())

    def _test_mini_yolo_data(*a):
        filepath = fpic0095ent1.get().strip()
        if not os.path.isdir(filepath):
            print('无效的测试数据地址。')
            return
        # if re.findall('[\u4e00-\u9fa5]', filepath):
        #     print('无效的测试数据地址，opencv 加载图片地址不能含有中文。')
        #     return
        try:
            try:
                from . import pymini_yolo
            except:
                import pymini_yolo
            modelfilepath = os.path.join(fpic0094ent1.get().strip(), 'net.pkl')
            if not os.path.isfile(modelfilepath):
                print('模型文件不存在 {}'.format(modelfilepath))
                return
            state = pymini_yolo.load_net(modelfilepath)
            idx = 0
            for file in os.listdir(filepath):
                if file.lower().endswith('jpg') or file.lower().endswith('png') or file.lower().endswith('jpeg'):
                    _file = os.path.join(filepath, file)
                    pymini_yolo.get_all_draw_rects(_file, state)
                    idx += 1
                    if idx == 5:
                        return 
        except:
            print(traceback.format_exc())

    def _create_use_mini_yolo_code(*a):
        zstring = (
            'rRlrj9vG8bt+BWF/EHlH8SRKd7CFqoDPPidG/Qhspw8oB2KPXEm0+SpJnUinAdw0jX1oHCdFkziO0zYt8igQOylcF2lsJz+mlu7yyX+hM7t86+6cM3qGSO7s'
            'vHdmdnZ9WJg+ujq9+e6Tb98WvDgcuU67dlh48t3HOw/eR4Dr66Onj24/fXR9eu/W9uN3Z1vfTe9t7fz997P3/zN9dPPpo62E/vH323/6Ynvr+uzOl0+++VZg'
            'hI2W0lGaDd1rr7CH3ZiYjkZsY6WjTEZWLsj1qKNvghwBBHmmJ5hOEBLLSiYauuuEvrnR4Br2em3g21JayyD+hztXdz77LRcfmINw+tF309/d3L73wez+e/+9'
            '+vps6+qTh5/O7n8xe+MmV5zrCFM1kL/90b9mb3862/p855O3pjfuT29+NXvwh52v3qvVTNtz/VDQN9X00xnbXiyQQHC8FMSsLA0Ux2EoTsbBDdIvm4Sj2sB3'
            'bUF3LYvqoek6gZBMnvMN6lPjhKmHtdrLF9a04y+fOCb0hIv+mArmIOGujw2imIFGNolpkQ2LipJArYAKJwk8ayfWfn7q+BpQ1RGxjnQZK4ZW171xHQ2ffv3m'
            '9sObO99fEzaIfnnDdaiwffuN7b/844dbD2bvfT27cW/n8ZezG3+bXX9n+vE7s79em/7xren1N7f/+XD6zo3p3Q9qBh0IHvEDqsWaB4qLMT5lgTj6yPUDWdAt'
            'EgRaGHsUBmZgmUHYY1rKQjjyaTByLaPXVFRZcGzAy0FStybAn05NcJIDxiwvwlss8JMYQmAObdc0AMEi9oZBhKjbWhJbi+hmhUae2Igkjmk6AzcAvP46Gw5c'
            'XzCNCMCCT5whFZF9oreUSGdkufdyIP4R4MXM7Xdl/NdZBHYLicLrCvhYlBSDhkQfwQeLG1HKOOBCHIjfnpyYIaZsoiUUJqlPQiqSfnNdKgtAxEuX5EtlRLOC'
            'lblKIR7knSGKwBzIQBk5cbZ4Sar4NIDghdVnQ1m4TONeshpmt2H22+scG6NlSEMtiqNY060rGmQ0oymoMCQe8Ou0VpaYL5RgRDzab61nCJEcM12AFhCROqdF'
            '0oLTsgmsHMREfJ5AqR3c3U0ZeQ69xc567lWcAUWfRdLswkOt0k1G2VpmmGqXSSgjghPmMZcRcz7c158dkrnSydezorCscfL1o4m49unnwSN+Xt0DKnpgFfdW'
            'LsLYSYtGHjgRlLCYzXjiwHJJKKe65rQ+IPmIJOqRsChE0gIEsQyjGEYxG+W4E8Ad7cJwMpLmkbB++RNpISlLfYjtdchrmU+MKhOFJMHkghcURSi4YlUWzEq5'
            'tCgCPD8SGiB3Sc3AWgJeLINjNBSsBexRETsBL5bBjqcEkPCebzqh67GtTgQVdDOAzx5Ufct06MQ0wlFPbTZlIRh7MB0EPdzwpGcHvOUOsYgEe6QpL6Q8sw8e'
            'ngdhvifbAhNwRghbTeC5Aew2CRziBOwGT7SkckmHIoqFulABytqBT3CVFdMxaARLHIk4lCSh1ysS9YHP+nyF53kBc3MzGz4ll/NQpOHYd4R+BDEexzJEBfzi'
            'ddzYr8hYV+XMwqzEw07Od4LyLuq4Id8vuilXNspQkNR0xyLuDsdkfK5WtiYStWQSwy9S4a2CAQy3hLMBOBuAswE4GxnOagnHNh0wA548syMRGQOhJPMRkAvA'
            'o1xOYCZi84zIhF4BJUSqJPNRrCKRWiaCsIdchucokYRcGlx+MxGHLBEUI6hsLywFdn8oqgE6SgsopkGqqiHeKuKBOo0NhgeaNOZMQLxTbNMMJwuoVGk2WRSG'
            'tCQy2YuMc4OBpGJMFPoobiZvA9i73+02CqVoMjItmix8SZ4+9v2URvFcr1K+IWKYIOIY8IvFPsaGz6ofUmJ7I/y03DWyvPFZRweU1faHyYRGwHTGtGp41uwg'
            'a6ka/YhQS3TiPWzOeRM9Md/USLwtQ124c5AUGiFQOVO3tKGXDOnutjCYVpv71asEb7M2P51M7dp8BejKWo3VDOGM6Zii4yhnXGNs0bQJZ1PHXWdz9ezcJP5h'
            '6moakIaaJgbUGsAamQ7Wh3GI7aDvUEsLzCu014YaD4c4g/YgxzxiGKYz7J2Fg0dlsWAjoD6U04xrZW/nlAJucWKBP2xLLUlYWhLUtOKkmOzgkwzKkkBdBXyB'
            'Cwm2oZUqxMGu6qfKZ6pDypsk4CcaaZ7thsM0BLarJNRHZ13fRt6Mre3a1AnHNpx+mq1daH1qjTntaSjI8Xl6+mWxqbSwmngW0Wlli8QlgJCbEN9IViCSusJu'
            '8ZFxFxMdxcwFYpQ29rus6B5nOoBSBxzUaxeWcJ/lY8Jc7NCxPSmcuRbE+Z63Qma7BrW4Uy7QX4/BfyaxxJKRhRO02J/Lf7HOo1hr1uWEZxLWmR2y0FYlSd6F'
            '9CXXtTihgBqcIRFCYEGh8u9BkkhrVaW1gaRzZB8xrecRo1bFdI7IwkpnHzHq84hpV8WsdGThSHMfMe3nEdOpijkCjdLRlX3EdJ5HzHJVzNEVaMaa+xCtnT3B'
            'BOXVAtDlQmCzZq5MXTgh5gk2l6/Vep0HPWSmAillj+HE3pRVuS1DzWDXL4ZPJtBRh6JpQznCL1kIaRSmtXtTVRBInKFFOU449uATgf0uHF1LALWLADBIVpeb'
            'cgt7FNabMl7YA2Kbn1BmdoCMU/bwmGFcBLmJDPiC1pAOUBvX44DjruX6PdbvLi/zBgjBF3BjUJsF89n12EunTqfXYqdsMoSiy14nwN7k8yTs5vkeag9BNwZX'
            'kJ74PolFNF/f5JK5Zgg5fu70ufPa6gvn1fMvrBaKDPoyZYJyFHwgWbE1d0I0M0VDHaCtH1MsWKJwCOeXAtMOxo4Shvqh3EQ4tTm6yza8Q+Nw0DhyqCxYQURR'
            'zHwmpV7MXCcz6b1Uhbk+pWQsnDZIwJ2ABhQNB6NVMD65wuEu9mna4fjgPzhUEMsS6/1Xxh3abDZeGR8dkOX1eim0cq/vGQAYMY2WyiOKBxVo0lIl4bAw/ez1'
            '2Z/vTO/emt754sk3d2fvX5te/5Bf4e58/+H25zf45fL2w1vT6//G2bsf7NLZoFXeOKwKFiM5Tmw+ee7sRe3FtfMXXlz7lXbh1JmXTq/9EoJP6VS14v5Izyb2'
            'sJbeV4ErNFwhDSM/EAfQ0DrEZt0ACdPOxaEYEwzSr8OgzvMj2d3yqQSQTBc2uxylAEzQHC9ztGLaBoU4orjCGOioTkEnA+l6MDeGDv8I2NVIDBtRczgC17Dj'
            'NjuOAs/kfi3N5qKcQiTtkTiwiP1YjmR9nhgaWQj5lFTstKCowiPJNQbWqkfiFFmVWzLsJshdxzsxzp1fMCMNDUV+Hj+JdxoXqROkSmqSMnYCaAwoyG5KSuiK'
            '/DI8kYs9Xvm6WvsR99XYaD3rulrpJNFTuWDGA8Bmsa5jeZ4/O+M5aP76h63UEvMdXzz8LvHC4xCv2+v8XCcm0AV/IsnZWGXjMmUroWyXKFuAOSpQttk4p0zP'
            'Sf29LEk2usNCkrdbV2d3tqb3bj95fGP79huzT96slcrGc0dz5l3/gN7lonfbNeuvvvabV7s/UdTBa3UF+NskxDsVvGlO4ocrDEs+EeshDUKoh9nmgHMTYoY/'
            'o7HYzEEGoPlufMyyfgFF1Z0EYrJvQ+waGsZyamxSR0I/7uKb1YLs6gmxC26xiadZrk7wRq3HMQy6aeq0HO800qkXdvfjJf0/qxQrgewIuVtCSSkS00BjbDQD'
            'G/Vi1cyx8uzNQHQT+v3kP34KNLwqFMs3m/0f'
            )

        # len(zstring): 3684
        import base64, zlib
        zstring = base64.b64decode(zstring)
        zstring = zlib.decompress(zstring,-15)
        string = zstring.decode("utf-8")
        testpath = fpic0095ent1.get().strip()
        if not testpath:
            print('没有指定测试文件路径。')
            return 
        testpath = repr(testpath)
        code = string+'''

if __name__ == '__main__':
    state = load_net('net.pkl')
    for i in os.listdir({}):
        if i.endswith('jpg'):
            print(i)
            get_all_draw_rects(os.path.join({}, i), state)
'''.format(testpath, testpath)
        name = askstring('脚本名','请输入脚本文件名，尽量小写无空格。\n(存放到桌面)')
        if not name: return
        if not name.endswith('.py'): name += '.py'
        desktop_script = os.path.join(os.path.expanduser("~"),'Desktop\\{}'.format(name))
        if not os.path.isfile(desktop_script):
            with open(desktop_script, 'w', encoding='utf-8') as f:
                f.write(code)
        else:
            tkinter.messagebox.showwarning('脚本已存在','脚本已存在')

    Button(fpic0093, text='加载数据',command=_load_voc_data,width=16).pack(side=tkinter.RIGHT)
    Button(fpic0094, text='开始训练',command=_pytrain_mini_yolo,width=16).pack(side=tkinter.RIGHT)
    Button(fpic0095, text='停止训练',command=_pystoptrain_mini_yolo,width=16).pack(side=tkinter.RIGHT)
    Button(fpic0096, text='测试数据(前五张)',command=_test_mini_yolo_data,width=16).pack(side=tkinter.RIGHT)
    Button(fpic0097, text='生成使用代码',command=_create_use_mini_yolo_code,width=16).pack(side=tkinter.RIGHT)

    Button(fpic0092, text='[算法]',command=_pymini_yolo_code,width=5).pack(side=tkinter.LEFT)
    # Label(fpic0093, text='voc数据集地址').pack(side=tkinter.LEFT)
    Button(fpic0093, text='[打开文件] voc数据集地址: ',command=_set_train_file_dir).pack(side=tkinter.LEFT)
    fpic009ent1 = Entry(fpic0093,width=40)
    fpic009ent1.pack(side=tkinter.RIGHT)
    desktoppath = os.path.join(os.path.expanduser("~"),'Desktop')
    Button(fpic0094, text='[打开文件] 模型存放地址: ',command=_save_train_model_dir).pack(side=tkinter.LEFT)
    fpic0094ent1 = Entry(fpic0094,width=40)
    fpic0094ent1.insert(tkinter.END, desktoppath)
    fpic0094ent1.pack(side=tkinter.RIGHT)
    Button(fpic0095, text='[打开文件] 测试数据(默认测5张): ',command=_save_test_model_dir).pack(side=tkinter.LEFT)
    fpic0095ent1 = Entry(fpic0095,width=40)
    fpic0095ent1.pack(side=tkinter.RIGHT)

    Label(fpic0092, text='EPOCH').pack(side=tkinter.LEFT)
    fpic0092ent1 = Entry(fpic0092,width=5)
    fpic0092ent1.pack(side=tkinter.LEFT)
    fpic0092ent1.insert(tkinter.END, '1000')
    Label(fpic0092, text='BATCH_SIZE').pack(side=tkinter.LEFT)
    fpic0092ent2 = Entry(fpic0092,width=4)
    fpic0092ent2.pack(side=tkinter.LEFT)
    fpic0092ent2.insert(tkinter.END, '4')
    Label(fpic0092, text='LR').pack(side=tkinter.LEFT)
    fpic0092ent3 = Entry(fpic0092,width=7)
    fpic0092ent3.pack(side=tkinter.LEFT)
    fpic0092ent3.insert(tkinter.END, '0.001')
    Label(fpic0092, text='anchors').pack(side=tkinter.LEFT)
    fpic0092ent4 = Entry(fpic0092,width=20)
    fpic0092ent4.pack(side=tkinter.LEFT)
    fpic0092ent4.insert(tkinter.END, '[[60, 60]]')


    # Label(fpic0093, text=' 背景图片，不填则默认桌面').pack(side=tkinter.LEFT)
    return fr # 开发时注意将该处放在该函数的最后部分





if __name__ == '__main__':
    # test frame
    fr = encode_window()
    fr.title('命令行输入 vv e 则可快速打开便捷加密窗口')
    sys.stdout = __org_stdout__
    fr.protocol("WM_DELETE_WINDOW",lambda *a:fr.master.quit())
    fr.master.withdraw()
    fr.mainloop()