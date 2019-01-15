from tkinter import ttk
from tkinter import scrolledtext



def test_mkfr():
    fr = ttk.Frame()
    sb = scrolledtext.ScrolledText(fr)
    sb.pack()
    return fr



# 现在主要就是设计这里的 Frame 结构。
