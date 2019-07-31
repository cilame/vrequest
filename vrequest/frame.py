
import requests

import io
import os
import re
import sys
import json
import zlib
import time
import hmac
import shutil
import base64
import hashlib
import tempfile
import traceback
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


    def send_req(*a):
        from .tab import send_request
        send_request()

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
    lab1 = Label(temp_fr0, text='请尽量发送请求后生成代码，那样会有更多功能：')
    lab1.pack(side=tkinter.LEFT)
    btn6 = Button(temp_fr0, text='生成[requests]代码[Alt+c]', command=test_code)
    btn6.pack(side=tkinter.LEFT)
    btn7 = Button(temp_fr0, text='生成[scrapy]代码[Alt+s]', command=scrapy_code)
    btn7.pack(side=tkinter.LEFT)

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
    else:
        tx2.insert(0.,DEFAULTS_HEADERS.strip())

    frame_setting[fr] = {}
    frame_setting[fr]['type'] = 'request'
    frame_setting[fr]['fr_method'] = cbx
    frame_setting[fr]['fr_url'] = tx1
    frame_setting[fr]['fr_headers'] = tx2
    frame_setting[fr]['fr_body'] = tx3
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
        fr_txt.delete(0.,tkinter.END)
        fr_txt.insert(0.,re.sub('[\uD800-\uDBFF][\uDC00-\uDFFF]|[\U00010000-\U0010ffff]','',txt))

    doc0 = '''列表解析路径方式
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
所以一些比较复杂的网页或许还是需要考虑自省分析xpath。

冒号后面配置需要处理的字符串
多个字符串可以通过空格分隔
eg.:
    <auto_list_xpath:白天 黑夜>
不写则为查找所有 "string(.)" (xpath语法)
能解析出含有非空字符串的内容路径
'''

    doc3 = '''简单分析json数据内容
找出最长的list进行初步的迭代分析，并给出分析结果在输出框
<auto_list_json:>
'''

    doc4 = '''生成scrapy代码
如果存在 “解析xpath”、“自动json” 或 “获取纯文字” 状态
则会在生成代码中包含相应的代码
'''

    doc5 = '''生成requests代码
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

    def test_code(*a):
        from .tab import create_test_code
        create_test_code()

    def scrapy_code(*a):
        from .tab import create_scrapy_code
        create_scrapy_code()

    temp_fr0 = Frame(fr)
    lab1 = Label(temp_fr0, text='功能说明：')
    lab1.pack(side=tkinter.LEFT)
    methods = ('(Alt+x) 解析xpath','(Alt+d) 获取纯文字','(Alt+f) 分析xpath','(Alt+z) 自动json', '(Alt+s) 生成 scrapy代码', '(Alt+c) 生成 requests代码')
    cbx = Combobox(temp_fr0,width=18,state='readonly')
    cbx['values'] = methods     # 设置下拉列表的值
    cbx.current(0)
    cbx.pack(side=tkinter.LEFT)
    cbx.bind('<<ComboboxSelected>>', document)
    temp_fr0.pack(fill=tkinter.X)
    btn3 = Button(temp_fr0, text='分析xpath', command=auto_xpath)
    btn3.pack(side=tkinter.LEFT)
    btn4 = Button(temp_fr0, text='解析xpath', command=xpath_elements)
    btn4.pack(side=tkinter.LEFT)
    btn2 = Button(temp_fr0, text='获取纯文字', command=html_pure_text)
    btn2.pack(side=tkinter.LEFT)
    btn5 = Button(temp_fr0, text='自动json', command=auto_json)
    btn5.pack(side=tkinter.LEFT)
    btn1 = Button(temp_fr0, text='显示/隐藏配置', command=switch_show)
    btn1.pack(side=tkinter.RIGHT)
    btn6 = Button(temp_fr0, text='生成[requests]代码', command=test_code)
    btn6.pack(side=tkinter.RIGHT)
    btn7 = Button(temp_fr0, text='生成[scrapy]代码', command=scrapy_code)
    btn7.pack(side=tkinter.RIGHT)

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

    # 检查数据格式
    # 非常坑，后续再考虑，现在只考虑 ['utf-8','gbk'] 两种
    # def parse_content_type(content, types=['utf-8','gbk']):
    #     itype = iter(types)
    #     while True:
    #         try:
    #             tp = next(itype)
    #             content = content.decode(tp)
    #             return tp, content
    #         except StopIteration:
    #             try:
    #                 import chardet
    #                 tp = chardet.detect(content)['encoding']
    #                 types.append(tp)
    #                 content = content.decode(tp)
    #                 return tp, content
    #             except:
    #                 raise TypeError('not in {}'.format(types))
    #         except:
    #             continue

    # 统一数据格式
    def format_content(content):
        if type(content) is bytes:
            try:
                content = content.decode('utf-8')
                typ = 'utf-8'
            except:
                try:
                    content = content.decode('gbk')
                    typ = 'gbk'
                except:
                    content = content.decode('utf-8',errors='ignore')
                    typ = 'utf-8 ignore'
            insert_txt(tx3, '解析格式：{}'.format(typ))
            return typ,content
        else:
            einfo = 'type:{} is not in type:[bytes]'.format(type(content))
            raise TypeError(einfo)

    def quote_val(url):
        import urllib
        for i in re.findall('=([^=&]+)',url):
            url = url.replace(i,'{}'.format(urllib.parse.quote(i)))
        return url

    tp = None
    if setting is not None:
        method  = setting.get('method')
        url     = setting.get('url')
        headers = setting.get('headers')
        body    = setting.get('body')
        try:
            if method == 'GET':
                s = requests.get(quote_val(ps.unquote(url)),headers=headers,verify=False)
                tp,content = format_content(s.content)
                insert_txt(tx1, content)
            elif method == 'POST':
                # 这里的post 里面的body 暂时还没有进行处理
                s = requests.post(quote_val(ps.unquote(url)),headers=headers,data=body,verify=False)
                tp,content = format_content(s.content)
                insert_txt(tx1, content)
        except:
            einfo = traceback.format_exc()
            tkinter.messagebox.showinfo('Error',einfo)
            raise
            # insert_txt(tx1, traceback.format_exc())

    frame_setting[fr]['fr_parse_type'] = tp
    return fr




# 暂时考虑用下面的方式来试着挂钩函数执行的状态。
# 不过似乎还是有些漏洞，先就这样，后面再补充完整。
import sys
__org_stdout__ = sys.stdout
__org_stderr__ = sys.stderr
class stdhooker:
    def __init__(self, hook=None, style=None):
        if hook.lower() == 'stdout':
            self.__org_func__ = __org_stdout__
        elif hook.lower() == 'stderr':
            self.__org_func__ = __org_stderr__
        else:
            raise 'stdhooker init error'
        self.cache = ''
        self.style = style
        self.predk = {}

    def write(self,text):
        self.logtx = get_tx()
        if self.logtx not in self.predk:
            self.predk[self.logtx] = 0

        self.cache += text
        if '\n' in self.cache:
            _text = self.cache.rsplit('\n',1)
            self.cache = '' if len(_text) == 1 else _text[1]
            _text_ = _text[0] + '\n'
            if self.logtx:
                self.logtx.insert(tkinter.END, _text_)
                self.logtx.see(tkinter.END)
                self.logtx.update()

    def flush(self):
        self.__org_func__.flush()

def get_tx():
    for i in inspect.stack():
        if '__very_unique_cd__' in i[0].f_locals:
            return i[0].f_locals['cd']

sys.stdout = stdhooker('stdout',style='normal')



# 生成代码临时放在这里
def code_window(setting=None):
    fr = Frame()
    ft = Font(family='Consolas',size=10)

    def _execute_code(*a):
        from .tab import execute_code
        execute_code()

    btn1 = Button(fr, text='执行代码 [Alt+v]', command=_execute_code)
    btn1.pack(side=tkinter.TOP)
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

    def execute_func():
        __very_unique_cd__ = None
        nonlocal cd
        cd.delete(0.,tkinter.END)
        td = tempfile.mkdtemp()
        tf = os.path.join(td,'temp.py')
        cs = tx.get(0.,tkinter.END)
        with open(tf,'w',encoding='utf-8') as f:
            f.write(cs)
        s = sys.executable
        s = s + ' ' + tf
        import subprocess
        p = subprocess.Popen(s, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, encoding='utf-8')
        print('============================== start ==============================')
        for line in iter(p.stdout.readline, ''):
            if line:
                print(line, end='')
            else:
                break
        print('==============================  end  ==============================')
        p.wait()
        p.stdout.close()
        shutil.rmtree(td)

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


# 生成代码临时放在这里
def scrapy_code_window(setting=None):
    fr = Frame()
    ft = Font(family='Consolas',size=10)

    def _execute_scrapy_code(*a):
        from .tab import execute_scrapy_code
        execute_scrapy_code()

    def save_project_in_desktop(*a):
        name = askstring('项目名称','请输入项目名称，尽量小写无空格。')
        if not name: return
        desktop = os.path.join(os.path.expanduser("~"),'Desktop\\{}'.format(name))
        if not os.path.isdir(desktop):
            with open(script,'w',encoding='utf-8') as f:
                f.write(tx.get(0.,tkinter.END))
            shutil.copytree(scrapypath, desktop)
            if hva.get():
                with open(desktop + '\\v\\spiders\\v.py','a',encoding='utf-8') as f:
                    f.write('\n'*10 + post_verification_model)
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
                    os.system(cmd)
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

    home = os.environ.get('HOME')
    home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
    filename = '.vscrapy'
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


    def pprint(*a):
        __org_stdout__.write(str(a)+'\n')
        __org_stdout__.flush()
    temp_fr0 = Frame(fr)
    va = tkinter.IntVar()
    rb = Checkbutton(temp_fr0,text='本地执行是否收集数据:',variable=va,command=local_collection)
    rb.deselect()
    et = Entry (temp_fr0,width=60)
    
    ltime = '%04d%02d%02d-%02d%02d%02d' % time.localtime()[:6]
    dtopfile = os.path.join('file:///' + os.path.expanduser("~"),'Desktop\\v{}.json'.format(ltime))
    et.insert(0,dtopfile)
    bt2 = Button(temp_fr0,text='拷贝项目文件到桌面',command=save_project_in_desktop)
    bt2.pack(side=tkinter.LEFT)
    btn1 = Button(temp_fr0, text='执行本地代码 [Alt+w]', command=_execute_scrapy_code)
    btn1.pack(side=tkinter.LEFT)
    hva = tkinter.IntVar()
    hrb = Checkbutton(temp_fr0,text='拷贝项目增加后验证模板',variable=hva)
    hrb.deselect()
    hrb.pack(side=tkinter.LEFT)
    cbx = Combobox(temp_fr0,width=10,state='readonly')
    cbx['values'] = ('DEBUG','INFO','WARNING','ERROR','CRITICAL')
    cbx.current(1)
    cbx.pack(side=tkinter.RIGHT)
    lab1 = Label(temp_fr0, text='本地日志等级:')
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

    def execute_func():
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
                    os.system(cmd)
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
    frame_setting[fr] = {}
    frame_setting[fr]['type'] = 'scrapy'
    frame_setting[fr]['execute_func'] = execute_func
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

请求窗口快捷键：
(Ctrl + r) 发送请求任务并保存
*(Alt + c) 生成请求代码(一般建议在请求后处理分析再生成代码，那样包含解析代码)
           HEADERS 窗口接受 “:” 或 “=” 分割
           BODY    窗口接受 “:” 或 “=” 分割
                   若是BODY窗口需要传字符串可以在字符串前后加英文双引号
*(Alt + s) 生成 scrapy 请求代码，格式化结构同上

响应窗口快捷键：
*(Alt + r) 打开一个空的响应标签(不常用)
(Alt + f) 智能解析列表路径，解析后使用 xpath 解析功能会自动弹出解析选择窗
(Alt + x) <代码过程> 使用 xpath 解析
(Alt + z) <代码过程> 智能提取 json 数据
(Alt + d) <代码过程> 获取纯文字内容
(Alt + c) 生成请求代码，有<代码过程>则生成代码中包含过程代码 [在js代码窗同样适用]
(Alt + s) 生成 scrapy 请求代码，有<代码过程>则生成代码中包含过程代码
(Esc)     开启/关闭 response 解析窗口

代码窗口快捷键：
(Alt + v) 代码执行 [在js代码窗同样适用]
(Esc)     开启/关闭 代码执行结果窗口 [在js代码窗同样适用]

scrapy 代码窗口快捷键：
(Alt + w) scrapy 代码执行

通用快捷键：
(Ctrl + q) 创建新的请求标签
(Ctrl + j) 创建 js 代码执行窗口
(Ctrl + e) 修改当前标签名字
(Ctrl + w) 关闭当前标签
(Ctrl + h) 创建帮助标签
(Ctrl + s) 保存当前全部请求配置(只能保存请求配置)
(Alt  + `) 用IDLE固定打开一个文件,方便长脚本测试

开源代码：
https://github.com/cilame/vrequest
'''
    temp_fr1 = Frame(fr,highlightthickness=lin)

    def create_req_window(*a):
        from .tab import create_new_reqtab
        create_new_reqtab()

    btn = Button(fr,text='创建请求窗口/[右键创建请求窗口]', command=create_req_window)
    btn.pack()
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

    def exec_javascript(*a):
        __very_unique_cd__ = None
        nonlocal cd
        cd.delete(0.,tkinter.END)
        td = tempfile.mkdtemp()
        tf = os.path.join(td,'temp.py')
        cs = txt2.get(0.,tkinter.END)
        with open(tf,'w',encoding='utf-8') as f:
            f.write(cs)
        s = sys.executable
        s = s + ' ' + tf
        import subprocess
        p = subprocess.Popen(s, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, encoding='utf-8')
        print('============================== start ==============================')
        for line in iter(p.stdout.readline, ''):
            if line:
                print(line, end='')
            else:
                break
        print('==============================  end  ==============================')
        p.wait()
        p.stdout.close()
        shutil.rmtree(td)

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

    # 查看常用的js解析器的引入状态
    support_modules = ['js2py', 'execjs']
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
    btn2 = Button(temp_fr0, text='[执行代码] <Alt+v>', command=_exec_javascript)
    btn2.pack(side=tkinter.RIGHT)


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

