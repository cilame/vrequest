import os
os.environ['EXECJS_RUNTIME'] = 'Node'
ctx = None

import execjs
if not execjs._external_runtime.node().is_available():
    # 检测node环境是否安装
    raise '[ !!! ] node is not available, pls install node.'
else:
    # 解压文件到目标地址
    import sys, os, zipfile
    def unzip_single(src_file, dest_dir, password=None):
        if password:
            password = password.encode()
        zf = zipfile.ZipFile(src_file)
        try:
            zf.extractall(path=dest_dir, pwd=password)
        except RuntimeError as e:
            print(e)
        zf.close()
    home = os.environ.get('HOME')
    home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
    hnode = os.path.join(home, '.vrequest_node')
    astjs = os.path.join(os.path.dirname(__file__), 'astjs.zip')
    unzip_single(astjs, hnode)
    # 加载代码到空间
    def get_node_ctx():
        global ctx
        if ctx:
            return ctx
        filepath = hnode
        mainjs = os.path.join(filepath, 'main.js')
        with open(mainjs, encoding='utf-8') as f:
            jscode = f.read()
        ctx = execjs.compile(jscode, cwd=filepath)
        return ctx

if __name__ == '__main__':
    code = r'''
function s1(a,b){
    return a+b
}
function s2(a,b){
    return a*b
}
s2(s1(1,3), s1(2,4))
'''
    ctx = get_node_ctx()
    v = ctx.call('muti_process_defusion', code) # 解混淆函数
    print(v)
