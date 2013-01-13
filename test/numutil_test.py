import unittest
from numutil import parsenum

class test_parsenum(unittest.TestCase):
    """Tests the parsenum function"""

    def test_ints(self):
        for twine, result in [('0', 0), ('-1', -1), ('1', 1), 
                ('123456789', 123456789), ('-123456789', -123456789)]:
            self.assertEquals(parsenum(twine), result)

    def test_empty_str(self):
        self.assertRaises(ValueError, lambda: parsenum(''))

    def test_unit_words(self):
        for twine, result in [('zero', 0), ('one', 1), ('two', 2), 
                ('three', 3), ('four', 4), ('five', 5), ('six', 6), 
                ('seven', 7), ('eight', 8), ('nine', 9), ('ten', 10), 
                ('eleven', 11), ('twelve', 12), ('thirteen', 13), 
                ('fourteen', 14), ('fifteen', 15), ('sixteen', 16),
                ('seventeen', 17), ('eighteen', 18), ('nineteen', 19),
                ('twenty', 20), ('thirty', 30), ('fourty', 40), ('fifty', 50),
                ('sixty', 60), ('seventy', 70), ('eighty', 80), 
                ('ninety', 90)]:
            self.assertEquals(parsenum(twine), result)

    def test_comma_ints(self):
        for twine, result in [('1,234', 1234), ('12,345', 12345), 
                ('123,456', 123456), ('1,234,567', 1234567), 
                ('12,345,678', 12345678), ('123,456,789', 123456789),
                ('1,234,567,890', 1234567890)]:
            self.assertEquals(parsenum(twine), result)
        for twine, result in [('-1,234', -1234), ('-12,345', -12345), 
                ('-123,456', -123456), ('-1,234,567', -1234567), 
                ('-12,345,678', -12345678), ('-123,456,789', -123456789),
                ('-1,234,567,890', -1234567890)]:
            self.assertEquals(parsenum(twine), result)

    def test_nonints(self):
        for twine in ['jim', 'zerox', 'bone', 'twos', 'threek', 'fourk']:
            self.assertRaises(ValueError, lambda: parsenum(''))
