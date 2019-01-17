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
    nb_names[tab_id]['setting'] = frame_setting.pop(frame)
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


def change_tab_name():
    name = askstring('修改标签','新的标签名字') # 简单弹窗请求字符串数据
    if name is not None:
        _select = nb.select()
        nb_names[_select]['name'] = name
        nb.tab(_select, text=name)


def create_new_tab(setting=None):
    # TODO
    # 后面想了想，感觉在创建新标签的时候配置名字会有点麻烦
    # 如果有需要的话最好还是通过自己主动修改名字会更好
    # 因为如果自己觉得有必要保留的配置，一般自己也会主动配置
    # 不需要的临时的请求就没有必要写一些名字，那样比较麻烦。
    # 所以决定，这里的处理将使用 '标签' + 数字id 的临时名字就可以。
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


def send_request():
    _select = nb.select()
    setting = nb_names[_select]['setting']
    if setting.get('type') == 'request':
        url = setting.get('fr_url').get(0.,tkinter.END).strip()
        headers = setting.get('fr_headers').get(0.,tkinter.END).strip()
        print('url:',url)
        print('headers:',headers)