var a = 123;
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



def encode_window(setting=None):
    '''
    处理简单的加密编码对比
    '''
    fr = tkinter.Toplevel()
    fr.title('命令行输入 vv e 则可快速打开便捷加密窗口, 组合快捷键 Alt+` 快速打开IDLE')
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
            if name == 'md2': continue
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
                    v = pymd2.md2(b'')
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

    def print(*a):
        # import pprint
        # pprint.pprint(enb_names)
        name = enb.select().rsplit('.')[-1]
        if enb_names[name] == 'hash':
            txt.insert(tkinter.END,' '.join(map(str,a)) + '\n')
        elif enb_names[name] == '纯py加解密':
            ftxt.insert(tkinter.END,' '.join(map(str,a)) + '\n')
        elif enb_names[name] == '依赖库加解密':
            ctxt.insert(tkinter.END,' '.join(map(str,a)) + '\n')
        elif enb_names[name] == '通用解密':
            bbtxt.insert(tkinter.END,' '.join(map(str,a)) + '\n')

    def _analysis_diff(*a):
        txt.delete(0.,tkinter.END)
        it = []
        for name,ge in list(dh.items()) + list(bs.items()):
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
import difflib

allow = \
$allow

salt = '$salt' # 字符串/byte类型  盐（默认空）
text = '$text' # 字符串/byte类型  需要被加密的数据
upper = True


