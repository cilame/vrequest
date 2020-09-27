try:
    from lxml import etree
except:
    pass

import re
import json
import urllib.parse as ps
import inspect
import builtins
import tkinter.messagebox
import traceback
import random

def dprint(*a):
    # debug print
    from .frame import __org_stdout__
    __org_stdout__.write(' '.join([str(i) for i in a])+'\n')
    __org_stdout__.flush()


def format_headers_str(headers:str):
    # return dict
    headers = headers.splitlines()
    headers = [re.split(':|=',i,1) for i in headers if i.strip() and ':' in i or '=' in i]
    headers = {k.strip():v.strip() for k,v in headers if (k.lower() != "content-length" and k.strip())}
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
            for i in sorted(p[:-1]): q += '        "'+i.replace('"','\\"')+'; "\n'
            for i in sorted(p[-1:]): q += '        "'+i.replace('"','\\"')+'"\n'
            q += '    )'
            ret = re.sub(r'("{}": )([^\n]+)(\n)'.format(name),r'\1$cookie,\3',ret,re.I)
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


def format_url_show(url:str, urlenc='utf-8'):
    # return str
    indent = 4
    url = ps.unquote_plus(url, encoding=urlenc)
    pls = re.findall('\?[^&]*|&[^&]*',url)
    pms = [None]
    for i in pls:
        url = url.replace(i,'',1) # fix
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



def format_url_code(url:str, urlenc):
    # return str
    isr = 'r' if '\\' in url else ''
    indent = 4
    url = ps.unquote_plus(url, encoding=urlenc)
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
        url = url.replace(i,'',1)
        if len(i) > 50 and ',' in i:
            _pms = []
            for j in i.split(','):
                j = (j + ',').join([symbol(j)]*2)
                j = ' '*2*indent + isr + j
                _pms.append(j)
            _pms[-1] = _pms[-1][:-2] + _pms[-1][-1]
            pms += _pms
            # dprint(_pms)
        else:
            i = i.join([symbol(i)]*2)
            i = ' '*indent + isr + i
            pms.append(i)
    u = symbol(url)
    pms[1] = ' '*indent + '{}{}{}{}'.format(isr, u,url,u)
    pms.append(')')
    return '\n'.join(pms)



def format_req(method,c_url,c_headers,c_body,urlenc,qplus):

    _head = '''
# 处理部分 IDE 执行脚本时可能输出乱码的问题
try:
    import io, sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
    sys.stdout._CHUNK_SIZE = 1
except:
    pass
# 解析 bytes 类型数据的编码格式（尾部有为中文编码兜底解析处理）
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
    err = 'encoding not in :[{}]. Guess encoding is [{},errors:ignore]'.format(','.join(etp), gtp)
    return err, content.decode(gtp, errors='ignore')




import re
import json
from urllib.parse import unquote_plus, quote_plus

import requests
from lxml import etree
requests.packages.urllib3.disable_warnings() # 取消不验证ssl警告$handle_3des_drop_out_stand$handle_dh_key_too_small
'''

    _format_get = _head + '''
def get_info():
    def mk_url_headers():
        $x_qplus
        $c_url
        url = quote_val(url) # 解决部分网页需要请求参数中的 param 保持编码状态，如有异常考虑注释
        $c_headers
        return url,headers

    proxies = None # {'http':'http://127.0.0.1:8888', 'https':'http://127.0.0.1:8888'}
    url,headers = mk_url_headers()
    s = requests.get(url,headers=headers,verify=False,proxies=proxies)
    tp, content = parse_content_type(s.content)
    print(s)
    print('decode type: {}'.format(tp))
    print('response length: {}'.format(len(s.content)))
$plus

get_info()

#
'''

    _format_post = _head + '''

def post_info():
    def mk_url_headers_body():
        $x_qplus
        $c_url
        url = quote_val(url) # 解决部分网页需要请求参数中的 param 保持编码状态，如有异常考虑注释
        $c_headers
        $c_body
        return url,headers,body

    proxies = None # {'http':'http://127.0.0.1:8888', 'https':'http://127.0.0.1:8888'}
    url,headers,body = mk_url_headers_body()
    #body = json.dumps(body) #极少情况需要data为string情况下的json数据，如需要解开该注释
    s = requests.post(url,headers=headers,data=body,verify=False,proxies=proxies) 
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
    rep = '''def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote_plus(unquote_plus(i.group(2),encoding='$x_urlenc'),encoding='$x_urlenc').replace('+', '%2B'), url)''' if qplus == 'yes' else \
          '''def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='$x_urlenc'),encoding='$x_urlenc'), url)'''
    rep2 = '''from urllib.parse import unquote_plus, quote_plus''' if qplus == 'yes' else \
           '''from urllib.parse import unquote, quote'''
    _format = _format.replace('$x_qplus', rep)
    _format = _format.replace('''from urllib.parse import unquote_plus, quote_plus''', rep2)
    _format = _format.replace('$x_urlenc',urlenc)
    return _format.strip()



def del_plus(string,extra=None):
    pas = r'''
    def show_info(s):
        def show_info_by_response(s):
            print('\n')
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
            # 请求信息
            print('===========\n| request |\n===========')
            print('request method: {}\nrequest url: {}'.format(s.request.method, s.url))
            print('------------------- request headers ---------------------')
            header_fprint(s.request.headers)
            print('------------------- request body ------------------------')
            print(s.request.body, end='\n')
            # 返回信息
            print('============\n| response |\n============')
            print('status:', s.status_code, '\nresponse length: {}'.format(len(s.content)))
            print('------------------- response headers --------------------')
            header_fprint(s.headers)
            print('------------------- response content[:1000] ----------------')
            print('response content[:1000]:\n {}'.format(s.content[:1000]))
            print('=========================================================')
        if s.history:
            chains = s.history + [s]
            for i in chains: show_info_by_response(i)
            print('redirect chain:')
            for i in chains: print('{} <-- ({})'.format(i, i.url))
            # 要打印域名的ip则注释上一行，并解开下面这块注释即可。
            # import socket, urllib
            # get_host_ip = lambda url:socket.gethostbyname(urllib.parse.splithost(urllib.parse.splittype(url)[1])[0])
            # for i in chains: print('{} <-- ({:<15} {})'.format(i, get_host_ip(i.url), i.url))
        else: show_info_by_response(s)
        print('\n')
    show_info(s)'''
    dhkey = '''
