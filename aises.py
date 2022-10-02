import re
import textwrap

import enigma

def encode(e, i, key, msg):
    assert(len(key) == 3)

    # normalize message
    norm_msg = msg.replace(' ', 'X').upper()
    norm_msg = re.sub(r'[^A-Z]', '', norm_msg)

    # set position using key
    e.setPosition(key)

    # encode message
    out = e.translate(norm_msg)

    # format output
    out = textwrap.fill(f'{f"{i})":<4}' + ' '.join(out[i:i+5] for i in range(0, len(out), 5)),
                        width=39, subsequent_indent=' ' * 4)

    # format solution
    sol = textwrap.fill(f'{f"{i})":<4}{key}: {msg}', width=74, subsequent_indent=' ' * 11)

    return sol, out

def main():
    e = enigma.Enigma('V', 'IV', 'I', 'B', ring='FOD', cables=['AL', 'CT', 'FN', 'IY'])

    # sanity check, rotors at position AAA
    p = 'A' * 90
    c = e.translate(p)
    p = textwrap.fill(' '.join(p[i:i+5] for i in range(0, len(p), 5)), width=20)
    c = textwrap.fill(' '.join(c[i:i+5] for i in range(0, len(c), 5)), width=20)
    print(p)
    print(c)
    print()

    ciphers = []
    solutions = []

    puzzles = [ (None, 'AAA'),
                ('SIGINT Agency', 'NSA'),
                ('Put me in a lock', 'KEY'),
                ('Untruth', 'LIE'),
                ('Secret agent', 'SPY'),
                ('Decimal base', 'TEN'),
                ('Binary digit', 'BIT'),
                ('Boolean truth value', 'ONE'),
                ('Numeric datatype', 'INT'),
                ('Base sixteen', 'HEX'),
                ('Ghidra purpose', 'SRE'),
                ('Intel copy mnemonic', 'MOV'),
                ('Forty-five years of advancing indigenous people in STEM', None) ]

    for i in range(1, len(puzzles)):
        key = puzzles[i-1][1]
        question = puzzles[i][0]
        s, c = encode(e, i, key, question)
        ciphers.append(c)
        solutions.append(s)

    print('\n'.join(solutions))
    print()
    print('\n'.join(ciphers))

if __name__ == '__main__':
    main()
