"""
Visualization tools for Eigenfaces presentation and analysis.
Generates publication-quality figures for slides, reports, and interactive demos.
"""

import os
from typing import List, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
from src.eigenfaces import EigenfacesClassifier


def set_plot_style():
    """Apply clean, elegant styling for scientific presentations."""
    plt.rcParams.update(
        {
            "figure.autolayout": True,
            "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
            "axes.edgecolor": "#333333",
            "axes.linewidth": 0.8,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
        }
    )


def plot_mean_and_eigenfaces(
    model: EigenfacesClassifier,
    n_eigenfaces: int = 15,
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Plots the Mean Face alongside the top K Eigenfaces.
    """
    set_plot_style()
    n_total = 1 + n_eigenfaces  # Mean face + K eigenfaces
    ncols = 4
    nrows = int(np.ceil(n_total / ncols))

    fig, axes = plt.subplots(nrows, ncols, figsize=(12, 3.2 * nrows))
    axes = axes.ravel()

    # 1. Mean Face
    mean_img = model.get_mean_face_image()
    axes[0].imshow(mean_img, cmap="gray")
    axes[0].set_title(r"Average Face ($\Psi$)", color="#1a237e")
    axes[0].axis("off")

    # 2. Top K Eigenfaces
    for i in range(n_eigenfaces):
        ax_idx = i + 1
        if i < model.n_components:
            ef_img = model.get_eigenface_image(i)
            var_pct = (
                model.explained_variance_ratio_[i] * 100
                if model.explained_variance_ratio_ is not None
                else 0.0
            )
            # Use 'bone' or 'gray' colormap to bring out eigenface features
            axes[ax_idx].imshow(ef_img, cmap="bone")
            axes[ax_idx].set_title(f"$u_{{{i+1}}}$ ({var_pct:.1f}% var)", fontsize=10)
        axes[ax_idx].axis("off")

    # Hide any unused subplots
    for j in range(n_total, len(axes)):
        axes[j].axis("off")

    plt.suptitle("Turk & Pentland (1991): Mean Face & Principal Eigenfaces", fontsize=14, y=1.01)
    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
    return fig


def plot_eigenvalue_spectrum(
    model: EigenfacesClassifier,
    max_k: int = 80,
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Plots Scree Plot (Eigenvalue spectrum) and Cumulative Explained Variance curve.
    """
    set_plot_style()
    if model.all_eigenvalues is None:
        raise RuntimeError("Model does not have eigenvalue data.")

    evals = model.all_eigenvalues
    total_var = np.sum(evals)
    var_ratio = evals / total_var
    cum_var = np.cumsum(var_ratio)
    k_range = min(len(evals), max_k)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))

    # Left: Eigenvalue magnitude (log-scale / scree)
    ax1.plot(range(1, k_range + 1), evals[:k_range], "o-", color="#0288d1", markersize=3, lw=1.5)
    ax1.set_title("Scree Plot: Eigenvalues of Covariance $L = A^T A$")
    ax1.set_xlabel("Principal Component Index ($k$)")
    ax1.set_ylabel(r"Eigenvalue ($\mu_k$)")
    ax1.grid(True, linestyle="--", alpha=0.5)

    # Right: Cumulative variance
    ax2.plot(range(1, k_range + 1), cum_var[:k_range] * 100, "-", color="#388e3c", lw=2)
    ax2.axhline(90, color="#d32f2f", linestyle="--", label="90% Variance Threshold")
    ax2.axhline(95, color="#f57c00", linestyle=":", label="95% Variance Threshold")

    # Find k for 90% and 95%
    k_90 = np.searchsorted(cum_var, 0.90) + 1
    k_95 = np.searchsorted(cum_var, 0.95) + 1
    ax2.axvline(k_90, color="#d32f2f", linestyle="--", alpha=0.6)
    ax2.axvline(k_95, color="#f57c00", linestyle=":", alpha=0.6)

    ax2.set_title(f"Cumulative Variance Explained (90% at K={k_90}, 95% at K={k_95})")
    ax2.set_xlabel("Number of Eigenfaces ($K$)")
    ax2.set_ylabel("Cumulative Variance (%)")
    ax2.set_ylim([0, 105])
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="lower right")

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
    return fig


