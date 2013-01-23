numutil
=======

numutil is a python package for converting strings to and from numbers.
For example,

    >>> from numutil import parsenum, prettynum
    >>> parsenum('1.3 million')
    1300000
    >>> parsenum('three and a half')
    Fraction(7, 2)
    >>> parsenum('123,456.789')
    123456.789
    >>> prettynum(1234567, mode='newspaper')
    '1.23 million'

Installation
------------

You can install numutil from source with
    
    $ sudo python setup.py install

Testing
-------

numutil is well-tested, with almost a hundred percent coverage, as determined
by 

    $ nosetests --with-coverage test.py

You can test numutil yourself with
    
    $ python test.py

In addition to testing numutil directly, test.py also tests the documentation
in numutil.py and this README with the doctest module, so all examples in the
documentation are guaranteed to be correct if the tests pass.

License
-------

numutil is BSD licensed. You can read the details in the LICENSE file.

Author and Maintainer
---------------------

Naftali Harris

www.naftaliharris.com
