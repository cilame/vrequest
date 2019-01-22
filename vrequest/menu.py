import tkinter
import types

from .root import root

menu = tkinter.Menu(root, tearoff=0)

def bind_menu(func, name=None):
    if not isinstance(func, types.FunctionType):
        raise TypeError('{} must be a FunctionType.'.format(str(func)))
    labelname = name if name is not None else func.__name__
    menu.add_command(label=labelname, command=func)
    root.bind("<Button-3>",lambda e:menu.post(e.x_root,e.y_root))
