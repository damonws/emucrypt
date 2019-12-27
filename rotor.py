import string

class RotorError(Exception): pass

# 0         1         2
# 01234567890123456789012345
# ABCDEFGHIJKLMNOPQRSTUVWXYZ

ALPHA = string.ascii_uppercase
A = ord('A')

class Rotor(object):
    def __init__(self, wiring, notches, position=None, ring=None, doublestep=False):
        self.setWiring(wiring)
        self.setNotches(notches)
        self.position = 0
        self.ring = 0
        self.doublestep = doublestep
        if position is not None:
            self.setPosition(position)
        if ring is not None:
            self.setRing(ring)

    def setWiring(self, wiring):
        self.wiring = [ord(w) - i for i, w in enumerate(wiring, ord('A'))]

    def setNotches(self, notches):
        self.notches = [ord(n) - A for n in notches]

    def setPosition(self, position):
        self.position = ord(position) - A

    def getPosition(self):
        return chr(self.position + A)

    def setRing(self, ring):
        self.ring = ord(ring) - A

    def step(self, do_step=True):
        turnover = False
        if do_step or (self.doublestep and self.position in self.notches):
            turnover = self.position in self.notches
            self.position = (self.position + 1) % 26
        return turnover

    def activate(self):
        rpath = {}
        lpath = {}
        position = (self.position - self.ring) % 26
        for i in range(26):
            rpos = (i - position) % 26
            lpos = (rpos + self.wiring[i]) % 26
            rpath[chr(A + rpos)] = chr(A + lpos)
            lpath[chr(A + lpos)] = chr(A + rpos)
        self.rtable = ''.maketrans(rpath)
        self.ltable = ''.maketrans(lpath)

    def rtrans(self, char):
        self.activate()
        return char.translate(self.rtable)

    def ltrans(self, char):
        self.activate()
        return char.translate(self.ltable)

class RotorI(Rotor):
    def __init__(self, position=None, ring=None, doublestep=False):
        super().__init__('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', position, ring, doublestep)

class RotorII(Rotor):
    def __init__(self, position=None, ring=None, doublestep=False):
        super().__init__('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E', position, ring, doublestep)

class RotorIII(Rotor):
    def __init__(self, position=None, ring=None, doublestep=False):
        super().__init__('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V', position, ring, doublestep)

class RotorIV(Rotor):
    def __init__(self, position=None, ring=None, doublestep=False):
        super().__init__('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J', position, ring, doublestep)

class RotorV(Rotor):
    def __init__(self, position=None, ring=None, doublestep=False):
        super().__init__('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z', position, ring, doublestep)

class RotorVI(Rotor):
    def __init__(self, position=None, ring=None, doublestep=False):
        super().__init__('JPGVOUMFYQBENHZRDKASXLICTW', 'ZM', position, ring, doublestep)

class RotorVII(Rotor):
    def __init__(self, position=None, ring=None, doublestep=False):
        super().__init__('NZJHGRCXMYSWBOUFAIVLPEKQDT', 'ZM', position, ring, doublestep)

class RotorVIII(Rotor):
    def __init__(self, position=None, ring=None, doublestep=False):
        super().__init__('FKQHTLXOCBJSPDZRAMEWNIUYGV', 'ZM', position, ring, doublestep)

class RotorBeta(Rotor):
    def __init__(self, position=None, ring=None):
        super().__init__('LEYJVCNIXWPBQMDRTAKZGFUHOS', '', position, ring, False)

class RotorGamma(Rotor):
    def __init__(self, position=None, ring=None):
        super().__init__('FSOKANUERHMBTIYCWLQPZXVGJD', '', position, ring, False)

