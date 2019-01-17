import tkinter
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.font import Font

Text = scrolledtext.ScrolledText
#Text = tkinter.Text
Label = ttk.Label
Button = ttk.Button

# 测试两种 Frame 效果
# Frame = ttk.Frame # ttk.Frame 没有 highlightthickness 这个参数
Frame = tkinter.Frame

frame_setting = {}

pdx = 0
pdy = 0
lin = 4

def request_window(setting=None):
    fr = Frame()
    ft = Font(family='Consolas',size=10)
    
    temp_fr1 = Frame(fr,highlightthickness=lin)
    temp_fold_fr1 = Frame(temp_fr1)
    temp_fold_fr2 = Frame(temp_fr1)
    lb1 = Label (temp_fold_fr1,text='url')
    tx1 = Text  (temp_fold_fr1,height=1,width=1,font=ft)
    #bt1 = Button(temp_fold_fr1,text='整理 url 结构')
    lb1.pack(side=tkinter.TOP)
    tx1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP,padx=pdx,pady=pdy)
    #bt1.pack(side=tkinter.BOTTOM)

    lb2 = Label (temp_fold_fr2,text='headers')
    tx2 = Text  (temp_fold_fr2,height=1,width=1,font=ft)
    #bt2 = Button(temp_fold_fr2,text='整理 headers 结构')
    lb2.pack(side=tkinter.TOP)
    tx2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP,padx=pdx,pady=pdy)
    #bt2.pack(side=tkinter.BOTTOM)
    temp_fold_fr1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.LEFT)
    temp_fold_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.LEFT)
    temp_fr1.pack(fill=tkinter.BOTH,expand=True,side=tkinter.TOP)

    temp_fr2 = Frame(fr,highlightthickness=lin)
    lb3 = Label (temp_fr2,text='body')
    sb3 = Text  (temp_fr2,height=1,width=1,font=ft)
    lb3.pack(side=tkinter.TOP)
    sb3.pack(fill=tkinter.BOTH,expand=True,padx=pdx,pady=pdy)
    temp_fr2.pack(fill=tkinter.BOTH,expand=True,side=tkinter.BOTTOM)

    frame_setting[fr] = {}
    frame_setting[fr]['type'] = 'request'
    frame_setting[fr]['fr_url'] = tx1
    frame_setting[fr]['fr_headers'] = tx2
    return fr


def response_window():
    fr = Frame()
    # TODO
    return fr


# 帮助文档
def helper_window():
    fr = Frame()
    ft = Font(family='Consolas',size=10)
    hp = '''
删除当前标签 (Ctrl + w)
创建新的标签 (Ctrl + c)
帮助文档标签 (Ctrl + h)
改当前标签名 (Ctrl + e)
发送请求任务 (Ctrl + s)
    针对 url请求使用的功能，执行时会自动整理 url结构
    并且会保存请求配置，下次开启工具时会回到当前配置
'''
    temp_fr1 = Frame(fr,highlightthickness=lin)
    lb1 = ttk.Label(temp_fr1,font=ft,text=hp)
    lb1.pack()
    temp_fr1.pack()

    frame_setting[fr] = {}
    frame_setting[fr]['type'] = 'help'
    return fr



if __name__ == '__main__':
    import tkinter
    top = tkinter.Tk()
    top.geometry('500x300')

    # test
    fr = request_window()
    fr.master = top
    fr.pack(fill=tkinter.BOTH, expand=True)
    top.bind('<Control-w>',lambda e:top.quit())
    top.mainloop()
    
