"""numutil.py"""

import re
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
    ('nonillion', 10 ** 30), ('a', 1)])

_str2denom = dict([('half', 2), ('third', 3), ('fourth', 4), ('fifth', 5),
    ('sixth', 6), ('seventh', 7), ('eighth', 8), ('ninth', 9), ('tenth', 10),
    ('eleventh', 11), ('twelfth', 12), ('thirteenth', 13), ('fourteenth', 14),
    ('fifteenth', 15), ('sixteenth', 16), ('seventeenth', 17),
    ('eighteenth', 18), ('nineteenth', 19), ('twentieth', 20),
    ('thirtieth', 30), ('fortieth', 40), ('fiftieth', 50), ('sixtieth', 60),
    ('seventieth', 70), ('eightieth', 80), ('ninetieth', 90),
    ('hundredth', 100), ('thousandth', 1000), ('millionth', 10 ** 6),
    ('billionth', 10 ** 9), ('trillionth', 10 ** 12),
    ('quadrillionth', 10 ** 15), ('quintillionth', 10 ** 18),
    ('sextillionth', 10 ** 21), ('septillionth', 10 ** 24),
    ('octillionth', 10 ** 27), ('nonillionth', 10 ** 30)])

# Add plurals
for denomstr, denom in _str2denom.items():
    _str2denom[denomstr + 's'] = denom
_str2denom['halves'] = 2

# Make reverse dictionaries
_num2str = dict((y, x) for x, y in _str2num.iteritems() if x != 'a')
_denom2str = dict((y, x) for x, y in _str2denom.iteritems() if x != 'halfs')

# Strings that aren't numbers
_special_nonnum_strs = set(['and', 'a', '', '-'])

def parsenum(numstr):
    """parsenum takes a string representation of a number, and returns 
    the number. If it doesn't find a number, it will raise a ValueError.

    Example:
    >>> from numutil import parsenum
    >>> parsenum('4.5 million')
    4500000
    >>> parsenum('two and a third')
    Fraction(7, 3)
    >>> parsenum('123,456,789')
    123456789

    """

    # See if the number is of form str(num), or closely related
    try: return int(numstr.replace(',', ''))
    except ValueError: pass

    try: return float(numstr.replace(',', ''))
    except ValueError: pass

    m = re.match(r'[ ]*[-]?[0-9,]+[ ]*/[ ]*[0-9,]+[ ]*', numstr)
    if m:
        return Fraction(re.sub(r'[, ]*', '', numstr))

    # Try to parse numstr as a word-mix
    numstr = numstr.lower()
    if numstr in _special_nonnum_strs:
        raise ValueError("Could not parse '%s' into a number" % numstr)
    words = [''.join(word.split(',')) for word in re.split(r'[- ]*', numstr)
            if word != '']
    result = 0
    magnitude = 0
    andcount = 0

    for word in words:
        if word == 'and':
            result += magnitude
            magnitude = 0
            andcount += 1
        else: 
            num = None
            try: num = int(word)
            except ValueError:
                try: num = float(word)
                except ValueError: pass

            if num is not None: # word is not spelled-out
                magnitude += num
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
                    if andcount: # like 'three and a half'
                        if int(magnitude) == magnitude:
                            result += Fraction(int(magnitude), denom)
                        else:
                            result += float(magnitude) / float(denom)
                    else: # like 'three halves'
                        result += magnitude
                        if int(result) == result:
                            result = Fraction(int(result), denom)
                        else:
                            result = float(result) / float(denom)
                    magnitude = 0
                else:
                    raise ValueError("Could not parse '%s' into a number, because"
                            " did not recognize the word '%s'" % (numstr, word))

    result += magnitude
    if int(result) == result and not isinstance(result, Fraction):
        return int(result)
    else:
        return result

def sigfig_round(num, sig_figs):
    """rounds num to a given number of significant digits, sig_figs.
    sig_figs must a positive integer, or else this throws a ValueError
    sigfig_round always returns a float. 

    >>> from numutil import sigfig_round
    >>> sigfig_round(1.2345, 3)
    1.23
    >>> sigfig_round(1234567890, 5)
    1234600000.0
    
    """
    if sig_figs <= 0:
        raise ValueError("sig_figs is %s, but must be strictly greater than"
                " zero." % str(sig_figs))

    if num != 0:
        return round(num, -int(floor(log10(abs(num))) - (sig_figs - 1)))
    else:
        return 0.0  # Can't take the log of 0
