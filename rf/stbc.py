def alamouti_encode(symbol1, symbol2):

    tx1 = [symbol1, -symbol2.conjugate()]
    tx2 = [symbol2, symbol1.conjugate()]

    return tx1, tx2
def alamouti_decode(r1, r2, h1, h2):

    denominator = abs(h1)**2 + abs(h2)**2

    if denominator == 0:
        raise ValueError("Channel gain cannot be zero")

    s1 = (h1.conjugate() * r1 + h2 * r2.conjugate()) / denominator

    s2 = (h2.conjugate() * r1 - h1 * r2.conjugate()) / denominator

    return s1, s2