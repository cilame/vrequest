from lxml import etree

import re
import os
import json
import shutil
import pprint
import traceback
import threading
import tkinter
import tkinter.messagebox
from tkinter import ttk
from tkinter.simpledialog import askstring

from .root import (
    root,
    config,
    save,
)
from .frame import (
    request_window,
    response_window,
    code_window,
    scrapy_code_window,
    helper_window,
    frame_setting,
    exec_js_window,
    encode_window,
    __org_stdout__,
)
from .util import (
    format_url,
    format_url_show,
    format_url_code,
    format_headers_str,
    format_headers_code,
    format_body_str,
    format_body_code,
    format_request,
    format_response,
    format_scrapy_request,
    format_scrapy_response,
    get_simple_path_tail,
    get_xpath_by_str,
    get_json_show,
    parse_json_content,
)

nb = ttk.Notebook(root)
nb.place(relx=0, rely=0, relwidth=1, relheight=1)
nb_names = {} 
'''
nb_names 的数据结构：
{
    tab_id1: 
        {
            'name':tab_name1,
            'setting':setting1,
        }, 
    tab_id2:
        {
            'name':tab_name2,
            'setting':setting2,
        }, 
}
setting 是一个字典，里面至少有一个 type字段描述什么类型。
'''


def bind_frame(frame, name=None):
    global config, nb_names
    frame.master = nb
    name = name if name is not None else frame._name
    v = set(nb.tabs())
    nb.add(frame, text=name)
    tab_id = (set(nb.tabs())^v).pop() # 由于没有接口，只能用这种方式来获取新增的 tab_id
    nb_names[tab_id] = {}
    nb_names[tab_id]['name'] = name
    nb_names[tab_id]['setting'] = frame_setting.pop(frame) if frame in frame_setting else {}
    return tab_id


cancel_limit = 30
cancel_list = []

def delete_curr_tab():
    _select = nb.select()
    cname = nb_names.get(_select)['name']
    if _select is not '':
        if len(nb.tabs()) == 1 and cname == '帮助':
            root.quit()
        elif len(nb.tabs()) == 1:
            nb.forget(_select)
            create_helper()
        else:
            nb.forget(_select)
        nb_names.pop(_select)
        if cname in config['set']:
            _set = config['set'].pop(cname)
            cancel_list.append((cname,_set))
            if len(cancel_list) > cancel_limit:
                cancel_list.pop(0)


def cancel_delete():
    if cancel_list:
        key,setting = cancel_list.pop()
        tab_id = bind_frame(request_window(setting),key)
        config['set'][key] = setting
        nb.select(tab_id)


def change_tab_name():
    name = askstring('修改标签','新的标签名字') # 简单弹窗请求字符串数据
    if name is not None:
        _select = nb.select()
        oname = nb_names[_select]['name']
        cname = name
        allname = [val['name'] for val in nb_names.values()]
        idx = 0
        while True:
            if cname in allname:
                idx += 1
                cname = '{}_{}'.format(name,idx)
            else:
                break
        # name不能重复，因为需要作为字典的key持久化
        nb_names[_select]['name'] = cname
        if oname in config['set']:
            config['set'][cname] = config['set'].pop(oname)
        nb.tab(_select, text=cname)



def create_new_tab(setting=None, prefix=None, window=None):
    nums = []
    for val in nb_names.values():
        v = re.findall('{}\d+'.format(prefix), val['name'])
        if val['name'] == prefix:
            nums.append(0)
        if v:
            num = int(re.findall('{}(\d+)'.format(prefix), v[0])[0])
            nums.append(num)
    idx = 0
    while True:
        if idx in nums:
            idx += 1
        else:
            retn = idx
            break
    name = '{}{}'.format(prefix, '' if retn==0 else retn)
    nb.select(bind_frame(window(setting),name))


def create_new_reqtab(setting=None, prefix='请求'):
    create_new_tab(setting, prefix, request_window)


def create_new_rsptab(setting=None, prefix='响应', reqname=None):
    fmt = '<{}>'
    prefix = prefix+fmt.format('空') if reqname is None else prefix+fmt.format(reqname)
    create_new_tab(setting, prefix, response_window)

def create_new_codetab(setting=None, prefix='代码', reqname=None):
    fmt = '<{}>'
    prefix = prefix+fmt.format('空') if reqname is None else prefix+fmt.format(reqname)
    create_new_tab(setting, prefix, code_window)

