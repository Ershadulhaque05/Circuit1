from qiskit import QuantumCircuit
import numpy as np

def int_to_bin_list(value, bits):
    """Convert integer to binary list of bits (big-endian)."""
    return list(map(int, format(value, '0{}b'.format(bits))))

def prepare_NEQR(image):
    """
    Simulate NEQR encoding for a small grayscale image.
    Image must be a 2D numpy array with pixel values in [0, 255].
    """
    height, width = new_func1(image)
    n = int(np.ceil(np.log2(max(height, width))))  # position qubits per axis
    q = 8  # grayscale qubits (8 bits for 0-255)

    total_qubits = 2 * n + q
    qc = QuantumCircuit(total_qubits, name='NEQR')

    # Put position qubits into superposition
    for i in range(2 * n):
        qc.h(i)

    # Now, classically simulate mapping pixel values
    for y in range(height):
        for x in range(width):
            pixel_value = image[y, x]
            bin_pixel = int_to_bin_list(pixel_value, q)

            # Position address
            new_var = int_to_bin_list(y, n) + int_to_bin_list(x, n)
            address = new_var

            controls = []  # use list, and use append

            # Loop over address (pixel location)
            for idx, bit in enumerate(address):
                #if bit == 0:
                #qc.x(idx)  # Flip qubit if bit is 0
                controls.append(idx)  # Add position qubit to control list

            # Loop over the grayscale pixel bits and apply multi-controlled gates
            for idx, bit in enumerate(bin_pixel):
               # if bit == 1:
                #    # Apply multi-controlled X (MCX) gate to link all qubits at the same location
                qc.mcx(controls, 2 * n + idx)

            # Uncompute: restore qubits after applying gates (important for next pixel)
          # for idx, bit in enumerate(address):
            #    if bit == 0:
             #       qc.x(idx)

    return qc

def new_func1(image):
    height, width = new_func(image)
    return height, width

def new_func(image):
    height, width = image.shape
    return height, width

if __name__ == "__main__":
    # Tiny 2x2 image example
    image = np.array([
        [0, 255],
        [128, 0]
    ], dtype=np.uint8)

    circuit = prepare_NEQR(image)
    print(circuit.draw(fold=80))
