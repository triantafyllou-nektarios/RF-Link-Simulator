import math

import random

from rf.modulation import (

    bpsk_modulate,

    bpsk_demodulate,

    qpsk_modulate,

    qpsk_demodulate,

    qam16_modulate,

    qam16_demodulate

)

from rf.stbc import alamouti_encode, alamouti_decode
from rf.fading import rayleigh_fading, rician_fading, nakagami_fading

from rf.mrc import mrc_combine

import matplotlib.pyplot as plt

print("==============================")
print("       RF LINK SIMULATOR")
print("==============================")
print()
print("Select transmission system:")
print("1. SISO")
print("2. MIMO")

system_choice = input("Enter choice: ")

if system_choice == "1":
    system = "SISO"

elif system_choice == "2":
    system = "MIMO"

else:
    print("Invalid system choice.")
    exit()

if system == "MIMO":

    print()
    print("Select MIMO technique:")
    print("1. Alamouti STBC (2Tx - 1Rx)")
    print("2. MRC (1Tx - 2Rx)")
    print("3. MRC (1Tx - 4Rx)")
    print("4. Compare all MIMO techniques")

    mimo_choice = input("Enter choice: ")

    if mimo_choice == "1":
        mimo_technique = "Alamouti"

    elif mimo_choice == "2":
        mimo_technique = "MRC"
        n_rx = 2

    elif mimo_choice == "3":
        mimo_technique = "MRC"
        n_rx = 4

    elif mimo_choice == "4":
        mimo_technique = "Compare"
        comparison_results = {}

    else:
        print("Invalid MIMO choice.")
        exit()

if system == "SISO":
    tx_power = float(input("Transmit power (dBm): "))

    tx_gain = float(input("Tx antenna gain (dBi): "))

    rx_gain = float(input("Rx antenna gain (dBi): "))

    bandwidth = float(input("Bandwidth (MHz): "))

    frequency = float(input("Frequency (MHz): "))

    distance = float(input("Distance (km): "))

    cable_loss = float(input("Cable loss (dB): "))

    amount_of_obstacles = int(input("Amount of obstacles: "))


    losses = []


    for i in range(amount_of_obstacles):

        loss = float(input(f"Loss of obstacle {i + 1} (dB): "))
        losses.append(loss)





    total_loss = 0



    for loss in losses:
        total_loss = total_loss + loss


    print()
    print("Select modulation:")

    print("1. BPSK")
    print("2. QPSK")
    print("3. 16-QAM")



    modulation_choice = input("Enter choice: ")
    print()
    print("Select channel:")

    print("1. AWGN")
    print("2. Rayleigh fading")
    print("3. Rician fading")
    print("4. Nakagami-m fading")

    channel_choice = input("Enter choice: ")


    if channel_choice == "1":
        channel = "AWGN"

    elif channel_choice == "2":
        channel = "Rayleigh"

    elif channel_choice == "3":
        channel = "Rician"

    elif channel_choice == "4":
        channel = "Nakagami"

    else:
        print("Invalid channel choice.")
        exit()



    if modulation_choice == "1":

        modulation = "BPSK"



    elif modulation_choice == "2":

        modulation = "QPSK"



    elif modulation_choice == "3":

        modulation = "16-QAM"


    else:

        print("Invalid modulation choice.")
        exit()


    bandwidth_hz = bandwidth * 1_000_000

    noise_figure = 5

    noise_power = -174 + 10 * math.log10(bandwidth_hz) + noise_figure

    bits = []


    for i in range(10000):

        bit = random.choice([0, 1])
        bits.append(bit)


    if modulation == "BPSK":
        symbols = bpsk_modulate(bits)


    elif modulation == "QPSK":
        symbols = qpsk_modulate(bits)


    elif modulation == "16-QAM":
        symbols = qam16_modulate(bits)


    fspl = (20 * math.log10(distance)+ 20 * math.log10(frequency)+ 32.44)

    received_power = (tx_power + tx_gain + rx_gain - fspl - cable_loss - total_loss)

    snr = received_power - noise_power
    snr_linear = 10 ** (snr / 10)
    sigma = math.sqrt(1 / (2 * snr_linear))

    if channel == "AWGN":
        h = complex(1, 0)

    elif channel == "Rayleigh":
        h = rayleigh_fading()

    elif channel == "Rician":
        h = rician_fading(k_factor=5)

    elif channel == "Nakagami":
        m = float(input("Enter Nakagami m (0.5, 1, 3): "))
        h = nakagami_fading(m=m)


    print(f"Channel coefficient: {h}")
    print(f"Channel magnitude:   {abs(h):.4f}")
    print(f"Channel phase:       {math.degrees(math.atan2(h.imag, h.real)):.2f} degrees")
    print()
    print("==============================")
    print("       LINK RESULTS")
    print("==============================")
    print(f"Modulation:        {modulation}")
    print(f"Total additional loss: {cable_loss + total_loss:.2f} dB")
    print(f"FSPL:              {fspl:.2f} dB")
    print(f"Received Power:    {received_power:.2f} dBm")
    print(f"Noise Power:       {noise_power:.2f} dBm")
    print(f"SNR:               {snr:.2f} dB")
    print(f"SNR linear:        {snr_linear:.4f}")
    print(f"Noise sigma:       {sigma:.6f}")

    received_symbols = []

    for symbol in symbols:
        noise_real = random.gauss(0, sigma)
        noise_imag = random.gauss(0, sigma)
        noise = complex(noise_real,noise_imag)

        faded_signal = h * symbol

        received = faded_signal + noise

        received_symbols.append(received)


    equalized_symbols = []


    for received in received_symbols:
        equalized = received / h
        equalized_symbols.append(equalized)


    if modulation == "BPSK":
        received_bits = bpsk_demodulate(equalized_symbols)


    elif modulation == "QPSK":
        received_bits = qpsk_demodulate(equalized_symbols)


    elif modulation == "16-QAM":
        received_bits = qam16_demodulate(equalized_symbols)

    errors = 0

    for i in range(len(bits)):

        if bits[i] != received_bits[i]:

            errors = errors + 1

    ber = errors / len(bits)

    print()
    print("==============================")
    print("       COMMUNICATION")
    print("==============================")
    print(f"Bits transmitted: {len(bits)}")
    print(f"Bit errors:       {errors}")
    print(f"BER:              {ber:.6f}")
    plt.figure(figsize=(6, 6))

    real_parts = [s.real for s in received_symbols]
    imag_parts = [s.imag for s in received_symbols]

    plt.scatter(real_parts, imag_parts, color='blue', alpha=0.3, s=10, label='Received Symbols')
    plt.axhline(0, color='black', linewidth=1, linestyle='--')
    plt.axvline(0, color='black', linewidth=1, linestyle='--')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.title(f"Constellation Diagram ({modulation} over {channel})")
    plt.xlabel("In-Phase (I)")
    plt.ylabel("Quadrature (Q)")
    plt.legend()
    plt.axis('equal')
    plt.show()

