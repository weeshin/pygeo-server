import numpy as np
import pandas as pd

# Function to parse the .hdr file and load metadata
def parse_hdr(hdr_file):
    metadata = {}
    with open(hdr_file, 'r') as f:
        hdr_data = f.readlines()

    for line in hdr_data:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ' = ' in line:
            key, value = line.split(' = ', 1)
            metadata[key.strip()] = value.strip()
        else:
            print(f"Skipping malformed line: {line}")
    return metadata

# Function to load hyperspectral data using metadata
def load_hyperspectral_data(hdr_file, spe_file):
    # Parse the metadata
    metadata = parse_hdr(hdr_file)
    
    # Map data type
    dtype_map = {
        '4': np.float32,
        '12': np.int16,
    }
    dtype = dtype_map.get(metadata.get('data type'), np.float32)

    # Extract metadata
    interleave = metadata.get('interleave', '').lower()
    samples = int(metadata.get('samples', 0))
    bands = int(metadata.get('bands', 0))
    lines = int(metadata.get('lines', 0))

    # Load the spectral data
    data = np.fromfile(spe_file, dtype=dtype)

    # Reshape based on interleave
    if interleave == 'bil':
        data = data.reshape((lines, bands, samples))
    elif interleave == 'bip':
        data = data.reshape((lines, samples, bands))
    elif interleave == 'bsq':
        data = data.reshape((bands, lines, samples))
    else:
        raise ValueError(f"Unknown interleave format: {interleave}")

    return data

# Load CSV file for image names and labels
labels_df = pd.read_csv('D:\\hyperspectral\\coffee\\labels.csv')  # Replace with your actual file path

# Prepare dataset
data = []
all_labels = []

for _, row in labels_df.iterrows():
    image_name = row['image_name']
    label = row['label']
    
    # Define file paths
    hdr_file = f"D:\\hyperspectral\\coffee\\{image_name}.hdr"
    spe_file = f"D:\\hyperspectral\\coffee\\{image_name}.spe"
    
    # Load the hyperspectral image
    hyperspectral_data = load_hyperspectral_data(hdr_file, spe_file)
    
    print(hyperspectral_data)

    # Reshape to (pixels, bands) assuming spatial dimensions first
    if hyperspectral_data.ndim == 3:
        flattened_data = hyperspectral_data.reshape(-1, hyperspectral_data.shape[-1])
    else:
        raise ValueError("Unexpected data dimensions for hyperspectral image")

    # Append data and labels
    data.append(flattened_data)
    all_labels.extend([label] * flattened_data.shape[0])

# Combine data and labels
data = np.vstack(data)  # Shape: (total_pixels, bands)
all_labels = np.array(all_labels)  # Shape: (total_pixels,)

print(all_labels)
print(data.shape)
# Save the dataset
np.savez('hyperspectral_dataset.npz', data=data, labels=all_labels)

print("Dataset prepared and saved as 'hyperspectral_dataset.npz'")
