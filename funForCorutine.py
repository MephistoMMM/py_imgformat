#!/usr/local/Cellar/python3/
"""
some function tool for corutine

@author MephistoPheies
@createDate 2015/8/7
@upDate     2015/8/7
"""
"""
Index:
    corutine --function wrapper-- ready the corutine
    cteContrlCreator --function-- create coroutine contrlor(starter, closer)
"""

import functools
from assertTool import *


def coroutine(function):
    """
    coroutine decorater
    """

    @functools.wraps(function)
    def wrapper(*args,**kwargs):
        generator = function(*args, **kwargs)
        next(generator)
        return generator

    return wrapper


def cteContrlCreator(*args,starter=None):
    """
    a creator for creating start and close contrlor
    if start is None ,args[-1] will be starter
    """
    #assert arguments
    for arg in args:
        assert assertClass(arg, 'generator'),('funForCorutine.cteContrlCreator:'
        'type of arg in args must be generator!')
    assert assertClass(starter, 'generator', 'NoneType'), ('funForCorutine.cteContrlCreator:'
    'type of start must be generator or NoneType')
    #assert over

    def closer():
        """
        close the coroutine
        """ 
        for argv in args :
            argv.close()
        starter.close()

    args = list(args)
    starter = starter or args.pop()
    
    return starter, closer


if __name__ == '__main__':
    import doctest
    doctest.testmod()
