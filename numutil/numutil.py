"""numutil.py"""

from math import log10

_str2num = dict([('zero', 0), ('one', 1), ('two', 2), ('three', 3),
    ('four', 4), ('five', 5), ('six', 6), ('seven', 7), ('eight', 8),
    ('nine', 9), ('ten', 10), ('eleven', 11), ('twelve', 12),
    ('thirteen', 13), ('fourteen', 14), ('fifteen', 15), ('sixteen', 16),
    ('seventeen', 17), ('eighteen', 18), ('nineteen', 19), ('twenty', 20),
    ('thirty', 30), ('fourty', 40), ('fifty', 50), ('sixty', 60),
    ('seventy', 70), ('eighty', 80), ('ninety', 90), ('hundred', 100),
    ('thousand', 10 ** 3), ('million', 10 ** 6), ('billion', 10 ** 9),
    ('trillion', 10 ** 12), ('quadrillion', 10 ** 15),
    ('quintillion', 10 ** 18), ('sextillion', 10 ** 21),
    ('septillion', 10 ** 24), ('octillion', 10 ** 27),
    ('nonillion', 10 ** 30)])

_num2str = dict((y, x) for x, y in _str2num.items())

def parsenum(numstr):
    """parsenum takes a string representation of a number, and returns 
    the number. If it doesn't find a number, it will raise a ValueError.

    Example:
    >>> parsenum('4.5 million')
    4500000
    """

    # See if the number is of form str(num)
    try: return int(numstr)
    except ValueError: pass

    try: return float(numstr)
    except ValueError: pass

    # See if the number just has commas
    try: return int("".join(numstr.split(',')))
    except ValueError: pass

    try: return float("".join(numstr.split(',')))
    except ValueError: pass

    # Try to parse numstr as a word-mix
    numstr = numstr.lower()
    words = numstr.split(' ')
    result = 0
    magnitude = 0

    # Failure, so raise a ValueError
    raise ValueError("Could not parse '%s' into a number" % numstr)

def sigfig_round(num, sig_figs):
    """rounds x to a given number of significant digits"""
    if num != 0:
        x = round(num, -int(math.floor(log10(abs(num))) - (sig_figs - 1)))
        return int(x) if int(x) == x else x
    else:
        return 0  # Can't take the log of 0

if __name__ == "__main__":
    import doctest
    doctest.testmod()
