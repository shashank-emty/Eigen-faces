"""
================================================================================
EIGEN FACES FOR RECOGNITION (Turk & Pentland, 1991)
================================================================================
Student Name : Shashank M T
UUCMS No.    : U01BH25C0174
Degree       : BCA(AI), 3rd Semester, 2nd Year
Subject      : Machine Learning
Institution  : Pooja Bhagavat Mahajana First Grade College, Mysuru
Course Guide : Ragunandan B (Guest Lecturer – Introduction to Machine Learning)
GitHub Repo  : https://github.com/shashank-emty/Eigen-faces
================================================================================

This is the all-in-one standalone implementation containing:
1. Local Dataset Loader (AT&T / Olivetti Faces, 40 subjects x 10 photos = 400 faces)
2. Mean Face Vector Calculation (Psi) and Mean-Centering (Phi = Gamma - Psi)
3. The Turk-Pentland Covariance Reduction Trick (L = A^T * A in R^{M x M})
4. Eigendecomposition & Eigenface Basis Vector Normalization (u_k)
5. Face Subspace Projection (Omega = U^T * Phi) & Reconstruction (Gamma_hat)
6. Complete 2-Threshold 4-Way Decision Engine (eps_d: DFFS, eps_c: DIFS)
7. Full Evaluation Benchmark & Demonstration Suite
================================================================================
"""

import os
import sys
import numpy as np
from sklearn.datasets import fetch_olivetti_faces