def encode_all(salt, text):
    salt = salt.encode() if type(salt) == str else salt
    text = text.encode() if type(text) == str else text
    for name in allow:
        v = hmac.new(salt,text,name).hexdigest()
        v = v.upper() if upper else v.lower()
        print('{:<10}{}'.format(name, v))


def compare_encode(salt, text, compare_str):
    salt = salt.encode() if type(salt) == str else salt
    text = text.encode() if type(text) == str else text
    it = []
    for name in allow:
        v = hmac.new(salt,text,name).hexdigest()
        v = v.upper() if upper else v.lower()
        a, b = v, compare_str
        s = difflib.SequenceMatcher(None, a.upper(), b.upper())
        q = s.find_longest_match(0, len(a), 0, len(b))
        if q.size>0:
            it.append([name, a, b, q.size])
    # 因为这类加密的互异性很高，所以只获取前三个最长匹配的加密字符串对比查看
    p = '-'
    for name,a,b,max_match in sorted(it,key=lambda max_match:-max_match[3])[:3]:
        s = difflib.SequenceMatcher(None, a.upper(), b.upper())
        prefix = '[len:compare]:{:<5} {:<18}'.format(len(a), p + '[len:{}]:{}'.format(name, len(b)))
        p = '-' if p == '+' else '+'
        for match in sorted(s.get_matching_blocks(),key=lambda i:-i.size):
            if match.size:
                v = a[match.a:match.a+match.size]
                print('{} [match.size:{}]  {}'.format(prefix, match.size, v))