elif system == "MIMO":

    print("\nSelect modulation:")
    print("1. BPSK")
    print("2. QPSK")
    print("3. 16-QAM")

    modulation_choice = input("Enter choice: ")

    if modulation_choice == "1":
        modulation = "BPSK"
        modulate = bpsk_modulate
        demodulate = bpsk_demodulate

    elif modulation_choice == "2":
        modulation = "QPSK"
        modulate = qpsk_modulate
        demodulate = qpsk_demodulate

    elif modulation_choice == "3":
        modulation = "16-QAM"
        modulate = qam16_modulate
        demodulate = qam16_demodulate

    else:
        print("Invalid modulation choice.")
        exit()

    bits = [random.randint(0, 1) for _ in range(10000)]
    symbols = modulate(bits)

    print("\nBits transmitted:", len(bits))
    print("Symbols generated:", len(symbols))

    print("\nSelect channel:")
    print("1. Rayleigh fading")
    print("2. Rician fading")
    print("3. Nakagami-m fading")

    channel_choice = input("Enter choice: ")

    if channel_choice == "1":
        channel_type = "Rayleigh"

    elif channel_choice == "2":
        channel_type = "Rician"
        k_factor = float(input("Enter Rician K factor: "))

    elif channel_choice == "3":
        channel_type = "Nakagami"
        m = float(input("Enter Nakagami m parameter: "))

    else:
        print("Invalid channel choice.")
        exit()


    def generate_channel():

        if channel_type == "Rayleigh":
            return rayleigh_fading()

        elif channel_type == "Rician":
            return rician_fading(k_factor)

        elif channel_type == "Nakagami":
            return nakagami_fading(m)


    snr_values = list(range(0, 22, 2))

    # Alamouti 

    def simulate_alamouti():

        ber_values = []
        last_decoded_symbols = []

        for snr_db in snr_values:

            snr_linear = 10 ** (snr_db / 10)
            noise_sigma = math.sqrt(1 / (2 * snr_linear))

            decoded_symbols = []

            for i in range(0, len(symbols), 2):

                s1 = symbols[i]
                s2 = symbols[i + 1]

                tx1, tx2 = alamouti_encode(s1, s2)

                h1 = generate_channel()
                h2 = generate_channel()

                n1 = complex(random.gauss(0, noise_sigma),random.gauss(0, noise_sigma))

                n2 = complex( random.gauss(0, noise_sigma),random.gauss(0, noise_sigma))

                r1 = (h1 * tx1[0] + h2 * tx2[0]) / math.sqrt(2) + n1

                r2 = ( h1 * tx1[1] + h2 * tx2[1]) / math.sqrt(2) + n2

                s1_hat, s2_hat = alamouti_decode(r1, r2, h1, h2)

                decoded_symbols.append(s1_hat * math.sqrt(2))
                decoded_symbols.append(s2_hat * math.sqrt(2))

            received_bits = demodulate(decoded_symbols)

            errors = sum(
                bits[i] != received_bits[i]
                for i in range(len(bits))
            )

            ber = errors / len(bits)
            ber_values.append(ber)

            print(
                f"Alamouti | SNR: {snr_db} dB | "
                f"Errors: {errors} | BER: {ber:.6f}"
            )

            last_decoded_symbols = decoded_symbols

        return ber_values, last_decoded_symbols


    # MRC simulation

    def simulate_mrc(n_rx):

        ber_values = []
        last_decoded_symbols = []

        for snr_db in snr_values:

            snr_linear = 10 ** (snr_db / 10)
            noise_sigma = math.sqrt(1 / (2 * snr_linear))

            decoded_symbols = []

            for symbol in symbols:

                channel_coefficients = []
                received_signals = []

                for _ in range(n_rx):

                    h = generate_channel()
                    channel_coefficients.append(h)

                    noise = complex(random.gauss(0, noise_sigma),random.gauss(0, noise_sigma))

                    received = h * symbol + noise
                    received_signals.append(received)

                combined = mrc_combine(
                    received_signals,
                    channel_coefficients
                )

                decoded_symbols.append(combined)

            received_bits = demodulate(decoded_symbols)

            errors = sum(
                bits[i] != received_bits[i]
                for i in range(len(bits))
            )

            ber = errors / len(bits)
            ber_values.append(ber)

            print(
                f"MRC {n_rx}Rx | SNR: {snr_db} dB | "
                f"Errors: {errors} | BER: {ber:.6f}"
            )

            last_decoded_symbols = decoded_symbols

        return ber_values, last_decoded_symbols


    # Run


    results = {}
    constellation_results = {}

    if mimo_technique == "Alamouti":

        results["Alamouti 2Tx-1Rx"], constellation_results["Alamouti"] = (
            simulate_alamouti()
        )

    elif mimo_technique == "MRC":

        results[f"MRC 1Tx-{n_rx}Rx"], constellation_results["MRC"] = (
            simulate_mrc(n_rx)
        )

    elif mimo_technique == "Compare":

        results["Alamouti 2Tx-1Rx"], constellation_results["Alamouti"] = (
            simulate_alamouti()
        )

        results["MRC 1Tx-2Rx"], constellation_results["MRC 2Rx"] = (
            simulate_mrc(2)
        )

        results["MRC 1Tx-4Rx"], constellation_results["MRC 4Rx"] = (
            simulate_mrc(4)
        )


    #  BER vs SNR plot


    plt.figure(figsize=(9, 6))

    for label, ber_values in results.items():

        # Avoid zero values on logarithmic plot
        plot_values = [
            max(ber, 0.5 / len(bits))
            for ber in ber_values
        ]

        plt.semilogy(
            snr_values,
            plot_values,
            marker="o",
            label=label
        )

    plt.title(
        f"MIMO BER vs SNR - {modulation} - {channel_type}"
    )

    plt.xlabel("SNR (dB)")
    plt.ylabel("Bit Error Rate (BER)")
    plt.grid(True, which="both")
    plt.legend()
    plt.tight_layout()
    plt.show()



    for label, decoded_symbols in constellation_results.items():

        plt.figure(figsize=(6, 6))

        plt.scatter(
            [s.real for s in decoded_symbols],
            [s.imag for s in decoded_symbols],
            s=5,
            alpha=0.5
        )

        plt.title(f"{label} Constellation - {modulation}")
        plt.xlabel("In-phase")
        plt.ylabel("Quadrature")
        plt.grid(True)
        plt.axis("equal")
        plt.tight_layout()
        plt.show()
