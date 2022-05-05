# mini requests @author: vilame
def mini_requests(defaultencode='utf-8'):
    def requests(method):
        import ssl, json
        from urllib import request, error
        from urllib.parse import quote
        class resper:
            def __init__(self, url, res, req, encode, errormsg=None):
                self.url = url
                self.resb = res.read()
                self.status_code = res.status
                self.dectype = encode
                self.errormsg = errormsg
                self.request = req
                self.headers = dict(res.getheaders())
            def __getattr__(self, name):
                if name == 'content': return self._content()
                if name == 'text': return self._text()
            def __str__(self): return '<Response [{}]>'.format(self.status_code)
            def _content(self): return self.resb
            def _text(self): return self.resb.decode(self.dectype, errors='ignore')
            def json(self): return json.loads(self.resb)
        def func(url, headers=None, data=None, verify=True, proxies=None, encode=defaultencode):
            req = request.Request(url, method=method)
            if type(data) == dict: data = '&'.join(['{}={}'.format(quote(k), quote(v)) for k, v in data.items()]).encode()
            if type(data) == str: data = data.encode()
            req.body = data or b''
            headers = headers or {}
            for k, v in list(headers.items()):
                if k.lower() == 'accept-encoding': 
                    headers.pop(k); continue
                req.add_header(k, v)
            lis = [request.ProxyHandler(proxies)]
            if not verify:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                lis.append(request.HTTPSHandler(context = ctx))
            opener = request.build_opener(*lis)
            errormsg = None
            try:
                ret = opener.open(req) if method == 'GET' else opener.open(req, data=data)
            except error.HTTPError as e:
                class err: 
                    def __init__(self, status, headers, body=b''): 
                        self.status = status
                        self.read = lambda:body
                        self.getheaders = lambda: headers
                ret = err(e.getcode(), e.headers.items(), e.file.read()); errormsg = e.msg
            return resper(url, ret, req, encode, errormsg)
        return func
    requests.get = requests('GET')
    requests.post = requests('POST')
    return requests
requests = mini_requests()