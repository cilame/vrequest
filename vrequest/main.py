import os
import sys

from . import __version__

from .root import (
    root,
    config,
    change_siz,
)
from .menu import bind_menu
from .tab import (
    nb,
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
    execute_code,
    execute_scrapy_code,
    create_js_parse,
    execute_js_code,
    create_encoder,
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
bind_menu(create_new_reqtab,'创建请求标签 [Ctrl+q]')
bind_menu(delete_curr_tab,  '删除当前标签 [Ctrl+w]')
bind_menu(change_tab_name,  '改当前标签名 [Ctrl+e]')
bind_menu(save_config,      '保存配置快照 [Ctrl+s]')
bind_menu(create_js_parse,  '创建 js解析页 [Ctrl+j]')
bind_menu(create_helper,    '帮助文档标签 [Ctrl+h]')
bind_menu(create_encoder,   '创建便捷加密编码窗口')

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

# 绑定 response 事件
bind_alt_key(create_new_rsptab,     'r')
bind_alt_key(create_test_code,      'c') # 生成代码
bind_alt_key(get_html_pure_text,    'd') # 获取文本
bind_alt_key(get_xpath_elements,    'x') # 获取xpath
bind_alt_key(get_auto_xpath,        'f') # 解析路径xpath
bind_alt_key(get_auto_json,         'z') # 解析json数据
bind_alt_key(execute_code,          'v') # 代码执行
bind_alt_key(create_scrapy_code,    's') # 生成scrapy代码
bind_alt_key(execute_scrapy_code,   'w') # 用自动生成的环境执行scrapy代码


def execute():
    argv = sys.argv
    if 'e' in argv:
        from .frame import encode_window
        fr = encode_window()
        fr.title('命令行输入 vv e 则可快速打开便捷加密窗口')
        fr.bind('<Escape>',lambda *a:fr.master.quit())
        fr.protocol("WM_DELETE_WINDOW",lambda *a:fr.master.quit())
        fr.master.withdraw()
        fr.mainloop()
        return

    root.title('vrequest [{}]'.format(__version__))
    ico = os.path.join(os.path.split(__file__)[0],'ico.ico')
    root.iconbitmap(ico)
    root.geometry(config.get('siz') or '600x725+100+100')
    root.bind('<Configure>',lambda e:change_siz())
    root.bind('<Escape>',lambda e:switch_response_log())
    root.mainloop()

if __name__ == '__main__':
    execute()