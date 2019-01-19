import re
import json
import urllib.parse as ps
import inspect


def format_headers_str(headers:str):
    # return dict
    headers = headers.splitlines()
    headers = [i.split(':',1) for i in headers if i.strip() and ':' in i]
    headers = {k.strip():v.strip() for k,v in headers}
    return headers


def format_headers_code(headers):
    # headers 参数可以是字符串，可以是字典
    # return str
    assert type(headers) in (str, dict)
    if type(headers) is str:
        headers = format_headers_str(headers)
    return 'headers = ' + json.dumps(headers,indent=4,ensure_ascii=False)


def format_url(url:str):
    # return str
    return ''.join([i.strip() for i in url.splitlines()])


def format_url_show(url:str):
    # return str
    indent = 4
    url = ps.unquote(url)
    pls = re.findall('\?[^&]*|&[^&]*',url)
    pms = [None]
    for i in pls:
        url = url.replace(i,'')
        if len(i) > 50 and ',' in i:
            _pms = []
            for j in i.split(','):
                j = ' '*indent + j + ','
                _pms.append(j)
            _pms[-1] = _pms[-1][:-1]
            pms += _pms
        else:
            pms.append(i)
    pms[0] = url
    return '\n'.join(pms)



def format_url_code(url:str):
    # return str
    indent = 4
    url = ps.unquote(url)
    pls = re.findall('\?[^&]*|&[^&]*',url)
    pms = ['url = (',None]
    def symbol(strs):
        if '\'' not in strs:
            return '\''
        if '"' not in strs:
            return '"'
        if '\'\'\'' not in strs:
            return '\'\'\''
        return '"""'
    for i in pls:
        url = url.replace(i,'')
        if len(i) > 50 and ',' in i:
            _pms = []
            for j in i.split(','):
                j = j.join([symbol(j)]*2)
                j = ' '*2*indent + j + ','
                _pms.append(j)
            _pms[-1] = _pms[-1][:-1]
            pms += _pms
        else:
            i = i.join([symbol(i)]*2)
            i = ' '*indent + i
            pms.append(i)
    u = symbol(url)
    pms[1] = ' '*indent + '{}{}{}'.format(u,url,u)
    pms.append(')')
    return '\n'.join(pms)



def format_request(method,c_url,c_headers,body):

    _format_get = '''
import requests
from lxml import etree

{}
{}

def get(url,headers):
    s = requests.get(url,headers=headers)
    e = etree.HTML(s.content)
    return e

get(url,headers)
'''

    _format_post = '''
import requests
from lxml import etree

{}
{}{}

def post(url,headers{}):
    s = requests.get(url,headers=headers{})
    e = etree.HTML(s.content)
    return e

post(url,headers{})
'''

    if method == 'GET':
        _format = _format_get.format(c_url,c_headers)
    elif method == 'POST':
        if body.strip():
            # 这里暂时没有对 body 的处理，
            # 因为 post 请求还没有进行全面的了解
            # 后续的 body 肯定是需要进行一定的处理后再放在下面的地方
            _body = '\ndata={}'.format(body)
            _body2 = ',data'
            _body3 = ',data=data'
        else:
            _body = ''
            _body2 = ''
            _body3 = ''
        _format = _format_post.format(c_url,c_headers,_body,_body2,_body3,_body2)
    return _format.strip()




def format_response(r_setting,c_set):

    _format_get = '''
import requests
from lxml import etree

{}
{}

def get(url,headers):
    s = requests.get(url,headers=headers)
    e = etree.HTML(s.content)
    return e

get(url,headers)
'''

    _format_post = '''
import requests
from lxml import etree

{}
{}{}

def post(url,headers{}):
    s = requests.get(url,headers=headers{})
    e = etree.HTML(s.content)
    return e

post(url,headers{})
'''

    # 请求部分的代码
    if r_setting is not None:
        method,c_url,c_headers,body = r_setting
        if method == 'GET':
            _format = _format_get.format(c_url,c_headers)
        elif method == 'POST':
            if body.strip():
                # 这里暂时没有对 body 的处理，
                # 因为 post 请求还没有进行全面的了解
                # 后续的 body 肯定是需要进行一定的处理后再放在下面的地方
                _body = '\ndata={}'.format(body)
                _body2 = ',data'
                _body3 = ',data=data'
            else:
                _body = ''
                _body2 = ''
                _body3 = ''
            _format = _format_post.format(c_url,c_headers,_body,_body2,_body3,_body2)
        else:
            _format = ''
    else:
        _format = ''
    _format = _format.strip()



    for i in c_set.splitlines():
        i = i.strip()
        if i.startswith('<') and i.endswith('>'):
            if i.startswith('<normal_content:'):
                rt = re.findall('<normal_content:(.*)>', i)[0].strip()
                rt = rt if rt else '//html'
                from tab import normal_content
                func_code = inspect.getsource(normal_content).strip()
                func_code += '\n\ncontent = normal_content(content, rootxpath="{}")'.format(rt)
                print(func_code)


    


    return _format
    