def create_new_scrapy_codetab(setting=None, prefix='scrapy', reqname=None):
    fmt = '<{}>'
    prefix = prefix+fmt.format('空') if reqname is None else prefix+fmt.format(reqname)
    create_new_tab(setting, prefix, scrapy_code_window)

def create_helper():
    nb.select(bind_frame(helper_window(),'帮助'))

def create_js_parse(setting=None, prefix='js执行窗'):
    create_new_tab(setting, prefix, exec_js_window)

def create_encoder(setting=None):
    encode_window()

def set_request_config(name,setting):
    method  = setting.get('fr_method').get()
    url     = setting.get('fr_url').get(0.,tkinter.END).strip()
    url     = format_url(url)
    headers = setting.get('fr_headers').get(0.,tkinter.END).strip()
    body    = setting.get('fr_body').get(0.,tkinter.END).strip()
    config['set'][name] = {}
    config['set'][name]['type'] = 'request'
    config['set'][name]['method'] = method
    config['set'][name]['url'] = url
    config['set'][name]['headers'] = headers
    config['set'][name]['body'] = body
    headers = format_headers_str(headers)
    body    = format_body_str(body)
    setting.get('fr_url').delete(0.,tkinter.END)
    setting.get('fr_url').insert(0.,format_url_show(url))
    return method,url,headers,body



def get_request_config(setting):
    method  = setting.get('fr_method').get()
    url     = setting.get('fr_url').get(0.,tkinter.END).strip()
    url     = format_url(url)
    headers = setting.get('fr_headers').get(0.,tkinter.END).strip()
    body    = setting.get('fr_body').get(0.,tkinter.END).strip()
    c_headers = format_headers_code(headers)
    c_url = format_url_code(url)
    c_body = format_body_code(body)
    return method,c_url,c_headers,c_body




def get_response_config(setting):
    tx1 = setting.get('fr_html_content')
    tx2 = setting.get('fr_local_set')
    tx3 = setting.get('fr_local_info')
    tx4 = setting.get('fr_parse_info')
    tps = setting.get('fr_parse_type')
    temp_fr2 = setting.get('fr_temp2')

    c_content = tx1.get(0.,tkinter.END).strip() # 配置，目前在解析json数据部分有用
    c_set = tx2.get(0.,tkinter.END).strip() # 配置，用来配置生成代码的方式

    r_setting = setting.get('fr_setting')
    if r_setting is not None:
        method    = r_setting.get('method')
        url       = r_setting.get('url')
        headers   = r_setting.get('headers')
        body      = r_setting.get('body')
        c_url     = format_url_code(url)
        c_headers = format_headers_code(headers)
        c_body    = format_body_code(body) if type(body) == dict else 'body = ' + json.dumps(body)
        r_setting = method,c_url,c_headers,c_body
    return r_setting,c_set,c_content,tps




@save
def send_request():
    global config
    _select = nb.select()
    name    = nb_names[_select]['name']
    setting = nb_names[_select]['setting']
    foc_tog = True
    if setting.get('type') == 'request':
        method,url,headers,body = set_request_config(name,setting)
        _setting = {}
        _setting['method'] = method
        _setting['url'] = url
        _setting['headers'] = headers
        _setting['body'] = body
        create_new_rsptab(_setting,reqname=name)
    else:
        foc_tog = False
    if foc_tog:
        config['focus'] = name



def save_config():
    toggle = tkinter.messagebox.askokcancel('是否保存','确定保存当前全部[请求配置]信息吗？')
    @save
    def _save_config():
        for tad_id in nb.tabs():
            name = nb_names[tad_id]['name']
            setting = nb_names[tad_id]['setting']
            if setting.get('type') == 'request':
                set_request_config(name,setting)
    if toggle: _save_config()


# 切换状态：显示/取消显示 response 窗口内的输出窗口
def switch_response_log(*a):
    _select = nb.select()
    setting = nb_names[_select]['setting']
    if setting.get('type') in ['response','code','js']:
        temp_fr2 = setting.get('fr_temp2')
        try:
            temp_fr2.pack_info()
            packed = True
        except:
            packed = False
        if packed:
            temp_fr2.pack_forget()
        else:
            temp_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.BOTTOM)



# 生成代码的函数
def create_test_code(*a):
    _select = nb.select()
    name    = nb_names[_select]['name']
    setting = nb_names[_select]['setting']
    code_string = None
    if setting.get('type') == 'request':
        method,c_url,c_headers,c_body = get_request_config(setting)
        code_string = format_request(method,c_url,c_headers,c_body)
    if setting.get('type') == 'response':
        r_setting,c_set,c_content,tps = get_response_config(setting)
        code_string = format_response(r_setting,c_set,c_content)
    if setting.get('type') == 'js':
        setting.get('execute_func0')()

    if code_string:
        setting = {}
        setting['code_string'] = code_string
        create_new_codetab(setting,reqname=name)


