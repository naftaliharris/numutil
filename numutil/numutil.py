"""numutil.py"""

from math import log10, floor
from fractions import Fraction

_str2num = dict([('zero', 0), ('one', 1), ('two', 2), ('three', 3),
    ('four', 4), ('five', 5), ('six', 6), ('seven', 7), ('eight', 8),
    ('nine', 9), ('ten', 10), ('eleven', 11), ('twelve', 12),
    ('thirteen', 13), ('fourteen', 14), ('fifteen', 15), ('sixteen', 16),
    ('seventeen', 17), ('eighteen', 18), ('nineteen', 19), ('twenty', 20),
    ('thirty', 30), ('forty', 40), ('fifty', 50), ('sixty', 60),
    ('seventy', 70), ('eighty', 80), ('ninety', 90), ('hundred', 100),
    ('thousand', 10 ** 3), ('million', 10 ** 6), ('billion', 10 ** 9),
    ('trillion', 10 ** 12), ('quadrillion', 10 ** 15),
    ('quintillion', 10 ** 18), ('sextillion', 10 ** 21),
    ('septillion', 10 ** 24), ('octillion', 10 ** 27),
    ('nonillion', 10 ** 30)])

_str2denom = dict([('half', 2), ('third', 3), ('fourth', 4), ('fifth', 5),
    ('sixth', 6), ('seventh', 7), ('eighth', 8), ('ninth', 9), ('tenth', 10),
    ('eleventh', 11), ('twelfth', 12), ('thirteenth', 13), ('fourteenth', 14),
    ('fifteenth', 15), ('sixteenth', 16), ('seventeenth', 17),
    ('eighteenth', 18), ('nineteenth', 19), ('twentieth', 20),
    ('thirtieth', 30), ('fortieth', 40), ('fiftieth', 50), ('sixtieth', 60),
    ('seventieth', 70), ('eightieth', 80), ('ninetieth', 90)])

# Add plurals
for denomstr, denom in _str2denom.items():
    _str2denom[denomstr + 's'] = denom

# Make reverse dictionaries
_num2str = dict((y, x) for x, y in _str2num.iteritems())
_denom2str = dict((y, x) for x, y in _str2denom.iteritems())

def parsenum(numstr):
    """parsenum takes a string representation of a number, and returns 
    the number. If it doesn't find a number, it will raise a ValueError.

    Example:
    >>> from numutil import parsenum
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
    words = [''.join(word.split(',')) for word in numstr.split(' ')]
    result = 0
    magnitude = 0

    for word in words:
        if word == 'and':
            continue

        num = None
        try: num = int(word)
        except ValueError:
            try: num = float(word)
            except ValueError: pass

        if num is not None: # word is not spelled-out
            magnitude = num
        else: # word is spelled-out
            if word in _str2num:
                num = _str2num[word]
                if num < 100:
                    magnitude += num
                elif num == 100:
                    magnitude *= 100
                else:
                    result += magnitude * num
                    magnitude = 0
            elif word in _str2denom:
                denom = _str2denom[word]
                if int(magnitude) == magnitude:
                    result += Fraction(int(magnitude), denom)
                else:
                    result += float(magnitude) / float(denom)
                magnitude = 0
            else:
                raise ValueError("Could not parse '%s' into a number, because"
                        " did not recognize the word '%s'" % (numstr, word))

    result += magnitude
    return int(result) if int(result) == result else result

    # Failure, so raise a ValueError
    raise ValueError("Could not parse '%s' into a number" % numstr)

def sigfig_round(num, sig_figs):
    """rounds num to a given number of significant digits, sig_figs.
    sig_figs must a positive integer, or else this throws a ValueError"""
    if sig_figs <= 0:
        raise ValueError("sig_figs is %s, but must be strictly greater than"
                " zero." % str(sig_figs))

    if num != 0:
        x = round(num, -int(floor(log10(abs(num))) - (sig_figs - 1)))
        return int(x) if int(x) == x else x
    else:
        return 0  # Can't take the log of 0

if __name__ == "__main__":
    import doctest
    doctest.testmod()
