"""
Interactive Web Presentation Dashboard for Eigenfaces (Turk & Pentland, 1991).
Equips the presenter with live interactive demonstrations:
- Live face reconstruction slider across K components
- Interactive 4-way decision rule tester (Known, Unknown, Non-face)
- Eigenfaces and Mean face inspector
- Embedded presentation slides with mathematical formulas
"""

import base64
import io
import os
import sys
from typing import Tuple

from flask import Flask, jsonify, render_template, request, send_from_directory
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.dataset import generate_non_face_samples, load_face_data
from src.eigenfaces import EigenfacesClassifier

app = Flask(__name__)

# Global model state
MODEL = None
DATA = None
NON_FACES = None
NON_FACE_NAMES = None


def array_to_base64_png(arr: np.ndarray, cmap: str = "gray") -> str:
    """Convert a 2D numpy float array to base64 encoded PNG data URI."""
    fig, ax = plt.subplots(figsize=(2.5, 2.5), dpi=100)
    ax.imshow(arr, cmap=cmap)
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def init_app():
    global MODEL, DATA, NON_FACES, NON_FACE_NAMES
    print("[INIT] Loading face dataset and training model...")
    DATA = load_face_data(train_per_subject=7, num_known_subjects=35, random_state=42)
    NON_FACES, NON_FACE_NAMES = generate_non_face_samples(n_samples=10, shape=(64, 64))

    MODEL = EigenfacesClassifier(n_components=50)
    MODEL.fit(DATA["X_train"], DATA["y_train"], calibrate_thresholds=True)
    print(f"[INIT] Model ready: D={MODEL.D}, M={MODEL.M}, K={MODEL.n_components}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/report")
def serve_report():
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "REPORT.html")
    with open(report_path, "r", encoding="utf-8") as f:
        return f.read()


@app.route("/slides")
def serve_slides():
    slides_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "slides.html")
    with open(slides_path, "r", encoding="utf-8") as f:
        return f.read()


@app.route("/slides/download")
def download_slides_pptx():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(root_dir, "EigenFaces_Presentation.pptx", as_attachment=True)


@app.route("/results/<path:filename>")
def serve_results(filename):
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    return send_from_directory(results_dir, filename)


@app.route("/api/info")
def api_info():
    cum_var = float(np.sum(MODEL.explained_variance_ratio_) * 100)
    return jsonify(
        {
            "dimension_D": MODEL.D,
            "image_shape": MODEL.img_shape,
            "training_samples_M": MODEL.M,
            "n_components_K": MODEL.n_components,
            "theta_face": round(MODEL.theta_face, 3),
            "theta_class": round(MODEL.theta_class, 3),
            "cumulative_variance_pct": round(cum_var, 2),
            "known_subjects_count": len(MODEL.class_centroids),
            "unknown_test_count": len(DATA["X_test_unknown"]),
        }
    )


@app.route("/api/mean_face")
def api_mean_face():
    img_b64 = array_to_base64_png(MODEL.get_mean_face_image(), cmap="gray")
    return jsonify({"image": img_b64})


@app.route("/api/eigenfaces")
def api_eigenfaces():
    count = int(request.args.get("count", 16))
    count = min(count, MODEL.n_components)
    eigenfaces_list = []
    for i in range(count):
        img_b64 = array_to_base64_png(MODEL.get_eigenface_image(i), cmap="bone")
        var_pct = float(MODEL.explained_variance_ratio_[i] * 100)
        eigenfaces_list.append(
            {
                "index": i + 1,
                "variance_pct": round(var_pct, 2),
                "image": img_b64,
            }
        )
    return jsonify({"eigenfaces": eigenfaces_list})


