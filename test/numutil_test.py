import unittest
from numutil import parsenum
from fractions import Fraction

class test_parsenum(unittest.TestCase):
    """Tests the parsenum function"""

    def test_ints(self):
        for numstr, result in [('0', 0), ('-1', -1), ('1', 1), 
                ('123456789', 123456789), ('-123456789', -123456789)]:
            self.assertEquals(parsenum(numstr), result)

    def test_empty_str(self):
        self.assertRaises(ValueError, lambda: parsenum(''))

    def test_unit_words(self):
        for numstr, result in [('zero', 0), ('one', 1), ('two', 2), 
                ('three', 3), ('four', 4), ('five', 5), ('six', 6), 
                ('seven', 7), ('eight', 8), ('nine', 9), ('ten', 10), 
                ('eleven', 11), ('twelve', 12), ('thirteen', 13), 
                ('fourteen', 14), ('fifteen', 15), ('sixteen', 16),
                ('seventeen', 17), ('eighteen', 18), ('nineteen', 19),
                ('twenty', 20), ('thirty', 30), ('forty', 40), ('fifty', 50),
                ('sixty', 60), ('seventy', 70), ('eighty', 80), 
                ('ninety', 90)]:
            self.assertEquals(parsenum(numstr), result)

    def test_comma_ints(self):
        for numstr, result in [('1,234', 1234), ('12,345', 12345), 
                ('123,456', 123456), ('1,234,567', 1234567), 
                ('12,345,678', 12345678), ('123,456,789', 123456789),
                ('1,234,567,890', 1234567890)]:
            self.assertEquals(parsenum(numstr), result)
        for numstr, result in [('-1,234', -1234), ('-12,345', -12345), 
                ('-123,456', -123456), ('-1,234,567', -1234567), 
                ('-12,345,678', -12345678), ('-123,456,789', -123456789),
                ('-1,234,567,890', -1234567890)]:
            self.assertEquals(parsenum(numstr), result)

    def test_nonints(self):
        for numstr in ['jim', 'zerox', 'bone', 'twos', 'threek', 'fourk']:
            self.assertRaises(ValueError, lambda: parsenum(''))

    def test_newspaper_ints(self):
        for numstr, result in [('1 thousand', 10 ** 3), ('1 million', 10 ** 6),
                ('1 billion', 10 ** 9), ('1 trillion', 10 ** 12), 
                ('1 quadrillion', 10 ** 15), ('1 quintillion', 10 ** 18),
                ('1 sextillion', 10 ** 21), ('1 septillion', 10 ** 24),
                ('1 octillion', 10 ** 27), ('1 nonillion', 10 ** 30)]:
            self.assertEquals(parsenum(numstr), result)
        for numstr, result in [('1.2 million', 1200000), 
                ('12.3 million', 12300000), ('12.34 million', 12340000),
                ('123.456789 million', 123456789)]:
            self.assertEquals(parsenum(numstr), result)

    def test_word_ints(self):
        for numstr, result in [('twenty six', 26), 
                ('five hundred twelve', 512), 
                ('one thousand three hundred fifty two', 1352),
                ('fifteen million and thirty eight', 15000038),
                ('twelve hundred', 1200)]:
            self.assertEquals(parsenum(numstr), result) 

    def test_fractions(self):
        for denomstr, denom in [('half', 2), ('third', 3), ('fourth', 4),
                ('fifth', 5), ('sixth', 6), ('seventh', 7), ('eighth', 8),
                ('ninth', 9), ('tenth', 10), ('eleventh', 11),
                ('twelfth', 12), ('thirteenth', 13), ('fourteenth', 14),
                ('fifteenth', 15), ('sixteenth', 16), ('seventeenth', 17),
                ('eighteenth', 18), ('nineteenth', 19), ('twentieth', 20),
                ('thirtieth', 30), ('fortieth', 40), ('fiftieth', 50),
                ('sixtieth', 60), ('seventieth', 70), ('eightieth', 80),
                ('ninetieth', 90)]:
            self.assertEquals(parsenum('one ' + denomstr), Fraction(1, denom))
