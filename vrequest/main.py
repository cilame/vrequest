import os
import sys

from . import __version__

from .root import (
    root,
    config,
    change_siz,
    tails,
)
from .menu import bind_menu
from .tab import (
    nb,
    nb_names,
    bind_frame,
    delete_curr_tab,
    cancel_delete,
    create_new_reqtab,
    create_new_rsptab,
    create_helper,
    change_tab_name,
    send_request,
    save_config,
    switch_response_log,
    create_test_code,
    create_scrapy_code,
    get_html_pure_text,
    get_xpath_elements,
    get_auto_xpath,
    get_auto_json,
    choice_auto_json,
    execute_code,
    execute_scrapy_code,
    create_js_parse,
    create_selenium_parse,
    create_temp_idle,
    create_cmd_idle,
    create_encoder,
    create_test_code_urllib,
    pyset_pypi_gui,
)
from .combinekey import (
    bind_ctl_key,
    bind_alt_key,
)

# 这里的框架就是目前需要设计处理的图形内容
from .frame import (
    helper_window,
    request_window,
)


# === 初始化 ===
settings = config['set']
if not settings:
    create_helper()
else:
    for key,setting in settings.items():
        if setting.get('type') == 'request':
            tab_id = bind_frame(request_window(setting),key)
            if key == config['focus']:
                nb.select(tab_id) # 保持最后执行成功时的 tab 焦点


# === 创建/删除/帮助 ===
# 绑定右键菜单
bind_menu(create_new_reqtab,      '创建请求标签 [Ctrl+q]')
bind_menu(delete_curr_tab,        '删除当前标签 [Ctrl+w]')
bind_menu(change_tab_name,        '改当前标签名 [Ctrl+e]')
bind_menu(save_config,            '保存配置快照 [Ctrl+s]')
bind_menu(create_js_parse,        '创建 js解析页 [Ctrl+j]')
bind_menu(create_helper,          '帮助文档标签 [Ctrl+h]')
bind_menu(create_selenium_parse,  '浏览器执行窗 [Alt+w]*')
bind_menu(create_encoder,         '创建便捷加密编码窗口')
bind_menu(pyset_pypi_gui,         '设置全局 pypi 下载源')

# 绑定 Ctrl + key 的组合键
bind_ctl_key(create_new_reqtab, 'q')
bind_ctl_key(delete_curr_tab,   'w')
# 撤销 ctrl + shift + w （必须是保存过的配置，并且撤销队列在程序关闭后就清空）
bind_ctl_key(cancel_delete,     'w',shift=True)
bind_ctl_key(change_tab_name,   'e')
bind_ctl_key(save_config,       's')
bind_ctl_key(send_request,      'r')
bind_ctl_key(create_helper,     'h')
bind_ctl_key(create_js_parse,   'j')
bind_ctl_key(create_cmd_idle,   '`')

def _scrapy_or_selenium():
    _select = nb.select()
    cname = nb_names.get(_select)['name']
    ctype = (nb_names.get(_select).get('setting') or {}).get('type')
    # 如果当前窗口是 scrapy 代码窗口则代表直接项目执行 scrapy 代码，否则创建 selenium 窗口。
    create_selenium_parse() if ctype != 'scrapy' else execute_scrapy_code()

# 绑定 response 事件
bind_alt_key(create_new_rsptab,         'r')
bind_alt_key(create_test_code,          'c') # 生成代码
bind_alt_key(get_html_pure_text,        'd') # 获取文本
bind_alt_key(get_xpath_elements,        'x') # 获取xpath
bind_alt_key(get_auto_xpath,            'f') # 解析路径xpath
bind_alt_key(get_auto_json,             'z') # 分析json列表
bind_alt_key(choice_auto_json,          'q') # 选则json列表
bind_alt_key(execute_code,              'v') # 代码执行
bind_alt_key(create_scrapy_code,        's') # 生成scrapy代码
bind_alt_key(_scrapy_or_selenium,       'w') # 用自动生成的环境执行scrapy代码
bind_alt_key(create_temp_idle,          '`') # 使用临时的idle文本
bind_alt_key(create_test_code_urllib,   'u') # 生成 urllib(py3) 请求的代碼










def algo():
    from .frame import encode_window
    fr = encode_window()
    ico = os.path.join(os.path.split(__file__)[0],'ico.ico')
    fr.iconbitmap(ico)
    fr.title('命令行输入 ee 则可快速打开便捷加密窗口(为防冲突，输入vv e也可以打开), 组合快捷键 Alt+` 快速打开IDLE')
    fr.bind('<Escape>',lambda *a:fr.master.quit())
    fr.bind('<Alt-`>',lambda *a:create_temp_idle())
    fr.bind('<Control-`>',lambda *a:create_cmd_idle())
    fr.protocol("WM_DELETE_WINDOW",lambda *a:fr.master.quit())
    fr.master.withdraw()
    fr.mainloop()


escodegen = None
def execute():
    argv = sys.argv
    if 'e' in argv:
        algo()
        return

    def preimport():
        global escodegen
        import time
        time.sleep(.5) # 需要花点时间导包的部分，用别的线程进行预加载，增加工具顺滑度
        try: import js2py
        except: pass
        try: import execjs
        except: pass
        try: 
            import js2py.py_node_modules.escodegen as escodegen
        except: pass
    import threading
    threading.Thread(target=preimport).start()

    root.title('vrequest [{}]'.format(__version__))
    ico = os.path.join(os.path.split(__file__)[0],'ico.ico')
    root.iconbitmap(ico)
    root.geometry(config.get('siz') or '600x725+100+100')
    root.bind('<Configure>',lambda e:change_siz())
    root.bind('<Escape>',lambda e:switch_response_log())

    def quit_():
        try:
            for tail in tails:
                try:
                    tail()
                except:
                    import traceback
                    print(traceback.format_exc())
        finally:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW",lambda *a: quit_())
    root.mainloop()

if __name__ == '__main__':
    execute()