try:
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += ':HIGH:!DH:!aNULL'
except AttributeError:
    pass'''
    dhkeyc = '''
# try: # 当请求出现 ssl(dh key too small) 异常时，可以尝试解该处注释
#     requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
#     requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += ':HIGH:!DH:!aNULL'
# except AttributeError:
#     pass'''
    if extra and 'dh key too small' in extra:
        string = string.replace('$handle_dh_key_too_small', dhkey)
    elif extra is None:
        string = string.replace('$handle_dh_key_too_small', dhkeyc)
    else:
        string = string.replace('$handle_dh_key_too_small', '')

    desdrop = '''
# 以下补丁代码：为了兼容旧的 3DES 传输，（新标准中删除是因为存在不安全，非 requests 问题）
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
requests.adapters.HTTPAdapter.init_poolmanager = init_poolmanager
requests.adapters.HTTPAdapter.proxy_manager_for = proxy_manager_for'''
    if extra and '3des drop out stand' in extra:
        string = string.replace('$handle_3des_drop_out_stand', desdrop)
    else:
        string = string.replace('$handle_3des_drop_out_stand', '')
    return string.replace('$plus',pas).strip()


def format_request(method,c_url,c_headers,c_body,urlenc,qplus):
    return del_plus(format_req(method,c_url,c_headers,c_body,urlenc,qplus))


def format_response(r_setting,c_set,c_content,urlenc,qplus,extra):
    # 请求部分的代码
    if r_setting is not None:
        method,c_url,c_headers,c_body = r_setting
        _format = format_req(method,c_url,c_headers,c_body,urlenc,qplus)
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
                    p.append("items = []")
                    p.append("tree = etree.HTML(re.sub(r'^ *<\?xml[^<>]+\?>', '', content))")
                    p.append("for x in tree.xpath('{}'):".format(xp))
                    p.extend([' '*indent+func(i) for i in ax])
                    p.append(' '*indent+'items.append(d)')

                    p.append('')
                    p.append(' '*(max(0,indent-4)) + '''import os, time, json''')
                    p.append(' '*(max(0,indent-4)) + '''timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒''')
                    p.append(' '*(max(0,indent-4)) + '''filename = 'v{}.json'.format(timestamp) # 输出文件名(这里使用jsonlines格式存储)''')
                    p.append(' '*(max(0,indent-4)) + '#with open(filename, "a", encoding="utf-8") as f:')
                    p.append(' '*(max(0,indent-4)) + '#    for idx, d in enumerate(items):')
                    p.append(' '*(max(0,indent-4)) + '#        f.write(json.dumps(d, ensure_ascii=False)+"\\n")')
                    p.append(' '*(max(0,indent-4)) + '#        if idx % 10000 == 0: print("curr idx:", idx)')
                    func_code ='\n'.join(p)
                except:
                    import traceback
                    traceback.print_exc()
                    func_code =("print('------------------------------ split ------------------------------')\n"
                                "tree = etree.HTML(re.sub(r'^ *<\?xml[^<>]+\?>', '', content))\n"
                                "for x in tree.xpath('{}'):\n".format(xp) + 
                                "    strs = re.sub('\s+',' ',x.xpath('string(.)'))\n"
                                "    strs = strs[:40] + '...' if len(strs) > 40 else strs\n"
                                "    attr = '[ attrib ]: {} [ string ]: {}'.format(x.attrib, strs)\n"
                                "    print(attr)\n")
            if i.startswith('<auto_list_json:'):
                try:
                    func_code = get_json_code(c_content, i.replace('<auto_list_json:', '')[:-1].strip()).strip()
                except:
                    import traceback
                    traceback.print_exc()
                    func_code = ''
            if i.startswith('<just_json:'):
                func_code = "jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])\nimport pprint\npprint.pprint(jsondata, depth= None )"
            if i.startswith('<just_info:'):
                try:
                    func_code = '''def normal_tree(content,
        tags=['script','style','select','noscript','textarea']):
    e, q = etree.HTML(re.sub(r'^ *<\?xml[^<>]+\?>', '', content)), []
    for it in e.getiterator():
        if it.tag in tags or type(it.tag) is not str:
            q.append(it)
    for it in q:
        p = it.getparent()
        if p is not None:
            p.remove(it)
    return e
e = normal_tree(content)
d = {}\n'''
                    auton = 0
                    mxlen = 0
                    q = []
                    for j in c_set.splitlines()[1:]:
                        if j.strip():
                            name = re.findall('"([^"]+)"', j)
                            if name:
                                name = re.sub(r'[/\\:\*"<>\|\?-]', '_', name[0])
                            else:
                                name = 'auto_{}'.format(auton)
                                auton += 1
                            mxlen = len(name) if len(name) > mxlen else mxlen
                            q.append((name, j))
                    for name,xps in q:
                        left = ('{:<'+str(mxlen+6)+'}').format("d['{}']".format(name))
                        right = r'''= re.sub(r'\s+',' ', e.xpath('string({})'))'''.format(xps)
                        func_code += left + right + '\n'
                    func_code += 'import pprint\npprint.pprint(d, depth= None )'
                except:
                    dprint(traceback.format_exc())
        func = lambda c_:''.join(map(lambda i:'    '+i+'\n',c_.splitlines()))
        _format = _format.replace('$plus', '\n'+func(func_code)) if func_code is not None else _format
    # _format = _format if '$plus' not in _format else _format.replace('$plus','')
    return del_plus(_format,extra)






