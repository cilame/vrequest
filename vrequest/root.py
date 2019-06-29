import os
import tkinter
import json
import traceback

root = tkinter.Tk()

# 配置文件名字
DEFAULTS_NAME = '.vrequest'
DEFAULTS_HEADERS = '''
accept-encoding: gzip, deflate
accept-language: zh-CN,zh;q=0.9
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36
'''
# TODO, 一般新建请求页的时候需要的默认值，方便使用。

'''
#20190117
    # 1 边框大小位置
    # 2 需要的配置数据
    # 初步定下下面的数据结构
    {
        siz:'500x300'
        set:{
            tab_name1:{setting}
            tab_name2:{setting}
            tab_name3:{setting}
        }
    }
    关于 setting的数据结构
    {
        type:request # 这里要有多种类型的配置，为了方便处理保存和恢复选择用的函数
        set:{
            # 不同类型的配置结构不一样
            # 以 request为例，
            method: GET/POST/...
            url: url
            headers: headers
            body: body
            # 也有帮助标签
        }
    }
'''


# 默认的数据结构
config = {
    'siz':'600x725+200+200',
    'set':{},
    'focus':None,
}


# 用来配置一些需要持久化的配置
def get_config_from_homepath():
    global config
    defaults_conf = config.copy()
    try:
        home = os.environ.get('HOME')
        home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
        configfile = os.path.join(home,DEFAULTS_NAME)
        if os.path.exists(configfile):
            with open(configfile,encoding='utf-8') as f:
                defaults_conf = json.load(f)
                config = defaults_conf
    except:
        print('unlocal homepath.')
        traceback.print_exc()


# 修改本地的默认配置，让其变成一个全局可用参数
get_config_from_homepath()


# 用来持久化当前配置的情况，简单的快照，便于使用
def set_config_from_homepath():
    global config
    defaults_conf = config
    try:
        home = os.environ.get('HOME')
        home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
        configfile = os.path.join(home,DEFAULTS_NAME)
        with open(configfile,'w',encoding='utf-8') as f:
            f.write(json.dumps(defaults_conf,indent=4))
    except:
        print('unlocal homepath.')
        traceback.print_exc()


# 装饰器
# 装饰函数在执行时候进行持久化当前配置的操作（通常在请求 url 时候进行保存）
def save(func):
    def _save(*a,**kw):
        v = func(*a,**kw)
        set_config_from_homepath()
        return v
    return _save



# 绑定窗口大小变化，让配置也能记录窗口状态。
def change_siz():
    global config
    config['siz'] = '{}x{}+{}+{}'.format(
        root.winfo_width(),
        root.winfo_height(),
        root.winfo_x(),
        root.winfo_y(), )