# 生成 scrapy 代码的函数 # 暂时还在开发中
def create_scrapy_code(*a):
    '''
    这里的处理可能会需要花上挺长的一段时间，需要考虑新的code_window的处理
    等明天有时间的时候去处理一下
    '''
    _select = nb.select()
    name    = nb_names[_select]['name']
    setting = nb_names[_select]['setting']
    home = os.environ.get('HOME')
    home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
    model_path = os.path.join(os.path.split(__file__)[0],'template')
    filename = '.vscrapy'
    scrapypath = os.path.join(home,filename)
    scriptpath = os.path.join(scrapypath, 'v/spiders/')
    if not os.path.isdir(scrapypath):
        shutil.copytree(model_path, scrapypath)
    elif not os.path.isdir(os.path.join(scrapypath,'v')):
        toggle = tkinter.messagebox.askokcancel('是否删除已有的、错误的配置文件夹',
                                                '存在错误的配置文件夹 {} 确定删除该文件夹内容重新创建吗？\n'
                                                '配置文件夹地址 {}'.format(filename, scrapypath))
        if toggle:
            shutil.rmtree(scrapypath)
            shutil.copytree(model_path, scrapypath)
        else: return
    code_string = None
    if setting.get('type') == 'request':
        method,c_url,c_headers,c_body = get_request_config(setting)
        code_string = format_scrapy_request(method,c_url,c_headers,c_body)
    if setting.get('type') == 'response':
        r_setting,c_set,c_content,tps = get_response_config(setting)
        code_string = format_scrapy_response(r_setting,c_set,c_content,tps)
    if code_string:
        setting = {}
        setting['code_string'] = code_string
        create_new_scrapy_codetab(setting,reqname=name)



# 获取HTML纯文本函数
def normal_content(content,
                   tags=['script','style','select','noscript'],
                   rootxpath='//html'):
    if type(content) is bytes:
        try:
            c = content.decode('utf-8')
        except:
            c = content.decode('gbk')
    elif type(content) is str:
        c = content
    else:
        raise TypeError('content type must in [bytes, str].')
    c = re.sub('>([^>]*[\u4e00-\u9fa5]{1,}[^<]*)<','>\g<1> <',c)
    e = etree.HTML(c)
    q = []
    for it in e.getiterator():
        if it.tag in tags or type(it.tag) is not str:
            q.append(it)
    for it in q:
        p = it.getparent()
        if p is not None:
            p.remove(it)
    t = e.xpath('normalize-space({})'.format(rootxpath))
    return t.strip()

# 显示 response 窗口内的输出窗口
def show_response_log():
    _select = nb.select()
    setting = nb_names[_select]['setting']
    if setting.get('type') == 'response':
        setting.get('fr_temp2').pack(fill=tkinter.BOTH,expand=True,side=tkinter.BOTTOM)

# 获取内部文本的函数
def get_html_pure_text(*a):
    _select = nb.select()
    setting = nb_names[_select]['setting']
    if setting.get('type') == 'response':
        txt = setting.get('fr_html_content')
        tx2 = setting.get('fr_local_set')

        c_set = tx2.get(0.,tkinter.END).strip()
        rt = '//html'
        toggle = True
        for i in c_set.splitlines():
            i = i.strip()
            if i.startswith('<') and i.endswith('>'):
                if i.startswith('<normal_content:'):
                    rt = re.findall('<normal_content:(.*)>', i)[0].strip()
                    toggle = False

        tx4 = setting.get('fr_parse_info')
        try:
            content = normal_content(txt.get(0.,tkinter.END), rootxpath=rt)
        except:
            content = traceback.format_exc()
        tx4.delete(0.,tkinter.END)
        tx4.insert(0.,content)
        if toggle:
            tx2.delete(0.,tkinter.END)
            tx2.insert(0.,'<normal_content://html>')
            
        show_response_log()




# 显示 代码 窗口内的输出窗口
def show_code_log():
    _select = nb.select()
    setting = nb_names[_select]['setting']
    if setting.get('type') == 'code' or setting.get('type') == 'js':
        setting.get('fr_temp2').pack(fill=tkinter.BOTH,expand=True,side=tkinter.BOTTOM)

