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
    _select = nb.select()
    if _select is not '':
        nb.forget(_select)



