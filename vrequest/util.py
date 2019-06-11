import re
import json
import urllib.parse as ps
import inspect
import builtins
from lxml import etree
import tkinter.messagebox
import traceback


def dprint(*a):
    # debug print
    from .frame import __org_stdout__
    __org_stdout__.write(str(a)+'\n')
    __org_stdout__.flush()


def format_headers_str(headers:str):
    # return dict
    headers = headers.splitlines()
    headers = [re.split(':|=',i,1) for i in headers if i.strip() and ':' in i or '=' in i]
    headers = {k.strip():v.strip() for k,v in headers if k.lower() != "content-length"}
    for k,v in headers.items():
        if k.lower() == 'accept-encoding':
            headers[k] = v.replace('br','')
    return headers


def format_headers_code(headers):
    # headers 参数可以是字符串，可以是字典
    # return str
    assert type(headers) in (str, dict)
    if type(headers) is str:
        headers = format_headers_str(headers)
    ret = 'headers = ' + json.dumps(headers,indent=4,ensure_ascii=False)
    for name in headers:
        if name.lower() == 'cookie':
            q = '(\n'
            p =[]
            for i in headers[name].split('; '): p.append(i)
            for i in sorted(p):
                q += '        "'+i.replace('"','\\"')+'; "\n'
            q += '    )'
            ret = re.sub(r'("{}": )([^\n]+),'.format(name),r'\1$cookie,',ret,re.I)
            ret = ret.replace('$cookie',q)
        if name.lower() == 'accept-encoding':
            ret = re.sub(r'{}([^\n]+)'.format(name),r'{}\1 # auto delete br encoding. cos requests and scrapy can not decode it.'.format(name), ret)
    return ret


def format_body_str(body:str):
    # return dict
    body = body.splitlines()
    body = [i for i in body if i.strip()]
    # 如果只有一行并且以双引号开始和结尾的话，就直接传字符串，不用传字典了。
    if len(body) == 1:
        v = body[0].strip()
        if v.startswith('"')  and v.endswith('"'):
            return v.strip('"')
    body = [re.split(':|=',i,1) for i in body if ':' in i or '=' in i]
    body = {k.strip():v.strip() for k,v in body}
    return body


def format_body_code(body):
    # body 参数可以是字符串，可以是字典
    # return str
    assert type(body) in (str, dict)
    if type(body) is str:
        body = format_body_str(body)
    return 'body = ' + json.dumps(body,indent=4,ensure_ascii=False)



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
                j = (j + ',').join([symbol(j)]*2)
                j = ' '*2*indent + j
                _pms.append(j)
            _pms[-1] = _pms[-1][:-2] + _pms[-1][-1]
            pms += _pms
        else:
            i = i.join([symbol(i)]*2)
            i = ' '*indent + i
            pms.append(i)
    u = symbol(url)
    pms[1] = ' '*indent + '{}{}{}'.format(u,url,u)
    pms.append(')')
    return '\n'.join(pms)



