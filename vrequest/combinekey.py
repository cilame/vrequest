import types

from .root import root

def bind_ctl_key(func, key=None, shift=False):
    if key is None:
        raise TypeError('{} must be a lowercase.'.format(key))
    if not isinstance(func, types.FunctionType):
        raise TypeError('{} must be a FunctionType.'.format(str(func)))
    key = key.upper() if shift else key
    root.bind("<Control-{}>".format(key),lambda e:func())


def bind_alt_key(func, key=None, shift=False):
    if key is None:
        raise TypeError('{} must be a lowercase.'.format(key))
    if not isinstance(func, types.FunctionType):
        raise TypeError('{} must be a FunctionType.'.format(str(func)))
    key = key.upper() if shift else key
    root.bind("<Alt-{}>".format(key),lambda e:func())


