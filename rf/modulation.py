import math


def bpsk_modulate(bits):
    symbols = []

    for bit in bits:
        if bit == 0:
            symbols.append(-1)
        else:
            symbols.append(1)

    return symbols


def bpsk_demodulate(symbols):
    bits = []

    for symbol in symbols:
        if symbol.real < 0:
            bits.append(0)
        else:
            bits.append(1)

    return bits


def qpsk_modulate(bits):
    symbols = []

    for i in range(0, len(bits), 2):
        bit1 = bits[i]
        bit2 = bits[i + 1]

        if bit1 == 0 and bit2 == 0:
            symbol = complex(1, 1)

        elif bit1 == 0 and bit2 == 1:
            symbol = complex(-1, 1)

        elif bit1 == 1 and bit2 == 1:
            symbol = complex(-1, -1)

        else:
            symbol = complex(1, -1)

        symbols.append(symbol / math.sqrt(2))

    return symbols


def qpsk_demodulate(symbols):
    bits = []

    for symbol in symbols:

        if symbol.real >= 0 and symbol.imag >= 0:
            bits.extend([0, 0])

        elif symbol.real < 0 and symbol.imag >= 0:
            bits.extend([0, 1])

        elif symbol.real < 0 and symbol.imag < 0:
            bits.extend([1, 1])

        else:
            bits.extend([1, 0])

    return bits


def gray_to_level(bits):
    if bits == [0, 0]:
        return -3

    elif bits == [0, 1]:
        return -1

    elif bits == [1, 1]:
        return 1

    else:
        return 3


def level_to_gray(level):
    if level == -3:
        return [0, 0]

    elif level == -1:
        return [0, 1]

    elif level == 1:
        return [1, 1]

    else:
        return [1, 0]


def qam16_modulate(bits):
    symbols = []

    normalization = 10 ** 0.5

    for i in range(0, len(bits), 4):

        i_bits = bits[i:i + 2]
        q_bits = bits[i + 2:i + 4]

        i_level = gray_to_level(i_bits)
        q_level = gray_to_level(q_bits)

        symbol = complex(
            i_level / normalization,
            q_level / normalization
        )

        symbols.append(symbol)

    return symbols


def qam16_demodulate(symbols):
    bits = []

    normalization = 10 ** 0.5

    levels = [-3, -1, 1, 3]

    for symbol in symbols:

        i_value = symbol.real * normalization
        q_value = symbol.imag * normalization

        i_level = min(levels, key=lambda x: abs(x - i_value))
        q_level = min(levels, key=lambda x: abs(x - q_value))

        bits.extend(level_to_gray(i_level))
        bits.extend(level_to_gray(q_level))

    return bits