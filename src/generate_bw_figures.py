"""
Generate high-contrast, black-and-white / monochrome compatible figures
optimized for printing and formal academic report submission.
"""

import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dataset import generate_non_face_samples, load_face_data
from src.eigenfaces import EigenfacesClassifier
from src.evaluate import evaluate_accuracy_vs_k


def setup_bw_style():
    """Apply print-optimized monochrome styling."""
    plt.rcParams.update(
        {
            "figure.autolayout": True,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "black",
            "axes.linewidth": 1.0,
            "axes.titlesize": 11,
            "axes.titleweight": "bold",
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "xtick.color": "black",
            "ytick.color": "black",
            "grid.color": "#cccccc",
            "grid.linestyle": ":",
            "grid.linewidth": 0.8,
            "font.family": "serif",
        }
    )


def generate_all_bw_figures():
    setup_bw_style()
    bw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "bw")
    os.makedirs(bw_dir, exist_ok=True)

    print("[BW GEN] Loading dataset and fitting model...")
    data = load_face_data(train_per_subject=7, num_known_subjects=35, random_state=42)
    X_train = data["X_train"]
    y_train = data["y_train"]
    X_test_known = data["X_test_known"]
    y_test_known = data["y_test_known"]
    X_test_unknown = data["X_test_unknown"]
    non_faces, _ = generate_non_face_samples(10)

    model = EigenfacesClassifier(n_components=40)
    model.fit(X_train, y_train, calibrate_thresholds=True)

    # -------------------------------------------------------------
    # Figure 1: Mean Face and Top Eigenfaces
    # -------------------------------------------------------------
    print("[BW GEN] Generating Fig 1: Eigenfaces Gallery...")
    n_ef = 15
    ncols = 4
    nrows = int(np.ceil((1 + n_ef) / ncols))
    fig1, axes1 = plt.subplots(nrows, ncols, figsize=(10, 2.6 * nrows))
    axes1 = axes1.ravel()

    # Mean face
    axes1[0].imshow(model.get_mean_face_image(), cmap="gray")
    axes1[0].set_title(r"Average Face ($\Psi$)", fontsize=10, fontweight="bold")
    axes1[0].axis("off")

    for i in range(n_ef):
        ax = axes1[i + 1]
        img = model.get_eigenface_image(i)
        var_pct = model.explained_variance_ratio_[i] * 100
        ax.imshow(img, cmap="gray")
        ax.set_title(f"$u_{{{i+1}}}$ ({var_pct:.1f}% var)", fontsize=9)
        ax.axis("off")

    for j in range(1 + n_ef, len(axes1)):
        axes1[j].axis("off")

    plt.suptitle("Figure 1: Mean Face and Principal Eigenfaces (Turk & Pentland, 1991)", fontsize=12, fontweight="bold", y=1.01)
    fig1.savefig(os.path.join(bw_dir, "fig1_eigenfaces_gallery.png"), dpi=300, bbox_inches="tight")
    plt.close(fig1)

    # -------------------------------------------------------------
    # Figure 2: Scree Plot & Cumulative Variance
    # -------------------------------------------------------------
    print("[BW GEN] Generating Fig 2: Scree Plot...")
    evals = model.all_eigenvalues
    cum_var = np.cumsum(evals / np.sum(evals)) * 100
    k_range = min(len(evals), 80)

    fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    # Left: Scree
    ax1.plot(range(1, k_range + 1), evals[:k_range], "k.-", lw=1.2, markersize=4)
    ax1.set_title("Eigenvalue Magnitude (Scree Plot)")
    ax1.set_xlabel("Principal Component Index ($k$)")
    ax1.set_ylabel(r"Eigenvalue ($\mu_k$)")
    ax1.grid(True)

    # Right: Cumulative variance
    ax2.plot(range(1, k_range + 1), cum_var[:k_range], "k-", lw=1.8, label="Cumulative Variance")
    k_90 = int(np.searchsorted(cum_var, 90) + 1)
    k_95 = int(np.searchsorted(cum_var, 95) + 1)
    ax2.axhline(90, color="#555555", linestyle="--", lw=1.2, label=f"90% Threshold (K={k_90})")
    ax2.axhline(95, color="#888888", linestyle=":", lw=1.2, label=f"95% Threshold (K={k_95})")
    ax2.axvline(k_90, color="#555555", linestyle="--", lw=1.0)
    ax2.axvline(k_95, color="#888888", linestyle=":", lw=1.0)
    ax2.set_title("Cumulative Variance Explained")
    ax2.set_xlabel("Number of Eigenfaces ($K$)")
    ax2.set_ylabel("Variance Captured (%)")
    ax2.set_ylim([0, 105])
    ax2.grid(True)
    ax2.legend(loc="lower right", framealpha=0.9, edgecolor="black")

    plt.suptitle("Figure 2: Eigenvalue Spectrum and Dimensionality Reduction Tradeoff", fontsize=12, fontweight="bold")
    fig2.savefig(os.path.join(bw_dir, "fig2_scree_plot.png"), dpi=300, bbox_inches="tight")
    plt.close(fig2)

    # -------------------------------------------------------------
    # Figure 3: Face Reconstruction Across K
    # -------------------------------------------------------------
    print("[BW GEN] Generating Fig 3: Reconstructions...")
    sample_img = X_test_known[0]
    k_steps = [2, 5, 10, 20, 40]
    fig3, axes3 = plt.subplots(1, len(k_steps) + 1, figsize=(11, 2.6))

    axes3[0].imshow(sample_img, cmap="gray")
    axes3[0].set_title(r"Original $\Gamma$", fontsize=10, fontweight="bold")
    axes3[0].axis("off")

    for idx, k in enumerate(k_steps):
        recon, err = model.reconstruct(sample_img, n_components=k)
        ax = axes3[idx + 1]
        ax.imshow(recon.reshape(model.img_shape), cmap="gray")
        ax.set_title(f"$K={k}$\n" + r"$\epsilon_d=" + f"{err:.2f}$", fontsize=9)
        ax.axis("off")

    plt.suptitle("Figure 3: Progressive Face Reconstruction with Increasing Eigenfaces ($K$)", fontsize=12, fontweight="bold")
    fig3.savefig(os.path.join(bw_dir, "fig3_face_reconstruction.png"), dpi=300, bbox_inches="tight")
    plt.close(fig3)

    # -------------------------------------------------------------
    # Figure 4: 2D Decision Space Geometry (High-Contrast B&W)
    # -------------------------------------------------------------
    print("[BW GEN] Generating Fig 4: Decision Space...")
    known_dffs = [model.recognize(x)["dffs"] for x in X_test_known[:35]]
    known_difs = [model.recognize(x)["difs"] for x in X_test_known[:35]]

    unknown_dffs = [model.recognize(x)["dffs"] for x in X_test_unknown[:35]]
    unknown_difs = [model.recognize(x)["difs"] for x in X_test_unknown[:35]]

    nf_dffs = [model.recognize(x)["dffs"] for x in non_faces]
    nf_difs = [model.recognize(x)["difs"] for x in non_faces]

    fig4, ax4 = plt.subplots(figsize=(8, 5.5))
    ax4.scatter(known_dffs, known_difs, marker="o", facecolors="black", edgecolors="black", s=35, label="Known Probe Faces")
    ax4.scatter(unknown_dffs, unknown_difs, marker="^", facecolors="none", edgecolors="black", s=45, lw=1.2, label="Unknown Probe Faces")
    ax4.scatter(nf_dffs, nf_difs, marker="x", c="black", s=55, lw=1.5, label="Non-Face Images")

    th_f = model.theta_face
    th_c = model.theta_class

    ax4.axvline(th_f, color="black", linestyle="--", lw=1.5, label=r"Face Threshold ($\theta_f$)")
    ax4.axhline(th_c, color="black", linestyle=":", lw=1.5, label=r"Class Threshold ($\theta_c$)")

    xlim = ax4.get_xlim()
    ylim = ax4.get_ylim()
    max_x = max(xlim[1], max(nf_dffs) * 1.05)
    max_y = max(ylim[1], max(nf_difs) * 1.05)
    ax4.set_xlim([0, max_x])
    ax4.set_ylim([0, max_y])

    # Text annotations
    ax4.text(
        th_f * 0.45,
        th_c * 0.45,
        "ZONE 1: KNOWN FACE\n" + r"($\epsilon_d < \theta_f, \epsilon_c < \theta_c$)",
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="#f0f0f0", ec="black"),
        fontsize=8,
        fontweight="bold",
    )
    ax4.text(
        th_f * 0.45,
        th_c + (max_y - th_c) * 0.45,
        "ZONE 2: UNKNOWN FACE\n" + r"($\epsilon_d < \theta_f, \epsilon_c \geq \theta_c$)",
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="#e0e0e0", ec="black"),
        fontsize=8,
        fontweight="bold",
    )
    ax4.text(
        th_f + (max_x - th_f) * 0.5,
        max_y * 0.5,
        "ZONE 3: NOT A FACE\n" + r"($\epsilon_d \geq \theta_f$)",
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec="black", lw=1.5),
        fontsize=8,
        fontweight="bold",
    )

    ax4.set_xlabel(r"Distance from Face Space $\epsilon_d$ (DFFS) $\rightarrow$ Non-Face Rejection", fontsize=10)
    ax4.set_ylabel(r"Distance in Face Space $\epsilon_c$ (DIFS) $\rightarrow$ Unknown Identity", fontsize=10)
    ax4.set_title("Figure 4: Turk & Pentland 4-Way Decision Space Geometry", fontsize=11, fontweight="bold")
    ax4.grid(True)
    ax4.legend(loc="upper right", framealpha=0.9, edgecolor="black")

    fig4.savefig(os.path.join(bw_dir, "fig4_decision_space_geometry.png"), dpi=300, bbox_inches="tight")
    plt.close(fig4)

    # -------------------------------------------------------------
    # Figure 5: Robustness Analysis (Noise & Occlusions)
    # -------------------------------------------------------------
    print("[BW GEN] Generating Fig 5: Robustness...")
    h, w = model.img_shape
    img_mild = np.clip(sample_img + np.random.normal(0, 0.1, sample_img.shape), 0, 1)
    img_severe = np.clip(sample_img + np.random.normal(0, 0.25, sample_img.shape), 0, 1)
    img_eye = sample_img.copy()
    img_eye[int(h * 0.35) : int(h * 0.50), int(w * 0.15) : int(w * 0.85)] = 0.0
    img_mouth = sample_img.copy()
    img_mouth[int(h * 0.65) : int(h * 0.88), int(w * 0.2) : int(w * 0.8)] = 0.0

    cases = [
        ("Clean Input", sample_img),
        (r"Mild Noise ($\sigma=0.1$)", img_mild),
        (r"Severe Noise ($\sigma=0.25$)", img_severe),
        ("Eye Occlusion", img_eye),
        ("Mouth Occlusion", img_mouth),
    ]

    fig5, axes5 = plt.subplots(2, len(cases), figsize=(10, 4.2))
    for idx, (label, im) in enumerate(cases):
        res = model.recognize(im)
        recon_face = res["reconstructed"].reshape(model.img_shape)

        axes5[0, idx].imshow(im, cmap="gray")
        axes5[0, idx].set_title(f"{label}\n" + r"$\epsilon_d=" + f"{res['dffs']:.2f}$", fontsize=8)
        axes5[0, idx].axis("off")

        axes5[1, idx].imshow(recon_face, cmap="gray")
        axes5[1, idx].set_title(f"Reconstructed\n[{res['decision']}]", fontsize=8)
        axes5[1, idx].axis("off")

    plt.suptitle("Figure 5: Robustness Under Noise and Partial Occlusions", fontsize=12, fontweight="bold")
    fig5.savefig(os.path.join(bw_dir, "fig5_robustness_analysis.png"), dpi=300, bbox_inches="tight")
    plt.close(fig5)

    # -------------------------------------------------------------
    # Figure 6: Accuracy & Reconstruction Error vs K (Dual Axis B&W)
    # -------------------------------------------------------------
    print("[BW GEN] Generating Fig 6: Accuracy vs K...")
    k_vals = [2, 5, 10, 15, 20, 30, 40, 50, 75, 100]
    bench = evaluate_accuracy_vs_k(X_train, y_train, X_test_known, y_test_known, k_vals)

    fig6, ax_acc = plt.subplots(figsize=(8, 4.5))

    ax_acc.set_xlabel("Number of Principal Components ($K$)", fontsize=10)
    ax_acc.set_ylabel("Recognition Accuracy (%)", color="black", fontsize=10)
    line1 = ax_acc.plot(k_vals, [a * 100 for a in bench["accuracies"]], "ko-", lw=1.8, markersize=5, label="Test Accuracy (%)")
    ax_acc.tick_params(axis="y", labelcolor="black")
    ax_acc.grid(True)

    ax_err = ax_acc.twinx()
    ax_err.set_ylabel(r"Mean Reconstruction Error ($\epsilon_d$)", color="black", fontsize=10)
    line2 = ax_err.plot(k_vals, bench["reconstruction_errors"], "k^--", lw=1.5, markersize=5, label=r"Reconstruction Error ($\epsilon_d$)")
    ax_err.tick_params(axis="y", labelcolor="black")

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax_acc.legend(lines, labels, loc="center right", framealpha=0.9, edgecolor="black")

    plt.title("Figure 6: Classification Accuracy and Reconstruction Error Tradeoff vs. K", fontsize=11, fontweight="bold", pad=12)
    fig6.savefig(os.path.join(bw_dir, "fig6_accuracy_vs_k.png"), dpi=300, bbox_inches="tight")
    plt.close(fig6)

    print(f"[BW GEN] All 6 monochrome figures successfully generated in: {bw_dir}")


if __name__ == "__main__":
    generate_all_bw_figures()
