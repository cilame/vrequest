from tkinter import ttk
from tkinter import scrolledtext



def test_mkfr():
    fr = ttk.Frame()
    sb = scrolledtext.ScrolledText(fr)
    sb.pack()
    return fr




if __name__ == '__main__':
    import tkinter
    top = tkinter.Tk()

    # test
    fr = test_mkfr()
    fr.master = top
    fr.pack()
    top.mainloop()
    