def format_scrapy_req(method,c_url,c_headers,c_body,urlenc,qplus,extra=None):
    _format_head = '''
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree$handle_3des_drop_out_stand$handle_dh_key_too_small$handle_headers_non_standard
'''
    _format_get = _format_head + '''
import re
import json
from urllib.parse import unquote_plus, quote_plus

class VSpider(scrapy.Spider):
    name = 'v'

    custom_settings = {
        'COOKIES_ENABLED': False,  # Do not use automatic cookie caching(set 'dont_merge_cookies' as True in Request.meta is same)
    }
    proxy = None # 'http://127.0.0.1:8888'

    def start_requests(self):
        def mk_url_headers():
            $x_qplus
            $c_url
            url = quote_val(url)
            $c_headers
            return url,headers
        url,headers = mk_url_headers()
        meta = {}
        meta['proxy'] = self.proxy
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
        # ps. if you use "etree.HTML(text)" and text startswith '<?xml version="1.0" encoding="utf-8"?>'
        # pls use "etree.HTML(re.sub(r'^ *<\?xml[^<>]+\?>', '', text))"

        $plus
'''

    _format_post = _format_head + '''
import re
import json
from urllib.parse import unquote_plus, quote_plus, urlencode

class VSpider(scrapy.Spider):
    name = 'v'

    custom_settings = {
        'COOKIES_ENABLED': False,  # Do not use automatic cookie caching(set 'dont_merge_cookies' as True in Request.meta is same)
    }
    proxy = None # 'http://127.0.0.1:8888'

    def start_requests(self):
        def mk_url_headers_body():
            $x_qplus
            $c_url
            url = quote_val(url)
            $c_headers
            $c_body
            return url,headers,body
        url,headers,body = mk_url_headers_body()
        meta = {}
        meta['proxy'] = self.proxy
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
        # ps. if you use "etree.HTML(text)" and text startswith '<?xml version="1.0" encoding="utf-8"?>'
        # pls use "etree.HTML(re.sub(r'^ *<\?xml[^<>]+\?>', '', text))"

        $plus
'''

    for_single_script_tail = '''\n\n\n
# 配置在单脚本情况也能爬取的脚本的备选方案，使用项目启动则下面的代码无效
if __name__ == '__main__':
    import os, time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）
    jobdir   = 'JOBDIR/$jobdir'          # 这是队列信息地址（解开 'JOBDIR'   配置注释生效）

    p = CrawlerProcess({
        'TELNETCONSOLE_ENABLED':    False,        # 几乎没人使用到这个功能，直接关闭提高爬虫启动时间
        'MEDIA_ALLOW_REDIRECTS':    True,         # 允许图片下载地址重定向，存在图片下载需求时，请尽量使用该设置
        'LOG_LEVEL':                'INFO',       # DEBUG , INFO , WARNING , ERROR , CRITICAL
        # 'JOBDIR':                   jobdir,     # 解开注释则增加断点续爬功能
                                                  # 任务队列、任务去重指纹、任务状态存储空间(简单来说就是一个文件夹)
        # 'FEED_URI':                 filename,   # 下载数据到文件
        # 'FEED_EXPORT_ENCODING':     'utf-8',    # 在某种程度上，约等于 ensure_ascii=False 的配置选项
        # 'FEED_FORMAT':              'json',     # 下载的文件格式，不配置默认以 jsonlines 方式写入文件，
                                                  # 支持的格式 json, jsonlines, csv, xml, pickle, marshal
        # 'DOWNLOAD_TIMEOUT':         8,          # 全局请求超时，默认180。也可以在 meta 中配置单个请求的超时( download_timeout )
        # 'DOWNLOAD_DELAY':           1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多
    })
    p.crawl(VSpider)
    p.start()
'''.replace('$jobdir', ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 10)))

    _format_get  = _format_get  + for_single_script_tail
    _format_post = _format_post + for_single_script_tail

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
    rep = '''def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote_plus(unquote_plus(i.group(2),encoding='$x_urlenc'),encoding='$x_urlenc').replace('+', '%2B'), url)''' if qplus == 'yes' else \
          '''def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='$x_urlenc'),encoding='$x_urlenc'), url)'''
    rep2 = '''from urllib.parse import unquote_plus, quote_plus''' if qplus == 'yes' else \
           '''from urllib.parse import unquote, quote'''
    _format = _format.replace('$x_qplus', rep)
    _format = _format.replace('''from urllib.parse import unquote_plus, quote_plus''', rep2)
    _format = _format.replace('$x_urlenc',urlenc)
    dhkey = """

from twisted.internet.ssl import AcceptableCiphers
from scrapy.core.downloader import contextfactory
contextfactory.DEFAULT_CIPHERS = AcceptableCiphers.fromOpenSSLCipherString('DEFAULT:!DH')"""
    dhkeyc = """

# from twisted.internet.ssl import AcceptableCiphers # 当请求出现 ssl(dh key too small) 异常时，可以尝试解该处注释
# from scrapy.core.downloader import contextfactory
# contextfactory.DEFAULT_CIPHERS = AcceptableCiphers.fromOpenSSLCipherString('DEFAULT:!DH')"""
    if extra and 'dh key too small' in extra:
        _format = _format.replace('$handle_dh_key_too_small', dhkey)
    elif extra is None:
        _format = _format.replace('$handle_dh_key_too_small', dhkeyc)
    else:
        _format = _format.replace('$handle_dh_key_too_small', '')

    desdrop = '''



# 注意 ! ! ! 
# 注意 ! ! ! 
# 注意 ! ! ! 
# 该请求的网页中存在非常旧的协议，导致 scrapy 有可能无法获取内容，问题源于 scrapy 依赖的 pyopenssl 库内部。
# 目前 scrapy 因为 pyopenssl 的问题暂时无法解决， requests 可以请求到内容是因为不使用 pyopenssl 进行交互。


'''
    if extra and '3des drop out stand' in extra:
        _format = _format.replace('$handle_3des_drop_out_stand', desdrop)
    else:
        _format = _format.replace('$handle_3des_drop_out_stand', '')

    headers_non_standard = r'''

# 以下补丁代码：用于预防有人可能会用 pythonw 执行 scrapy 单脚本时可能会出现的编码问题，如果直接用 python 执行该处则有无皆可。
# import io, sys; sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
# 以下补丁代码：用于预防处理 “scrapy(twisted) 对极少数的某些网站返回的不规范 headers 无法处理” 的异常情况
def lineReceived(self, line):
    if line[-1:] == b'\r': line = line[:-1]
    if self.state == u'STATUS': self.statusReceived(line); self.state = u'HEADER'
    elif self.state == u'HEADER':
        if not line or line[0] not in b' \t':
            if self._partialHeader is not None:
                _temp = b''.join(self._partialHeader).split(b':', 1)
                name, value = _temp if len(_temp) == 2 else (_temp[0], b'')
                self.headerReceived(name, value.strip())
            if not line: self.allHeadersReceived()
            else: self._partialHeader = [line]
        else: self._partialHeader.append(line)
import twisted.web._newclient
twisted.web._newclient.HTTPParser.lineReceived = lineReceived
# 以下补丁代码：解决 idna 库过于严格，导致带有下划线的 hostname 无法验证通过的异常
import idna.core
_check_label_bak = idna.core.check_label
def check_label(label):
    try: return _check_label_bak(label)
    except idna.core.InvalidCodepoint: pass
idna.core.check_label = check_label'''

    _format = _format.replace('$handle_headers_non_standard', headers_non_standard)
    return _format.strip()

