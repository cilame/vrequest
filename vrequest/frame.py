
import requests

import os
import re
import sys
import json
import shutil
import tempfile
import traceback
import tkinter
import inspect
import urllib.parse as ps
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.font import Font

from .root import DEFAULTS_HEADERS

Text = scrolledtext.ScrolledText
#Text = tkinter.Text
Label = ttk.Label
Button = ttk.Button
Combobox = ttk.Combobox

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

    temp_fr0 = Frame(fr)
    methods = ('GET','POST')
    cbx = Combobox(temp_fr0,width=10,state='readonly')
    cbx['values'] = methods     # 设置下拉列表的值
    cbx.current(0)
    cbx.pack(side=tkinter.RIGHT)
    cbx.bind('<<ComboboxSelected>>', change_method)
    temp_fr0.pack(fill=tkinter.X)


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
'''

    doc1 = '''纯文字内容解析
若在此生成代码，将自动添加解析函数的代码
<normal_content://html>
'''

    doc2 = '''根据字符串自动解析 xpath 路径
一般用于列表形式的路径
冒号后面配置需要处理的字符串
多个字符串可以通过空格分隔
eg.:
    <auto_list_xpath:白天 黑夜>
不写则为查找所有 "string(.)" (xpath语法)
能解析出含有非空字符串的内容路径
'''

    doc3 = '''简单分析json数据内容
找出最长的list进行初步的迭代分析
<auto_list_json:>
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

    fr = Frame()
    ft = Font(family='Consolas',size=10)

    temp_fr0 = Frame(fr)
    methods = ('(Alt+x) 列表路径解析说明','(Alt+d) 纯文字内容说明','(Alt+f) 用内容查找路径说明','(Alt+z) 用内容解析数据说明')
    cbx = Combobox(temp_fr0,width=22,state='readonly')
    cbx['values'] = methods     # 设置下拉列表的值
    cbx.current(0)
    cbx.pack(side=tkinter.RIGHT)
    cbx.bind('<<ComboboxSelected>>', document)
    temp_fr0.pack(fill=tkinter.X)

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
    temp_fold_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.LEFT)
    temp_fr1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)

    temp_fr2 = Frame(fr,highlightthickness=lin)
    lb4 = Label (temp_fr2,text='解析内容')
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


    # 简单处理数据的格式
    def format_content(content):
        if type(content) is str:
            return content
        elif type(content) is bytes:
            try:
                content = content.decode('utf-8')
                typ = 'utf-8'
            except:
                content = content.decode('gbk')
                typ = 'gbk'
            insert_txt(tx3, '解析格式：{}'.format(typ))
            return content
        else:
            raise TypeError('type:{} is not in [str,bytes]'.format(type(content)))

    def quote_val(url):
        import urllib
        for i in re.findall('=([^=&]+)',url):
            url = url.replace(i,'{}'.format(urllib.parse.quote(i)))
        return url

    if setting is not None:
        method  = setting.get('method')
        url     = setting.get('url')
        headers = setting.get('headers')
        body    = setting.get('body')
        try:
            if method == 'GET':
                s = requests.get(quote_val(ps.unquote(url)),headers=headers)
                insert_txt(tx1, format_content(s.content))
            elif method == 'POST':
                # 这里的post 里面的body 暂时还没有进行处理
                s = requests.post(quote_val(ps.unquote(url)),headers=headers,data=body)
                insert_txt(tx1, format_content(s.content))
        except:
            insert_txt(tx1, format_content(traceback.format_exc()))
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
                if _text_.startswith('Traceback (most recent call last):'):
                    self.logtx.tag_add('tag1',self.predk[self.logtx],tkinter.END)
                    self.logtx.tag_config('tag1',foreground='red')
                else:
                    self.predk[self.logtx] = self.logtx.index('insert')

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
    tx = Text(fr,height=1,width=1,font=ft)
    cs = setting.get('code_string')
    if cs:
        tx.delete(0.,tkinter.END)
        tx.insert(0.,cs)
    tx.pack(fill=tkinter.BOTH,expand=True,padx=pdx,pady=pdy)

    # TODO
    # 生成一个代码输出窗口，并且这里的代码执行需要考虑实时输出
    # 不能等全部的输出结果都输出完毕再进行写入操作，那样非常傻逼
    # 这里考虑使用 Ctrl+v 的方式来实现代码的执行，不爽再改
    temp_fr2 = Frame(fr,highlightthickness=lin)
    lb = Label (temp_fr2,text='代码执行')
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
        p.stdout.close()
        p.wait()
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


# 帮助文档
def helper_window():
    fr = Frame()
    ft = Font(family='Consolas',size=10)
    hp = '''

vrequest：
基于 requests 和 lxml 库
用于快速发起请求，快速生成测试代码的工具

请求窗口快捷键：
(Ctrl + q) 创建新的请求标签
(Ctrl + r) 发送请求任务并保存
*(Alt + c) 生成请求代码(该窗口下该功能不常用)

响应窗口快捷键：
*(Alt + r) 打开一个空的响应标签(不常用)
(Alt + f) 智能解析列表路径
(Alt + x) <代码过程> 使用 xpath 解析
(Alt + z) <代码过程> 智能提取 json 数据
(Alt + d) <代码过程> 获取纯文字内容
(Alt + c) 生成请求代码，有<代码过程>则生成代码中包含过程代码
(Esc)     开启/关闭 response 解析窗口

代码窗口快捷键：
(Alt + v) 代码执行
(Esc)     开启/关闭 代码执行结果窗口

通用快捷键：
(Ctrl + e) 修改当前标签名字
(Ctrl + w) 关闭当前标签
(Ctrl + h) 创建帮助标签
(Ctrl + s) 保存当前全部请求配置(只能保存请求配置)

开源代码：
https://github.com/cilame/vrequest
'''
    temp_fr1 = Frame(fr,highlightthickness=lin)
    lb1 = ttk.Label(temp_fr1,font=ft,text=hp)
    lb1.pack()
    temp_fr1.pack()

    return fr