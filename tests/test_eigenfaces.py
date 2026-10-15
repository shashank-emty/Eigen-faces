"""
Unit tests verifying the mathematical correctness of Eigenfaces implementation.
"""

import unittest
import numpy as np
from src.eigenfaces import EigenfacesClassifier


class TestEigenfacesMathematics(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)
        # Create a small synthetic dataset: M=8 samples, D=36 (6x6 pixels), 4 subjects
        self.M = 8
        self.D = 36
        self.H, self.W = 6, 6
        self.X = np.random.randn(self.M, self.H, self.W)
        self.y = np.array([0, 0, 1, 1, 2, 2, 3, 3])

    def test_orthonormality_of_eigenfaces(self):
        """Eigenfaces must form an orthonormal basis: U^T * U == Identity"""
        model = EigenfacesClassifier(n_components=6)
        model.fit(self.X, self.y)
        U = model.eigenfaces
        gram = np.dot(U.T, U)
        identity = np.eye(model.n_components)
        np.testing.assert_allclose(gram, identity, atol=1e-7, err_msg="Eigenfaces are not orthonormal!")

    def test_turk_pentland_trick_equivalence(self):
        """
        Verify Turk-Pentland surrogate L = A^T * A yields the exact same eigenvectors
        as direct covariance C = A * A^T.
        """
        # Mean center
        Gamma = self.X.reshape(self.M, self.D).T  # (D, M)
        Psi = np.mean(Gamma, axis=1, keepdims=True)
        A = Gamma - Psi

        # Direct Covariance: C = A * A^T (D x D)
        C = np.dot(A, A.T)
        evals_C, evecs_C = np.linalg.eigh(C)
        idx_C = np.argsort(evals_C)[::-1]
        evals_C = evals_C[idx_C]
        evecs_C = evecs_C[:, idx_C]

        # Turk-Pentland Trick: L = A^T * A (M x M)
        L = np.dot(A.T, A)
        evals_L, evecs_L = np.linalg.eigh(L)
        idx_L = np.argsort(evals_L)[::-1]
        evals_L = evals_L[idx_L]
        evecs_L = evecs_L[:, idx_L]

        # Map L eigenvectors to C eigenvectors: u_k = A * v_k / ||A * v_k||
        U_derived = np.dot(A, evecs_L)
        norms = np.linalg.norm(U_derived, axis=0, keepdims=True)
        norms[norms == 0] = 1e-12
        U_derived = U_derived / norms

        # Non-zero eigenvalues must match
        rank = min(self.M - 1, self.D)
        np.testing.assert_allclose(
            evals_C[:rank],
            evals_L[:rank],
            rtol=1e-5,
            err_msg="Eigenvalues between A*A^T and A^T*A do not match!",
        )

        # Eigenvectors must match up to sign flip: |u_direct^T * u_derived| == 1
        for k in range(rank):
            overlap = np.abs(np.dot(evecs_C[:, k], U_derived[:, k]))
            self.assertAlmostEqual(
                overlap,
                1.0,
                places=5,
                msg=f"Eigenvector {k} does not align with direct covariance eigenvector!",
            )

    def test_reconstruction_monotonicity(self):
        """As K increases, reconstruction error must monotonically decrease."""
        model = EigenfacesClassifier(n_components=self.M - 1)
        model.fit(self.X, self.y)

        sample = self.X[0]
        prev_error = float("inf")
        errors = []
        for k in range(1, model.n_components + 1):
            _, dffs = model.reconstruct(sample, n_components=k)
            errors.append(dffs)
            self.assertLessEqual(dffs, prev_error + 1e-7, f"Error did not decrease at K={k}")
            prev_error = dffs

    def test_four_way_decision_rule(self):
        """Verify face rejection for noise/non-face and detection for face."""
        model = EigenfacesClassifier(n_components=4)
        model.fit(self.X, self.y)

        # Training sample should be recognized as KNOWN_FACE
        res_known = model.recognize(self.X[0], use_centroids=True)
        self.assertEqual(res_known["decision"], "KNOWN_FACE")
        self.assertEqual(res_known["predicted_label"], self.y[0])

        # A completely random high-variance noise image should be rejected as NOT_A_FACE
        np.random.seed(999)
        noise_image = np.random.uniform(20.0, 50.0, size=(self.H, self.W))
        res_noise = model.recognize(noise_image)
        self.assertGreater(res_noise["dffs"], model.theta_face)
        self.assertEqual(res_noise["decision"], "NOT_A_FACE")


if __name__ == "__main__":
    unittest.main()