def format_req(method,c_url,c_headers,c_body):

    _format_get = '''
try:
    # 处理 sublime 执行时输出乱码
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
    sys.stdout._CHUNK_SIZE = 1
except:
    pass

import re
import json
import requests
from lxml import etree
requests.packages.urllib3.disable_warnings() # 取消不验证ssl警告

def get_info():
    # 功能函数（解析解码格式）
    def parse_content_type(content, types=['utf-8','gbk']):
        itype = iter(types)
        while True:
            try:
                tp = next(itype)
                content = content.decode(tp)
                return tp, content
            except StopIteration:
                try:
                    import chardet
                    tp = chardet.detect(content)['encoding']
                    types.append(tp)
                    content = content.decode(tp)
                    return tp, content
                except:
                    raise TypeError('not in {}'.format(types))
            except:
                continue
    # 生成请求参数函数
    def mk_url_headers():
        def quote_val(url):
            import urllib
            url = urllib.parse.unquote(url)
            for i in re.findall('=([^=&]+)',url):
                url = url.replace(i,'{}'.format(urllib.parse.quote(i)))
            return url
        $c_url
        url = quote_val(url) # 解决部分网页需要请求参数中的 param 保持编码状态，如有异常考虑注释
        $c_headers
        return url,headers

    url,headers = mk_url_headers()
    s = requests.get(url,headers=headers,verify=False)
    tp, content = parse_content_type(s.content)
    print(s)
    print('decode type: {}'.format(tp))
    print('response length: {}'.format(len(s.content)))
$plus

get_info()

#
'''

    _format_post = '''
try:
    # 处理 sublime 执行时输出乱码
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
    sys.stdout._CHUNK_SIZE = 1
except:
    pass

import re
import json
import requests
from lxml import etree
requests.packages.urllib3.disable_warnings() # 取消不验证ssl警告

def post_info():
    # 功能函数（解析解码格式）
    def parse_content_type(content, types=['utf-8','gbk']):
        itype = iter(types)
        while True:
            try:
                tp = next(itype)
                content = content.decode(tp)
                return tp, content
            except StopIteration:
                try:
                    import chardet
                    tp = chardet.detect(content)['encoding']
                    types.append(tp)
                    content = content.decode(tp)
                    return tp, content
                except:
                    raise TypeError('not in {}'.format(types))
            except:
                continue
    # 生成请求参数函数
    def mk_url_headers_body():
        def quote_val(url):
            import urllib
            url = urllib.parse.unquote(url)
            for i in re.findall('=([^=&]+)',url):
                url = url.replace(i,'{}'.format(urllib.parse.quote(i)))
            return url
        $c_url
        url = quote_val(url) # 解决部分网页需要请求参数中的 param 保持编码状态，如有异常考虑注释
        $c_headers
        $c_body
        return url,headers,body

    url,headers,body = mk_url_headers_body()    
    #body = json.dumps(body) #极少情况需要data为string情况下的json数据，如需要解开该注释
    s = requests.post(url,headers=headers,data=body,verify=False) 
    tp, content = parse_content_type(s.content)
    print(s)
    print('decode type: {}'.format(tp))
    print('response length: {}'.format(len(s.content)))
$plus

post_info()

#
'''

    func = lambda c_:''.join(map(lambda i:'        '+i+'\n',c_.splitlines()))
    c_url       = func(c_url).strip()
    c_headers   = func(c_headers).strip()
    c_body      = func(c_body).strip()
    if method == 'GET':
        _format = _format_get
        _format = _format.replace('$c_url',c_url)
        _format = _format.replace('$c_headers',c_headers)
    elif method == 'POST':
        _format = _format_post
        _format = _format.replace('$c_url',c_url)
        _format = _format.replace('$c_headers',c_headers)
        _format = _format.replace('$c_body',c_body)
    return _format.strip()


def format_request(method,c_url,c_headers,c_body):
    return format_req(method,c_url,c_headers,c_body).replace('$plus','')


def format_response(r_setting,c_set,c_content):
    # 请求部分的代码
    if r_setting is not None:
        method,c_url,c_headers,c_body = r_setting
        _format = format_req(method,c_url,c_headers,c_body)
    else:
        tkinter.messagebox.showinfo('Error','Canot create code without request.')
        raise TypeError('Canot create code without request.')
    _format = _format.strip()

    for i in c_set.splitlines():
        i = i.strip()
        if not i: continue
        func_code = None
        if i.startswith('<') and i.endswith('>'):
            if i.startswith('<normal_content:'):
                rt = re.findall('<normal_content:(.*)>', i)[0].strip()
                rt = rt if rt else '//html'
                from .tab import normal_content
                func_code = inspect.getsource(normal_content).strip()
                func_code += '''\n\ncontent = normal_content(content, rootxpath='{}')\nprint(content)'''.format(rt)
            if i.startswith('<xpath:'):
                xp = re.findall('<xpath:(.*)>', i)[0].strip()
                xp = xp if xp else '//html'
                indent = 4
                try:
                    skey = lambda i:-(int(re.findall(r'# \[cnt:(\d+)\]',i)[0]) if re.findall(r'# \[cnt:(\d+)\]',i) else (float('inf') if i.startswith('d = {}') else -1))
                    ax = sorted(auto_xpath(xp,c_content),key=skey)
                    func = lambda i:i.replace('\n',' ').strip()
                    p = []
                    p.append("tree = etree.HTML(content)")
                    p.append("for x in tree.xpath('{}'):".format(xp))
                    p.extend([' '*indent+func(i) for i in ax])
                    func_code ='\n'.join(p)
                except:
                    traceback.print_exc()
                    func_code =("print('------------------------------ split ------------------------------')\n"
                                "tree = etree.HTML(content)\n"
                                "for x in tree.xpath('{}'):\n".format(xp) + 
                                "    strs = re.sub('\s+',' ',x.xpath('string(.)'))\n"
                                "    strs = strs[:40] + '...' if len(strs) > 40 else strs\n"
                                "    attr = '[ attrib ]: {} [ string ]: {}'.format(x.attrib, strs)\n"
                                "    print(attr)\n")
            if i.startswith('<auto_list_json:'):
                try:
                    func_code = get_json_code(c_content).strip()
                except:
                    import traceback
                    traceback.print_exc()
                    func_code = ''
        func = lambda c_:''.join(map(lambda i:'    '+i+'\n',c_.splitlines()))
        _format = _format.replace('$plus', '\n'+func(func_code)) if func_code is not None else _format
    _format = _format if '$plus' not in _format else _format.replace('$plus','')
    return _format.strip()






