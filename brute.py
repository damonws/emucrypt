import string
import random

import enigma

#ROTORS = ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII')
ROTORS = ('I', 'IV', 'V')

def random_rotors():
    all = list(ROTORS)
    random.shuffle(all)
    return all

def random_reflector():
    return random.choice(('B', 'C'))

def random_letter():
    return random.choice((string.ascii_uppercase))

def random_3letters():
    return random_letter() + random_letter() + random_letter()

def random_cables():
    count = random.randrange(14, 23, 2)
    letters = list(string.ascii_uppercase[:count])
    random.shuffle(letters)
    return [f'{letters[i]}{letters[i+1]}' for i in range(0, count, 2)]

def create_random_enigma(r1=None, r2=None, r3=None, rf=None, pos=None, ring=None, cables=None):
    rotors = random_rotors()
    if r1 is None: r1 = rotors.pop()
    if r2 is None: r2 = rotors.pop()
    if r3 is None: r3 = rotors.pop()
    if rf is None: rf = random_reflector()
    if pos is None: pos = random_3letters()
    if ring is None: ring = random_3letters()
    if cables is None: cables = random_cables()

    e = enigma.Enigma(r1, r2, r3, rf, pos, ring, cables)

    print('Created Enigma')
    print(f'ROTORS: {r1}, {r2}, {r3}')
    print(f'REFLECTOR: {rf}')
    print(f'POS: {pos}')
    print(f'RING: {ring}')
    print(f'CABLES: {cables}')

    return e

def find_key(pos, cables, plain, cipher):
    for r1 in ROTORS:
        for r2 in ROTORS:
            if r2 == r1:
                continue
            for r3 in ROTORS:
                if r3 in (r1, r2):
                    continue
                #for rf in ('B', 'C'):
                for rf in ('B', ):
                    for ring1 in string.ascii_uppercase:
                        for ring2 in string.ascii_uppercase:
                            for ring3 in string.ascii_uppercase:
                                ring = ring1 + ring2 + ring3
                                e = enigma.Enigma(r1, r2, r3, rf, pos, ring, cables)
                                if e.match(plain, cipher):
                                    print(r1, r2, r3, rf, ring)

def trial():
    #random.seed(2)
    cables = random_cables()
    e = create_random_enigma(pos='AAA', cables=cables)
    p = 'A' * 10
    c = e.translate(p)
    print(c[:64])
    find_key('AAA', cables, p, c)

def brute():
    #cables = ['YL', 'CT', 'FN']
    #c = 'HPXWEUMKZW'
    #find_key('AAA', cables, p, c)

    # get from Enigma
    cables = ['AL', 'CT', 'FN', 'IY']

    #c = 'VJPUFSIEOH'
    #find_key('AAA', cables, p, c)

    #c = 'TWGHOZVFDJ'
    #find_key('CMW', cables, p, c)

    #c = 'DRJVQKOJNU'
    #find_key('EBH', cables, p, c)

    # output from typing A's, rotors starting at "AAA"
    c = 'OIZVZSRXOM'

    p = 'A' * len(c)
    find_key('GTO', cables, p, c)

if __name__ == '__main__':
    #trial()
    brute()
