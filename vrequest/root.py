import os
import tkinter
import json
import traceback

root = tkinter.Tk()

# 配置文件名字
DEFAULTS_NAME = '.vrequest'
DEFAULTS_HEADERS = None 
# TODO, 一般新建请求页的时候需要的默认值，方便使用。

'''
#20190117
考虑到插入的顺序的问题，所以需要一个数字id来标识创建的顺序
这样在重启时候也会保持创建顺序的去获取配置结构，即便是中间有删除也能保持顺序
    # 1 配置顺序id
    # 2 边框大小
    # 3 需要的配置数据
    # 初步定下下面的数据结构
    {
        idx:0
        siz:'500x300'
        set:{
            id1:{setting}
            id2:{setting}
            id3:{setting}
        }
    }
'''


# 默认的数据结构
config = {
    'idx':0,
    'siz':'500x300',
    'set':{

    },
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
        set_config_from_homepath()
        return func(*a,**kw)
    return _save



# 绑定窗口大小变化，让配置也能记录窗口状态。
def change_siz():
    global config
    config['siz'] = '{}x{}+{}+{}'.format(
        root.winfo_width(),
        root.winfo_height(),
        root.winfo_x(),
        root.winfo_y(), )



