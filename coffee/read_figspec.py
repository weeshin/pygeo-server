import numpy as np
import matplotlib.pyplot as plt

# Define file paths
hdr_file = "D:\hyperspectral\coffee\HS-20241212163312.hdr"
spe_file = "D:\\hyperspectral\\coffee\\HS-20241212163312.spe"

# Parse the .hdr file
metadata = {}
with open(hdr_file, 'r') as f:
    hdr_data = f.readlines()

for line in hdr_data:
    # Strip whitespace and ignore empty lines or comments
    line = line.strip()
    if not line or line.startswith('#'):
        continue

    # Split line into key-value pairs safely
    if ' = ' in line:
        key, value = line.split(' = ', 1)
        metadata[key.strip()] = value.strip()
    else:
        print(f"Skipping malformed line: {line}")

# Print parsed metadata
print("Parsed metadata:")
for key, value in metadata.items():
    print(f"{key}: {value}")

# Map data type from metadata
dtype_map = {
    '4': np.float32,  # Replace '4' with the actual data type ID from .hdr
    '12': np.int16,   # Example: add other mappings as needed
}
dtype = dtype_map.get(metadata.get('data type'), np.float32)

# Extract other metadata
interleave = metadata.get('interleave', '').lower()  # e.g., 'bil', 'bip', 'bsq'
samples = int(metadata.get('samples', 0))
bands = int(metadata.get('bands', 0))
lines = int(metadata.get('lines', 0))

# Load the spectral data
data = np.fromfile(spe_file, dtype=dtype)

# Reshape the data based on interleave
if interleave == 'bil':  # Band Interleaved by Line
    data = data.reshape((lines, bands, samples))
elif interleave == 'bip':  # Band Interleaved by Pixel
    data = data.reshape((lines, samples, bands))
elif interleave == 'bsq':  # Band Sequential
    data = data.reshape((bands, lines, samples))
else:
    print("Unknown interleave format. Data may not be reshaped correctly.")

print("First band (wavelength):")
print(data[0, :, :])  # For 'bsq' interleave

# Access wavelengths
wavelengths = metadata.get('wavelength', '')
if wavelengths.startswith('{') and wavelengths.endswith('}'):
    wavelengths = wavelengths.strip('{}').split(',')
    wavelengths = [float(w) for w in wavelengths]
else:
    print("Wavelength data is missing or malformed.")
    wavelengths = []

print("===============================")
# print("Wavelengths:", wavelengths)

import matplotlib.pyplot as plt

# Example: Display the first band
print(data.shape)
first_band = data[100, :, :] if interleave == 'bsq' else data[:, 0, :]
plt.imshow(first_band, cmap='gray')
plt.colorbar()
plt.title("First Band (Wavelength)")
plt.show()
