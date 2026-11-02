def mrc_combine(received_signals, channel_coefficients):

    numerator = 0
    denominator = 0

    for r, h in zip(received_signals, channel_coefficients):

        numerator += h.conjugate() * r

        denominator += abs(h)**2

    if denominator == 0:
        raise ValueError("Channel gain cannot be zero")

    combined_signal = numerator / denominator

    return combined_signal