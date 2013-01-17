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

def prettynum(num, **kwds):
    """Turns the number num into a pretty string.

    Possible keywords:
    sig_figs:   if not None, it will round num to the specified number of
                significant digits. Has no effect on Fractions.
                Default is None, ie, no rounding

                Examples:

                >>> from numutil import prettynum
                >>> prettynum(12.345)
                '12.345'
                >>> prettynum(12.345, sig_figs=3)
                '12.3'
                >>> prettynum(12.345, sig_figs=1)
                '10'

    mode:       if 'commas', it will display numbers with commas
                if 'nocommas', it will display numbers without any commas
                if 'words', it will display numbers with words
                if 'newspaper', it will display numbers like in newspapers,
                    eg, '1.3 billion'. Numbers less than a million will be
                    displayed in comma format, because '12.34 thousand'
                    is never used in newspapers.
                Default is 'commas'

                Examples:

                >>> from numutil import prettynum
                >>> prettynum(1234567890, mode='commas')
                '1,234,567,890'
                >>> prettynum(1234567890, mode='nocommas')
                '1234567890'
                >>> prettynum(1234567890, mode='newspaper', sig_figs=3)
                '1.23 billion'
                >>> prettynum(123456, mode='newspaper', sig_figs=3)
                '123,000'


    frac_mode:  if 'mixed', it will display fractions as mixed, like '1 1/2'
                if 'improper', it will display fractions as improper, like '3/2'
                Default is 'mixed'

                Examples:

                >>> from numutil import prettynum
                >>> from fractions import Fraction
                >>> prettynum(Fraction(3, 2), frac_mode='mixed')
                '1 1/2'
                >>> prettynum(Fraction(3, 2), frac_mode='improper')
                '3/2'

    Notes:
    1) Fractions with denominators are converted into ints.

    """

    # Test the arguments for misspellings
    for arg in kwds:
        if arg not in set(('sig_figs', 'mode', 'frac_mode')):
            raise TypeError("'%s' is not a valid option. Maybe you misspelled"
                    " the option you're looking for?" % arg)

    # Unpack the arguments
    sig_figs = kwds['sig_figs'] if 'sig_figs' in kwds else None
    mode = kwds['mode'] if 'mode' in kwds else 'commas'
    frac_mode = kwds['frac_mode'] if 'frac_mode' in kwds else 'mixed'

    # Fractions
    numerator, denominator = None, None
    try: # use ducktyping
        numerator = num.numerator
        denominator = num.denominator
    except AttributeError:
        pass

    if numerator is not None and denominator != 1:

        # negative numerators make the divmod trick not work
        if numerator < 0:
            numerator *= -1
            result = "negative " if mode == 'words' else '-'
        else:
            result = ""

        if frac_mode == 'mixed':
            wholepart, numerator = divmod(numerator, denominator)
            if wholepart:
                result += prettynum(wholepart, **kwds)
                result += " and " if mode == 'words' else " "

        result += prettynum(numerator, **kwds)
        result += " " if mode == 'words' else "/"
        result += prettynum(denominator, **kwds) # fix this

        return result

    # Round and simplify to int if possible
    if sig_figs is not None:
        num = sigfig_round(num, sig_figs)
        if num == int(num):
            num = int(num)

    if mode == 'nocommas':
        return str(num)
    elif mode == 'commas':
        if num < 0: # negative nums mess with divmods
            return '-' + prettynum(-num, **kwds)

        result = '.' + str(num).split('.')[1] if isinstance(num, float) else ''
        while num >= 1000:
            num, r = divmod(num, 1000)
            result = ",%03d%s" % (r, result)
        return "%d%s" % (num, result)
    elif mode == 'newspaper':
        # nonpositive nums mess with logs
        if num < 0:
            return '-' + prettynum(-num, **kwds)
        elif num == 0:
            return '0'

        d = int(log10(num) / 3) * 3
        if 10 ** d in _num2str and d > 3:
            y = float(num) / (10 ** d)
            y = int(y) if y == int(y) else y
            return str(y) + ' ' + _num2str[10 ** d]
        else:
            kwds['mode'] = 'commas'
            return prettynum(num, **kwds)
            
    elif mode == 'words':
        raise NotImplementedError
    else:
        raise ValueError("Unrecognized mode: '%s'" % mode)