def del_scrapy_plus(string):
    pas = r'''print('\n')
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
        # 请求信息
        print('===========\n| request |\n===========')
        print('request method: {}\nrequest url: {}'.format(response.request.method, response.url))
        print('------------------- request headers ---------------------')
        header_fprint(response.request.headers.to_unicode_dict())
        print('------------------- request body ------------------------')
        print(response.request.body, end='\n')
        # 返回信息
        print('============\n| response |\n============')
        print('status:', response.status, '\nresponse length: {}'.format(len(response.body)))
        print('------------------- response headers --------------------')
        header_fprint(response.headers.to_unicode_dict())
        print('------------------- response content[:1000] ----------------')
        print('response content[:1000]:\n {}'.format(response.body[:1000]))
        print('=========================================================')
        chains = response.meta.get('redirect_urls') or []
        if chains: print('redirect chain:'); [print('    '+i) for i in chains+[response.url]]
        print('\n')'''
    return string.replace('$plus',pas)

def format_scrapy_request(method,c_url,c_headers,c_body,urlenc,qplus):
    return del_scrapy_plus(format_scrapy_req(method,c_url,c_headers,c_body,urlenc,qplus))

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
    utf8len = len(re.findall('[\u4e00-\u9fa5]', content.decode('utf-8', errors='ignore')[:4096]))
    gbklen  = len(re.findall('[\u4e00-\u9fa5]', content.decode('gbk', errors='ignore')[:4096]))
    gtp = 'gb18030' if gbklen > utf8len else 'utf-8'
    err = 'encoding not in :[{}]. Guess encoding is [{},errors:ignore]'.format(','.join(etp), gtp)
    return err, content.decode(gtp, errors='ignore')