def execute_code(*a):
    _select = nb.select()
    setting = nb_names[_select]['setting']
    if setting.get('type') == 'code' or setting.get('type') == 'js':
        execute_func = setting.get('execute_func')
        show_code_log()
        execute_func()
        

def execute_scrapy_code(*a):
    _select = nb.select()
    setting = nb_names[_select]['setting']
    if setting.get('type') == 'scrapy':
        execute_func = setting.get('execute_func')
        execute_func()


from tkinter import (
    Toplevel,
    Message,
    LEFT,
    BOTH,
    TOP,
    RIDGE,
    Frame,
    Button,
)
class SimpleDialog:
    def __init__(self, master,
                 text='', buttons=[], default=None, cancel=None,
                 title=None, class_=None):
        if class_:
            self.root = Toplevel(master, class_=class_)
        else:
            self.root = Toplevel(master)
        if title:
            self.root.title(title)
            self.root.iconname(title)
        self.message = Message(self.root, text=text, aspect=400)
        self.message.pack(expand=1, fill=BOTH)
        self.frame = Frame(self.root)
        self.frame.pack()
        self.num = default
        self.cancel = cancel
        self.default = default
        self.root.bind('<Return>', self.return_event)
        self.root.bind('<Escape>', self.wm_delete_window)
        for num in range(len(buttons)):
            s = buttons[num]
            f = Frame(self.frame)
            b = Button(f, text=s, 
                       command=(lambda self=self, num=num: self.done(num)))
            if num == default:
                pass
            b.pack(side=LEFT, fill=BOTH)
            f.pack(side=TOP, fill=BOTH)
        self.root.protocol('WM_DELETE_WINDOW', self.wm_delete_window)
        self._set_transient(master)

    def _set_transient(self, master, relx=0.5, rely=0.3):
        widget = self.root
        widget.withdraw() # Remain invisible while we figure out the geometry
        widget.transient(master)
        widget.update_idletasks() # Actualize geometry information
        if master.winfo_ismapped():
            m_width = master.winfo_width()
            m_height = master.winfo_height()
            m_x = master.winfo_rootx()
            m_y = master.winfo_rooty()
        else:
            m_width = master.winfo_screenwidth()
            m_height = master.winfo_screenheight()
            m_x = m_y = 0
        w_width = widget.winfo_reqwidth()
        w_height = widget.winfo_reqheight()
        x = m_x + (m_width - w_width) * relx
        y = m_y + (m_height - w_height) * rely
        if x+w_width > master.winfo_screenwidth():
            x = master.winfo_screenwidth() - w_width
        elif x < 0:
            x = 0
        if y+w_height > master.winfo_screenheight():
            y = master.winfo_screenheight() - w_height
        elif y < 0:
            y = 0
        widget.geometry("+%d+%d" % (x, y))
        widget.deiconify() # Become visible at the desired location

    def go(self):
        self.root.wait_visibility()
        self.root.grab_set()
        self.root.mainloop()
        self.root.destroy()
        return self.num

    def return_event(self, event):
        if self.default is None:
            self.root.bell()
        else:
            self.done(self.default)

    def wm_delete_window(self, event=None):
        if self.cancel is None:
            self.root.bell()
        else:
            self.done(self.cancel)

    def done(self, num):
        self.num = num
        self.root.quit()


