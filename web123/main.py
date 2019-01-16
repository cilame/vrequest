
from root import root
from menu import bind_menu
from tab import bind_frame,clear_curr_tab
from combinekey import bind_ctl_key

# 这里的框架就是目前需要设计处理的图形内容
from frame import (
    test_mkfr,
    request_window,
)




# ================= 测试部分内容 =====================
import tkinter
def test_command_1():
    print('test command 1.')
def test_command_2():
    print('test command 2.')

test_frame_1 = tkinter.Frame()
tblb1 = tkinter.Label(test_frame_1, text='简单的 Label 用以测试框架')
tblb1.pack() # 在frame 内部的组件要进行展示处理

test_frame_2 = tkinter.Frame()
tblb2 = tkinter.Label(test_frame_2, text='简单的 Label2 用以测试框架')
tblb2.pack()

# 将函数方法绑定右键菜单，方便插拔
bind_menu(test_command_1) # 第二个参数默认为方法名字，请尽量填写保证意义
bind_menu(test_command_2,'你好')
# 将框架绑定 tab 标签，实现目前期望的开发，方便插拔
bind_frame(test_frame_1) # 第二个参数默认为tab名字，请尽量填写保证意义
bind_frame(test_frame_2,'标签二')
bind_frame(test_mkfr(),'标签三')
bind_frame(request_window(),'标签四')
# 测试右键菜单删除 tab 标签
def clear2():
    test_frame_2.destroy()
bind_menu(clear2,'清除标签二')
bind_menu(clear_curr_tab,'删除当前标签')

bind_ctl_key(clear_curr_tab,'w')
# ================= 测试部分内容 =====================




root.title('web123')
root.geometry('500x300')
root.mainloop()