import random
import math

def generate_mimo_channel(n_tx, n_rx, channel_type, k_factor=5):

    H = []

    for rx in range(n_rx):

        row = []

        for tx in range(n_tx):

            if channel_type == "Rayleigh":

                x = random.gauss(0, 1)
                y = random.gauss(0, 1)

                h = complex(x, y) / math.sqrt(2)

            elif channel_type == "Rician":

                los = math.sqrt(k_factor / (k_factor + 1))

                scatter_real = random.gauss(0, 1 / math.sqrt(2))
                scatter_imag = random.gauss(0, 1 / math.sqrt(2))

                scatter = complex(scatter_real, scatter_imag)

                h = los + scatter / math.sqrt(k_factor + 1)

            elif channel_type == "AWGN":

                h = complex(1, 0)

            else:

                raise ValueError("Unknown channel type")

            row.append(h)

        H.append(row)

    return H
