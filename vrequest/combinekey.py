import types

from root import root

def bind_ctl_key(func, key=None):
    if key is None:
        raise TypeError('{} must be a lowercase.'.format(key))
    if not isinstance(func, types.FunctionType):
        raise TypeError('{} must be a FunctionType.'.format(str(func)))
    root.bind("<Control-{}>".format(key),lambda e:func())