def format_scrapy_req(method,c_url,c_headers,c_body):
    _format_get = '''
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

import re
import json
from urllib.parse import quote,unquote

class VSpider(scrapy.Spider):
    name = 'v'

    custom_settings = {
        'COOKIES_ENABLED': False,  # use my create cookie in headers
    }

    def start_requests(self):
        def mk_url_headers():
            def quote_val(url):
                url = unquote(url)
                for i in re.findall('=([^=&]+)',url):
                    url = url.replace(i,'{}'.format(quote(i)))
                return url
            $c_url
            url = quote_val(url)
            $c_headers
            return url,headers
        url,headers = mk_url_headers()
        meta = {}
        r = Request(
                url,
                headers  = headers,
                callback = self.parse,
                meta     = meta,
            )
        yield r

    def parse(self, response):
        # If you need to parse another string in the parsing function.
        # use "etree.HTML(text)" or "Selector(text=text)" to parse it.

        $plus
'''

    _format_post = '''
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

import re
import json
from urllib.parse import quote,unquote,urlencode

class VSpider(scrapy.Spider):
    name = 'v'

    custom_settings = {
        'COOKIES_ENABLED': False,  # use my create cookie in headers
    }

    def start_requests(self):
        def mk_url_headers_body():
            def quote_val(url):
                url = unquote(url)
                for i in re.findall('=([^=&]+)',url):
                    url = url.replace(i,'{}'.format(quote(i)))
                return url
            $c_url
            url = quote_val(url)
            $c_headers
            $c_body
            return url,headers,body
        url,headers,body = mk_url_headers_body()
        meta = {}
        r = Request(
                url,
                method   = 'POST',
                headers  = headers,
                body     = urlencode(body),
                callback = self.parse,
                meta     = meta,
            )
        yield r

    def parse(self, response):
        # If you need to parse another string in the parsing function.
        # use "etree.HTML(text)" or "Selector(text=text)" to parse it.

        $plus
'''

    func = lambda c_:''.join(map(lambda i:'            '+i+'\n',c_.splitlines()))
    c_url       = func(c_url).strip()
    c_headers   = func(c_headers).strip()
    c_body      = func(c_body).strip()
    if method == 'GET':
        _format = _format_get
        _format = _format.replace('$c_url',c_url)
        _format = _format.replace('$c_headers',c_headers)
    elif method == 'POST':
        _format = _format_post
        _format = _format.replace('$c_url',c_url)
        _format = _format.replace('$c_headers',c_headers)
        _format = _format.replace('$c_body',c_body)
        if not c_body.strip().endswith('}'):
            _format = _format.replace('= urlencode(body)','= body')
    return _format.strip()


def format_scrapy_request(method,c_url,c_headers,c_body):
    pas = (
        "print('============================== start ==============================')\n"
        "        print('status:',response.status)\n"
        "        print('response length: {}'.format(len(response.body)))\n"
        "        print('response content[:1000]:\\n {}'.format(response.body[:1000]))\n"
        "        print('==============================  end  ==============================')"
    )
    return format_scrapy_req(method,c_url,c_headers,c_body).replace('$plus',pas)


def normal_scrapy_content(content,
                   tags=['script','style','select','noscript'],
                   rootxpath='//html'):
    c = re.sub('>([^>]*[\u4e00-\u9fa5]{1,}[^<]*)<','>\g<1> <',content)
    e, q = etree.HTML(c), []
    for it in e.getiterator():
        if it.tag in tags or type(it.tag) is not str:
            q.append(it)
    for it in q:
        p = it.getparent()
        if p is not None:
            p.remove(it)
    t = e.xpath('normalize-space({})'.format(rootxpath))
    return re.sub(r'\s+',' ',t.strip())