# TODO
# 通过xpath获取element内部数据和内容
def get_xpath_elements(*a):
    _select = nb.select()
    setting = nb_names[_select]['setting']
    if setting.get('type') == 'response':
        txt = setting.get('fr_html_content')
        tx2 = setting.get('fr_local_set')
        tx4 = setting.get('fr_parse_info')

        c_set = tx2.get(0.,tkinter.END).strip()
        xp = '//html'
        toggle = 0
        for i in c_set.splitlines():
            i = i.strip()
            if i.startswith('<') and i.endswith('>'):
                if i.startswith('<xpath:'):
                    xp = re.findall('<xpath:(.*)>', i)[0].strip()
                    toggle = 1
                    break
                if i.startswith('<auto_list_xpath:'):
                    q = ['//html']
                    d = {}
                    p = None
                    for j in tx4.get(0.,tkinter.END).strip().splitlines():
                        v = re.findall(r'^\[ xpath \]: (.*)$',j)
                        if v:
                            p = v[0]
                            d[p] = 0
                        elif p:
                            d[p] += 1
                    show_num = 25
                    m = sorted(d,key=len)[:show_num]
                    for i in m:
                        q.append('[ cnt:{} ]'.format(d[i]) + i)
                    q = sorted(q,key=len)[:show_num]
                    d = SimpleDialog(nb,
                        text="是否选择自动解析出的xpath路径？\n"
                             "（不选择，默认填充 “//html” ，最大显示{}条内容）".format(show_num),
                        buttons=q,
                        default=0,
                        cancel=-1,
                        title="Test Dialog")
                    id = d.go()
                    if id == -1: return
                    xp = re.sub(r'^\[ cnt:\d+ \]', '', q[id])
                    toggle = 2
                    break
        tx4 = setting.get('fr_parse_info')
        if xp.startswith('//'):
            p = ['[ xpath ]: {}'.format(xp)]
            tree = etree.HTML(txt.get(0.,tkinter.END))
            idx = 0
            for x in tree.xpath(xp):
                xpth = get_simple_path_tail(x)
                strs = re.sub('\s+',' ',x.xpath('string(.)'))
                strs = strs[:40] + '...' if len(strs) > 40 else strs
                xpth = '[ xptail ]: {} {}'.format(xpth[1] if xpth else xpth, strs)
                p.append(xpth)
                idx += 1
            p.append('[ count ]: {}'.format(idx))
            content = '\n'.join(p)
        tx4.delete(0.,tkinter.END)
        tx4.insert(0.,content)
        if toggle == 0:
            tx2.delete(0.,tkinter.END)
            tx2.insert(0.,'<xpath://html>')
        if toggle == 2:
            tx2.delete(0.,tkinter.END)
            tx2.insert(0.,'<xpath:{}>'.format(xp))
        show_response_log()


# 通过xpath获取element内部数据和内容
def get_auto_xpath(*a):
    _select = nb.select()
    setting = nb_names[_select]['setting']
    if setting.get('type') == 'response':
        txt = setting.get('fr_html_content')
        tx2 = setting.get('fr_local_set')

        c_set = tx2.get(0.,tkinter.END).strip()
        sx = ''
        toggle = True
        for i in c_set.splitlines():
            i = i.strip()
            if i.startswith('<') and i.endswith('>'):
                if i.startswith('<auto_list_xpath:'):
                    sx = re.findall('<auto_list_xpath:(.*)>', i)[0].strip()
                    toggle = False
        tx4 = setting.get('fr_parse_info')
        # 通过字符串自动分析列表文件路径的函数
        strs = re.split('\s+',sx)
        p = []
        idx = 0
        for xp,strs in get_xpath_by_str(strs,txt.get(0.,tkinter.END)):
            idx += 1
            q = []
            q.append('[ xpath ]: {}'.format(xp))
            for j,c in strs:
                q.append('    [ content ]: {} {}'.format(j,c))
            p.append(q)
        q = []
        for i in sorted(p,key=lambda i:len(i[0])):
            q.extend(i)
        q.append('[ count ]: {}'.format(idx))
        content = '\n'.join(q)
        tx4.delete(0.,tkinter.END)
        tx4.insert(0.,content)
        if toggle:
            tx2.delete(0.,tkinter.END)
            tx2.insert(0.,'<auto_list_xpath:>')
        show_response_log()



# 通过xpath获取element内部数据和内容
def get_auto_json(*a):
    _select = nb.select()
    setting = nb_names[_select]['setting']
    if setting.get('type') == 'response':
        txt = setting.get('fr_html_content')
        tx2 = setting.get('fr_local_set')

        c_set = tx2.get(0.,tkinter.END).strip()
        sx = ''
        toggle = True
        for i in c_set.splitlines():
            i = i.strip()
            if i.startswith('<') and i.endswith('>'):
                if i.startswith('<auto_list_json:'):
                    sx = re.findall('<auto_list_json:(.*)>', i)[0].strip()
                    toggle = False
        tx4 = setting.get('fr_parse_info')
        try:
            content = get_json_show(txt.get(0.,tkinter.END))
            if not content:
                try:
                    _content = 'cannot use auto parse json list\nnow use simple pprint json.\n===============================\n'
                    _content += pprint.pformat(parse_json_content(txt.get(0.,tkinter.END)))
                    content = _content
                except:
                    content = 'cannot format this content to json struct.\n'
                    content += '==========================================\n'
                    content += traceback.format_exc()
        except:
            content = traceback.format_exc()
        tx4.delete(0.,tkinter.END)
        tx4.insert(0.,content)
        if toggle:
            tx2.delete(0.,tkinter.END)
            tx2.insert(0.,'<auto_list_json:>')
        show_response_log()





def execute_js_code():
    pass