def normal_scrapy_content(content,
                   tags=['script','style','select','noscript','textarea'],
                   rootxpath='//html'):
    c = re.sub('>([^>]*[\u4e00-\u9fa5]{1,}[^<]*)<','>\g<1> <',content)
    e, q = etree.HTML(re.sub(r'^ *<\?xml[^<>]+\?>', '', c)), []
    for it in e.getiterator():
        if it.tag in tags or type(it.tag) is not str:
            q.append(it)
    for it in q:
        p = it.getparent()
        if p is not None:
            p.remove(it)
    t = e.xpath('normalize-space({})'.format(rootxpath))
    return re.sub(r'\s+',' ',t.strip())

def format_scrapy_response(r_setting,c_set,c_content,tps,urlenc,qplus,extra):
    # 请求部分的代码
    if r_setting is not None:
        method,c_url,c_headers,c_body = r_setting
        _format = format_scrapy_req(method,c_url,c_headers,c_body,urlenc,qplus,extra)
    else:
        tkinter.messagebox.showinfo('Error','Canot create code without request.')
        raise TypeError('Canot create code without request.')
    _format = _format.strip()

    if tps:
        tps,err = tps.split(' ') if len(tps.split(' '))==2 else (tps,'strict')
    else:
        tps,err = ('utf-8','strict')
    for i in c_set.splitlines():
        i = i.strip()
        if not i: continue
        func_code = None
        if i.startswith('<') and i.endswith('>'):
            if i.startswith('<normal_content:'):
                rt = re.findall('<normal_content:(.*)>', i)[0].strip()
                rt = rt if rt else '//html'
                func_code = inspect.getsource(parse_content_type).strip() + '\n\n'
                func_code += inspect.getsource(normal_scrapy_content).strip() + '\n\n'
                func_code += "_, html = parse_content_type(response.body)\n"
                func_code += "content = normal_scrapy_content(html, rootxpath='{}')\n".format(rt)
                func_code += "print(content)"
                # func_code = inspect.getsource(normal_scrapy_content).strip()
                # func_code += '''\ncontent = response.body.decode("{}",errors="{}")\ncontent = normal_scrapy_content(content, rootxpath='{}')\nprint(content)'''.format(tps,err,rt)
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
                    p.append(' '*indent+'yield d')
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
                    jsoncode = get_json_code(c_content, i.replace('<auto_list_json:', '')[:-1].strip()).strip()
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
            if i.startswith('<just_json:'):
                func_code = 'content = response.body.decode("{}",errors="{}")\n'.format(tps,err) + "jsondata = json.loads(content[content.find('{'):content.rfind('}')+1])\nimport pprint\npprint.pprint(jsondata, depth= None )"
            if i.startswith('<just_info:'):
                try:
                    func_code = '''def normal_tree(content,
        tags=['script','style','select','noscript','textarea']):
    e, q = etree.HTML((re.sub(r'^ *<\?xml[^<>]+\?>', '', content))), []
    for it in e.getiterator():
        if it.tag in tags or type(it.tag) is not str:
            q.append(it)
    for it in q:
        p = it.getparent()
        if p is not None:
            p.remove(it)
    return e
content = response.body.decode("{}",errors="{}")
e = normal_tree(content)
d = response.meta.get('_plusmeta') or {}\n'''.format(tps, err, {})
                    auton = 0
                    mxlen = 0
                    q = []
                    for j in c_set.splitlines()[1:]:
                        if j.strip():
                            name = re.findall('"([^"]+)"', j)
                            if name:
                                name = re.sub(r'[/\\:\*"<>\|\?-]', '_', name[0])
                            else:
                                name = 'auto_{}'.format(auton)
                                auton += 1
                            mxlen = len(name) if len(name) > mxlen else mxlen
                            q.append((name, j))
                    for name,xps in q:
                        left = ('{:<'+str(mxlen+6)+'}').format("d['{}']".format(name))
                        right = r'''= re.sub(r'\s+',' ', e.xpath('string({})'))'''.format(xps)
                        func_code += left + right + '\n'
                    func_code += 'import pprint\npprint.pprint(d, depth= None )\nyield d'
                except:
                    dprint(traceback.format_exc())
        func = lambda c_:''.join(map(lambda i:'        '+i+'\n',c_.splitlines())).strip()
        _format = _format.replace('$plus', func(func_code)) if func_code is not None else _format
    _format = _format if '$plus' not in _format else del_scrapy_plus(_format)
    return _format.strip()





