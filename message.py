import re
import textwrap

import enigma

def encode(e, i, key, msg, src):
    assert(len(key) == 6)

    # normalize message
    norm_msg = msg.replace(' ', 'X').upper()
    norm_msg = re.sub(r'[^A-Z]', '', norm_msg)

    # first 3 letters of key sent in the clear
    out = key[0:3]

    # send next 3 letters of key twice, encoded using 1st half of key as starting position
    e.setPosition(key[0:3])
    out += e.translate(key[3:6] * 2)

    # set position using 2nd half of key
    e.setPosition(key[3:6])

    # encode message
    out += e.translate(norm_msg)

    # format output
    out = textwrap.fill(f'{f"{i})":<4}' + ' '.join(out[i:i+5] for i in range(0, len(out), 5)),
                        width=39, subsequent_indent=' ' * 4)

    # format solution
    sol = textwrap.fill(f'{f"{i})":<4}{key} {src}', width=64, subsequent_indent=' ' * 11)
    sol += '\n'
    sol += textwrap.fill(msg, width=64, initial_indent=' ' * 4, subsequent_indent=' ' * 4)

    return sol, out

def main():
    e = enigma.Enigma('I', 'IV', 'V', 'B', ring='AOA', cables=['AL', 'CT', 'FN', 'OY'])
    p = 'A' * 40
    c = e.translate(p)
    print(p)
    print(c)

    ciphers = []
    solutions = []

    s, c = encode(e, 1, 'AAAAAA', 'Be Sure To Drink Your Ovaltine.', 'Christmas story')
    ciphers.append(c)
    solutions.append(s)

    s, c = encode(e, 2, 'ABCDEF', 'Knowledge is power.', "Elizebeth Friedman's hidden message on William Friedman's tombstone (Francis Bacon)")
    ciphers.append(c)
    solutions.append(s)

    s, c = encode(e, 3, 'MORRIS', 'Rule one of cryptanalysis: check for plaintext.', 'Robert Morris')
    ciphers.append(c)
    solutions.append(s)

    s, c = encode(e, 4, 'MTWAIN', 'Clothes make the man. Naked people have little or no influence in society.', 'Mark Twain')
    ciphers.append(c)
    solutions.append(s)

    s, c = encode(e, 5, 'MYDOOM', 'Error mail transaction failed.', 'Mydoom.A')
    ciphers.append(c)
    solutions.append(s)

    s, c = encode(e, 6, 'DIFFIE', 'The secret to strong security: less reliance on secrets.', 'Whitfield Diffie')
    ciphers.append(c)
    solutions.append(s)

    s, c = encode(e, 7, 'TURING', 'Sometimes it is the people no one imagines anything of who do the things that no one can imagine.', 'Alan Turing')
    ciphers.append(c)
    solutions.append(s)

    s, c = encode(e, 8, 'ABASIN', "If you're not falling, you're not learning.", 'a little something about skiing')
    ciphers.append(c)
    solutions.append(s)

    s, c = encode(e, 9, 'ASIMOV', 'People who think they know everything are a great annoyance to those of us who do.', 'Isaac Asimov')
    ciphers.append(c)
    solutions.append(s)

    s, c = encode(e, 10, 'GIBSON', "The future is here. It's just not widely distributed yet.", 'William Gibson')
    ciphers.append(c)
    solutions.append(s)

    e.setPosition('AAA')
    p = 'A' * 40
    c = e.translate(p)
    print(p)
    print(c)
    print()

    print('\n\n'.join(solutions))
    print('\n')
    print('\n\n'.join(ciphers))

    e.setPosition('DWS')
    p = 'Z' * 300
    c = e.translate(p)
    out = textwrap.fill(' '.join(c[i:i+5] for i in range(0, len(c), 5)), width=39)
    print(out)

if __name__ == '__main__':
    main()