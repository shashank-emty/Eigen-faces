import os
import numpy as np
from sklearn.datasets import fetch_olivetti_faces


def load_face_dataset():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    data = fetch_olivetti_faces(data_home=data_dir, shuffle=False)
    images = data.images
    targets = data.target

    rng = np.random.RandomState(42)
    X_train_list, y_train_list = [], []
    X_test_known_list, y_test_known_list = [], []
    X_test_unknown_list = []

    for subject_id in range(40):
        idx = np.where(targets == subject_id)[0]
        perm = rng.permutation(idx)

        if subject_id < 35:
            X_train_list.append(images[perm[:7]])
            y_train_list.append(targets[perm[:7]])
            X_test_known_list.append(images[perm[7:]])
            y_test_known_list.append(targets[perm[7:]])
        else:
            X_test_unknown_list.append(images[perm])

    return (
        np.vstack(X_train_list),
        np.concatenate(y_train_list),
        np.vstack(X_test_known_list),
        np.concatenate(y_test_known_list),
        np.vstack(X_test_unknown_list),
    )


class Eigenfaces:
    def __init__(self, n_components: int = 40):
        self.n_components = n_components
        self.mean_face = None
        self.eigenfaces = None
        self.eigenvalues = None
        self.explained_variance_ratio = None
        self.train_weights = None
        self.train_labels = None
        self.class_centroids = {}
        self.theta_f = None
        self.theta_c = None

    def fit(self, X_train: np.ndarray, y_train: np.ndarray):
        M, D = X_train.shape[0], X_train[0].size              # M = 245 photos, D = 4,096 pixels (64 x 64)
        Gamma = X_train.reshape(M, D).T                       # Gamma is M x D (245 x 4096)
        self.train_labels = np.asarray(y_train)

        # 1. Mean Face
        self.mean_face = np.mean(Gamma, axis=1)                   # mean_face is D x 1 (4096 x 1)

        # 2. Mean-Centered Data Matrix
        A = Gamma - self.mean_face[:, np.newaxis]              #for all 245 images

        # 3. Covariance Matrix Reduction (Turk & Pentland)
        L = np.dot(A.T, A)

        # 4. Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(L)      # h -> Symmetric (Hermitian)
        idx = np.argsort(eigenvalues)[::-1]                # Sorting from Most Important to Least Important
        eigenvalues = np.maximum(eigenvalues[idx], 0.0)
        eigenvectors = eigenvectors[:, idx]

        total_var = np.sum(eigenvalues)
        self.explained_variance_ratio = (eigenvalues[:self.n_components] / total_var) if total_var > 0 else np.zeros(self.n_components)

        K = min(self.n_components, M)
        self.eigenvalues = eigenvalues[:K]
        top_v = eigenvectors[:, :K]

        # 5. Recover Eigenfaces
        U = np.dot(A, top_v)
        norms = np.linalg.norm(U, axis=0, keepdims=True)
        norms[norms == 0] = 1.0
        self.eigenfaces = U / norms

        # 6. Project Training Images
        self.train_weights = np.dot(self.eigenfaces.T, A)

        # 7. Compute Class Centroids
        for c in np.unique(self.train_labels):
            class_idx = np.where(self.train_labels == c)[0]
            self.class_centroids[c] = np.mean(self.train_weights[:, class_idx], axis=1)

        # 8. Calibrate Thresholds
        A_recon = np.dot(self.eigenfaces, self.train_weights)
        recon_errors = np.linalg.norm(A - A_recon, axis=0)
        self.theta_f = float(np.max(recon_errors) + 8.0 * np.std(recon_errors))

        intra_dists = [
            np.linalg.norm(self.train_weights[:, i] - self.class_centroids[self.train_labels[i]])
            for i in range(M)
        ]
        self.theta_c = float(np.mean(intra_dists) + 1.2 * np.std(intra_dists))

        return self

    def project(self, image: np.ndarray) -> np.ndarray:
        gamma = image.flatten().astype(np.float64)
        return np.dot(self.eigenfaces.T, gamma - self.mean_face)

    def reconstruct(self, omega: np.ndarray) -> np.ndarray:
        return self.mean_face + np.dot(self.eigenfaces, omega)

    def compute_distances(self, image: np.ndarray):
        gamma = image.flatten().astype(np.float64)
        omega = self.project(gamma)
        gamma_hat = self.reconstruct(omega)

        eps_d = float(np.linalg.norm(gamma - gamma_hat))

        best_label, min_dist = None, float("inf")
        for label, centroid in self.class_centroids.items():
            dist = float(np.linalg.norm(omega - centroid))
            if dist < min_dist:
                min_dist, best_label = dist, label

        return eps_d, min_dist, best_label

    def predict(self, image: np.ndarray) -> dict:
        eps_d, eps_c, pred_label = self.compute_distances(image)

        if eps_d >= self.theta_f:
            decision = "NOT_A_FACE"
        elif eps_c < self.theta_c:
            decision = "KNOWN_FACE"
        else:
            decision = "UNKNOWN_FACE"

        return {
            "decision": decision,
            "predicted_label": pred_label if decision == "KNOWN_FACE" else None,
            "eps_d": eps_d,
            "eps_c": eps_c,
        }


