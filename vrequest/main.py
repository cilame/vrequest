
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
    cancel_delete,
    create_new_reqtab,
    create_new_rsptab,
    create_helper,
    change_tab_name,
    send_request,
    save_config,
    switch_response_log,
    create_test_code,
    get_html_pure_text,
)
from combinekey import (
    bind_ctl_key,
    bind_alt_key,
)

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
bind_menu(create_new_reqtab,'创建新的标签')
bind_menu(delete_curr_tab,  '删除当前标签')
bind_menu(change_tab_name,  '改当前标签名')
bind_menu(save_config,      '保存配置快照')
bind_menu(send_request,     '发送请求任务')
bind_menu(create_helper,    '帮助文档标签')
# 绑定 Ctrl + key 的组合键
bind_ctl_key(create_new_reqtab, 'q')
bind_ctl_key(delete_curr_tab,   'w')
# 撤销 ctrl + shift + w （必须是保存过的配置，并且撤销队列在程序关闭后就清空）
bind_ctl_key(cancel_delete,     'w',shift=True)
bind_ctl_key(change_tab_name,   'e')
bind_ctl_key(save_config,       's')
bind_ctl_key(send_request,      'r')
bind_ctl_key(create_helper,     'h')

# 绑定 response 事件
bind_alt_key(create_new_rsptab, 'r')
bind_alt_key(create_test_code,  'c') # 生成代码
bind_alt_key(get_html_pure_text,'d') # 获取文本









root.title('vrequest')
root.geometry(config['siz'])
root.bind('<Configure>',lambda e:change_siz())
root.bind('<Escape>',lambda e:switch_response_log())
root.mainloop()