#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import doctest
from numutil import parsenum, sigfig_round, prettynum
from fractions import Fraction

class test_parsenum(unittest.TestCase):
    """Tests the parsenum function"""

    def test_ints(self):
        for numstr, result in [('0', 0), ('-1', -1), ('1', 1), 
                ('123456789', 123456789), ('-123456789', -123456789)]:
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))

    def test_floats(self):
        for numstr, result in [('0.0', 0.0), ('-1.0', -1.0), ('1.0', 1.0), 
                ('123456789.0', 123456789.0), ('-123456789.0', -123456789.0),
                ('4.32E10', 4.32E10), ('-2.3e-23', -2.3e-23), 
                ('0.00043', 0.00043), ('-0.23', -0.23), ('1000.0', 1000.0)]:
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))

    def test_ordinary_fractions(self):
        for numstr, result in[('1/2', Fraction(1, 2)),
                ('1 / 2', Fraction(1, 2)), ('1/3', Fraction(1, 3)),
                ('6/5', Fraction(6, 5)), ('6/ 6', Fraction(6, 6)),
                (' 6,343 /5 ', Fraction(6343, 5)), (' 6/ 6 ', Fraction(6, 6)),
                ('0/5', Fraction(0, 5)), ('-6/7', Fraction(-6, 7))]:
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))

    def test_comma_floats(self):
        for numstr, result in [('123,456,789.0', 123456789.0),
                ('-123,456,789.0', -123456789.0), ('1,000.0', 1000.0)]:
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))

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
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))

    def test_comma_ints(self):
        for numstr, result in [('1,234', 1234), ('12,345', 12345),
                ('123,456', 123456), ('1,234,567', 1234567),
                ('12,345,678', 12345678), ('123,456,789', 123456789),
                ('1,234,567,890', 1234567890)]:
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))
        for numstr, result in [('-1,234', -1234), ('-12,345', -12345),
                ('-123,456', -123456), ('-1,234,567', -1234567),
                ('-12,345,678', -12345678), ('-123,456,789', -123456789),
                ('-1,234,567,890', -1234567890)]:
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))

    def test_nonints(self):
        for numstr in ['jim', 'zerox', 'bone', 'twos', 'threek', 'fourk',
                'and', 'the', 's', 'a', '-', '']:
            self.assertRaises(ValueError, lambda: parsenum(numstr))

    def test_newspaper_ints(self):
        for numstr, result in [('1 thousand', 10 ** 3), ('1 million', 10 ** 6),
                ('1 billion', 10 ** 9), ('1 trillion', 10 ** 12), 
                ('1 quadrillion', 10 ** 15), ('1 quintillion', 10 ** 18),
                ('1 sextillion', 10 ** 21), ('1 septillion', 10 ** 24),
                ('1 octillion', 10 ** 27), ('1 nonillion', 10 ** 30)]:
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))
        for numstr, result in [('1.2 million', 1200000), 
                ('12.3 million', 12300000), ('12.34 million', 12340000),
                ('123.456789 million', 123456789)]:
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))

    def test_word_ints(self):
        for numstr, result in [('twenty six', 26), 
                ('five hundred twelve', 512), 
                ('one thousand three hundred fifty two', 1352),
                ('fifteen million and thirty eight', 15000038),
                ('twelve hundred', 1200)]:
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))

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
            guess = parsenum('one ' + denomstr)
            self.assertEqual(guess, Fraction(1, denom))
            self.assertEqual(type(guess), type(Fraction(1, denom)))

            guess = parsenum('3 ' + denomstr + 's')
            self.assertEqual(guess, Fraction(3, denom))
            self.assertEqual(type(guess), type(Fraction(3, denom)))

    def test_bigfractions(self):
        for denomstr, denom in [('half', 2), ('third', 3), ('fourth', 4),
                ('fifth', 5), ('sixth', 6), ('seventh', 7), ('eighth', 8),
                ('ninth', 9), ('tenth', 10), ('eleventh', 11),
                ('twelfth', 12), ('thirteenth', 13), ('fourteenth', 14),
                ('fifteenth', 15), ('sixteenth', 16), ('seventeenth', 17),
                ('eighteenth', 18), ('nineteenth', 19), ('twentieth', 20),
                ('thirtieth', 30), ('fortieth', 40), ('fiftieth', 50),
                ('sixtieth', 60), ('seventieth', 70), ('eightieth', 80),
                ('ninetieth', 90)]:
            guess = parsenum('twelve million, three hundred forty five'
                    ' thousand, six hundred seventy eight ' + denomstr + 's')
            self.assertEqual(guess, Fraction(12345678, denom))
            self.assertEqual(type(guess), type(Fraction(12345678, denom)))

            guess = parsenum('twelve million, three hundred forty five' 
                    ' thousand, six hundred seventy eight and one '
                    + denomstr)
            self.assertEqual(guess, 12345678 + Fraction(1, denom))
            self.assertEqual(type(guess), type(12345678 + Fraction(1, denom)))

    def test_dashes(self):
        for numstr, result in [('twenty-six', 26), ('one-hundred nine', 109),
                ('twenty-five', 25), ('five-sixths', Fraction(5, 6))]:
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))

    def test_word_num_mix(self):
        for numstr, result in [('twenty 6', 26), ('one-hundred 9', 109),
                ('20 five', 25), ('5 sixths', Fraction(5, 6))]:
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))

    def test_unicode(self):
        for numstr, result in [(u'125', 125), (u'124.5', 124.5),
                (u'five sixths', Fraction(5, 6)), (u'one million', 1000000)]:
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))
        for numstr in [u'şimal', u'汉语漢語', u'תירִבְעִ']:
            self.assertRaises(ValueError, lambda: parsenum(numstr))

    def test_cap_and_space(self):
        for numstr, result in [('TWENTY FIVE', 25), ('Thirty  six', 36),
                ('ONE hundred and Five', 105), (' One  Hundred   SIX ', 106)]:
            guess = parsenum(numstr)
            self.assertEqual(guess, result)
            self.assertEqual(type(guess), type(result))

