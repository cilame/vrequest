import re
import json
import urllib.parse as ps


def format_headers_str(headers:str):
    # return dict
    headers = headers.splitlines()
    headers = [i.split(':',1) for i in headers if i.strip() and ':' in i]
    headers = {k.strip():v.strip() for k,v in headers}
    return headers


def format_headers_code(headers:dict):
    # return str
    return json.dumps(headers,indent=4,ensure_ascii=False)


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
        if len(i) > 50:
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
        if len(i) > 50:
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
    pms[1] = ' '*indent + '{}{}{}'.format(u,{},u).format(url)
    pms.append(')')
    return '\n'.join(pms)