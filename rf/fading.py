import math
import random


def rayleigh_fading():
    x = random.gauss(0, 1)
    y = random.gauss(0, 1)

    h = complex(x, y) / math.sqrt(2)

    return h

def rician_fading(k_factor=5):
    los = math.sqrt(k_factor / (k_factor + 1))

    scatter_real = random.gauss(0, 1 / math.sqrt(2))
    scatter_imag = random.gauss(0, 1 / math.sqrt(2))

    scatter = complex(scatter_real, scatter_imag)

    h = los + scatter / math.sqrt(k_factor + 1)

    return h

def nakagami_fading(m=1):
    omega = 1.0

    power = random.gammavariate(
        m,
        omega / m
    )

    amplitude = math.sqrt(power)

    phase = random.uniform(0, 2 * math.pi)

    h = amplitude * complex(
        math.cos(phase),
        math.sin(phase)
    )

    return h