class test_sigfig_round(unittest.TestCase):
    """tests the sigfig_round function"""

    def test_100(self):
        for x in [0, -1, 1, 109234, -120934, 1.19230413, -19203.01924,
                1.109324E100, -4.3E100]:
            guess = sigfig_round(x, 100)
            self.assertEqual(guess, x)
            self.assertEqual(type(guess), type(0.0))

    def test_0(self):
        for x in [0, -1, 1, 109234, -120934, 1.19230413, -19203.01924,
                1.109324E100, -4.3E100]:
            self.assertRaises(ValueError, lambda: sigfig_round(x, 0))

    def test_1(self):
        for x, x_round in [(0, 0), (-1, -1), (1, 1), (109234, 100000),
                (-120934, -100000), (1.19230413, 1), (-19203.01924, -20000),
                (1.109324E100, 1E100), (-4.3E100, -4E100)]:
            guess = sigfig_round(x, 1)
            self.assertEqual(guess, x_round)
            self.assertEqual(type(guess), type(0.0))

    def test_3(self):
        for x, x_round in [(0, 0), (-1, -1), (1, 1), (109234, 109000),
                (-120934, -121000), (1.19230413, 1.19), (-19203.01924, -19200),
                (1.109324E100, 1.11E100), (-4.0E100, -4E100)]:
            guess = sigfig_round(x, 3)
            self.assertEqual(guess, x_round)
            self.assertEqual(type(guess), type(0.0))

class test_prettynum(unittest.TestCase):
    """Tests the prettynum function"""
    
    def test_fractions_mixed(self):
        for num, result in [(Fraction(1, 2), '1/2'), (Fraction(3, 2), '1 1/2'),
                (Fraction(5, 3), '1 2/3'), (Fraction(-5, 3), '-1 2/3'),
                (Fraction(0, 3), '0'), (Fraction(100, 1), '100')]:
            guess = prettynum(num, frac_mode="mixed")
            self.assertEqual(guess, result)

    def test_fractions_improper(self):
        for num, result in [(Fraction(1, 2), '1/2'), (Fraction(3, 2), '3/2'),
                (Fraction(5, 3), '5/3'), (Fraction(-5, 3), '-5/3'),
                (Fraction(0, 3), '0'), (Fraction(100, 1), '100')]:
            guess = prettynum(num, frac_mode="improper")
            self.assertEqual(guess, result)

    def test_commas(self):
        for num, result in [(123456789, '123,456,789'),
                (1234567.89, '1,234,567.89'), (-1234567, '-1,234,567'),
                (0, '0'), (1234, '1,234'), (0.1234, '0.1234'),
                (-1234.56, '-1,234.56')]:
            guess = prettynum(num, mode="commas")
            self.assertEqual(guess, result)

    def test_newspaper(self):
        """
        for num, result in [(123456789, '123 million'),
                (1234567.89, '1.23 million'), (0, '0'), (1234, '1,230'),
                (0.1234, '0.1234'), (-1234.56, '-1,234.56')]:
            guess = prettynum(num, sig_figs=3, mode="newspaper")
            self.assertEqual(guess, result)
            """
        pass

class test_documentation(unittest.TestCase):
    """Doctests the documentation in the files"""

    def test_README(self):
        failures, tests = doctest.testfile('README.md')
        self.assertEqual(failures, 0)

    def test_numutil(self):
        failures, tests = doctest.testfile('numutil.py', package='numutil')
        self.assertEqual(failures, 0)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
