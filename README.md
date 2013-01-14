numutil
=======

numutil is a python package for converting strings to and from numbers.
For example,

    >>> from numutil import parsenum
    >>> parsenum('1.3 million')
    1300000
    >>> parsenum('three and a half')
    Fraction(7, 2)