def format_req_urllib(method,c_url,c_headers,c_body,urlenc,qplus):
    _format_head = '''
try:
    # 处理 sublime 执行时输出乱码
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
    sys.stdout._CHUNK_SIZE = 1
except:
    pass$handle_3des_drop_out_stand$handle_dh_key_too_small

import re, json
from urllib import request, parse
from urllib.parse import unquote_plus, quote_plus, urlencode
'''
    _format_get = _format_head+'''
def mk_url_headers():
    $x_qplus
    $c_url
    url = quote_val(url) # 解决部分网页需要请求参数中的 param 保持编码状态，如有异常考虑注释
    $c_headers
    return url,headers

def myget(url, headers):
    r = request.Request(url, method='GET')
    for k, v in list(headers.items()):
        if k.lower() == 'accept-encoding': 
            headers.pop(k); continue # urllib并不自动解压缩编码，所以忽略该headers字段
        r.add_header(k, v)
    proxies = None # {'http':'http://127.0.0.1:8888', 'https':'http://127.0.0.1:8888'}
    opener = request.build_opener(request.ProxyHandler(proxies))
    return opener.open(r)

url, headers = mk_url_headers()
body = None
s = myget(url, headers)
content = s.read()

$plus
#
'''
    _format_post = _format_head+'''
def mk_url_headers_body():
    $x_qplus
    $c_url
    url = quote_val(url) # 解决部分网页需要请求参数中的 param 保持编码状态，如有异常考虑注释
    $c_headers
    $c_body
    JSONString = False #，这里通常为False，极少情况需要data为string情况下的json数据，如需要，这里设置为True
    body = json.dumps(body).encode('utf-8') if JSONString else urlencode(body).encode('utf-8')
    return url,headers,body

def mypost(url, headers, body):
    r = request.Request(url, method='POST')
    for k, v in list(headers.items()):
        if k.lower() == 'accept-encoding': 
            headers.pop(k); continue # urllib并不自动解压缩编码，所以忽略该headers字段
        r.add_header(k, v)
    proxies = None # {'http':'http://127.0.0.1:8888', 'https':'http://127.0.0.1:8888'}
    opener = request.build_opener(request.ProxyHandler(proxies))
    return opener.open(r, data=body)

url, headers, body = mk_url_headers_body()
s = mypost(url, headers, body)
content = s.read()

$plus
#
'''

    func = lambda c_:''.join(map(lambda i:'    '+i+'\n',c_.splitlines()))
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
    rep = '''def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote_plus(unquote_plus(i.group(2),encoding='$x_urlenc'),encoding='$x_urlenc').replace('+', '%2B'), url)''' if qplus == 'yes' else \
          '''def quote_val(url): return re.sub(r'([\?&][^=&]*=)([^&]*)', lambda i:i.group(1)+quote(unquote(i.group(2),encoding='$x_urlenc'),encoding='$x_urlenc'), url)'''
    rep2 = '''from urllib.parse import unquote_plus, quote_plus, urlencode''' if qplus == 'yes' else \
           '''from urllib.parse import unquote, quote, urlencode'''
    _format = _format.replace('$x_qplus', rep)
    _format = _format.replace('''from urllib.parse import unquote_plus, quote_plus, urlencode''', rep2)
    _format = _format.replace('$x_urlenc',urlenc)
    return _format.strip()