def format_scrapy_response(r_setting,c_set,c_content,tps):
    # 请求部分的代码
    if r_setting is not None:
        method,c_url,c_headers,c_body = r_setting
        _format = format_scrapy_req(method,c_url,c_headers,c_body)
    else:
        tkinter.messagebox.showinfo('Error','Canot create code without request.')
        raise TypeError('Canot create code without request.')
    _format = _format.strip()

    tps,err = tps.split(' ') if len(tps.split(' '))==2 else tps,'strict'
    for i in c_set.splitlines():
        i = i.strip()
        if not i: continue
        func_code = None
        if i.startswith('<') and i.endswith('>'):
            if i.startswith('<normal_content:'):
                rt = re.findall('<normal_content:(.*)>', i)[0].strip()
                rt = rt if rt else '//html'
                func_code = inspect.getsource(normal_scrapy_content).strip()
                func_code += '''\ncontent = response.body.decode("{}")\ncontent = normal_scrapy_content(content, rootxpath='{}')\nprint(content)'''.format(tps,rt)
            if i.startswith('<xpath:'):
                xp = re.findall('<xpath:(.*)>', i)[0].strip()
                xp = xp if xp else '//html'
                indent = 4
                try:
                    skey = lambda i:-(int(re.findall(r'# \[cnt:(\d+)\]',i)[0]) if re.findall(r'# \[cnt:(\d+)\]',i) else (float('inf') if i.startswith('d = {}') else -1))
                    ax = sorted(auto_xpath(xp,c_content),key=skey)
                    func = lambda i:re.sub(r'( +# \[cnt:\d+\])',r'.extract()\1',i) \
                                      .replace(' or [None])[0]',' or [none])[0]') \
                                      .replace('\n',' ') \
                                      .strip()
                    def func2(i):
                        i = func(i)
                        if re.findall(r'''= (x\.xpath\('string\(.*?\)'\))\.extract\(\)   ''', i):
                            i = re.sub(r'''= (x\.xpath\('string\(.*?\)'\))\.extract\(\)   ''',r'= \1[0].extract()',i)
                        else:
                            i = re.sub(r'''= (x\.xpath\('string\(.*?\)'\))\.extract\(\)''',r'= \1[0].extract()',i)
                        return i
                    p = []
                    p.append("class none:pass")
                    p.append("none.extract = lambda:None")
                    p.append("for x in response.xpath('{}'):".format(xp))
                    p.extend([' '*indent+func2(i) for i in ax])
                    func_code ='\n'.join(p)
                except:
                    traceback.print_exc()
                    func_code =("for x in response.xpath('{}'):\n".format(xp) + 
                                "    strs = x.xpath('string(.)').extract()[0]\n"
                                "    strs = re.sub('\s+',' ',strs)\n"
                                "    strs = strs[:60] + '...' if len(strs) > 60 else strs\n"
                                "    attr = '[ attrib ]: {} [ string ]: {}'.format(x.attrib, strs)\n"
                                "    print(attr)\n")
            if i.startswith('<auto_list_json:'):
                try:
                    jsoncode = get_json_code(c_content).strip()
                    if jsoncode:
                        if 'pprint.pprint(d)' in jsoncode:
                            func_code = 'content = response.body.decode("{}",errors="{}")\n'.format(tps,err) + \
                                        jsoncode + '\n    yield d'
                        else:
                            func_code = 'content = response.body.decode("{}",errors="{}")\n'.format(tps,err) + \
                                        jsoncode + '\n    yield {"data": i} # yield data must be a dict.'
                except:
                    traceback.print_exc()
                    return _format.strip().replace('$plus','pass')
        func = lambda c_:''.join(map(lambda i:'        '+i+'\n',c_.splitlines())).strip()
        _format = _format.replace('$plus', func(func_code)) if func_code is not None else _format
    pas = (
        "print('============================== start ==============================')\n"
        "        print('status:',response.status)\n"
        "        print('decode type: {}')\n".format(tps) + 
        "        print('response length: {}'.format(len(response.body)))\n"
        "        print('response content[:1000]:\\n {}'.format(response.body[:1000]))\n"
        "        print('==============================  end  ==============================')"
    )
    _format = _format if '$plus' not in _format else _format.replace('$plus',pas)
    return _format.strip()