encode_all(salt, text)
compare_str = '$compare_str' # 需要被对比的字符串
compare_encode(salt, text, compare_str)
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





    basehp = '''
            通用加解密（请将需要加/解密的数据输入右侧窗口）
    base加密：
        [-] 这种类型只能对数字进行加解密
        [*] 这种类型能对一般数据流进行加解密
    注意：
        使用全部加解密时，请尽量不要使用超过一千的字符串
        否者entry窗口显示会有非常明显的卡顿
        如果需要长字符串的加解密，请使用单独的加解密按钮实现
        因为单独加解密统一使用右边的窗口输入和输出，不使用左边的 Entry组件
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
        'base_8',
        'base_10',
        'base_16',
        'quote',
        'escape',
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
        ctxt.delete(0.,tkinter.END)
        with open(pybase.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    def _pyplus_code(*a):
        try:
            from . import pyplus
        except:
            import pyplus
        ctxt.delete(0.,tkinter.END)
        with open(pyplus.__file__, encoding='utf-8') as f:
            data = f.read().strip('\n')
        print(data)

    def pack_button(name):
        def do():
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
                if name in html_quote:
                    plus_encode, plus_decode = pyplus.html_quote[name]
                    print(plus_encode(text, encd))
            except:
                import traceback
                print(traceback.format_exc())
        def undo():
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
    Button(f4,text='杂项代码',width=8,command=_pyplus_code).pack(side=tkinter.RIGHT)
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
    enb.add(_fr0, text='纯py加解密')
    enb.pack()
    enb_names[_fr0._name] = '纯py加解密'

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
    该处大部分算法均为从各个地方收集而来的纯 python 实现的加解密算法，
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
    f100 = Frame(ff0)
    f100.pack(side=tkinter.TOP,fill=tkinter.X)
    f101 = Frame(f100)
    f102 = Frame(f100)
    f101.pack(side=tkinter.TOP,fill=tkinter.X)
    f102.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(f101, text='     以下算法纯 python 解密 jsfuck。').pack(fill=tkinter.X,expand=True)
    def _jsfuck_decode(*a):
        data = ftxt.get(0.,tkinter.END).strip('\n')
        ftxt.delete(0.,tkinter.END)
        try:
            from . import pyjsfuck
        except:
            import pyjsfuck
        try:
            f = pyjsfuck.unjsfuck(data, debuglevel=1, logger=print)
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

    Button(f102, text='[算法]',command=_jsfuck_code,width=5).pack(side=tkinter.RIGHT)
    Button(f102, text='解密',command=_jsfuck_decode,width=5).pack(side=tkinter.RIGHT)






    bhashhelp = '''
            以下算法为使用本地的密码字典进行 hash 爆破。
    若想使用自己的字典，可以直接将字典内容粘贴到右侧窗口中，点击[自定义爆破]即可
    会自动使用选择的算法进行 hash 的对比。
    该算法会自动使用一定程度的黑客语(leetspeak)对密码进行膨胀处理，详细的处理请参考算法。
    另外，算法内还有名字前缀以及日期的组合，没有放在该功能中
    因为生成的字典会非常之大，爆破一次要花费好几十秒，
    所以如果有更详细的需求请直接点开算法，使用别的ide进行更丰富的爆破处理。