def run_project():
    # Load Data
    X_train, y_train, X_test_known, y_test_known, X_test_unknown = load_face_dataset()

    # Train Model
    K = 40
    model = Eigenfaces(n_components=K)
    model.fit(X_train, y_train)

    explained_var = np.sum(model.explained_variance_ratio) * 100
    print(f"Components: {K}")
    print(f"Explained Variance: {explained_var:.2f}%")
    print(f"Theta_Face (eps_d threshold): {model.theta_f:.3f}")
    print(f"Theta_Class (eps_c threshold): {model.theta_c:.3f}")

    # Evaluate Accuracy
    correct = 0
    recon_errors = []
    for i in range(len(X_test_known)):
        probe, true_id = X_test_known[i], y_test_known[i]
        res = model.predict(probe)
        recon_errors.append(res["eps_d"])
        _, _, pred_label = model.compute_distances(probe)
        if pred_label == true_id:
            correct += 1

    accuracy = (correct / len(X_test_known)) * 100
    print(f"Accuracy: {accuracy:.2f}% ({correct}/{len(X_test_known)})")
    print(f"Mean Reconstruction Error: {float(np.mean(recon_errors)):.3f}")

    # Test Probes
    print("\n--- Test Probes ---")
    res_known = model.predict(X_test_known[0])
    print(f"Known Probe   -> Decision: {res_known['decision']}, eps_d: {res_known['eps_d']:.3f}, eps_c: {res_known['eps_c']:.3f}")

    res_unknown = model.predict(X_test_unknown[1])
    print(f"Unknown Probe -> Decision: {res_unknown['decision']}, eps_d: {res_unknown['eps_d']:.3f}, eps_c: {res_unknown['eps_c']:.3f}")

    checkerboard = (np.indices((64, 64)).sum(axis=0) % 2).astype(np.float64)
    res_nonface = model.predict(checkerboard)
    print(f"Non-Face Probe-> Decision: {res_nonface['decision']}, eps_d: {res_nonface['eps_d']:.3f}, eps_c: {res_nonface['eps_c']:.3f}")

    # Plot and Display Graphs
    plot_results(model, X_test_known, X_test_unknown, checkerboard)


def plot_results(model, X_test_known, X_test_unknown, checkerboard):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(11, 9))

    # 1. Explained Variance Bar Chart
    axes[0, 0].bar(range(1, len(model.explained_variance_ratio) + 1), model.explained_variance_ratio, color="steelblue", edgecolor="black")
    axes[0, 0].set_title("Explained Variance per Eigenface", fontweight="bold")
    axes[0, 0].set_xlabel("Component Index")
    axes[0, 0].set_ylabel("Variance Ratio")
    axes[0, 0].grid(axis="y", linestyle="--", alpha=0.5)

    # 2. Cumulative Variance Curve
    cum_var = np.cumsum(model.explained_variance_ratio)
    axes[0, 1].plot(range(1, len(cum_var) + 1), cum_var * 100, marker="o", color="forestgreen", lw=2)
    axes[0, 1].axhline(85, color="red", linestyle="--", label="85% Threshold")
    axes[0, 1].set_title("Cumulative Explained Variance (%)", fontweight="bold")
    axes[0, 1].set_xlabel("Number of Eigenfaces (K)")
    axes[0, 1].set_ylabel("Cumulative Variance (%)")
    axes[0, 1].legend()
    axes[0, 1].grid(True, linestyle="--", alpha=0.5)

    # 3. Original vs Reconstructed Face
    sample = X_test_known[0]
    recon = model.reconstruct(model.project(sample)).reshape(64, 64)
    combined = np.hstack([sample, np.ones((64, 4)), recon])
    axes[1, 0].imshow(combined, cmap="gray")
    axes[1, 0].set_title("Original Face (Left) vs Reconstructed (Right)", fontweight="bold")
    axes[1, 0].axis("off")

    # 4. 2D Decision Space Scatter
    known_dffs = [model.compute_distances(x)[0] for x in X_test_known[:35]]
    known_difs = [model.compute_distances(x)[1] for x in X_test_known[:35]]
    unknown_dffs = [model.compute_distances(x)[0] for x in X_test_unknown[:20]]
    unknown_difs = [model.compute_distances(x)[1] for x in X_test_unknown[:20]]
    nf_dffs, nf_difs, _ = model.compute_distances(checkerboard)

    axes[1, 1].scatter(known_dffs, known_difs, c="green", label="Known Faces", alpha=0.7)
    axes[1, 1].scatter(unknown_dffs, unknown_difs, c="dodgerblue", marker="^", label="Unknown Faces", alpha=0.7)
    axes[1, 1].scatter([nf_dffs], [nf_difs], c="red", marker="x", s=80, label="Non-Face (Checkerboard)")
    axes[1, 1].axvline(model.theta_f, color="red", linestyle="--", label=r"$\theta_f$ (Face Space)")
    axes[1, 1].axhline(model.theta_c, color="orange", linestyle="--", label=r"$\theta_c$ (Class Margin)")
    axes[1, 1].set_title("Decision Space (DFFS vs DIFS)", fontweight="bold")
    axes[1, 1].set_xlabel(r"Distance from Face Space ($\epsilon_d$)")
    axes[1, 1].set_ylabel(r"Distance in Face Space ($\epsilon_c$)")
    axes[1, 1].legend(fontsize=8)
    axes[1, 1].grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/output_summary.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    run_project()
