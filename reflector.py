import plugboard

class ReflectorError(Exception): pass

class Reflector(plugboard.Plugboard):
    def __init__(self, wiring):
        super().__init__(wiring)

class ReflectorB(Reflector):
    def __init__(self):
        super().__init__(('AY', 'BR', 'CU', 'DH', 'EQ',
                          'FS', 'GL', 'IP', 'JX', 'KN',
                          'MO', 'TZ', 'VW'))

class ReflectorC(Reflector):
    def __init__(self):
        super().__init__(('AF', 'BV', 'CP', 'DJ', 'EI',
                          'GO', 'HY', 'KR', 'LZ', 'MX',
                          'NW', 'QT', 'SU'))

class ReflectorBThin(Reflector):
    def __init__(self):
        super().__init__(('AE', 'BN', 'CK', 'DQ', 'FU',
                          'GY', 'HW', 'IJ', 'LO', 'MP',
                          'RX', 'SZ', 'TV'))

class ReflectorCThin(Reflector):
    def __init__(self):
        super().__init__(('AR', 'BD', 'CO', 'EJ', 'FN',
                          'GT', 'HK', 'IV', 'LM', 'PW',
                          'QZ', 'SX', 'UY'))

if __name__ == '__main__':
    import unittest

    class TestReflector(unittest.TestCase):

        def test_ReflectorB(self):
            r = ReflectorB()
            for i, c in enumerate('YRUHQSLDPXNGOKMIEBFZCWVJAT', ord('A')):
                self.assertEqual(c, r.translate(chr(i)))

        def test_ReflectorC(self):
            r = ReflectorC()
            for i, c in enumerate('FVPJIAOYEDRZXWGCTKUQSBNMHL', ord('A')):
                self.assertEqual(c, r.translate(chr(i)))

        def test_ReflectorBThin(self):
            r = ReflectorBThin()
            for i, c in enumerate('ENKQAUYWJICOPBLMDXZVFTHRGS', ord('A')):
                self.assertEqual(c, r.translate(chr(i)))

        def test_ReflectorCThin(self):
            r = ReflectorCThin()
            for i, c in enumerate('RDOBJNTKVEHMLFCWZAXGYIPSUQ', ord('A')):
                self.assertEqual(c, r.translate(chr(i)))

    unittest.main()