def del_plus_urllib(string,extra=None):
    pas = r'''
print('\n')
print('生成 urllib 代码的功能本质就是用来解决无依赖的快速请求，用于简单的请求处理。')
print('暂无解码能力，所以自动将headers中的 accept-encoding 去除。同时也不会给出重定向链的解析功能。')
print('\n')
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
# 请求信息
print('===========\n| request |\n===========')
print('request url: {}'.format(url))
print('------------------- request headers ---------------------')
header_fprint(headers)
print('------------------- request body ------------------------')
print(body)
# 返回信息
print('============\n| response |\n============')
print('status:', s.status, '\nresponse length: {}'.format(len(content)))
print('------------------- response headers --------------------')
header_fprint(dict(s.getheaders()))
print('------------------- response content[:1000] ----------------')
print('response content[:1000]:\n {}'.format(content[:1000]))
print('=========================================================')
print('\n'*2)
'''

    # tail_xpath 这块貌似有一定的缺陷，目前就留在这里，以后有时间再看了。
    tail_xpath = '''

# 以下为 "简易xpath": 无依赖库的 xpath 解析代码，
# 为了让分析工具分析出的 xpath 在一定程度上能被无依赖库的代码使用所开发的代码片，不使用删除即可。
# 不支持轴功能，不支持任意的函数语法，简单的属性条件解析只支持 and 逻辑，其他和正常的 xpath 用法一样
import re
from html.parser import HTMLParser
class Vparser(HTMLParser):
    def __init__(s, *a, **k): super().__init__(*a, **k); s.maps = s.m = {'info':{'data':''}, 'sub':[]}; s.c = 0
    def _a(s, m):       [m.update({'m':m['m'][-1]['sub']}) for _ in range(s.c)]
    def _b(s, m, i):    (m.update({'m':m['m'][-1]['sub']}), i.append(m['m'][-1]['info']))
    def _c(s, m, i):    [s._b(m, i) for _ in range(s.c - 1)]
    def _d(s):          m = {}; m['m'] = s.m['sub']; s._a(m); return m['m']
    def _e(s, a=0):     m = {}; m['m'] = s.m['sub'];i = []; s._c(m, i); return i if a else m['m'][-1]['info']
    def _f(s):          s._d().append({'info':{'data':''}, 'sub':[]}); s.c += 1
    def _g(s, t, a=0):  c = s._e(); c['tag'], c['attrs'] = t, dict(a)
    def _h(s, c, d):    c.update({'data':d}) if 'data' not in c else c.update({'data':c['data'] + d})
    def _i(s, d):       return [s._h(c, d) for c in s._e(True)] if s._e(True) else 0
    def _j(s, t):       return True if t in ['br','meta','link'] else False
    def handle_starttag(s, t, a): s.handle_startendtag(t, a) if s._j(t) else (s._f(), s._g(t, a))
    def handle_endtag(s, t): s.c -= 1
    def handle_startendtag(s, t, a): s._f(); s._g(t, a); s.c -= 1
    def handle_data(s, d): s._i(d)
class Vnode:
    def __init__(self, mapsdict): self.maps = mapsdict
    def __repr__(self): r = self.maps['info'].get('data'); return "<class 'Vnode' data={}>".format(repr(r.strip()[:10])[:-1]+"...'" if r else None)
    def find_by_maps(self, maps, tag='*', attrs={}, depth=float('inf'), one=None):
        r = []
        def _a(s, t):       return all([i not in t for i in s.split('|')])
        def _b(s, n):       return (_a(s[1:],n) if s.startswith('*') else s != n) and s != '*'
        def _c(k, i, v):    return k not in i['attrs'] or _b(v, i['attrs'][k])
        def _d(n):          return any([_c(k, n['info'], v) for k,v in attrs.items()])
        def _e(n):          return not _d(n) and not _b(tag, n['info']['tag'])
        def _f(ns, d=0):    [(r.append(n) if _e(n) else 0, _f(n,d+1)) for n in ns['sub']] if d < depth else 0
        return _f(maps) or (([r[one]] if len(r) > one else []) if type(one) == int else r)
    def xpath(self, x):
        def _pc(k, m, d, n):
            x = float('inf') if k.startswith('//') else 1; o = re.findall(r'\d+', d); o = int(o[0]) if o else None
            p = r'@([a-zA-Z_][a-zA-Z_0-9]+) *= *"([^"]+)"'; q = p.replace('"',"'"); b = p.split(' ',1)[0]+'( *)$'
            w = re.findall(p, n) + re.findall(q, n) + [(x, '*') for x,y in re.findall(b, n)]
            r1 = ('r', dict(w)) if w else (None, {}); c = re.findall(r'@([a-zA-Z_][a-zA-Z_0-9]+) *$', m)
            r2 = ('c', ['attrs', c[0]]) if c and c[0] == m.strip('@ ') else (('c', ['data']) if m.strip() == 'text()' else (None, {}))
            return x, o, m, r1 if r1[0] else r2
        p = re.findall(r'(//?)([^/[\[\]]+)(\[ *\d+ *\])?(\[[^/\[\]]+\])?', x); r = {}; ms = [self.maps]
        for i, (k, m, d, n) in enumerate(p, 1):
            r[i] = []; d, o, m, (g, a) = _pc(k, m, d, n)
            if (i != len(p) or i == 1): [r[i].extend(self.find_by_maps(s, m, attrs=a, depth=d, one=o)) for s in ms]
            elif g == 'r':              [r[i].extend(self.find_by_maps(s, m, attrs=a, depth=d, one=o)) for s in ms]
            else: [r[i].append(s['info']['attrs'].get(a[1]) if a[0] =='attrs' else (s['info']['data'] if a[0] =='data' else None) if a else s) for s in ms]
            ms = r[i]; r[i - 1] = None
        return [Vnode(i) if type(i) == dict else i for i in ms]
class VHTML:
    def __init__(self, hc): self.pr = Vparser(); self.pr.feed(hc); self.root = Vnode(self.pr.maps)
    def xpath(self, x): return self.root.xpath(x)

# v = VHTML(content.decode())
# for i in v.xpath('//*/@href'): print(i)
'''
    dhkey = """
import ssl
ssl._DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'"""
    dhkeyc = """
# import ssl # 当请求出现 ssl(dh key too small) 异常时，可以尝试解该处注释
# ssl._DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'"""
    if extra and 'dh key too small' in extra:
        string = string.replace('$handle_dh_key_too_small', dhkey)
    elif extra is None:
        string = string.replace('$handle_dh_key_too_small', dhkeyc)
    else:
        string = string.replace('$handle_dh_key_too_small', '')
    desdrop = '''



# 注意 ! ! ! 
# 注意 ! ! ! 
# 注意 ! ! ! 
# 该请求的网页中存在非常旧的协议，可能导致请求失败，如果工具能正常请求到内容，请使用 requests 获取数据


'''
    if extra and '3des drop out stand' in extra:
        string = string.replace('$handle_3des_drop_out_stand', desdrop)
    else:
        string = string.replace('$handle_3des_drop_out_stand', '')
    return string.replace('$plus',pas).strip()

