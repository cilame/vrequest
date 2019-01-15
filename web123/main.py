from root import root
from menu import (
    bind_menu,
    test_command_1, # 函数方法
    test_command_2,
)

from tab import (
    bind_frame,
    test_frame_1, # frame 对象
    test_frame_2,
    clear_curr_tab,
)

from frame import (
    test_mkfr,
)


# 将函数方法绑定右键菜单，方便插拔
bind_menu(test_command_1) # 第二个参数默认为方法名字，请尽量填写保证意义
bind_menu(test_command_2,'你好')
# 将框架绑定 tab 标签，实现目前期望的开发，方便插拔
bind_frame(test_frame_1) # 第二个参数默认为tab名字，请尽量填写保证意义
bind_frame(test_frame_2,'标签二')
bind_frame(test_mkfr(),'标签三')
# 测试右键菜单删除 tab 标签
def clear2():
    test_frame_2.destroy()
bind_menu(clear2,'清除标签二')
bind_menu(clear_curr_tab,'删除当前标签')



root.title('web123')
root.geometry('500x300')
root.mainloop()