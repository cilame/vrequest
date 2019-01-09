import tkinter
import types

from root import root


menu = tkinter.Menu(root,tearoff=0)

def bind_menu(func):
    if not isinstance(func, types.FunctionType):
        raise TypeError('{} must be a FunctionType.'.format(str(func)))
    menu.add_command(label=func.__name__, command=func)
    popupmenu = lambda e:menu.post(e.x_root,e.y_root)
    root.bind("<Button-3>",popupmenu)





def test_command_1():
    print('test command 1.')
def test_command_2():
    print('test command 2.')