import string

class PlugboardError(Exception): pass
class PlugboardBadChar(PlugboardError): pass
class PlugboardDuplicatePlug(PlugboardError): pass
class PlugboardMissingPlug(PlugboardError): pass
class PlugboardNeedTwoPlugs(PlugboardError): pass
class PlugboardIncorrectCable(PlugboardError): pass

class Plugboard(object):
    def __init__(self, cables=None):
        self.plugs = set()
        self.cables = []
        if cables is not None:
            for cable in cables:
                self.addCable(cable)
        self.activate()

    def insertPlug(self, char):
        if char not in string.ascii_uppercase:
            raise PlugboardBadChar()
        if char in self.plugs:
            raise PlugboardDuplicatePlug()
        self.plugs.add(char)

    def removePlug(self, char):
        try:
            self.plugs.remove(char)
        except KeyError:
            raise PlugboardMissingPlug()

    def addCable(self, cable):
        if len(cable) != 2:
            raise PlugboardNeedTwoPlugs()
        for char in cable:
            self.insertPlug(char)
        self.cables.append(cable)
        self.activate()

    def removeCable(self, cable):
        if len(cable) != 2:
            raise PlugboardNeedTwoPlugs()
        for char in cable:
            self.removePlug(char)
        if cable in self.cables:
            self.cables.remove(cable)
        elif cable[::-1] in self.cables:
            self.cables.remove(cable[::-1])
        else:
            raise PlugboardIncorrectCable()
        self.activate()

    def activate(self):
        connected = {}
        for cable in self.cables:
            connected[cable[0]] = cable[1]
            connected[cable[1]] = cable[0]
        self.table = ''.maketrans(connected)

    def translate(self, char):
        return char.translate(self.table)

if __name__ == '__main__':
    import unittest

    class TestPlugboard(unittest.TestCase):

        def test_nocables(self):
            p = Plugboard()
            for ch in string.ascii_uppercase:
                self.assertEqual(ch, p.translate(ch))

        def test_1cable(self):
            p = Plugboard(['AB'])
            self.assertEqual('A', p.translate('B'))
            self.assertEqual('B', p.translate('A'))
            for ch in string.ascii_uppercase[2:]:
                self.assertEqual(ch, p.translate(ch))

        def test_addcable(self):
            p = Plugboard()
            p.addCable('AB')
            self.assertEqual('A', p.translate('B'))
            self.assertEqual('B', p.translate('A'))
            for ch in string.ascii_uppercase[2:]:
                self.assertEqual(ch, p.translate(ch))

        def test_removecable(self):
            p = Plugboard(['AB'])
            p.removeCable('AB')
            for ch in string.ascii_uppercase:
                self.assertEqual(ch, p.translate(ch))

        def test_removereverse(self):
            p = Plugboard(['AB'])
            p.removeCable('BA')
            for ch in string.ascii_uppercase:
                self.assertEqual(ch, p.translate(ch))

        def test_multiple(self):
            p = Plugboard(('ZQ', 'TW', 'BF'))
            p.addCable('AX')
            p.removeCable('TW')
            p.addCable('TS')
            p.addCable('HI')
            p.removeCable('AX')
            p.addCable('XM')
            p.addCable('AC')
            self.assertEqual('A', p.translate('C'))
            self.assertEqual('B', p.translate('F'))
            self.assertEqual('C', p.translate('A'))
            self.assertEqual('D', p.translate('D'))
            self.assertEqual('E', p.translate('E'))
            self.assertEqual('F', p.translate('B'))
            self.assertEqual('G', p.translate('G'))
            self.assertEqual('H', p.translate('I'))
            self.assertEqual('I', p.translate('H'))
            self.assertEqual('J', p.translate('J'))
            self.assertEqual('K', p.translate('K'))
            self.assertEqual('L', p.translate('L'))
            self.assertEqual('M', p.translate('X'))
            self.assertEqual('N', p.translate('N'))
            self.assertEqual('O', p.translate('O'))
            self.assertEqual('P', p.translate('P'))
            self.assertEqual('Q', p.translate('Z'))
            self.assertEqual('R', p.translate('R'))
            self.assertEqual('S', p.translate('T'))
            self.assertEqual('T', p.translate('S'))
            self.assertEqual('U', p.translate('U'))
            self.assertEqual('V', p.translate('V'))
            self.assertEqual('W', p.translate('W'))
            self.assertEqual('X', p.translate('M'))
            self.assertEqual('Y', p.translate('Y'))
            self.assertEqual('Z', p.translate('Q'))

        def test_initbadchar(self):
            self.assertRaises(PlugboardBadChar, Plugboard, ['aB'])

        def test_initshortcable(self):
            self.assertRaises(PlugboardNeedTwoPlugs, Plugboard, ['B'])

        def test_initlongcable(self):
            self.assertRaises(PlugboardNeedTwoPlugs, Plugboard, ['ABC'])

        def test_addshortcable(self):
            p = Plugboard()
            self.assertRaises(PlugboardNeedTwoPlugs, p.addCable, ['B'])

        def test_addlongcable(self):
            p = Plugboard()
            self.assertRaises(PlugboardNeedTwoPlugs, p.addCable, ['ABC'])

        def test_removeshortcable(self):
            p = Plugboard(['AB'])
            self.assertRaises(PlugboardNeedTwoPlugs, p.removeCable, ['B'])

        def test_removelongcable(self):
            p = Plugboard(['AB', 'CD'])
            self.assertRaises(PlugboardNeedTwoPlugs, p.removeCable, ['ABC'])

        def test_duplicateplug(self):
            p = Plugboard(['MX'])
            self.assertRaises(PlugboardDuplicatePlug, p.addCable, 'MY')

        def test_duplicatecable(self):
            p = Plugboard(['MX'])
            self.assertRaises(PlugboardDuplicatePlug, p.addCable, 'MX')

        def test_removefromempty(self):
            p = Plugboard()
            self.assertRaises(PlugboardMissingPlug, p.removeCable, 'MY')

        def test_removemissingplug(self):
            p = Plugboard(['MX'])
            self.assertRaises(PlugboardMissingPlug, p.removeCable, 'MY')

        def test_removemissingcable(self):
            p = Plugboard(['MX', 'NY'])
            self.assertRaises(PlugboardIncorrectCable, p.removeCable, 'MY')

    unittest.main()
