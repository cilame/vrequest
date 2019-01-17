import re
import tkinter
from tkinter import ttk
from tkinter.simpledialog import askstring

from root import (
    root,
    config,
    save,
)
from frame import (
    request_window,
    helper_window,
    frame_setting,
)

nb = ttk.Notebook(root)
nb.place(relx=0, rely=0, relwidth=1, relheight=1)
nb_names = {} 
'''
nb_names 的数据结构：
{
    tab_id1: 
        {
            'name':tab_name,
            'setting':setting1,
        }, 
    tab_id2:
        {
            'name':tab_name,
            'setting':setting2,
        }, 
}
setting 是一个字典，里面至少有一个 type字段描述什么类型。
'''


def bind_frame(frame, name=None):
    global config, nb_names
    #print(config)
    frame.master = nb
    name = name if name is not None else frame._name
    v = set(nb.tabs())
    nb.add(frame, text=name)
    tab_id = (set(nb.tabs())^v).pop() # 由于没有接口，只能用这种方式来获取新增的 tab_id
    nb_names[tab_id] = {}
    nb_names[tab_id]['name'] = name
    nb_names[tab_id]['setting'] = frame_setting.pop(frame) if frame in frame_setting else {}
    return tab_id


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
            config['set'].pop(cname)


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


def create_new_tab(setting=None):
    nums = []
    for val in nb_names.values():
        v = re.findall('标签\d+', val['name'])
        if v:
            num = int(re.findall('标签(\d+)', v[0])[0])
            nums.append(num)
    idx = 0
    while True:
        if idx in nums:
            idx += 1
        else:
            retn = idx
            break
    name = '标签{}'.format(retn)
    nb.select(bind_frame(request_window(setting),name))


def create_helper():
    nb.select(bind_frame(helper_window(),'帮助'))


@save
def send_request():
    global config
    _select = nb.select()
    name = nb_names[_select]['name']
    setting = nb_names[_select]['setting']
    foc_toggle = True
    if setting.get('type') == 'request':
        method = setting.get('fr_method').get()
        url = setting.get('fr_url').get(0.,tkinter.END).strip()
        headers = setting.get('fr_headers').get(0.,tkinter.END).strip()
        body = setting.get('fr_body').get(0.,tkinter.END).strip()
        config['set'][name] = {}
        config['set'][name]['type'] = 'request'
        config['set'][name]['method'] = method
        config['set'][name]['url'] = url
        config['set'][name]['headers'] = headers
        config['set'][name]['body'] = body

        print('[ method ]:',method)
        print('[ url ]:',url)
        print('[ headers ]:',headers)
        print('[ body ]:',body)
        print('================')
        print(config)
    else:
        foc_toggle = False
    if foc_toggle:
        config['focus'] = name
