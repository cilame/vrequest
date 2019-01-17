import tkinter
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.font import Font

# 测试两种 Text 效果
Text = scrolledtext.ScrolledText
#Text = tkinter.Text

# 测试两种 Frame 效果
Frame = ttk.Frame
Frame = tkinter.Frame

pdx = 0
pdy = 0
lin = 4




def request_window(setting=None):
    fr = Frame()
    ft = Font(family='Consolas',size=10)
    
    temp_fr1 = Frame(fr,highlightthickness=lin)    
    sb1 = Text(temp_fr1,height=1,width=1,font=ft)
    sb2 = Text(temp_fr1,height=1,width=1,font=ft)
    sb1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.LEFT,padx=pdx,pady=pdy)
    sb2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.LEFT,padx=pdx,pady=pdy)
    temp_fr1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)

    temp_fr2 = Frame(fr,highlightthickness=lin)
    btn1 = ttk.Button(temp_fr2,text='btn1')
    btn2 = ttk.Button(temp_fr2,text='btn2')
    btn1.pack(side=tkinter.LEFT,padx=pdx,pady=pdy)
    btn2.pack(side=tkinter.RIGHT,padx=pdx,pady=pdy)
    temp_fr2.pack(fill=tkinter.X,side=tkinter.TOP)

    temp_fr3 = Frame(fr,highlightthickness=lin)
    sb3 = Text(temp_fr3,height=1,width=1,font=ft, state = 'disabled')
    sb3.pack(fill=tkinter.BOTH,expand=True,padx=pdx,pady=pdy)
    temp_fr3.pack(fill=tkinter.BOTH,expand=True,side=tkinter.BOTTOM)
    
    return fr


def response_window():
    fr = Frame()
    # TODO
    return fr


# 帮助文档
hp = '''
删除当前标签 (Ctrl + w)
创建新的标签 (Ctrl + c)
帮助文档标签 (Ctrl + h)
改当前标签名 (Ctrl + e)
'''

def helper_window():
    fr = Frame()
    ft = Font(family='Consolas',size=10)
    temp_fr1 = Frame(fr,highlightthickness=lin)
    lb1 = ttk.Label(temp_fr1,font=ft,text=hp)
    lb1.pack()
    temp_fr1.pack()
    return fr



if __name__ == '__main__':
    import tkinter
    top = tkinter.Tk()
    top.geometry('500x300')

    # test
    fr = request_window()
    fr.master = top
    fr.pack(fill=tkinter.BOTH, expand=True)
    top.mainloop()
    
