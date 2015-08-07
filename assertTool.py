#!/usr/local/Cellar/python3/
"""
some function tool for assert

@author MephistoPheies
@createDate 2015/8/7
@upDate     2015/8/7
"""
"""
Index:
    assertClass --function-- assert obj class name
"""

def assertClass(obj, *cNames):
    """
    for assert obj type
    cNames must be a tuple<str>.

    >>> assertClass('ex', 'number','str')
    True
    >>> assertClass(2, 'str')
    False
    """
    for className in cNames :
        assert type(className).__name__ == 'str','assertTool.assertClass:\
                                                  className must be a str.'
    return type(obj).__name__ in cNames




if __name__ == '__main__':
    import doctest
    doctest.testmod()