# 下面是通过字符串模糊查找xpath的函数
def get_simple_path_tail(e):
    root = e.getroottree()
    try:
        xp = root.getelementpath(e)
    except:
        return
    v = xp.count('/')
    # 优先找路径上的id和class项优化路径
    for i in range(v):
        xpa = xp.rsplit('/',i)[0]
        rke = '/'.join(xp.rsplit('/',i)[1:])
        ele = root.xpath(xpa)[0].attrib
        tag = root.xpath(xpa)[0].tag
        if 'id' in ele:
            key = '[@id="{}"]'.format(ele["id"])
            rke = '/'+rke if rke else ""
            val = '//{}{}{}'.format(xpa.rsplit('/',1)[1],key,rke)
            return xp,val,key
        if 'class' in ele:
            if ' ' in ele["class"] and not ele["class"].startswith(' '):
                elass = ele["class"].split(' ',1)[0]
            else:
                elass = ele["class"]
            key = '[@class="{}"]'.format(elass)
            rke = '/'+rke if rke else ""
            val = '//{}{}{}'.format(xpa.rsplit('/',1)[1],key,rke)
            if not elass.strip():
                continue
            return xp,val,key


# 对列表的优化处理
def get_simple_path_head(p,lilimit=5):
    # 先通过绝对xpath路径进行分块处理
    s = {}
    w = {}
    for xp, sxp, key in p:
        q = re.sub('\[\d+\]','',xp)#.rsplit('/',1)[0]
        if q not in s:
            s[q] = [[xp, sxp, key]]
        else:
            s[q].append([xp, sxp, key])
    rm = []
    for px in sorted(s,key=lambda i: -len(i)):
        xps,sxps,keys = zip(*s[px])
        if len(sxps) == len(set(sxps)): continue
        p = {}
        ls = list(set(keys))
        for j in s[px]:
            if j[2] not in p:
                p[j[2]] = [j]
            else:
                p[j[2]].append(j)
        for i in p:
            le = len(p[i])
            v = ''
            if le > lilimit:
                for idx in range(p[i][0][0].count('/')):
                    v = p[i][0][0].rsplit('/',idx)[0]
                    q = list(map(lambda i:i[0].startswith(v),p[i]))
                    if all(q):
                        break
                for idx,j in enumerate(p[i]):
                    a,b,c = j
                    t = '/{}{}'.format(a.replace(v,''),c) + b.split(c,1)[1]
                    t = t if t.startswith('//') else '/' + t
                    p[i][idx][1] = t
                    p[i][idx].append(px)
                    yield j

def get_xpath_by_str(strs, html_content):
    e = etree.HTML(html_content)
    q = []
    p = []
    for i in e.xpath('//*'):
        xps = get_simple_path_tail(i) 
        if xps:
            xp, sxp, key = xps
            if sxp not in q:
                q.append(xp)
                p.append([xp, sxp, key])
    p.sort(key=lambda i: -len(i[0]))
    p = get_simple_path_head(p)

    def instrs(strs,v):
        if type(strs) is str:
            return strs in v
        elif type(strs) in (tuple,list):
            for i in strs:
                if i in v:
                    return True

    rets = []
    for key, xp, sxp, px in p:
        v = e.xpath('string({})'.format(xp))
        v = re.sub('\s+',' ',v)
        v = v[:40] + '...' if len(v) > 40 else v
        v = '[{}] {}'.format(len(v),v)
        if instrs(strs,v) and len(v.strip()) > 3: # '[0]' 如果该节点内容为空则过滤
            rets.append((xp,v))
    return find_xtree(rets)

def find_xtree(item_list):
    d = {}
    for i,v in item_list:
        b = re.sub(r'\[\d+\]','[$]',i)
        p = list(map(int,re.findall(r'\[(\d+)\]',i)))
        if b not in d: 
            d[b] = { 'level':
                         { 'all':None,
                           'map':{}, },
                     'info':[],
                     'xtree':None, }
        d[b]['info'].append({'path':i,'content':v,'ids':p})
        if d[b]['level']['all'] is None:
            d[b]['level']['all'] = len(p)
            d[b]['level']['map'] = {i:[] for i in range(1,len(p)+1)}
            d[b]['minfo'] = {i:None for i in range(1,len(p)+1)}
        for idx,i in enumerate(p,1):
            d[b]['level']['map'][idx].append(i)
    for i in d:
        for j in d[i]['level']['map'].items():
            d[i]['minfo'][j[0]] = 0 if len(set(j[1])) != 1 else j[1][0]
    for i in d:
        m = d[i]['minfo']
        x = i
        for j in range(1,len(m)+1):
            if j == len(m):
                v = re.sub(r'\[\$\]\[[^\[\]]+\]',r'[$]',x)
                v = re.findall(r'\[\$\]([^\$]*)$',v)[0]
                c = re.sub(r'\[[^\[\]]+\]',r'[]',v).count('/')
                c = '/parent::*' * c
                # 测试过了，这里用轴处理确实会更方便一些，且能解决子节点的条件约束问题。
                # c = ''
            if m[j] == 0:
                x = re.sub(r'^([^\$]+)\[\$\]',r'\1',x)
            else:
                x = re.sub(r'^([^\$]+)\[\$\]',r'\1[{}]'.format(m[j]),x)
        d[i]['xtree'] = x + c
    for i in d:
        yield d[i]['xtree'],[(i['path'],i['content']) for i in d[i]['info']]


