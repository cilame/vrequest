# 该脚本切分gif无需依赖
from tkinter import *

def mk_phlist(filename):
    global phlist # 这个 global 是必须的，PhotoImage 加载多个图片的机制有点迷。
    phlist = []
    for i in range(100):
        try:
            photo = PhotoImage(file=filename, format='gif -index {}'.format(i))
            phlist.append(photo)
        except:
            print(i)
            break
    return phlist

if __name__ == '__main__':
    root = Tk()

    filename = 'eee.gif'
    phlist = mk_phlist(filename) # 先有 tk 对象之后再创建才能成功
    text = Text(root)
    for i in phlist:
        text.image_create(END, image=i)

    text.pack(fill=BOTH,expand=True)
    root.mainloop()


