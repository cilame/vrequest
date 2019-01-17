
from root import (
    root,
    config,
    change_siz,
)
from menu import bind_menu
from tab import (
    nb,
    bind_frame,
    delete_curr_tab,
    create_new_tab,
    create_helper,
    change_tab_name,
    send_request,
)
from combinekey import bind_ctl_key

# 这里的框架就是目前需要设计处理的图形内容
from frame import (
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
bind_menu(delete_curr_tab,  '删除当前标签')
bind_menu(create_new_tab,   '创建新的标签')
bind_menu(create_helper,    '帮助文档标签')
bind_menu(change_tab_name,  '改当前标签名')
bind_menu(send_request,     '发送请求任务')
# 绑定 Ctrl + key 的组合键
bind_ctl_key(delete_curr_tab,   'w')
bind_ctl_key(create_new_tab,    'r')
bind_ctl_key(create_helper,     'h')
bind_ctl_key(change_tab_name,   'e')
bind_ctl_key(send_request,      's')


root.title('vrequest')
root.geometry(config['siz'])
root.bind('<Configure>',lambda e:change_siz())
root.mainloop()