# 这里的代码应该会是最后一次对自动列表解析处理的精准度的提升
# 以各种函数处理将解析上升到像是对json列表解析一样的高度
def auto_xpath(oxp,content,_type=None):
    tps = ['href', 'title']
    d = {}
    e = {}
    _oxp = re.sub('//[^/]+/','./',oxp)
    _oxp = re.sub(r'\[[^\[\]]+\]',r'',_oxp).replace('/parent::*','')
    def fmti(i):
        v = re.findall(r'^string\((.*?)\)$',i.strip())
        i,rf = (v[0],'string({})') if v else (i,'{}')
        o = ''
        t = ['.']
        for idx,j in enumerate(i.split('/')):
            if idx == 0: continue
            if idx > _oxp.count('/'):
                t.append(j)
                continue
            r1 = r'\[\d+\]' + r'(\[@.*\])'
            r2 = r'\[\d+\]'
            j = re.sub(r1,r'\1',j)
            j = re.sub(r2,r'',j)
            t.append(j)
        r = rf.format('/'.join(t))
        return r
    def normal_tree(content,
                    rootxpath='//html',
                    tags=['script','style','select','noscript'],):
        e = etree.HTML(content)
        q = []
        for it in e.getiterator():
            if it.tag in tags or type(it.tag) is not str:
                q.append(it)
        for it in q:
            p = it.getparent()
            if p is not None:
                p.remove(it)
        return e
    tree = normal_tree(content)
    for x in tree.xpath(oxp):
        def mk_attr_strs(x,s=0,idx=1,xp='.'):
            if type(x.tag) is not str: return
            strs = re.sub(r'\s+',' ',x.xpath('string(.)')).strip()
            if s!=0: xp += '/{}[{}]'.format(x.tag, idx)
            if 'id' in x.attrib:
                a = '[@id="{}"]'.format(x.attrib['id'])
            elif 'class' in x.attrib:
                a = '[@class="{}"]'.format(x.attrib['class'])
            elif x.attrib:
                for i in sorted(x.attrib.items(),key=lambda i:-len(i[1].strip())):
                    a = '[@{}]'.format(i[0])
            else:
                a = ''
            _xp = xp + a
            _sxp = 'string({})'.format(_xp if not _xp.startswith('.[') else '.')
            if strs and x.tag not in ['em']:
                _sxp = fmti(_sxp)
                if _sxp not in e: e[_sxp] = []
                e[_sxp].append(strs)
            for k,v in x.attrib.items():
                _lxp = '{}/@{}'.format(_xp,k)
                _lxp = fmti(_lxp)
                if k in tps:
                    if _lxp not in d: d[_lxp] = []
                    if v.strip():     d[_lxp].append(v)
            for idx,i in enumerate(x.getchildren(),1):
                mk_attr_strs(i,s+1,idx,xp)
        mk_attr_strs(x)
    f = {}
    for i in e.items():
        v = str(i[1])
        if v not in f: f[v] = []
        f[v].append(i[0])
    p = []
    for i in f.items():
        if len(i[1]) > 1:
            p.extend(sorted(i[1],key=lambda i:-len(i))[1:])
    for i in p:
        e.pop(i)
    m = set()
    def func(name):
        if name not in m:
            m.add(name)
            return name
        else:
            v = re.findall(r'_(\d+)$',name)
            name = re.sub(r'_\d+$','_{}'.format(int(v[0]) + 1),name)\
                if v else name + '_1'
            if name not in m:
                m.add(name)
                return name
            else:
                return func(name)
    def _mk_q():
        q = []
        for i in d:
            v = '''(x.xpath('{}') or [None])[0]'''.format(i)
            k = func((re.findall(r'@([^@]*)$', i) or [None])[0])
            q.append((k,v,len(d[i])))
        for i in e:
            v = '''x.xpath('{}')'''.format(i)
            k = (re.findall(r'@[^@"]*"([^@"]*)"[^@"]*$', i) or ['None'])[0]
            k = func('str_' + re.findall('[a-zA-Z0-9]+', k)[0]) if i != 'string(.)' else 'str_all'
            q.append((k,v,len(e[i])))
        return q
    def count_lu(q):
        l,u = 0,0
        for (k,v,_),_ in q:
            l = len(k) if len(k)>l else l
            u = len(v) if len(v)>u else u
        return l,u
    def clear_dregs(q):
        d = {}
        for x in tree.xpath(oxp):
            for k,v,_ in q:
                if k not in d: d[k] = 0
                n = eval(v)
                if n and str(n).strip():
                    d[k] += 1
                    d['$_'+k] = n
        return [(i,d['$_'+i[0]]) for i in q if d[i[0]] > 1]
    def mk_code_struct(q,l,u):
        r = ['d = {}']
        fmt = '{:<'+str(l+5)+'} = {:<' + str(u) +'} # [cnt:{}] [len:{}] '
        fmt2 = 'if {:<'+str(l+2)+'''} in d: d[{:<'''+str(l+2)+'''}] = re.sub(r'\s+',' ',d["{}"])'''
        limit = 30
        fmtstr = []
        for i,pr in q:
            pr = re.sub(r'\s+',' ',pr.replace('\n',''))
            lpr = len(pr)
            pr = pr[:limit]+'...' if lpr > limit else pr
            k,v,n = i
            k = 'd["{}"]'.format(k)
            f = fmt.format(k,v,n,lpr)+pr
            r.append(f)
            if not v.endswith('[None])[0]'):
                fmtstr.append(i)
        for i in fmtstr:
            k,v,n = i
            f = fmt2.format('"{}"'.format(k),'"{}"'.format(k),k)
            r.append(f)
        r.append("print('------------------------------ split ------------------------------')")
        r.append('import pprint')
        r.append('pprint.pprint(d)')
        return r
    q = _mk_q()
    q = clear_dregs(q)
    l,u = count_lu(q)
    s = mk_code_struct(q,l,u)
    return s

