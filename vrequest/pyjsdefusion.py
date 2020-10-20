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
    mainjs = os.path.join(os.path.dirname(__file__), 'main.js')
    unzip_single(astjs, hnode)
    # 加载代码到空间
    def get_node_ctx():
        global ctx
        if ctx:
            return ctx
        with open(mainjs, encoding='utf-8') as f:
            jscode = f.read()
        ctx = execjs.compile(jscode, cwd=hnode)
        return ctx

import sys
from subprocess import Popen, PIPE
import execjs
_bak_exec_with_pipe = execjs._external_runtime.ExternalRuntime.Context._exec_with_pipe
def _exec_with_pipe(self, source):
    cmd = self._runtime._binary()
    p = None
    try:
        # 这里 Popen 里面的 encoding='utf-8' 在源码里面没有，所以用了偏 geek 的方式将这里钩住处理
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=self._cwd, 
                    universal_newlines=True, encoding='utf-8') 
        input = self._compile(source)
        stdoutdata, stderrdata = p.communicate(input=input)
        ret = p.wait()
    finally:
        del p
    self._fail_on_non_zero_status(ret, stdoutdata, stderrdata)
    return stdoutdata
def hook_popen_encoding():
    execjs._external_runtime.ExternalRuntime.Context._exec_with_pipe = _exec_with_pipe
def back_popen_encoding():
    execjs._external_runtime.ExternalRuntime.Context._exec_with_pipe = _bak_exec_with_pipe




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