'''.strip('\n')
    # 这里是 twofish 算法的部分
    def fbx_change_cbit_1(*content):
        if content:
            blen = len(content[0])
            fbx_cbit1['text'] = str(blen)
            return True

    fbx_change_cbit1 = root.register(fbx_change_cbit_1)
    fbx100 = Frame(ff0)
    fbx100.pack(side=tkinter.TOP,fill=tkinter.X)
    fbx101 = Frame(fbx100)
    fbx102 = Frame(fbx100)
    fbx103 = Frame(fbx100)
    fbx101.pack(side=tkinter.TOP,fill=tkinter.X)
    fbx102.pack(side=tkinter.TOP,fill=tkinter.X)
    fbx103.pack(side=tkinter.TOP,fill=tkinter.X)
    Label(fbx101, text=bhashhelp).pack(fill=tkinter.X,expand=True)
    def _pymapmd5_decode(*a):
        _hash = fbxent.get().strip()
        _mode = fbx1_mode1.get()
        ftxt.delete(0.,tkinter.END)
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
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())

    def _inputdict_map(*a):
        _hash = fbxent.get().strip()
        _mode = fbx1_mode1.get()
        _list = ftxt.get(0.,tkinter.END).strip('\n').splitlines()
        ftxt.delete(0.,tkinter.END)
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
            ftxt.delete(0.,tkinter.END)
            print(traceback.format_exc())

    def _pymapmd5_code(*a):
        try:
            from . import pymapmd5
        except:
            import pymapmd5
        ftxt.delete(0.,tkinter.END)
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
    Button(fbx103, text='自定义爆破',command=_pymapmd5_decode,width=10).pack(side=tkinter.RIGHT)










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
    return fr







if __name__ == '__main__':
    # test frame
    fr = encode_window()
    fr.title('命令行输入 vv e 则可快速打开便捷加密窗口')
    sys.stdout = __org_stdout__
    fr.protocol("WM_DELETE_WINDOW",lambda *a:fr.master.quit())
    fr.master.withdraw()
    fr.mainloop()