# ==============================================================================
# SECTION 1: EIGENFACES CORE ALGORITHM (Turk & Pentland, 1991)
# ==============================================================================
class Eigenfaces:
    """
    Pure NumPy implementation of Principal Component Analysis for Face Recognition
    using the exact formulations from Matthew Turk and Alex Pentland (1991).
    """

    def __init__(self, n_components: int = 40):
        self.n_components = n_components
        self.mean_face = None       # Psi: Shape (D,)
        self.eigenfaces = None      # U: Shape (D, K)
        self.eigenvalues = None     # Top K eigenvalues of covariance matrix
        self.all_eigenvalues = None # All eigenvalues of surrogate matrix L
        self.explained_variance_ratio = None
        self.train_weights = None   # Omega_train: Shape (K, M)
        self.train_labels = None    # Array of class labels (M,)
        self.class_centroids = {}   # Mapping: class_label -> average weight vector (K,)
        self.theta_f = None         # Face space threshold (Distance from face space)
        self.theta_c = None         # Classification threshold (Distance in face space)

    def fit(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train the Eigenfaces model:
        1. Reshape images to column vectors Gamma_i in R^D (D = 4096).
        2. Compute Average Face Psi = (1/M) * sum(Gamma_i).
        3. Mean-center faces: Phi_i = Gamma_i - Psi. Form matrix A = [Phi_1 ... Phi_M].
        4. Compute surrogate covariance matrix L = A^T * A of size (M x M).
        5. Solve eigenvectors v_k of L: L * v_k = mu_k * v_k.
        6. Recover true eigenfaces: u_k = (A * v_k) / ||A * v_k||_2.
        7. Project training faces into face space: Omega_i = U^T * Phi_i.
        8. Auto-calibrate decision thresholds theta_f and theta_c.
        """
        # Step 1: Flatten images if in 2D (M, H, W) -> (M, D)
        M, D = X_train.shape[0], X_train[0].size
        Gamma = X_train.reshape(M, D).T  # Shape: (D, M)
        self.train_labels = np.asarray(y_train)

        # Step 2: Compute Mean Face Vector (Psi)
        # Psi = (1/M) * sum_{i=1}^M Gamma_i
        self.mean_face = np.mean(Gamma, axis=1)  # Shape: (D,)

        # Step 3: Mean-Center Difference Matrix (A)
        # Phi_i = Gamma_i - Psi
        A = Gamma - self.mean_face[:, np.newaxis]  # Shape: (D, M)

        # Step 4: The Turk-Pentland Covariance Reduction Trick
        # Direct covariance C = (1/M) * A * A^T is (4096 x 4096 = 16.7 million elements) -> Intractable!
        # Instead, compute surrogate L = A^T * A of size (M x M = 245 x 245 = 60,025 elements).
        L = np.dot(A.T, A)  # Shape: (M, M)

        # Step 5: Eigendecomposition of L
        eigenvalues, eigenvectors = np.linalg.eigh(L)

        # Sort eigenvalues and eigenvectors in descending order
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Clip numerical negatives from floating point rounding
        eigenvalues = np.maximum(eigenvalues, 0.0)
        self.all_eigenvalues = eigenvalues

        # Calculate explained variance ratio
        total_var = np.sum(eigenvalues)
        self.explained_variance_ratio = (eigenvalues[:self.n_components] / total_var) if total_var > 0 else np.zeros(self.n_components)

        # Retain top K components
        K = min(self.n_components, M)
        self.eigenvalues = eigenvalues[:K]
        top_eigenvectors_v = eigenvectors[:, :K]  # Shape: (M, K)

        # Step 6: Map surrogate eigenvectors v_k back to full pixel eigenfaces u_k
        # Formula: u_k = (A * v_k) / ||A * v_k||_2
        U = np.dot(A, top_eigenvectors_v)  # Shape: (D, K)
        # Normalize each column vector to unit L2 norm
        norms = np.linalg.norm(U, axis=0, keepdims=True)
        norms[norms == 0] = 1.0
        self.eigenfaces = U / norms  # Shape: (D, K)

        # Step 7: Project training faces into face space
        # Omega = U^T * (Gamma - Psi)
        self.train_weights = np.dot(self.eigenfaces.T, A)  # Shape: (K, M)

        # Step 8: Compute class centroids (average weight vector per person)
        unique_classes = np.unique(self.train_labels)
        for c in unique_classes:
            class_indices = np.where(self.train_labels == c)[0]
            self.class_centroids[c] = np.mean(self.train_weights[:, class_indices], axis=1)

        # Step 9: Calibrate Decision Thresholds (theta_f and theta_c)
        # Calculate training reconstruction errors (eps_d)
        A_proj = np.dot(self.eigenfaces, self.train_weights)  # (D, M)
        recon_errors = np.linalg.norm(A - A_proj, axis=0)
        # theta_f sets the boundary for face space (DFFS)
        self.theta_f = float(np.max(recon_errors) + 8.0 * np.std(recon_errors))

        # Calculate within-class distances (intra-class spread)
        intra_dists = []
        for i in range(M):
            label = self.train_labels[i]
            centroid = self.class_centroids[label]
            d = np.linalg.norm(self.train_weights[:, i] - centroid)
            intra_dists.append(d)
        # theta_c: classification margin distinguishing enrolled subjects from unknown faces
        self.theta_c = float(np.mean(intra_dists) + 1.2 * np.std(intra_dists))

        return self

    def project(self, image: np.ndarray) -> np.ndarray:
        """Project an input image into the K-dimensional face subspace: Omega = U^T * (Gamma - Psi)."""
        gamma = image.flatten().astype(np.float64)
        phi = gamma - self.mean_face
        return np.dot(self.eigenfaces.T, phi)  # Shape: (K,)

    def reconstruct(self, omega: np.ndarray) -> np.ndarray:
        """Reconstruct an image vector from its weight coordinates: Gamma_hat = Psi + U * Omega."""
        phi_f = np.dot(self.eigenfaces, omega)  # Shape: (D,)
        return self.mean_face + phi_f

    def compute_distances(self, image: np.ndarray) -> tuple:
        """
        Compute Turk & Pentland's two fundamental distance metrics:
        1. eps_d (DFFS: Distance From Face Space) = ||Gamma - Gamma_hat||_2
        2. eps_c (DIFS: Distance In Face Space)   = min_k ||Omega - Omega_k||_2
        """
        gamma = image.flatten().astype(np.float64)
        omega = self.project(gamma)
        gamma_hat = self.reconstruct(omega)

        # Distance from face space (Reconstruction residual)
        eps_d = float(np.linalg.norm(gamma - gamma_hat))

        # Distance in face space to closest enrolled class centroid
        best_label = None
        min_dist = float("inf")
        for label, centroid in self.class_centroids.items():
            dist = float(np.linalg.norm(omega - centroid))
            if dist < min_dist:
                min_dist = dist
                best_label = label

        return eps_d, min_dist, best_label

    def predict(self, image: np.ndarray) -> dict:
        """
        Execute the 4-Way Decision Rule (Turk & Pentland Section 3.2):
        - If eps_d >= theta_f:              Input is NOT A FACE (Case 1)
        - If eps_d < theta_f & eps_c < theta_c:  Input is a KNOWN FACE (Case 2)
        - If eps_d < theta_f & eps_c >= theta_c: Input is an UNKNOWN FACE (Case 3)
        """
        eps_d, eps_c, predicted_label = self.compute_distances(image)

        if eps_d >= self.theta_f:
            decision = "NOT_A_FACE"
            details = f"Rejection: Distance from Face Space (eps_d={eps_d:.2f}) >= theta_f ({self.theta_f:.2f})"
        elif eps_c < self.theta_c:
            decision = "KNOWN_FACE"
            details = f"Recognized as Subject {predicted_label} (eps_c={eps_c:.2f} < theta_c={self.theta_c:.2f})"
        else:
            decision = "UNKNOWN_FACE"
            details = f"Detected new human face (eps_c={eps_c:.2f} >= theta_c={self.theta_c:.2f}). Ready for enrollment."

        return {
            "decision": decision,
            "predicted_label": predicted_label if decision == "KNOWN_FACE" else None,
            "eps_d": eps_d,
            "eps_c": eps_c,
            "theta_f": self.theta_f,
            "theta_c": self.theta_c,
            "details": details,
        }


# ==============================================================================
# SECTION 2: DATASET LOADER & PREPARATION
# ==============================================================================
def load_dataset():
    """
    Load the benchmark Olivetti / AT&T face dataset:
    - 40 unique individuals, 10 photos each (Total: 400 photos)
    - Grayscale resolution: 64 x 64 pixels (D = 4096 dimensions)
    - Partitioning:
      * 35 subjects for Training & Testing (Known subjects)
      * 5 subjects held out completely as Unseen (Unknown subjects)
    """
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    data = fetch_olivetti_faces(data_home=data_dir, shuffle=False)
    images = data.images   # Shape: (400, 64, 64), normalized [0, 1]
    targets = data.target  # Shape: (400,)

    rng = np.random.RandomState(42)
    X_train_list, y_train_list = [], []
    X_test_known_list, y_test_known_list = [], []
    X_test_unknown_list, y_test_unknown_list = [], []

    for subject_id in range(40):
        idx = np.where(targets == subject_id)[0]
        perm = rng.permutation(idx)

        if subject_id < 35:
            # First 35 subjects: 7 images for training, 3 for testing
            train_idx = perm[:7]
            test_idx = perm[7:]
            X_train_list.append(images[train_idx])
            y_train_list.append(targets[train_idx])
            X_test_known_list.append(images[test_idx])
            y_test_known_list.append(targets[test_idx])
        else:
            # Remaining 5 subjects: All 10 images held out as unknown
            X_test_unknown_list.append(images[perm])
            y_test_unknown_list.append(targets[perm])

    return {
        "X_train": np.vstack(X_train_list),
        "y_train": np.concatenate(y_train_list),
        "X_test_known": np.vstack(X_test_known_list),
        "y_test_known": np.concatenate(y_test_known_list),
        "X_test_unknown": np.vstack(X_test_unknown_list),
        "y_test_unknown": np.concatenate(y_test_unknown_list),
    }


# ==============================================================================
# SECTION 3: DEMONSTRATION & BENCHMARK SUITE
# ==============================================================================
def run_project():
    print("=" * 76)
    print("  EIGEN FACES FOR RECOGNITION (Turk & Pentland, 1991)")
    print("=" * 76)
    print("  Student Name : Shashank M T")
    print("  UUCMS No.    : U01BH25C0174")
    print("  Course       : BCA(AI), 3rd Semester, 2nd Year")
    print("  Subject      : Machine Learning")
    print("  College      : Pooja Bhagavat Mahajana First Grade College, Mysuru")
    print("  Guide        : Ragunandan B (Guest Lecturer – Introduction to Machine Learning)")
    print("  GitHub Repo  : https://github.com/shashank-emty/Eigen-faces")
    print("=" * 76)

    # Step 1: Load Data
    print("\n[STEP 1] Loading Face Dataset...")
    data = load_dataset()
    X_train, y_train = data["X_train"], data["y_train"]
    X_test_known, y_test_known = data["X_test_known"], data["y_test_known"]
    X_test_unknown = data["X_test_unknown"]

    M_train = len(X_train)
    D = X_train[0].size
    print(f"  [+] Enrolled Training Gallery : {M_train} images (35 subjects x 7 photos)")
    print(f"  [+] Known Test Probes         : {len(X_test_known)} images (35 subjects x 3 photos)")
    print(f"  [+] Unseen Unknown Probes     : {len(X_test_unknown)} images (5 subjects x 10 photos)")
    print(f"  [+] Image Resolution          : 64 x 64 pixels (Pixel dimension D = {D})")

    # Step 2: Model Training
    K = 40
    print(f"\n[STEP 2] Training Eigenfaces Model with K = {K} components...")
    model = Eigenfaces(n_components=K)
    model.fit(X_train, y_train)

    explained_var = np.sum(model.explained_variance_ratio) * 100
    print(f"  [+] Average Face (Psi) Shape  : {model.mean_face.shape}")
    print(f"  [+] Covariance Reduction      : (4096 x 4096 = 16.7M) -> (245 x 245 = 60,025)")
    print(f"  [+] Subspace Dimension (K)    : {K} eigenfaces")
    print(f"  [+] Explained Variance Ratio  : {explained_var:.2f}% of total dataset variance")
    print(f"  [+] Calibrated Theta_Face     : {model.theta_f:.3f} (DFFS Threshold)")
    print(f"  [+] Calibrated Theta_Class    : {model.theta_c:.3f} (DIFS Threshold)")

    # Step 3: Top-1 Recognition Accuracy on Known Faces
    print("\n[STEP 3] Evaluating Top-1 Identification Accuracy on Known Probes...")
    correct = 0
    total = len(X_test_known)
    recon_errors = []

    for i in range(total):
        probe = X_test_known[i]
        true_label = y_test_known[i]
        res = model.predict(probe)
        recon_errors.append(res["eps_d"])
        # For nearest neighbor identification
        _, _, pred_label = model.compute_distances(probe)
        if pred_label == true_label:
            correct += 1

    accuracy = (correct / total) * 100
    mean_recon_err = float(np.mean(recon_errors))
    print(f"  [+] Correctly Identified      : {correct} / {total}")
    print(f"  [+] Top-1 Recognition Accuracy: {accuracy:.2f}%")
    print(f"  [+] Mean Reconstruction Error : {mean_recon_err:.3f}")

    # Step 4: Testing 4-Way Decision Rules
    print("\n[STEP 4] Validating 4-Way Decision Rule (Turk & Pentland Section 3.2):")

    # 4A. Known face probe
    known_probe = X_test_known[0]
    res_known = model.predict(known_probe)
    print(f"\n  A. Known Subject Probe (Subject {y_test_known[0]}):")
    print(f"     * eps_d = {res_known['eps_d']:.3f} (Threshold theta_f = {model.theta_f:.3f})")
    print(f"     * eps_c = {res_known['eps_c']:.3f} (Threshold theta_c = {model.theta_c:.3f})")
    print(f"     * Decision -> [{res_known['decision']}]: {res_known['details']}")

    # 4B. Unknown face probe (Unseen subject)
    unknown_probe = X_test_unknown[1]
    res_unknown = model.predict(unknown_probe)
    print(f"\n  B. Unseen Subject Probe (Subject 36 - never in training set):")
    print(f"     * eps_d = {res_unknown['eps_d']:.3f} (Threshold theta_f = {model.theta_f:.3f})")
    print(f"     * eps_c = {res_unknown['eps_c']:.3f} (Threshold theta_c = {model.theta_c:.3f})")
    print(f"     * Decision -> [{res_unknown['decision']}]: {res_unknown['details']}")

    # 4C. Non-face pattern (Synthetic Checkerboard)
    checkerboard = np.indices((64, 64)).sum(axis=0) % 2
    checkerboard = checkerboard.astype(np.float64)
    res_nonface = model.predict(checkerboard)
    print(f"\n  C. Non-Face Pattern (Geometric Checkerboard):")
    print(f"     * eps_d = {res_nonface['eps_d']:.3f} (Threshold theta_f = {model.theta_f:.3f})")
    print(f"     * eps_c = {res_nonface['eps_c']:.3f} (Threshold theta_c = {model.theta_c:.3f})")
    print(f"     * Decision -> [{res_nonface['decision']}]: {res_nonface['details']}")

    # Step 5: Summary
    print("\n" + "=" * 76)
    print("  PROJECT EXECUTION COMPLETED SUCCESSFULLY!")
    print(f"  Summary: Top-1 Accuracy = {accuracy:.2f}%, Compression = 99.02%")
    print("  To showcase the project code and visual graphs interactively,")
    print("  open 'index.html' in any web browser.")
    print("=" * 76)


if __name__ == "__main__":
    run_project()