@app.route("/api/samples")
def api_samples():
    """List selectable sample images for testing."""
    samples = []

    # 1. Known Test Probes
    for i in [0, 1, 2, 5, 10, 15, 20]:
        if i < len(DATA["X_test_known"]):
            samples.append(
                {
                    "type": "known",
                    "id": i,
                    "label": f"Enrolled Subject #{DATA['y_test_known'][i]} (Test Probe)",
                    "thumb": array_to_base64_png(DATA["X_test_known"][i]),
                }
            )

    # 2. Unknown Test Probes
    for i in [0, 1, 10, 20]:
        if i < len(DATA["X_test_unknown"]):
            samples.append(
                {
                    "type": "unknown",
                    "id": i,
                    "label": f"Unenrolled Individual #{DATA['y_test_unknown'][i]} (Unseen)",
                    "thumb": array_to_base64_png(DATA["X_test_unknown"][i]),
                }
            )

    # 3. Non-Faces
    for i in range(min(5, len(NON_FACES))):
        samples.append(
            {
                "type": "nonface",
                "id": i,
                "label": f"Non-Face: {NON_FACE_NAMES[i]}",
                "thumb": array_to_base64_png(NON_FACES[i]),
            }
        )

    return jsonify({"samples": samples})


@app.route("/api/reconstruct", methods=["POST"])
def api_reconstruct():
    payload = request.json or {}
    sample_type = payload.get("type", "known")
    sample_id = int(payload.get("id", 0))
    k = int(payload.get("k", 20))
    k = max(1, min(k, MODEL.n_components))

    # Retrieve source image
    if sample_type == "known":
        img = DATA["X_test_known"][sample_id]
    elif sample_type == "unknown":
        img = DATA["X_test_unknown"][sample_id]
    elif sample_type == "nonface":
        img = NON_FACES[sample_id]
    else:
        img = DATA["X_test_known"][0]

    recon_flat, dffs = MODEL.reconstruct(img, n_components=k)
    recon_img = recon_flat.reshape(MODEL.img_shape)
    diff_img = np.abs(img - recon_img)

    total_var = np.sum(MODEL.explained_variance_ratio_[:k]) * 100

    return jsonify(
        {
            "k": k,
            "dffs": round(dffs, 3),
            "variance_captured_pct": round(float(total_var), 2),
            "original_image": array_to_base64_png(img),
            "reconstructed_image": array_to_base64_png(recon_img),
            "diff_image": array_to_base64_png(diff_img, cmap="hot"),
        }
    )


@app.route("/api/recognize", methods=["POST"])
def api_recognize():
    payload = request.json or {}
    sample_type = payload.get("type", "known")
    sample_id = int(payload.get("id", 0))

    if sample_type == "known":
        img = DATA["X_test_known"][sample_id]
        true_label = int(DATA["y_test_known"][sample_id])
    elif sample_type == "unknown":
        img = DATA["X_test_unknown"][sample_id]
        true_label = f"Unseen (Subject #{DATA['y_test_unknown'][sample_id]})"
    elif sample_type == "nonface":
        img = NON_FACES[sample_id]
        true_label = "Not a Face"
    else:
        img = DATA["X_test_known"][0]
        true_label = 0

    res = MODEL.recognize(img)
    pred_label = int(res["predicted_label"]) if res["predicted_label"] is not None else None

    # If predicted a known subject, fetch an enrolled reference image
    matched_thumb = None
    if pred_label is not None:
        idx_match = np.where(DATA["y_train"] == pred_label)[0]
        if len(idx_match) > 0:
            matched_thumb = array_to_base64_png(DATA["X_train"][idx_match[0]])

    recon_img = res["reconstructed"].reshape(MODEL.img_shape)

    return jsonify(
        {
            "decision": res["decision"],
            "is_face": bool(res["is_face"]),
            "is_known": bool(res["is_known"]),
            "true_identity": str(true_label),
            "predicted_identity": pred_label,
            "dffs": round(float(res["dffs"]), 3),
            "difs": round(float(res["difs"]), 3),
            "theta_face": round(float(res["theta_face"]), 3),
            "theta_class": round(float(res["theta_class"]), 3),
            "query_image": array_to_base64_png(img),
            "reconstructed_image": array_to_base64_png(recon_img),
            "matched_thumbnail": matched_thumb,
        }
    )


if __name__ == "__main__":
    init_app()
    port = int(os.environ.get("PORT", 5050))
    print(f"\n=================================================================")
    print(f"  EIGENFACES INTERACTIVE PRESENTATION SERVER RUNNING")
    print(f"  Access live at: http://localhost:{port}")
    print(f"=================================================================\n")
    app.run(host="127.0.0.1", port=port, debug=False)