def plot_reconstructions(
    model: EigenfacesClassifier,
    sample_image: np.ndarray,
    k_values: List[int] = [2, 5, 10, 25, 50, 100],
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Demonstrates image reconstruction fidelity as K increases:
    shows Original, then reconstructions for increasing K values, with DFFS error.
    """
    set_plot_style()
    n_cols = len(k_values) + 1
    fig, axes = plt.subplots(1, n_cols, figsize=(2.4 * n_cols, 3.2))

    # Original
    axes[0].imshow(sample_image, cmap="gray")
    axes[0].set_title(r"Original Face" + "\n" + r"($\Gamma$)", color="#0d47a1")
    axes[0].axis("off")

    for idx, k in enumerate(k_values):
        ax = axes[idx + 1]
        k_clamped = min(k, model.n_components)
        recon, eps_d = model.reconstruct(sample_image, n_components=k_clamped)
        recon_img = recon.reshape(model.img_shape)
        ax.imshow(recon_img, cmap="gray")
        ax.set_title(f"$K={k_clamped}$\n" + r"$\epsilon_d=" + f"{eps_d:.2f}$", fontsize=9)
        ax.axis("off")

    plt.suptitle("Face Reconstruction Convergence with Increasing Eigenfaces ($K$)", fontsize=13)
    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
    return fig


def plot_decision_space(
    model: EigenfacesClassifier,
    known_test_images: np.ndarray,
    unknown_test_images: np.ndarray,
    non_face_images: np.ndarray,
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Plots the 2D Decision Space:
    X-axis: Distance from Face Space (epsilon_d / DFFS)
    Y-axis: Distance in Face Space to nearest known class (epsilon_c / DIFS)
    Demonstrating the Turk & Pentland 4-Way Decision Rule boundaries.
    """
    set_plot_style()
    fig, ax = plt.subplots(figsize=(9, 6.5))

    # Collect coordinates for known faces
    known_dffs, known_difs = [], []
    for img in known_test_images:
        res = model.recognize(img)
        known_dffs.append(res["dffs"])
        known_difs.append(res["difs"])

    # Unknown faces
    unknown_dffs, unknown_difs = [], []
    for img in unknown_test_images:
        res = model.recognize(img)
        unknown_dffs.append(res["dffs"])
        unknown_difs.append(res["difs"])

    # Non-faces
    nonface_dffs, nonface_difs = [], []
    for img in non_face_images:
        res = model.recognize(img)
        nonface_dffs.append(res["dffs"])
        nonface_difs.append(res["difs"])

    # Scatter points
    ax.scatter(known_dffs, known_difs, c="#2e7d32", label="Known Probe Faces", alpha=0.75, s=40, edgecolors="none")
    ax.scatter(unknown_dffs, unknown_difs, c="#0288d1", label="Unknown Probe Faces", alpha=0.75, s=40, marker="^")
    ax.scatter(nonface_dffs, nonface_difs, c="#c62828", label="Non-Face Images", alpha=0.85, s=55, marker="x")

    # Decision Thresholds
    th_f = model.theta_face
    th_c = model.theta_class

    ax.axvline(th_f, color="#d32f2f", linestyle="--", lw=1.8, label=r"Face Space Threshold ($\theta_f$)")
    ax.axhline(th_c, color="#f57c00", linestyle="--", lw=1.8, label=r"Classification Threshold ($\theta_c$)")

    # Annotate quadrants
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    max_x = max(xlim[1], max(nonface_dffs) * 1.05)
    max_y = max(ylim[1], max(nonface_difs) * 1.05)
    ax.set_xlim([0, max_x])
    ax.set_ylim([0, max_y])

    # Shaded / text regions
    ax.text(
        th_f * 0.4,
        th_c * 0.4,
        r"ZONE 1: KNOWN FACE" + "\n" + r"($\epsilon_d < \theta_f, \epsilon_c < \theta_c$)",
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.4", fc="#e8f5e9", ec="#2e7d32", alpha=0.8),
        fontsize=9,
        fontweight="bold",
    )

    ax.text(
        th_f * 0.4,
        th_c + (max_y - th_c) * 0.4,
        r"ZONE 2: UNKNOWN FACE" + "\n" + r"($\epsilon_d < \theta_f, \epsilon_c \geq \theta_c$)",
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.4", fc="#e1f5fe", ec="#0288d1", alpha=0.8),
        fontsize=9,
        fontweight="bold",
    )

    ax.text(
        th_f + (max_x - th_f) * 0.5,
        th_c + (max_y - th_c) * 0.5,
        r"ZONE 3: NOT A FACE" + "\n" + r"($\epsilon_d \geq \theta_f, \epsilon_c \geq \theta_c$)",
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.4", fc="#ffebee", ec="#c62828", alpha=0.8),
        fontsize=9,
        fontweight="bold",
    )

    ax.text(
        th_f + (max_x - th_f) * 0.5,
        th_c * 0.5,
        r"ZONE 4: NOT A FACE" + "\n" + r"(False Match: $\epsilon_d \geq \theta_f, \epsilon_c < \theta_c$)",
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.4", fc="#fff3e0", ec="#f57c00", alpha=0.8),
        fontsize=8.5,
        fontweight="bold",
    )

    ax.set_xlabel(r"Distance from Face Space $\epsilon_d$ (DFFS) $\rightarrow$ Non-Face Rejection", fontsize=11)
    ax.set_ylabel(r"Distance in Face Space $\epsilon_c$ (DIFS) $\rightarrow$ Unknown Identity", fontsize=11)
    ax.set_title("Turk & Pentland (1991): 4-Way Decision Space Geometry", fontsize=13)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", framealpha=0.9)

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
    return fig


def plot_robustness_test(
    model: EigenfacesClassifier,
    sample_image: np.ndarray,
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Evaluates robustness under perturbations:
    1. Clean image
    2. Mild Gaussian Noise
    3. Severe Gaussian Noise
    4. Eye Occlusion (Sunglasses effect)
    5. Mouth Occlusion (Mask effect)
    """
    set_plot_style()
    h, w = model.img_shape

    # 1. Clean
    img_clean = sample_image.copy()

    # 2. Mild Noise
    np.random.seed(42)
    img_mild = np.clip(sample_image + np.random.normal(0, 0.1, sample_image.shape), 0, 1)

    # 3. Severe Noise
    img_severe = np.clip(sample_image + np.random.normal(0, 0.25, sample_image.shape), 0, 1)

    # 4. Eye Occlusion
    img_eye_occ = sample_image.copy()
    img_eye_occ[int(h * 0.35) : int(h * 0.50), int(w * 0.15) : int(w * 0.85)] = 0.0

    # 5. Mouth Occlusion
    img_mouth_occ = sample_image.copy()
    img_mouth_occ[int(h * 0.65) : int(h * 0.88), int(w * 0.2) : int(w * 0.8)] = 0.0

    variants = [
        ("Clean Face", img_clean),
        (r"Mild Noise ($\sigma=0.10$)", img_mild),
        (r"Severe Noise ($\sigma=0.25$)", img_severe),
        ("Eye Occlusion", img_eye_occ),
        ("Mouth Occlusion", img_mouth_occ),
    ]

    fig, axes = plt.subplots(2, len(variants), figsize=(3 * len(variants), 5.5))

    for idx, (name, img) in enumerate(variants):
        res = model.recognize(img)
        recon_img = res["reconstructed"].reshape(model.img_shape)

        # Top row: Input image
        axes[0, idx].imshow(img, cmap="gray")
        axes[0, idx].set_title(f"Input: {name}\n" + r"$\epsilon_d=" + f"{res['dffs']:.2f}$", fontsize=9)
        axes[0, idx].axis("off")

        # Bottom row: Reconstructed face
        axes[1, idx].imshow(recon_img, cmap="gray")
        axes[1, idx].set_title(
            f"Reconstructed\nDec: {res['decision']}",
            fontsize=9,
            color="#2e7d32" if res["decision"] == "KNOWN_FACE" else "#c62828",
        )
        axes[1, idx].axis("off")

    plt.suptitle("Turk & Pentland (1991): Robustness Analysis to Noise & Occlusion", fontsize=13)
    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
    return fig