def get_xpath_code():
    pass











# ==== 解析 json 格式的数据 ====

def get_parse_list(jsondata):
    p = {}
    def parse_list(jsondata,uri=''):
        if type(jsondata) == dict:
            for idi,i in enumerate(jsondata):
                _uri = uri + "['{}']".format(i)
                iner = jsondata[i]
                if type(iner) == list:
                    if iner: 
                        p[_uri] = {}
                        p[_uri]['iner'] = iner
                        p[_uri]['lens'] = len(iner)
                    for idj,j in enumerate(iner):
                        _urj = _uri + "[{}]".format(idj)
                        parse_list(j, _urj)
                elif type(iner) == dict:
                    parse_list(iner, _uri)
        elif type(jsondata) == list:
            if jsondata:
                p[uri] = {}
                p[uri]['iner'] = jsondata
                p[uri]['lens'] = len(jsondata)
            for idj,j in enumerate(jsondata):
                _urj = uri + "[{}]".format(idj)
                parse_list(j, _urj)
    parse_list(jsondata)
    return p

def get_max_len_list(p):
    templen = 0
    temp = None
    for i in p:
        lens = p[i]['lens']
        iner = p[i]['iner']
        if lens > templen:
            templen = lens
            temp = i, iner
    return templen, temp

def analisys_key_sort(p):
    lens, (okey, iner) = p
    allkeys = []
    for i in iner:
        for j in i:
            if j not in allkeys:
                allkeys.append(j)
    keyscores = []
    mx = 0
    for key in allkeys:
        mx = len(key) if len(key)>mx else mx
        temp = []
        for i in iner:
            val = i.get(key, '')
            temp.append(str(val))
        dupscore = len(set(temp))/float(lens)
        argvlens = len(''.join(temp))/5.
        # 第一个是重复度，越大越不重复，0~1
        # 第二个是平均字符串长度，
        keyscores.append([key, argvlens, dupscore, str(val)])
    return mx,okey,sorted(keyscores,key=lambda i:i[1:])

