"""
Quantitative Evaluation and Experimentation suite for Eigenfaces.
Implements benchmarks for:
1. Accuracy vs Number of Eigenfaces (K)
2. 4-Way Decision Rule Performance (Face detection vs Unknown vs Known)
3. Noise and Occlusion Tolerance
4. Confusion Matrix and Error Analysis
"""

from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from src.eigenfaces import EigenfacesClassifier


def evaluate_accuracy_vs_k(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    k_values: List[int],
) -> Dict[str, List[float]]:
    """
    Computes classification accuracy for various numbers of eigenfaces K.
    Demonstrates the dimensionality reduction tradeoff.
    """
    accuracies = []
    reconstruction_errors = []

    # Flatten test set
    M_test, h, w = X_test.shape
    X_test_flat = X_test.reshape(M_test, h * w)

    for k in k_values:
        model_k = EigenfacesClassifier(n_components=k)
        model_k.fit(X_train, y_train, calibrate_thresholds=False)

        preds = []
        rec_errs = []
        for i in range(M_test):
            res = model_k.recognize(X_test_flat[i], use_centroids=True)
            preds.append(res["predicted_label"])
            rec_errs.append(res["dffs"])

        acc = float(np.mean(np.array(preds) == y_test))
        accuracies.append(acc)
        reconstruction_errors.append(float(np.mean(rec_errs)))

    return {
        "k_values": k_values,
        "accuracies": accuracies,
        "reconstruction_errors": reconstruction_errors,
    }


def evaluate_4way_decisions(
    model: EigenfacesClassifier,
    X_known_test: np.ndarray,
    y_known_test: np.ndarray,
    X_unknown_test: np.ndarray,
    X_non_face: np.ndarray,
) -> Dict[str, Dict[str, float]]:
    """
    Evaluates the complete Turk & Pentland 4-way decision matrix across:
    1. Known probe faces (Expected: KNOWN_FACE with correct ID)
    2. Unknown probe faces (Expected: UNKNOWN_FACE)
    3. Non-face images (Expected: NOT_A_FACE)
    """
    # 1. Known faces
    known_results = {"KNOWN_FACE": 0, "UNKNOWN_FACE": 0, "NOT_A_FACE": 0, "correct_id": 0}
    for i, img in enumerate(X_known_test):
        res = model.recognize(img)
        dec = res["decision"]
        known_results[dec] += 1
        if dec == "KNOWN_FACE" and res["predicted_label"] == y_known_test[i]:
            known_results["correct_id"] += 1

    total_known = len(X_known_test)
    known_metrics = {
        "known_acceptance_rate": (known_results["KNOWN_FACE"] + known_results["UNKNOWN_FACE"]) / total_known,
        "correct_recognition_rate": known_results["correct_id"] / total_known,
        "false_rejection_rate": known_results["NOT_A_FACE"] / total_known,
    }

    # 2. Unknown faces
    unknown_results = {"KNOWN_FACE": 0, "UNKNOWN_FACE": 0, "NOT_A_FACE": 0}
    for img in X_unknown_test:
        res = model.recognize(img)
        unknown_results[res["decision"]] += 1

    total_unknown = len(X_unknown_test)
    unknown_metrics = {
        "correct_unknown_detection_rate": unknown_results["UNKNOWN_FACE"] / total_unknown,
        "false_acceptance_rate": unknown_results["KNOWN_FACE"] / total_unknown,
        "false_nonface_rate": unknown_results["NOT_A_FACE"] / total_unknown,
    }

    # 3. Non-face images
    nonface_results = {"KNOWN_FACE": 0, "UNKNOWN_FACE": 0, "NOT_A_FACE": 0}
    for img in X_non_face:
        res = model.recognize(img)
        nonface_results[res["decision"]] += 1

    total_nonface = len(X_non_face)
    nonface_metrics = {
        "nonface_rejection_rate": nonface_results["NOT_A_FACE"] / total_nonface,
        "false_face_rate": (nonface_results["KNOWN_FACE"] + nonface_results["UNKNOWN_FACE"]) / total_nonface,
    }

    return {
        "known_probes": known_metrics,
        "unknown_probes": unknown_metrics,
        "non_faces": nonface_metrics,
        "raw_counts": {
            "known": known_results,
            "unknown": unknown_results,
            "nonface": nonface_results,
        },
    }


def plot_accuracy_and_error_vs_k(
    results: Dict[str, List[float]],
    save_path: str = None,
) -> plt.Figure:
    """
    Plots dual-axis curve: Accuracy vs K and Reconstruction error vs K.
    """
    k_vals = results["k_values"]
    accs = [a * 100 for a in results["accuracies"]]
    rec_errs = results["reconstruction_errors"]

    fig, ax1 = plt.subplots(figsize=(8, 4.8))

    color = "#1565c0"
    ax1.set_xlabel("Number of Eigenfaces ($K$)", fontsize=11)
    ax1.set_ylabel("Recognition Accuracy (%)", color=color, fontsize=11)
    line1 = ax1.plot(k_vals, accs, "o-", color=color, lw=2, markersize=5, label="Test Accuracy (%)")
    ax1.tick_params(axis="y", labelcolor=color)
    ax1.grid(True, linestyle="--", alpha=0.5)

    ax2 = ax1.twinx()
    color2 = "#e65100"
    ax2.set_ylabel(r"Mean Reconstruction Error ($\epsilon_d$)", color=color2, fontsize=11)
    line2 = ax2.plot(k_vals, rec_errs, "s--", color=color2, lw=1.8, markersize=4, label="Reconstruction Error")
    ax2.tick_params(axis="y", labelcolor=color2)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="center right")

    plt.title("Effect of Dimensionality ($K$) on Accuracy and Reconstruction Error", fontsize=12, pad=12)

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
    return fig
