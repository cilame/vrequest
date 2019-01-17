
from root import (
    root,
    config,
    change_siz,
)
from menu import bind_menu
from tab import (
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




# ================= 测试部分内容 =====================
# === 初始化 ===
#config['set']
setting=None # 初始化需要通过config来获取各个setting配置
bind_frame(request_window(setting),'标签2')
bind_frame(request_window(setting),'标签3')

# === 创建/删除/帮助 ===
# 右键菜单删除 tab 标签，快捷键删除
bind_menu(delete_curr_tab,'删除当前标签')
bind_ctl_key(delete_curr_tab,'w')
# 右键菜单创建标签标签，快捷键创建（创建函数内setting默认为None）
bind_menu(create_new_tab,'创建新的标签')
bind_ctl_key(create_new_tab,'c')
# 右键菜单帮助，快捷键帮助
bind_menu(create_helper,'帮助文档标签')
bind_ctl_key(create_helper,'h')
# 改名
bind_menu(change_tab_name,'改当前标签名')
bind_ctl_key(change_tab_name,'e')
# 发送请求任务
bind_menu(send_request,'发送请求任务')
bind_ctl_key(send_request,'s')
# ================= 测试部分内容 =====================







root.title('vrequest')
root.geometry(config['siz'])
root.bind('<Configure>',lambda e:change_siz())
root.mainloop()