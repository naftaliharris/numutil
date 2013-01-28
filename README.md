numutil
=======

numutil is a python package for converting strings to and from numbers.
For example,

    >>> from numutil import str2num, num2str
    >>> str2num('1.3 million')
    1300000
    >>> str2num('three and a half')
    Fraction(7, 2)
    >>> str2num('123,456.789')
    123456.789
    >>> num2str(1234567, style='newspaper')
    '1.23 million'
    >>> num2str(1234567, style='words')
    'one million, two hundred thirty four thousand, five hundred sixty seven'

Installation
------------

You can install numutil from source with
    
    $ sudo python setup.py install

Testing
-------

numutil is well-tested, with almost a hundred percent coverage, as determined
by 

    $ nosetests --with-coverage test.py

You can test numutil yourself with nosetests, as above, or with
    
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
