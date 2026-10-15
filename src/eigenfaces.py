"""
Core implementation of the 'Eigenfaces for Recognition' technical paper
by Matthew Turk and Alex Pentland (Journal of Cognitive Neuroscience, 1991).

Mathematical Framework:
1. Face vectors: Gamma_i in R^D (D = H * W)
2. Mean face: Psi = (1/M) * sum(Gamma_i)
3. Mean-centered differences: Phi_i = Gamma_i - Psi
4. Difference matrix: A = [Phi_1, Phi_2, ..., Phi_M] (shape: D x M)
5. Covariance surrogate matrix: L = A^T * A (shape: M x M)
6. Turk-Pentland Eigendecomposition Trick:
      L * v_k = mu_k * v_k  =>  (A * A^T) * (A * v_k) = mu_k * (A * v_k)
   Therefore, eigenvectors of C = (1/M) * A * A^T are:
      u_k = (A * v_k) / ||A * v_k||_2
7. Face space projection: Omega = U^T * (Gamma - Psi)
8. Reconstruction: Gamma_reconstructed = Psi + U * Omega
9. Two-threshold 4-way decision rule:
   - Distance from face space: epsilon_d = ||Gamma - Gamma_reconstructed||_2
   - Distance to known class:  epsilon_c = min_k ||Omega - Omega_k||_2
"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np


class EigenfacesClassifier:
    """
    Pure NumPy implementation of Turk & Pentland (1991) Eigenfaces for Recognition.
    """

    def __init__(
        self,
        n_components: Optional[int] = None,
        variance_ratio: Optional[float] = None,
        theta_face: Optional[float] = None,
        theta_class: Optional[float] = None,
    ):
        """
        Args:
            n_components: Number of eigenfaces K to retain.
            variance_ratio: Alternatively, retain enough components to explain
                           this fraction of total variance (e.g. 0.95).
            theta_face: Face space distance threshold (epsilon_d threshold).
                        If None, can be auto-calibrated from training data.
            theta_class: Classification distance threshold (epsilon_c threshold).
                         If None, can be auto-calibrated from training data.
        """
        self.n_components = n_components
        self.variance_ratio = variance_ratio
        self.theta_face = theta_face
        self.theta_class = theta_class

        # Model attributes learned during fit()
        self.img_shape: Optional[Tuple[int, int]] = None
        self.D: int = 0  # Pixel dimension (H * W)
        self.M: int = 0  # Number of training samples
        self.mean_face: Optional[np.ndarray] = None  # Psi (D,)
        self.eigenfaces: Optional[np.ndarray] = None  # U (D, K)
        self.eigenvalues: Optional[np.ndarray] = None  # Top K eigenvalues
        self.all_eigenvalues: Optional[np.ndarray] = None  # All eigenvalues of L
        self.explained_variance_ratio_: Optional[np.ndarray] = None
        self.projected_train_faces: Optional[np.ndarray] = None  # (K, M)
        self.train_labels: Optional[np.ndarray] = None  # (M,)
        self.class_centroids: Dict[Union[int, str], np.ndarray] = {}  # class -> (K,)

    def fit(
        self,
        images: np.ndarray,
        labels: np.ndarray,
        calibrate_thresholds: bool = True,
    ) -> "EigenfacesClassifier":
        """
        Train the Eigenfaces model using the Turk & Pentland algorithm.

        Args:
            images: Array of face images. Can be:
                    - (M, H, W) 2D images
                    - (M, D) flattened vectors
            labels: Array of subject labels of length M.
            calibrate_thresholds: If True, automatically estimates theta_face
                                 and theta_class from training distributions.

        Returns:
            self
        """
        images = np.asarray(images, dtype=np.float64)
        labels = np.asarray(labels)

        if images.ndim == 3:
            self.M, h, w = images.shape
            self.img_shape = (h, w)
            self.D = h * w
            # Flatten each image into a column vector: Gamma of shape (D, M)
            Gamma = images.reshape(self.M, self.D).T
        elif images.ndim == 2:
            self.M, self.D = images.shape
            # If square root is integer, assume square image shape
            side = int(np.round(np.sqrt(self.D)))
            if side * side == self.D:
                self.img_shape = (side, side)
            else:
                self.img_shape = (self.D, 1)
            Gamma = images.T  # (D, M)
        else:
            raise ValueError(f"Images must have 2 or 3 dimensions, got {images.ndim}")

        if len(labels) != self.M:
            raise ValueError(f"Length of labels ({len(labels)}) does not match samples ({self.M})")

        self.train_labels = labels

        # Step 1: Compute the Average / Mean Face (Psi)
        # Psi = (1 / M) * sum_{i=1}^M Gamma_i
        self.mean_face = np.mean(Gamma, axis=1)  # shape: (D,)

        # Step 2: Mean-center the face vectors
        # Phi_i = Gamma_i - Psi
        # Matrix A has columns Phi_i: shape (D, M)
        A = Gamma - self.mean_face[:, np.newaxis]

        # Step 3: Turk-Pentland Dimensionality Reduction Trick
        # Direct covariance C = (1/M) * A * A^T is (D x D), which is huge.
        # Instead, construct surrogate matrix L = A^T * A of shape (M, M).
        L = np.dot(A.T, A)  # shape: (M, M)

        # Step 4: Eigenvalue decomposition of L
        # Since L is symmetric and positive semi-definite, use eigh for numerical stability.
        eigenvals, eigenvecs = np.linalg.eigh(L)

        # Sort eigenvalues and eigenvectors in descending order
        idx = np.argsort(eigenvals)[::-1]
        eigenvals = eigenvals[idx]
        eigenvecs = eigenvecs[:, idx]  # shape: (M, M)

        # Ensure eigenvalues are non-negative (clean up float precision artifacts)
        eigenvals = np.maximum(eigenvals, 0.0)
        self.all_eigenvalues = eigenvals.copy()

        # Step 5: Convert eigenvectors of L into eigenvectors of C (Eigenfaces)
        # u_k = A * v_k
        U = np.dot(A, eigenvecs)  # shape: (D, M)

        # Normalize each eigenface to have unit L2 norm: ||u_k||_2 = 1
        norms = np.linalg.norm(U, axis=0, keepdims=True)
        # Avoid division by zero for any degenerate vectors
        norms[norms == 0] = 1e-12
        U = U / norms

        # Determine number of components K to keep
        total_var = np.sum(eigenvals)
        if total_var > 0:
            var_ratios = eigenvals / total_var
        else:
            var_ratios = np.zeros_like(eigenvals)

        if self.variance_ratio is not None:
            cumsum = np.cumsum(var_ratios)
            k = int(np.searchsorted(cumsum, self.variance_ratio) + 1)
            k = max(1, min(k, self.M))
            self.n_components = k
        elif self.n_components is not None:
            self.n_components = max(1, min(self.n_components, self.M))
        else:
            # Default to min(M - 1, D, 50) as recommended in practical implementations
            self.n_components = min(self.M, 50)

        # Keep top K eigenfaces
        self.eigenfaces = U[:, : self.n_components]  # shape: (D, K)
        self.eigenvalues = eigenvals[: self.n_components]
        self.explained_variance_ratio_ = var_ratios[: self.n_components]

        # Step 6: Project training faces into Face Space
        # Omega_i = U^T * (Gamma_i - Psi)
        # Shape: (K, M)
        self.projected_train_faces = np.dot(self.eigenfaces.T, A)

        # Step 7: Compute Class Centroids in Face Space
        self.class_centroids = {}
        unique_classes = np.unique(self.train_labels)
        for c in unique_classes:
            mask = self.train_labels == c
            centroid = np.mean(self.projected_train_faces[:, mask], axis=1)  # shape: (K,)
            self.class_centroids[c] = centroid

        # Step 8: Calibrate decision thresholds (theta_face, theta_class) if requested
        if calibrate_thresholds:
            self._calibrate_thresholds(Gamma)

        return self

    def _calibrate_thresholds(self, Gamma: np.ndarray) -> None:
        """
        Calibrate theta_face and theta_class based on training set statistics
        as outlined in Section 3.2 & 4 of Turk & Pentland (1991).
        """
        # 1. Distance from face space for training set
        train_dffs = []
        for i in range(self.M):
            x = Gamma[:, i]
            _, eps_d = self.reconstruct(x)
            train_dffs.append(eps_d)
        train_dffs = np.array(train_dffs)

        # theta_face: maximum reconstruction distance across training faces, with margin
        # Turk & Pentland note: theta_face can be chosen based on the distribution of face images
        max_dffs = np.max(train_dffs)
        std_dffs = np.std(train_dffs)
        self.theta_face = float(max_dffs + 8.0 * std_dffs)

        # 2. Distance in face space between samples of the same class (intra-class distance)
        intra_dists = []
        for i in range(self.M):
            label = self.train_labels[i]
            omega = self.projected_train_faces[:, i]
            dist_to_centroid = np.linalg.norm(omega - self.class_centroids[label])
            intra_dists.append(dist_to_centroid)
        intra_dists = np.array(intra_dists)

        # theta_class: threshold distinguishing known classes from unseen faces
        # Turk & Pentland recommend setting theta_c as the classification margin
        self.theta_class = float(np.mean(intra_dists) + 1.2 * np.std(intra_dists))

    def project(self, image: np.ndarray) -> np.ndarray:
        """
        Project an input image into Face Space.

        Formula:
            Phi = Gamma - Psi
            Omega = U^T * Phi

        Args:
            image: Image vector (D,) or (H, W).

        Returns:
            Omega: Face weight vector of shape (K,).
        """
        gamma = self._flatten(image)
        phi = gamma - self.mean_face
        omega = np.dot(self.eigenfaces.T, phi)  # (K,)
        return omega

    def reconstruct(
        self,
        image_or_omega: np.ndarray,
        n_components: Optional[int] = None,
    ) -> Tuple[np.ndarray, float]:
        """
        Reconstruct a face from its projection in Face Space.

        Formula:
            Phi_f = sum_{k=1}^K omega_k * u_k = U_k * Omega_k
            Gamma_f = Psi + Phi_f
            epsilon_d = ||Gamma - Gamma_f||_2

        Args:
            image_or_omega: Either raw image (D,) or weight vector Omega (K,).
            n_components: Optional subset of eigenfaces to use for reconstruction.

        Returns:
            reconstructed_image: Reconstructed image vector (D,).
            dffs: Distance from face space (epsilon_d). If given Omega, dffs is 0.0.
        """
        if self.eigenfaces is None or self.mean_face is None:
            raise RuntimeError("Model has not been fitted yet.")

        k = self.n_components if n_components is None else min(n_components, self.n_components)
        U_sub = self.eigenfaces[:, :k]  # (D, k)

        arr = np.asarray(image_or_omega, dtype=np.float64)

        if arr.size == self.D:
            # Input is raw image Gamma
            gamma = arr.ravel()
            phi = gamma - self.mean_face
            omega_sub = np.dot(U_sub.T, phi)  # (k,)
            phi_f = np.dot(U_sub, omega_sub)  # (D,)
            gamma_f = self.mean_face + phi_f
            dffs = float(np.linalg.norm(gamma - gamma_f))
            return gamma_f, dffs
        elif arr.size == self.n_components or arr.size == k:
            # Input is already omega weight vector
            omega_sub = arr.ravel()[:k]
            phi_f = np.dot(U_sub, omega_sub)
            gamma_f = self.mean_face + phi_f
            return gamma_f, 0.0
        else:
            raise ValueError(f"Input size ({arr.size}) does not match D ({self.D}) or K ({self.n_components})")

    def recognize(
        self,
        image: np.ndarray,
        use_centroids: bool = True,
    ) -> Dict[str, Union[str, float, int, bool, np.ndarray]]:
        """
        Full 4-Way Decision Rule from Turk & Pentland (1991), Section 3.2.

        Decision Cases:
        1. epsilon_d >= theta_face:
           => "NOT_A_FACE" (Input image does not lie close to Face Space).
        2. epsilon_d < theta_face and epsilon_c < theta_class:
           => "KNOWN_FACE" (Input image is a face and recognized as known subject).
        3. epsilon_d < theta_face and epsilon_c >= theta_class:
           => "UNKNOWN_FACE" (Input image is indeed a face, but not in known gallery).

        Args:
            image: Query image of shape (H, W) or (D,).
            use_centroids: If True, matches against class centroids Omega_c.
                          If False, uses 1-Nearest Neighbor across all training exemplars.

        Returns:
            Dictionary containing:
                - decision: "KNOWN_FACE", "UNKNOWN_FACE", or "NOT_A_FACE"
                - is_face: bool
                - is_known: bool
                - predicted_label: recognized subject (or None)
                - dffs (epsilon_d): Distance from Face Space
                - difs (epsilon_c): Distance to nearest class in Face Space
                - theta_face: Threshold for face space
                - theta_class: Threshold for classification
                - reconstructed: Reconstructed face vector (D,)
                - omega: Projection vector in Face Space (K,)
        """
        gamma = self._flatten(image)

        # 1. Project and Reconstruct
        omega = self.project(gamma)
        gamma_reconstructed, epsilon_d = self.reconstruct(gamma)

        # 2. Compute Distance to Known Classes in Face Space (epsilon_c)
        if use_centroids:
            best_class = None
            min_dist = float("inf")
            class_distances = {}
            for c, centroid in self.class_centroids.items():
                d = float(np.linalg.norm(omega - centroid))
                class_distances[c] = d
                if d < min_dist:
                    min_dist = d
                    best_class = c
            epsilon_c = min_dist
            predicted_label = best_class
        else:
            # 1-Nearest Neighbor against all training exemplars
            diffs = self.projected_train_faces - omega[:, np.newaxis]
            dists = np.linalg.norm(diffs, axis=0)
            min_idx = int(np.argmin(dists))
            epsilon_c = float(dists[min_idx])
            predicted_label = self.train_labels[min_idx]

        # 3. Apply Turk & Pentland 4-Way Decision Rule
        th_face = self.theta_face if self.theta_face is not None else float("inf")
        th_class = self.theta_class if self.theta_class is not None else float("inf")

        if epsilon_d >= th_face:
            decision = "NOT_A_FACE"
            is_face = False
            is_known = False
        elif epsilon_c < th_class:
            decision = "KNOWN_FACE"
            is_face = True
            is_known = True
        else:
            decision = "UNKNOWN_FACE"
            is_face = True
            is_known = False

        return {
            "decision": decision,
            "is_face": is_face,
            "is_known": is_known,
            "predicted_label": predicted_label if is_known else None,
            "dffs": epsilon_d,
            "difs": epsilon_c,
            "theta_face": th_face,
            "theta_class": th_class,
            "reconstructed": gamma_reconstructed,
            "omega": omega,
        }

    def predict(self, images: np.ndarray, use_centroids: bool = True) -> np.ndarray:
        """
        Predict subject labels for multiple query images (without threshold rejection).

        Args:
            images: Array of images of shape (N, H, W) or (N, D).
            use_centroids: If True, uses nearest class centroid; else 1-NN.

        Returns:
            predictions: Array of predicted labels of length N.
        """
        images = np.asarray(images, dtype=np.float64)
        if images.ndim == 3:
            N = images.shape[0]
            flat_images = images.reshape(N, self.D)
        elif images.ndim == 2:
            N = images.shape[0]
            flat_images = images
        else:
            flat_images = images[np.newaxis, :]
            N = 1

        preds = []
        for i in range(N):
            res = self.recognize(flat_images[i], use_centroids=use_centroids)
            # For standard benchmark accuracy evaluation, report closest class
            if use_centroids:
                omega = res["omega"]
                best_c = min(self.class_centroids.keys(), key=lambda c: np.linalg.norm(omega - self.class_centroids[c]))
                preds.append(best_c)
            else:
                preds.append(res["predicted_label"])
        return np.array(preds)

    def score(self, images: np.ndarray, labels: np.ndarray, use_centroids: bool = True) -> float:
        """
        Compute top-1 classification accuracy.
        """
        preds = self.predict(images, use_centroids=use_centroids)
        labels = np.asarray(labels)
        return float(np.mean(preds == labels))

    def get_eigenface_image(self, index: int) -> np.ndarray:
        """
        Retrieve the k-th eigenface reshaped as a 2D image.
        """
        if self.eigenfaces is None or self.img_shape is None:
            raise RuntimeError("Model has not been fitted yet.")
        if index < 0 or index >= self.n_components:
            raise IndexError(f"Index {index} out of range (0 to {self.n_components - 1})")
        return self.eigenfaces[:, index].reshape(self.img_shape)

    def get_mean_face_image(self) -> np.ndarray:
        """
        Retrieve the mean face reshaped as a 2D image.
        """
        if self.mean_face is None or self.img_shape is None:
            raise RuntimeError("Model has not been fitted yet.")
        return self.mean_face.reshape(self.img_shape)

    def _flatten(self, image: np.ndarray) -> np.ndarray:
        arr = np.asarray(image, dtype=np.float64).ravel()
        if arr.size != self.D:
            raise ValueError(f"Input image flattened size {arr.size} does not match model dimension {self.D}")
        return arr
