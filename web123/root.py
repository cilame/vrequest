import tkinter
root = tkinter.Tk()

# 配置文件名字
DEFAULTS_NAME = '.web123'
DEFAULTS_HEADERS = None 
# TODO, 一般新建请求页的时候需要的默认值，方便使用。

# 用来配置一些需要持久化的配置
def get_config_from_homepath():
    defaults_conf = {}
    try:
        home = os.environ.get('HOME')
        home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
        configfile = os.path.join(home,DEFAULTS_NAME)
        if os.path.exists(configfile):
            with open(configfile,encoding='utf-8') as f:
                defaults_conf = json.load(f)
    except:
        print('unlocal homepath.')
        defaults_conf = {}
    return defaults_conf


def get_current_settings():
    # TODO
    # 先要设计出一个更好的快照存储的数据结构，后面才能顺利进行下去。
    return {}


# 用来持久化当前配置的情况，简单的快照，便于使用
def set_config_from_homepath():
    defaults_conf = get_current_settings()
    try:
        home = os.environ.get('HOME')
        home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
        configfile = os.path.join(home,DEFAULTS_NAME)
        with open(configfile,encoding='utf-8') as f:
            f.write(json.dumps(defaults_conf))
    except:
        print('unlocal homepath.')
        defaults_conf = {}
    return defaults_conf


# 装饰器
# 装饰函数在执行时候进行持久化当前配置的操作（通常在请求 url 时候进行保存）
def save(func):
    def _save(*a,**kw):
        # TODO
        # 保存当前的数据结构，持久化
        return func(*a,**kw)
    return _save