"""setup.py"""

from distutils.core import setup

setup(name='numutil',
        version='0.1.0',
        description='Utilities for parsing strings into numbers, and printing numbers as pretty strings',
        author='Naftali Harris',
        author_email='naftaliharris@gmail.com',
        url='www.naftaliharris.com',
        packages=['.'],
        keywords = ["number", "parse", "text", 'user-entered'],
        classifiers = [
            "Programming Language :: Python",
            "Development Status :: 2 - Pre-Alpha",
            "Environment :: Other Environment",
            "Environment :: Web Environment",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Natural Language :: English",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Text Processing :: Linguistic",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
            ],
        long_description = """\
Convert between numbers and strings
-----------------------------------

Strings to Numbers::

    >>> from numutil import str2num, num2str
    >>> str2num('1.3 million')
    1300000
    >>> str2num('three and a half')
    Fraction(7, 2)
    >>> str2num('123,456.789')
    123456.789

Numbers to Strings::

    >>> num2str(1234567, style='newspaper')
    '1.23 million'
    >>> num2str(1234567, style='words')
    'one million, two hundred thirty four thousand, five hundred sixty seven'

numutil might be useful for people mining data from text, or for people running web apps that need to parse numbers from user-entered strings, or render numbers in a user-friendly format.
"""
)