def format_request_urllib(method,c_url,c_headers,c_body,urlenc,qplus,extra=None):
    return del_plus_urllib(format_req_urllib(method,c_url,c_headers,c_body,urlenc,qplus),extra)


















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
                key = '[contains(@class, "{}")]'.format(elass)
                # key = '[@class="{}"]'.format(elass)
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
        q = re.sub(r'\[\d+\]','',xp)#.rsplit('/',1)[0]
        if q not in s:
            s[q] = [[xp, sxp, key]]
        else:
            s[q].append([xp, sxp, key])
    rm = []
    for px in sorted(s,key=lambda i: -len(i)):
        xps,sxps,keys = zip(*s[px])
        # if len(sxps) == len(set(sxps)): continue # 后续发现这行妨碍了分析，注释即可。
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
                    if b.endswith(a.replace(v,'')): # 你看不懂这里的修改也不要在意，因为我也已经开始看不懂了，只要知道这里的修改是有用的就行。
                        t = b
                    else:
                        t = '/{}{}'.format(a.replace(v,''),c) + b.split(c,1)[1]
                        t = t if t.startswith('//') else '/' + t
                    p[i][idx][1] = t
                    p[i][idx].append(px)
                    yield j

def get_xpath_by_str(strs, html_content):
    e = etree.HTML(re.sub(r'^ *<\?xml[^<>]+\?>', '', html_content))
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
        try:
            v = e.xpath('string({})'.format(xp))
        except:
            continue
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
        c = None
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
        d[i]['xtree'] = x + (c or "")
    for i in d:
        yield d[i]['xtree'],[(i['path'],i['content']) for i in d[i]['info']]


# 这里的代码应该会是最后一次对自动列表解析处理的精准度的提升
# 以各种函数处理将解析上升到像是对json列表解析一样的高度
def auto_xpath(oxp,content,_type=None):
    tps = ['href', 'title', 'src']
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
                    tags=['script','style','select','noscript','textarea'],):
        e = etree.HTML(re.sub(r'^ *<\?xml[^<>]+\?>', '', content))
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
    # 貌似这块的过滤没有起到作用，甚至妨碍了部分解析解析不到内容。
    # f = {}
    # for i in e.items():
    #     v = str(i[1])
    #     if v not in f: f[v] = []
    #     f[v].append(i[0])
    # p = []
    # for i in f.items():
    #     if len(i[1]) > 1:
    #         p.extend(sorted(i[1],key=lambda i:-len(i))[1:])
    # for i in p:
    #     e.pop(i)
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
            try:
                k = func('str_' + re.findall('[a-zA-Z0-9]+', k)[0]) if i != 'string(.)' else 'str_all'
                q.append((k,v,len(e[i])))
            except:
                pass
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
        fmt2 = 'if {:<'+str(l+2)+'''} in d: d[{:<'''+str(l+2)+'''}] = re.sub(r'\s+',' ',d["{}"]).strip()'''
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
        lens, (okey, iner) = p
        mx,okey,sortkeys = analisys_key_sort(p)
        ret = '[cnt:{}] jsondata{}\n'.format(lens, okey)
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
        ret = '[cnt:{}] jsondata{}\n'.format(lens, okey)
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

def get_json_code(content, parsestring=None):
    s,tp = parse_json_content(content)
    p = get_parse_list(s)
    if not parsestring:
        p = get_max_len_list(p)
        if p[0] == 0: return ''
        standard = True if all(map(lambda i:type(i)==dict,p[1][1])) else False
        return format_json_parse_code(p,standard,tp)
    else:
        for i in p:
            lens = p[i]['lens']
            iner = p[i]['iner']
            x = lens, (i, iner)
            if lens == 0: continue
            standard = True if all(map(lambda i:type(i)==dict,iner)) else False
            if 'jsondata'+i == parsestring:
                return format_json_parse_code(x,standard,tp)


def get_json_show(content):
    s,tp = parse_json_content(content)
    p = get_parse_list(s)
    v = []
    for i in p:
        lens = p[i]['lens']
        iner = p[i]['iner']
        x = lens, (i, iner)
        if lens == 0: continue
        standard = True if all(map(lambda i:type(i)==dict,iner)) else False
        v.append([format_json_parse_show(x,standard), lens])
    v = sorted(v, key=lambda i:i[1])[::-1]
    v = [i[0] for i in v][:10]
    return '\n\n'.join(v)

    # 之前只显示最长的列表，所以之前的代码将抛弃
    # p = get_max_len_list(p)
    # if p[0] == 0: return ''
    # standard = True if all(map(lambda i:type(i)==dict,p[1][1])) else False
    # return format_json_parse_show(p,standard)