def format_json_parse_code(p,standard=True,tp=1):
    # 这里将处理一些非典型的数据结构
    # 通常能解析的json列表的数据结构都是 list[dict1,dict2,...]，将这些当作标准解析结构
    # 不过也会有一些列表内部并非都是dict的数据结构，这时候就需要考虑一些别的方法进行格式化处理。
    if tp == 1:
        ret = '''jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])\nfor i in jsondata%s:\n'''
    if tp == 2:
        ret = '''jsondata = json.loads(content[content.find('['):content.rfind(']')+1])\nfor i in jsondata%s:\n'''
    if standard:
        mx,okey,sortkeys = analisys_key_sort(p)
        ret = ret % okey
        indent = 4
        ret += ' '*indent + 'd = {}\n'
        for key,alen,dups,val in sortkeys:
            key1 = '_'+key if key in dir(builtins) or key in ['d','i','s','e','content'] else key
            _ret = ' '*indent + ('d["{} = i.get("{:<'+str(mx+3)+'}').format(('{:<'+str(mx+2)+'}').format(key1+'"]'),key+'")')
            _comment = ''
            for i in range(5):
                slen = 60
                sval = val[i*slen:(i+1)*slen]
                spre = ' '*len(_ret) if i != 0 else ''
                if not sval:
                    break
                _comment += spre + '# {:<20}\n'.format(sval.replace('\n','')) # 注释部分
            if not _comment:
                _comment = '\n'
            ret += (_ret + _comment).rstrip() + '\n'
        tail = ' '*indent + "print('------------------------------ split ------------------------------')\n"
        tail += ' '*indent + 'import pprint\n'
        tail += ' '*indent + 'pprint.pprint(d)\n'
        return ret + tail
    else:
        lens, (okey, iner) = p
        ret = ret % okey
        indent = 4
        tail = ' '*indent + "print('------------------------------ split ------------------------------')\n"
        tail += ' '*indent + 'import pprint\n'
        tail += ' '*indent + 'pprint.pprint(i)\n'
        return ret + tail

def format_json_parse_show(p,standard=True):
    # 这里将处理一些非典型的数据结构
    # 通常能解析的json列表的数据结构都是 list[dict1,dict2,...]，将这些当作标准解析结构
    # 不过也会有一些列表内部并非都是dict的数据结构，这时候就需要考虑一些别的方法进行格式化处理。
    if standard:
        mx,okey,sortkeys = analisys_key_sort(p)
        ret = 'jsondata{}\n'.format(okey)
        ret += '='*(len(ret)-1) + '\n'
        for key,alen,dups,val in sortkeys:
            _ret = ('{:<'+str(mx)+'}').format(key)
            _comment = ''
            for i in range(5):
                slen = 60
                sval = val[i*slen:(i+1)*slen]
                spre = ' '*len(_ret) if i != 0 else ''
                if not sval:
                    break
                _comment += spre + ' # {:<20}\n'.format(sval.replace('\n','')) # 注释部分
            if not _comment:
                _comment = '\n'
            ret += (_ret + _comment).rstrip() + '\n'
        return ret
    else:
        lens, (okey, iner) = p
        ret = 'jsondata{}\n'.format(okey)
        ret += '='*(len(ret)-1) + '\n'
        for i in iner:
            ret += str(i) + '\n'
        return ret


def parse_json_content(content):
    if type(content) == str:
        try:
            json_content = json.loads(content[content.find('{'):content.rfind('}')+1])
            tp = 1
        except:
            json_content = json.loads(content[content.find('['):content.rfind(']')+1])
            tp = 2
    elif type(content) == bytes:
        try:
            json_content = json.loads(content[content.find(b'{'):content.rfind(b'}')+1])
            tp = 1
        except:
            json_content = json.loads(content[content.find(b'['):content.rfind(b']')+1])
            tp = 2
    else:
        raise TypeError('unparse type {}'.format(type(s)))
    return json_content,tp

def get_json_code(content):
    s,tp = parse_json_content(content)
    p = get_parse_list(s)
    p = get_max_len_list(p)
    if p[0] == 0: return ''
    standard = True if all(map(lambda i:type(i)==dict,p[1][1])) else False
    return format_json_parse_code(p,standard,tp)

def get_json_show(content):
    s,tp = parse_json_content(content)
    p = get_parse_list(s)
    p = get_max_len_list(p)
    if p[0] == 0: return ''
    standard = True if all(map(lambda i:type(i)==dict,p[1][1])) else False
    return format_json_parse_show(p,standard)