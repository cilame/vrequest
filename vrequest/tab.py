from lxml import etree

import re
import json
import traceback
import tkinter
import tkinter.messagebox
from tkinter import ttk
from tkinter.simpledialog import askstring

from root import (
    root,
    config,
    save,
)
from frame import (
    request_window,
    response_window,
    helper_window,
    frame_setting,
)
from util import (
    format_url,
    format_url_show,
    format_url_code,
    format_headers_str,
    format_headers_code,
    format_request,
    format_response,
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


def create_helper():
    nb.select(bind_frame(helper_window(),'帮助'))



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
    return method,c_url,c_headers,body




def get_response_config(setting):
    tx1 = setting.get('fr_html_content')
    tx2 = setting.get('fr_local_set')
    tx3 = setting.get('fr_undefined2')
    tx4 = setting.get('fr_parse_info')
    temp_fr2 = setting.get('fr_temp2')

    c_set = tx2.get(0.,tkinter.END).strip() # 配置，用来配置生成代码的方式

    r_setting = setting.get('fr_setting')
    r_setting = r_setting if r_setting is not None else None
    return r_setting,c_set




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
    toggle = tkinter.messagebox.askokcancel('是否保存','确定保存当前全部配置信息吗？')
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
    if setting.get('type') == 'response':
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
    setting = nb_names[_select]['setting']
    if setting.get('type') == 'request':
        method,c_url,c_headers,body = get_request_config(setting)
        code_string = format_request(method,c_url,c_headers,body)
        print(code_string)
    if setting.get('type') == 'response':
        r_setting,c_set = get_response_config(setting)
        code_string = format_response(r_setting,c_set)
        print(code_string)




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