if __name__ == '__main__':
    import unittest

    class TestRotor(unittest.TestCase):

        def test_RotorIIIturnover(self):
            r = RotorIII(position = 'S')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'T')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'U')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'V')
            self.assertTrue(r.step())
            self.assertEqual(r.getPosition(), 'W')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'X')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'Y')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'Z')
            r = RotorIII(position = 'U', ring='Q')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'V')
            self.assertTrue(r.step())
            self.assertEqual(r.getPosition(), 'W')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'X')

        def test_RotorVIturnover(self):
            r = RotorVI(position = 'Y')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'Z')
            self.assertTrue(r.step())
            self.assertEqual(r.getPosition(), 'A')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'B')
            r = RotorVI(position = 'L', ring='C')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'M')
            self.assertTrue(r.step())
            self.assertEqual(r.getPosition(), 'N')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'O')

        def test_RotorIdoublestep(self):
            r = RotorI(position = 'N', doublestep=True)
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'O')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'P')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'Q')
            self.assertTrue(r.step(False))
            self.assertEqual(r.getPosition(), 'R')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'S')
            self.assertFalse(r.step())
            self.assertEqual(r.getPosition(), 'T')

        def test_RotorIIIpArA(self):
            r = RotorIII()
            r.step()
            self.assertEqual('C', r.rtrans('A'))
            self.assertEqual('B', r.ltrans('E'))
            r.step()
            self.assertEqual('D', r.rtrans('A'))
            self.assertEqual('D', r.ltrans('J'))
            r.step()
            r.step()
            r.step()
            self.assertEqual('G', r.rtrans('A'))
            self.assertEqual('O', r.ltrans('V'))
            r.step()
            self.assertEqual('W', r.rtrans('A'))
            self.assertEqual('W', r.ltrans('Z'))

        def test_RotorIIIpMrA(self):
            r = RotorIII(position='M')
            r.step()
            self.assertEqual('A', r.rtrans('A'))
            self.assertEqual('B', r.ltrans('L'))
            r.step()
            self.assertEqual('K', r.rtrans('A'))
            self.assertEqual('T', r.ltrans('B'))
            r.step()
            r.step()
            r.step()
            self.assertEqual('F', r.rtrans('A'))
            self.assertEqual('D', r.ltrans('T'))
            r.step()
            self.assertEqual('O', r.rtrans('A'))
            self.assertEqual('L', r.ltrans('P'))

        def test_RotorIIIpArB(self):
            r = RotorIII(ring='B')
            r.step()
            self.assertEqual('B', r.rtrans('A'))
            self.assertEqual('U', r.ltrans('K'))
            r.step()
            self.assertEqual('C', r.rtrans('A'))
            self.assertEqual('B', r.ltrans('E'))
            r.step()
            r.step()
            r.step()
            self.assertEqual('F', r.rtrans('A'))
            self.assertEqual('G', r.ltrans('T'))
            r.step()
            self.assertEqual('G', r.rtrans('A'))
            self.assertEqual('O', r.ltrans('V'))

        def test_RotorIpJrS(self):
            r = RotorI('J', 'S')
            r.step()
            self.assertEqual('A', r.rtrans('A'))
            self.assertEqual('Y', r.ltrans('F'))
            r.step()
            self.assertEqual('W', r.rtrans('A'))
            self.assertEqual('X', r.ltrans('E'))
            r.step()
            r.step()
            r.step()
            self.assertEqual('F', r.rtrans('A'))
            self.assertEqual('R', r.ltrans('A'))
            r.step()
            self.assertEqual('U', r.rtrans('A'))
            self.assertEqual('V', r.ltrans('V'))

        def test_RotorII(self):
            r = RotorII()
            self.assertEqual('D', r.rtrans('C'))
            self.assertEqual('E', r.ltrans('S'))
            self.assertEqual('K', r.rtrans('D'))
            self.assertEqual('J', r.ltrans('B'))
            self.assertEqual('R', r.rtrans('G'))
            self.assertEqual('V', r.ltrans('Y'))
            self.assertEqual('F', r.rtrans('W'))
            self.assertEqual('Z', r.ltrans('E'))

        def test_ThreeRotorDoublestep(self):
            r1 = RotorI(position='O')
            r2 = RotorII(position='D', doublestep=True)
            r3 = RotorIII()
            turnover = r1.step()
            turnover = r2.step(turnover)
            r3.step(turnover)
            self.assertEqual(r1.getPosition(), 'P')
            self.assertEqual(r2.getPosition(), 'D')
            self.assertEqual(r3.getPosition(), 'A')
            turnover = r1.step()
            turnover = r2.step(turnover)
            r3.step(turnover)
            self.assertEqual(r1.getPosition(), 'Q')
            self.assertEqual(r2.getPosition(), 'D')
            self.assertEqual(r3.getPosition(), 'A')
            turnover = r1.step()
            turnover = r2.step(turnover)
            r3.step(turnover)
            self.assertEqual(r1.getPosition(), 'R')
            self.assertEqual(r2.getPosition(), 'E')
            self.assertEqual(r3.getPosition(), 'A')
            turnover = r1.step()
            turnover = r2.step(turnover)
            r3.step(turnover)
            self.assertEqual(r1.getPosition(), 'S')
            self.assertEqual(r2.getPosition(), 'F')
            self.assertEqual(r3.getPosition(), 'B')
            turnover = r1.step()
            turnover = r2.step(turnover)
            r3.step(turnover)
            self.assertEqual(r1.getPosition(), 'T')
            self.assertEqual(r2.getPosition(), 'F')
            self.assertEqual(r3.getPosition(), 'B')
            turnover = r1.step()
            turnover = r2.step(turnover)
            r3.step(turnover)
            self.assertEqual(r1.getPosition(), 'U')
            self.assertEqual(r2.getPosition(), 'F')
            self.assertEqual(r3.getPosition(), 'B')

    unittest.main()
