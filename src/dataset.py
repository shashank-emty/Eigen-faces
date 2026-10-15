"""
Dataset loader and preprocessor for Eigenfaces experiments.
Loads the Olivetti / AT&T face database and creates structured splits:
- Known training faces (gallery)
- Known testing faces (probes of enrolled subjects)
- Unknown testing faces (probes of unseen subjects)
- Non-face images (for testing face detection/rejection)
"""

from typing import Dict, Optional, Tuple
import numpy as np
from sklearn.datasets import fetch_olivetti_faces


def load_face_data(
    train_per_subject: int = 7,
    num_known_subjects: int = 35,
    random_state: int = 42,
) -> Dict[str, np.ndarray]:
    """
    Load and partition the Olivetti Faces dataset (400 images, 40 subjects, 64x64).

    Partitioning:
    - Known subjects (0 to num_known_subjects - 1):
        * train_per_subject images -> X_train, y_train
        * (10 - train_per_subject) images -> X_test_known, y_test_known
    - Unknown subjects (num_known_subjects to 39):
        * all 10 images -> X_test_unknown, y_test_unknown

    Returns:
        dict containing:
            - 'X_train': (M_train, 64, 64)
            - 'y_train': (M_train,)
            - 'X_test_known': (M_test_known, 64, 64)
            - 'y_test_known': (M_test_known,)
            - 'X_test_unknown': (M_test_unknown, 64, 64)
            - 'y_test_unknown': (M_test_unknown,)
            - 'image_shape': (64, 64)
    """
    import os
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    data = fetch_olivetti_faces(data_home=data_dir, shuffle=False)
    images = data.images  # (400, 64, 64), normalized to [0, 1]
    targets = data.target  # 40 subjects, 10 images each

    rng = np.random.RandomState(random_state)

    X_train_list, y_train_list = [], []
    X_test_known_list, y_test_known_list = [], []
    X_test_unknown_list, y_test_unknown_list = [], []

    for subject_id in range(40):
        subject_indices = np.where(targets == subject_id)[0]
        # Shuffle images for this subject deterministically
        perm = rng.permutation(subject_indices)

        if subject_id < num_known_subjects:
            train_idx = perm[:train_per_subject]
            test_idx = perm[train_per_subject:]

            X_train_list.append(images[train_idx])
            y_train_list.append(targets[train_idx])

            X_test_known_list.append(images[test_idx])
            y_test_known_list.append(targets[test_idx])
        else:
            X_test_unknown_list.append(images[perm])
            y_test_unknown_list.append(targets[perm])

    return {
        "X_train": np.vstack(X_train_list),
        "y_train": np.concatenate(y_train_list),
        "X_test_known": np.vstack(X_test_known_list),
        "y_test_known": np.concatenate(y_test_known_list),
        "X_test_unknown": np.vstack(X_test_unknown_list),
        "y_test_unknown": np.concatenate(y_test_unknown_list),
        "image_shape": (64, 64),
    }


def generate_non_face_samples(
    n_samples: int = 10,
    shape: Tuple[int, int] = (64, 64),
    random_state: int = 42,
) -> Tuple[np.ndarray, list]:
    """
    Generate realistic non-face images (textures, gradients, geometric patterns, noise)
    to test Turk & Pentland's face-space rejection rule (epsilon_d >= theta_face).

    Returns:
        non_faces: (n_samples, shape[0], shape[1])
        descriptions: list of descriptions for each non-face
    """
    rng = np.random.RandomState(random_state)
    h, w = shape
    samples = []
    descriptions = []

    # 1. Uniform noise
    samples.append(rng.uniform(0.1, 0.9, size=(h, w)))
    descriptions.append("Uniform Random Noise")

    # 2. Checkerboard texture
    cb = np.indices((h, w)).sum(axis=0) % 2
    samples.append(cb.astype(np.float64))
    descriptions.append("Checkerboard Pattern")

    # 3. Horizontal gradient
    grad_h = np.linspace(0, 1, w)[np.newaxis, :].repeat(h, axis=0)
    samples.append(grad_h)
    descriptions.append("Linear Horizontal Gradient")

    # 4. Vertical gradient
    grad_v = np.linspace(0, 1, h)[:, np.newaxis].repeat(w, axis=1)
    samples.append(grad_v)
    descriptions.append("Linear Vertical Gradient")

    # 5. Concentric circles / radial pattern
    y, x = np.ogrid[:h, :w]
    r = np.sqrt((x - w / 2) ** 2 + (y - h / 2) ** 2)
    radial = 0.5 + 0.5 * np.sin(r / 3.0)
    samples.append(radial)
    descriptions.append("Radial Ripple Pattern")

    # 6. Diagonal striped texture
    stripes = 0.5 + 0.5 * np.sin((x + y) / 4.0)
    samples.append(stripes)
    descriptions.append("Diagonal Waves")

    # 7. Salt and pepper block
    sp = rng.choice([0.0, 1.0], size=(h, w), p=[0.5, 0.5])
    samples.append(sp)
    descriptions.append("Binary Salt-and-Pepper")

    # 8. High-frequency sinusoidal grating
    grating = np.tile(0.5 + 0.5 * np.cos(np.linspace(0, 10 * np.pi, w)), (h, 1))
    samples.append(grating)
    descriptions.append("High-Frequency Grating")

    # 9. Random blobs / coarse texture
    coarse = rng.randn(h // 4, w // 4)
    from scipy.ndimage import zoom
    coarse_zoomed = zoom(coarse, (4, 4), order=1)[:h, :w]
    coarse_norm = (coarse_zoomed - coarse_zoomed.min()) / (coarse_zoomed.max() - coarse_zoomed.min() + 1e-6)
    samples.append(coarse_norm)
    descriptions.append("Coarse Organic Texture")

    # 10. Center box / square frame
    box = np.zeros((h, w), dtype=np.float64)
    box[h // 4 : 3 * h // 4, w // 4 : 3 * w // 4] = 0.8
    samples.append(box)
    descriptions.append("Geometric Box")

    # Ensure every sample has shape (h, w) and float64
    clean_samples = [np.asarray(s, dtype=np.float64).reshape((h, w)) for s in samples[:n_samples]]
    samples_arr = np.stack(clean_samples, axis=0)
    return samples_arr, descriptions[:n_samples]
