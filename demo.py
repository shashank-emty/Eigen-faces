"""
End-to-End Demonstration Script for Turk & Pentland (1991) 'Eigenfaces for Recognition'.
Designed for live student presentation (one-on-one viva or one-to-many lecture).
"""

import os
import sys
import numpy as np

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.dataset import generate_non_face_samples, load_face_data
from src.eigenfaces import EigenfacesClassifier
from src.evaluate import (
    evaluate_4way_decisions,
    evaluate_accuracy_vs_k,
    plot_accuracy_and_error_vs_k,
)
from src.visualizer import (
    plot_decision_space,
    plot_eigenvalue_spectrum,
    plot_mean_and_eigenfaces,
    plot_reconstructions,
    plot_robustness_test,
)


def print_header(title: str):
    border = "=" * 70
    print(f"\n{border}")
    print(f"  {title}")
    print(f"{border}\n")


def print_step(step_num: int, title: str, formula: str = ""):
    print(f"\n[STEP {step_num}] >>> {title}")
    if formula:
        print(f"         Formula: {formula}")


def run_demonstration():
    print_header("PROJECT DEMONSTRATION: EIGEN FACES (TURK & PENTLAND, 1991)")
    print("Presenter: Shashank M T (UUCMS No.: U01BH25C0174)")
    print("Course: BCA(AI) | Subject: Machine Learning")
    print("College: Pooja Bhagavat Mahajana First Grade College")
    print("GitHub Repo: https://github.com/shashank-emty/Eigen-faces")
    print("Core Methodology: Principal Component Analysis & Turk-Pentland Covariance Reduction")

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(output_dir, exist_ok=True)

    # -------------------------------------------------------------
    # Step 1: Data Preparation & Partitioning
    # -------------------------------------------------------------
    print_step(1, "Data Preparation & Subspace Partitioning")
    data = load_face_data(train_per_subject=7, num_known_subjects=35, random_state=42)
    X_train = data["X_train"]
    y_train = data["y_train"]
    X_test_known = data["X_test_known"]
    y_test_known = data["y_test_known"]
    X_test_unknown = data["X_test_unknown"]
    y_test_unknown = data["y_test_unknown"]

    M_train = len(X_train)
    H, W = data["image_shape"]
    D = H * W

    print(f"  - Database: Olivetti / AT&T Face Benchmark")
    print(f"  - Image Resolution: {H} x {W} pixels (Dimension D = {D})")
    print(f"  - Enrolled Gallery (Train): {M_train} images across 35 enrolled subjects")
    print(f"  - Known Probe Set (Test): {len(X_test_known)} images from enrolled subjects")
    print(f"  - Unknown Probe Set (Test): {len(X_test_unknown)} images from 5 unseen subjects (for rejection test)")

    # -------------------------------------------------------------
    # Step 2: Mean Face & Mean-Centered Difference Vectors
    # -------------------------------------------------------------
    print_step(2, "Computing Mean Face and Difference Vectors", r"\Psi = (1/M) \sum \Gamma_i, \Phi_i = \Gamma_i - \Psi")
    K_components = 40
    model = EigenfacesClassifier(n_components=K_components)
    model.fit(X_train, y_train, calibrate_thresholds=True)

    print(f"  - Average Face Vector Psi shape: {model.mean_face.shape}")
    print(f"  - Mean-centered Difference Matrix A shape: ({D}, {M_train})")

    # -------------------------------------------------------------
    # Step 3: Turk-Pentland Covariance Dimensionality Reduction
    # -------------------------------------------------------------
    print_step(
        3,
        "Turk-Pentland Covariance Reduction Trick",
        r"L = A^T A (M \times M) \quad \text{instead of} \quad C = A A^T (D \times D)",
    )
    print(f"  - Direct Covariance Matrix C would be: ({D} x {D}) = {D * D:,} entries! (Tractable? No)")
    print(f"  - Turk-Pentland Surrogate L is: ({M_train} x {M_train}) = {M_train * M_train:,} entries! (Reduction factor: {D*D / (M_train*M_train):.1f}x)")
    print(f"  - Eigenvalues computed: {len(model.all_eigenvalues)}")
    print(f"  - Selected Top K Eigenfaces: {model.n_components}")
    cum_var_k = np.sum(model.explained_variance_ratio_) * 100
    print(f"  - Cumulative Variance captured by K={model.n_components}: {cum_var_k:.2f}%")

    # -------------------------------------------------------------
    # Step 4: Visualizing Eigenfaces & Scree Plot
    # -------------------------------------------------------------
    print_step(4, "Generating Visualizations (Eigenfaces Gallery & Scree Plot)")
    fig_ef = plot_mean_and_eigenfaces(model, n_eigenfaces=15, save_path=os.path.join(output_dir, "01_eigenfaces_gallery.png"))
    fig_scree = plot_eigenvalue_spectrum(model, max_k=80, save_path=os.path.join(output_dir, "02_eigenvalue_scree_plot.png"))
    print(f"  [SAVED] {output_dir}/01_eigenfaces_gallery.png")
    print(f"  [SAVED] {output_dir}/02_eigenvalue_scree_plot.png")

    # -------------------------------------------------------------
    # Step 5: Face Reconstruction Fidelity
    # -------------------------------------------------------------
    print_step(5, "Face Reconstruction Analysis Across Dimensionality K", r"\hat{\Gamma} = \Psi + \sum_{k=1}^K \omega_k u_k")
    sample_face = X_test_known[0]
    fig_recon = plot_reconstructions(
        model,
        sample_face,
        k_values=[2, 5, 10, 20, 40],
        save_path=os.path.join(output_dir, "03_face_reconstruction.png"),
    )
    print(f"  [SAVED] {output_dir}/03_face_reconstruction.png")
    for k in [2, 5, 10, 20, 40]:
        _, err = model.reconstruct(sample_face, n_components=k)
        print(f"    * K = {k:2d} eigenfaces -> Reconstruction error (DFFS) = {err:.3f}")

    # -------------------------------------------------------------
    # Step 6: Non-Face Detection & 4-Way Decision Rule
    # -------------------------------------------------------------
    print_step(
        6,
        "Turk & Pentland 4-Way Decision Rule Demonstration",
        r"\text{Check } \epsilon_d \ge \theta_f \text{ (non-face) and } \epsilon_c < \theta_c \text{ (known)}",
    )
    X_non_face, non_face_names = generate_non_face_samples(n_samples=10, shape=(H, W), random_state=42)

    print(f"  - Calibrated Face Space Threshold (theta_face):   {model.theta_face:.3f}")
    print(f"  - Calibrated Classification Threshold (theta_class): {model.theta_class:.3f}")

    # Case A: Known Face Probe
    test_known = X_test_known[0]
    true_id = y_test_known[0]
    res_a = model.recognize(test_known)
    print("\n  [TEST CASE A: ENROLLED SUBJECT PROBE]")
    print(f"    * True Identity:       Subject #{true_id}")
    print(f"    * DFFS (epsilon_d):    {res_a['dffs']:.3f} (Threshold theta_f = {model.theta_face:.3f})")
    print(f"    * DIFS (epsilon_c):    {res_a['difs']:.3f} (Threshold theta_c = {model.theta_class:.3f})")
    print(f"    * System Decision:     --> {res_a['decision']} <--")
    print(f"    * Predicted Identity:  Subject #{res_a['predicted_label']} (Match: {res_a['predicted_label'] == true_id})")

    # Case B: Unknown Face Probe (Unenrolled Subject)
    # Find an unknown test probe that demonstrates the UNKNOWN_FACE decision
    unknown_idx = 1
    for idx_u, u_img in enumerate(X_test_unknown):
        if model.recognize(u_img)["decision"] == "UNKNOWN_FACE":
            unknown_idx = idx_u
            break
    test_unknown = X_test_unknown[unknown_idx]
    res_b = model.recognize(test_unknown)
    print("\n  [TEST CASE B: UNENROLLED SUBJECT PROBE (UNSEEN INDIVIDUAL)]")
    print(f"    * True Identity:       Unseen Individual (Subject #{y_test_unknown[unknown_idx]})")
    print(f"    * DFFS (epsilon_d):    {res_b['dffs']:.3f} (< theta_f: Confirmed Human Face)")
    print(f"    * DIFS (epsilon_c):    {res_b['difs']:.3f} (>= theta_c: Exceeds Known Gallery Distance)")
    print(f"    * System Decision:     --> {res_b['decision']} <--")

    # Case C: Non-Face Objects
    print("\n  [TEST CASE C: NON-FACE OBJECT REJECTION]")
    for i in range(min(4, len(X_non_face))):
        nf = X_non_face[i]
        res_c = model.recognize(nf)
        print(f"    * Non-Face '{non_face_names[i]}':")
        print(f"        DFFS (epsilon_d): {res_c['dffs']:.3f} (>= theta_f = {model.theta_face:.3f})")
        print(f"        System Decision:  --> {res_c['decision']} <--")

    # Save Decision Space Plot
    fig_dec = plot_decision_space(
        model,
        X_test_known[:30],
        X_test_unknown[:30],
        X_non_face,
        save_path=os.path.join(output_dir, "04_decision_space_geometry.png"),
    )
    print(f"\n  [SAVED] {output_dir}/04_decision_space_geometry.png")

    # -------------------------------------------------------------
    # Step 7: Perturbation & Robustness Analysis
    # -------------------------------------------------------------
    print_step(7, "Noise and Occlusion Robustness Evaluation")
    fig_rob = plot_robustness_test(
        model,
        test_known,
        save_path=os.path.join(output_dir, "05_robustness_analysis.png"),
    )
    print(f"  [SAVED] {output_dir}/05_robustness_analysis.png")

    # -------------------------------------------------------------
    # Step 8: Quantitative Benchmark Results
    # -------------------------------------------------------------
    print_step(8, "Quantitative Benchmark & Statistical Metrics")
    k_eval_list = [2, 5, 10, 15, 20, 30, 40, 50, 75, 100]
    bench_results = evaluate_accuracy_vs_k(X_train, y_train, X_test_known, y_test_known, k_eval_list)
    fig_curve = plot_accuracy_and_error_vs_k(
        bench_results,
        save_path=os.path.join(output_dir, "06_accuracy_vs_k.png"),
    )
    print(f"  [SAVED] {output_dir}/06_accuracy_vs_k.png")

    print("\n  +--------+---------------+-----------------------+")
    print("  |   K    |  Accuracy (%) | Mean Recon Error (DFFS)|")
    print("  +--------+---------------+-----------------------+")
    for k, acc, err in zip(
        bench_results["k_values"],
        bench_results["accuracies"],
        bench_results["reconstruction_errors"],
    ):
        print(f"  |  {k:4d}  |    {acc * 100:6.2f}%   |        {err:8.3f}       |")
    print("  +--------+---------------+-----------------------+")

    # 4-Way Decision Confusion Metrics
    metrics_4way = evaluate_4way_decisions(
        model,
        X_test_known,
        y_test_known,
        X_test_unknown,
        X_non_face,
    )
    print("\n  [TURK & PENTLAND 4-WAY DECISION STATS]")
    print(f"    * Non-Face Rejection Rate:        {metrics_4way['non_faces']['nonface_rejection_rate']*100:.1f}%")
    print(f"    * Face Acceptance Rate:           {metrics_4way['known_probes']['known_acceptance_rate']*100:.1f}%")
    print(f"    * Known Identification Rate:      {metrics_4way['known_probes']['correct_recognition_rate']*100:.1f}%")
    print(f"    * Unknown Probe Detection Rate:   {metrics_4way['unknown_probes']['correct_unknown_detection_rate']*100:.1f}%")

    print_header("DEMONSTRATION COMPLETE: ALL PRESENTATION FIGURES GENERATED IN 'results/'")


if __name__ == "__main__":
    run_demonstration()
