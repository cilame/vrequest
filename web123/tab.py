import tkinter
from tkinter import ttk

from root import root

nb = ttk.Notebook(root)
nb.place(relx=0, rely=0, relwidth=1, relheight=1)


def bind_frame(frame, name=None):
    frame.master = nb
    name = name if name is not None else frame._name
    nb.add(frame, text=name)


def clear_curr_tab():
    nb.forget(nb.select())



test_frame_1 = tkinter.Frame()
tblb1 = tkinter.Label(test_frame_1, text='简单的 Label 用以测试框架')
tblb1.pack() # 在frame 内部的组件要进行展示处理

test_frame_2 = tkinter.Frame()
tblb2 = tkinter.Label(test_frame_2, text='简单的 Label2 用以测试框架')
tblb2.pack()