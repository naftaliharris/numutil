"""
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

It exposes two functions to the user: str2num and num2str, which do what you 
would think.
"""

__all__ = ["str2num", "num2str"]

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
    ('octillionth', 10 ** 27), ('nonillionth', 10 ** 30), ('quarter', 4)])

# Make reverse dictionaries
_num2str = dict((y, x) for x, y in _str2num.iteritems() if x != 'a')
_denom2str = dict((y, x) for x, y in _str2denom.iteritems() if x != 'quarter')
_small_denom2str = dict((y, x) for x, y in _str2denom.iteritems() if x != 'fourth'
        and y < 20)

# Add plurals.( _denom2str does not have plurals)
for denomstr, denom in _str2denom.items():
    _str2denom[denomstr + 's'] = denom
_str2denom['halves'] = 2
del denomstr, denom

# Add unit words
_unit_words = {'dozen': 12, 'gross': 144, 'score': 20, 'scores': 20}

# Strings that aren't numbers
_special_nonnum_strs = set(['and', 'a', '', '-'])

def str2num(numstr):
    """str2num takes a string representation of a number, and returns 
    the number. If it doesn't find a number, it will raise a ValueError.

    Example:
    >>> from numutil import str2num
    >>> str2num('4.5 million')
    4500000
    >>> str2num('two and a third')
    Fraction(7, 3)
    >>> str2num('123,456,789')
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

            if num is not None:  # word is not spelled-out
                magnitude += num
            else:  # word is spelled-out
                if word in _str2num:
                    num = _str2num[word]
                    if num < 100:
                        magnitude += num
                    elif num == 100:
                        magnitude *= num
                    else:
                        result += magnitude * num
                        magnitude = 0
                elif word in _unit_words:
                    if magnitude != 0:
                        magnitude *= _unit_words[word]
                    else:
                        magnitude = _unit_words[word]
                elif word in _str2denom:
                    denom = _str2denom[word]
                    if andcount:  # like 'three and a half'
                        if int(magnitude) == magnitude:
                            result += Fraction(int(magnitude), denom)
                        else:
                            result += float(magnitude) / float(denom)
                    else:  # like 'three halves'
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

def _sigfig_round(num, sig_figs):
    """rounds num to a given number of significant digits, sig_figs.
    sig_figs must a positive integer, or else this throws a ValueError
    _sigfig_round always returns a float. Meant for internal use only.

    >>> from numutil import _sigfig_round
    >>> _sigfig_round(1.2345, 3)
    1.23
    >>> _sigfig_round(1234567890, 5)
    1234600000.0
    
    """
    if sig_figs <= 0:
        raise ValueError("sig_figs is %s, but must be strictly greater than"
                " zero." % str(sig_figs))

    if num != 0:
        return round(num, -int(floor(log10(abs(num))) - (sig_figs - 1)))
    else:
        return 0.0  # Can't take the log of 0

def _small_wordify(num):
    """Turns num, an int 0 <= num < 1000, into words. For internal use only."""
    if num < 20:
        return _num2str[num]
    else:
        results = [_num2str[(num // 100)] + " hundred"] if num >= 100 else []
        num %= 100
        if num == 0:
            pass
        elif 0 < num < 20:
            results.append(_num2str[num])
        else:
            results.append(_num2str[(num // 10) * 10])
            if num % 10 != 0:
                results.append(_num2str[num % 10])
        return " ".join(results)

def num2str(num, style='commas', frac_style='mixed', sig_figs='default'):
    """Turns the number num into a pretty string.

    Arguments:
    style:      if 'commas', it will display numbers with commas
                if 'nocommas', it will display numbers without any commas
                if 'words', it will display numbers with words
                if 'newspaper', it will display numbers like in newspapers,
                    eg, '1.3 billion'. Numbers less than a million will be
                    displayed in comma format, because '12.34 thousand'
                    is never used in newspapers. Newspaper style uses a default
                    value of sig_figs=3. If you don't want rounding, set
                    sig_figs=None manually.
                Default is 'commas'

                Examples:

                >>> from numutil import num2str
                >>> num2str(1234567890, style='commas')
                '1,234,567,890'
                >>> num2str(1234567890, style='nocommas')
                '1234567890'
                >>> num2str(1234567890, style='newspaper')
                '1.23 billion'
                >>> num2str(123456, style='newspaper')
                '123,000'
                >>> num2str(123456, style='newspaper', sig_figs=None)
                '123,456'


    frac_style: if 'mixed', it will display fractions as mixed, like '1 1/2'
                if 'improper', it will display fractions as improper, like '3/2'
                Default is 'mixed'

                Examples:

                >>> from numutil import num2str
                >>> from fractions import Fraction
                >>> num2str(Fraction(3, 2), frac_style='mixed')
                '1 1/2'
                >>> num2str(Fraction(3, 2), frac_style='improper')
                '3/2'
                >>> num2str(Fraction(3, 2), style='words')
                'one and one half'

                Note that fractions with denominators of one are converted
                into ints.


    sig_figs:   if not None, it will round num to the specified number of
                significant digits. Has no effect on Fractions.
                Default is None, ie, no rounding, for all styles except
                newspaper mode, which has a default value of sig_figs=3.

                Examples:

                >>> from numutil import num2str
                >>> num2str(12.345)
                '12.345'
                >>> num2str(12.345, sig_figs=3)
                '12.3'
                >>> num2str(12.345, sig_figs=1)
                '10'

    """

    # Test the arguments for misspellings
    if sig_figs == 'default':
        sig_figs = None if style != 'newspaper' else 3

    # Fractions
    numerator, denominator = None, None
    try:  # use ducktyping
        numerator = num.numerator
        denominator = num.denominator
    except AttributeError:
        pass

    if numerator is not None and denominator != 1:

        # negative numerators mess with the divmod trick
        if numerator < 0:
            numerator *= -1
            result = "negative " if style == 'words' else '-'
        else:
            result = ""

        if frac_style == 'mixed':
            wholepart, numerator = divmod(numerator, denominator)
            if wholepart:
                result += num2str(wholepart, style, frac_style, sig_figs)
                result += " and " if style == 'words' else " "

        result += num2str(numerator, style, frac_style, sig_figs)
        result += " " if style == 'words' else "/"
        if style != "words":
            result += num2str(denominator, style, frac_style, sig_figs)
        else:
            denom = []
            mod_by = 1
            while denominator > 0:
                denominator, r = divmod(denominator, 1000)
                if r != 0:
                    if denom:
                        denom.append(
                                _small_wordify(r) + ' ' + _num2str[mod_by])
                    else:
                        if mod_by == 1:
                            hundreds, ones_tens = divmod(r, 100)
                            tens, ones = divmod(ones_tens, 10)

                            if ones_tens:
                                if hundreds:
                                    res = _num2str[hundreds] + ' hundred '
                                else:
                                    res = ''

                                if ones_tens < 20:
                                    res += _small_denom2str[ones_tens]
                                elif ones == 0:
                                    res += _denom2str[tens * 10]
                                else:
                                    res += _num2str[tens * 10] + ' ' + \
                                            _denom2str[ones]

                                denom.append(res)
                            else:
                                denom.append(_num2str[hundreds] + ' hundreth')
                        else:
                            denom.append(_small_wordify(r) + ' ' + _denom2str[mod_by])
                mod_by *= 1000
            denomstr = ", ".join(reversed(denom))

            # Deal with plurals
            if numerator > 1:
                if denomstr[-4:] != "half":
                    denomstr += 's'
                else:
                    denomstr = denomstr[:-4] + "halves"

            result += denomstr
        return result

    # Round and simplify to int if possible
    if sig_figs is not None:
        num = _sigfig_round(num, sig_figs)
        if num == int(num):
            num = int(num)

    if style == 'nocommas':
        if sig_figs is not None:
            if isinstance(num, float):
                return str(num) + '0' * (sig_figs - (len(str(num)) - 1))
            elif isinstance(num, (int, long)):
                res = str(num)
                if len(res) >= sig_figs:
                    return res
                else:
                    return res + '.' + '0' * (sig_figs - len(res))
            else:
                raise TypeError("Can't apply 'nocommas' style to type %s"
                        % type(num))
        else:
            return str(num)

    elif style == 'commas':
        if num < 0:  # negative nums mess with divmods
            return '-' + num2str(-num, style, frac_style, sig_figs)

        if isinstance(num, float):
            result = '.' + str(num).split('.')[1]
            # Add extra zeros for extra sig_figs
            if sig_figs is not None:
                result += '0' * (sig_figs - (len(str(num)) - 1))
        else:
            result = ''
        while num >= 1000:
            num, r = divmod(num, 1000)
            result = ",%03d%s" % (r, result)
        return "%d%s" % (num, result)

    elif style == 'newspaper':
        if num < 0:  # nonpositive nums mess with logs
            return '-' + num2str(-num, style, frac_style, sig_figs)
        elif num == 0:
            return '0'

        d = int(log10(num) / 3) * 3
        if 10 ** d in _num2str and d > 3:
            y = float(num) / (10 ** d)
            y = int(y) if y == int(y) else y
            return num2str(y, 'nocommas', frac_style, sig_figs) + \
                    ' ' + _num2str[10 ** d]
        else:
            return num2str(num, 'commas', frac_style, sig_figs)
            
    elif style == 'words':
        if num < 0:
            return "negative " + num2str(-num, style, frac_style, sig_figs)
        if isinstance(num, float):
            raise NotImplementedError
        elif isinstance(num, (int, long)):
            if num == 0:
                return "zero"
            results = []
            mod_by = 1
            while num > 0:
                num, r = divmod(num, 1000)
                if r != 0:
                    results.append(_small_wordify(r) +
                        (' ' + _num2str[mod_by] if mod_by != 1 else ''))
                mod_by *= 1000
            return ", ".join(reversed(results))
        else:
            raise TypeError("Don't know how to turn %s into words" % type(num))

    else:
        raise ValueError("Unrecognized style: '%s'" % style)
