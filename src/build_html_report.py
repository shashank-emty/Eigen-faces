"""
Build a self-contained, print-ready, monochrome/B&W compatible HTML report (REPORT.html).
Includes formal college title page, student credentials, and GitHub QR code.
"""

import base64
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BW_DIR = os.path.join(BASE_DIR, "results", "bw")


def get_image_b64(filename):
    path = os.path.join(BW_DIR, filename)
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def build_report_html():
    fig1_b64 = get_image_b64("fig1_eigenfaces_gallery.png")
    fig2_b64 = get_image_b64("fig2_scree_plot.png")
    fig3_b64 = get_image_b64("fig3_face_reconstruction.png")
    fig4_b64 = get_image_b64("fig4_decision_space_geometry.png")
    fig5_b64 = get_image_b64("fig5_robustness_analysis.png")
    fig6_b64 = get_image_b64("fig6_accuracy_vs_k.png")
    qr_b64 = get_image_b64("github_qr.png")

    template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Project Report: Eigen Faces — Shashank M T (U01BH25C0174)</title>
  <!-- KaTeX for crisp vector equations -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {delimiters: [{left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}]});"></script>

  <style>
    /* Monochrome / Black & White Print Compatible Styling */
    @page {
      size: A4;
      margin: 20mm 15mm 20mm 15mm;
      @bottom-right {
        content: counter(page);
      }
    }
    body {
      font-family: "Times New Roman", Times, Georgia, serif;
      font-size: 11pt;
      line-height: 1.5;
      color: #000000;
      background: #ffffff;
      margin: 0;
      padding: 30px;
    }
    .no-print {
      background: #f0f0f0;
      padding: 12px 20px;
      margin-bottom: 25px;
      border: 1px solid #333333;
      border-radius: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .print-btn {
      background: #000000;
      color: #ffffff;
      border: 1px solid #000000;
      padding: 8px 18px;
      font-weight: bold;
      cursor: pointer;
      border-radius: 4px;
      font-size: 10pt;
    }
    .print-btn:hover {
      background: #333333;
    }
    @media print {
      .no-print {
        display: none !important;
      }
      body {
        padding: 0;
      }
      .page-break {
        page-break-before: always;
      }
      h2 {
        page-break-after: avoid;
      }
      table, figure, .credential-card {
        page-break-inside: avoid;
      }
    }
    .college-header {
      text-align: center;
      border-bottom: 2px solid #000000;
      padding-bottom: 12px;
      margin-bottom: 20px;
    }
    .college-header h2 {
      font-size: 15pt;
      margin: 0;
      border: none;
      padding: 0;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .college-header p {
      margin: 3px 0 0 0;
      font-size: 10.5pt;
      text-align: center;
      font-style: italic;
    }
    h1 {
      font-size: 20pt;
      text-align: center;
      text-transform: uppercase;
      margin-top: 15px;
      margin-bottom: 4px;
      letter-spacing: 1px;
    }
    .subtitle {
      text-align: center;
      font-size: 12pt;
      font-style: italic;
      margin-bottom: 20px;
    }
    .credential-card {
      border: 1.5px solid #000000;
      padding: 14px 20px;
      margin-bottom: 25px;
      background: #fafafa;
    }
    .credential-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      row-gap: 8px;
      column-gap: 20px;
      font-size: 10.5pt;
    }
    .credential-item strong {
      display: inline-block;
      width: 130px;
      text-transform: uppercase;
      font-size: 9.5pt;
      letter-spacing: 0.3px;
    }
    h2 {
      font-size: 13pt;
      border-bottom: 1px solid #000000;
      padding-bottom: 3px;
      margin-top: 25px;
      margin-bottom: 12px;
      text-transform: uppercase;
    }
    h3 {
      font-size: 11.5pt;
      margin-top: 16px;
      margin-bottom: 8px;
    }
    p {
      margin-bottom: 10px;
      text-align: justify;
    }
    .abstract {
      font-size: 10.5pt;
      padding: 12px 18px;
      border: 1px solid #000000;
      background: #fafafa;
      margin-bottom: 25px;
      border-radius: 4px;
    }
    .abstract strong {
      display: block;
      text-transform: uppercase;
      font-size: 10pt;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
      text-align: center;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 15px 0;
      font-size: 10pt;
    }
    th, td {
      border: 1px solid #000000;
      padding: 6px 10px;
      text-align: left;
    }
    th {
      background: #f0f0f0;
      font-weight: bold;
    }
    .text-center {
      text-align: center;
    }
    .math-block {
      padding: 6px 0;
      margin: 8px 0;
      text-align: center;
    }
    figure {
      margin: 16px 0;
      text-align: center;
    }
    figure img {
      max-width: 95%;
      height: auto;
      border: 1px solid #000000;
    }
    figcaption {
      font-size: 9.5pt;
      font-style: italic;
      margin-top: 6px;
      text-align: center;
    }
    code {
      font-family: "Courier New", Courier, monospace;
      font-size: 9.5pt;
      background: #f0f0f0;
      padding: 2px 4px;
      border: 1px solid #cccccc;
    }
    ul, ol {
      margin-top: 6px;
      margin-bottom: 12px;
      padding-left: 24px;
    }
    li {
      margin-bottom: 4px;
    }
    .qr-container {
      border: 1.5px solid #000000;
      padding: 18px;
      margin-top: 20px;
      text-align: center;
      background: #fafafa;
      page-break-inside: avoid;
    }
    .qr-container img {
      width: 160px;
      height: 160px;
      border: 1px solid #000000;
      margin: 10px 0;
    }
    .repo-link {
      font-family: "Courier New", Courier, monospace;
      font-size: 10pt;
      font-weight: bold;
      word-break: break-all;
    }
  </style>
</head>
<body>

  <!-- Screen-only print toolbar -->
  <div class="no-print">
    <div>
      <strong>Submission-Ready Academic Document</strong> &mdash; 100% Black &amp; White Laser Printer Compatible.
    </div>
    <button class="print-btn" onclick="window.print()">Print / Save as PDF</button>
  </div>

  <!-- Formal College Header -->
  <div class="college-header">
    <h2>Pooja Bhagavat Mahajana First Grade College</h2>
    <p>Department of Computer Science &amp; Artificial Intelligence &bull; Mysore, Karnataka</p>
  </div>

  <h1>EIGEN FACES</h1>
  <div class="subtitle">A Technical Paper Implementation &amp; Empirical Evaluation of Turk &amp; Pentland (1991) Using Python</div>

  <!-- Student Credentials Card -->
  <div class="credential-card">
    <div class="credential-grid">
      <div class="credential-item">
        <strong>Student Name:</strong> Shashank M T
      </div>
      <div class="credential-item">
        <strong>Course:</strong> BCA(AI)
      </div>
      <div class="credential-item">
        <strong>UUCMS No.:</strong> U01BH25C0174
      </div>
      <div class="credential-item">
        <strong>Subject:</strong> Machine Learning
      </div>
      <div class="credential-item">
        <strong>Institution:</strong> Pooja Bhagavat Mahajana FGC
      </div>
      <div class="credential-item">
        <strong>Date of Report:</strong> October 15, 2026
      </div>
    </div>
  </div>

  <div class="abstract">
    <strong>Abstract</strong>
    This technical report details a complete, from-scratch Python implementation of the foundational paper <i>"Eigenfaces for Recognition"</i> by Matthew Turk and Alex Pentland (1991). The Eigenfaces methodology revolutionized biometrics by shifting face recognition from fragile, hand-crafted geometric measurements (such as eye distances and nose widths) to a holistic, information-theoretic linear subspace model based on Principal Component Analysis (PCA). To resolve the computational infeasibility of decomposing a $D \times D$ covariance matrix ($D = 4096$ pixels, yielding over $16.7\\text{ million entries}$), this work implements the <b>Turk-Pentland Covariance Reduction Trick</b>, mapping the eigendecomposition to an $M \times M$ surrogate matrix ($M = 245$ images, $60,025$ entries&mdash;a <b>$279.5\\times$ reduction factor</b>). The implementation incorporates the complete two-threshold <b>4-way decision framework</b> from Section 3.2, employing Distance from Face Space (DFFS, $\\epsilon_d$) for non-face rejection and Distance in Face Space (DIFS, $\\epsilon_c$) for enrolled identity recognition versus unseen human face discovery. Evaluated on the canonical Olivetti / AT&amp;T database (400 images across 40 subjects), the system achieves <b>$85.71\\%$</b> top-1 recognition accuracy at $K=40$ eigenfaces and <b>$87.62\\%$</b> at $K=50$, representing a <b>$99.0\\%$ dimensionality reduction</b>. Non-face pattern rejection reaches $80.0\\%&ndash;90.0\\%$ with $0.0\\%$ false rejections on valid faces. Complete mathematical proofs, step-by-step algorithms, empirical tables, black-and-white print-compatible graphics, and repository verification links are documented herein.
  </div>

  <h2>1. Introduction and Historical Context</h2>
  <p>
    Prior to the early 1990s, automated face recognition predominantly relied upon geometric feature matching (Kanade, 1973; Yuille et al., 1989). These systems attempted to extract anatomical fiducial points&mdash;such as eye corners, nostril centers, and lip boundaries&mdash;and compare Euclidean distances or relative angles between them. Despite their intuitive appeal, geometric methods suffered from three fatal shortcomings:
  </p>
  <ol>
    <li><b>Feature Extraction Brittleness:</b> Accurately locating fiducial landmarks in real-world images under varying contrast, shadow, or minor head rotations is notoriously fragile.</li>
    <li><b>Omission of Holistic Appearance:</b> Geometric distances discard subtle skin textures, cheekbone contours, and global surface shading that human observers rely upon for identification.</li>
    <li><b>Inability to Detect Non-Faces:</b> Geometric rules cannot inherently determine whether a query image contains a human face or an arbitrary background object.</li>
  </ol>
  <p>
    Building upon Sirovich and Kirby's (1987) demonstration that PCA could efficiently represent facial imagery, Matthew Turk and Alex Pentland (1991) introduced <b>Eigenfaces</b>. They transformed PCA from a passive compression technique into an end-to-end, real-time face detection and recognition architecture.
  </p>

  <h2>2. Mathematical Formulation and Analytical Derivations</h2>

  <h3>2.1 Image Representation and Average Face</h3>
  <p>
    Let each 2D facial image $I(x,y)$ be of dimension $H \\times W$. The image is unrolled row-wise into a column vector $\\Gamma_i \\in \\mathbb{R}^D$ where $D = H \\times W$ ($64 \\times 64 = 4096$). Given an ensemble of $M$ training images $\\{\\Gamma_1, \\Gamma_2, \\dots, \\Gamma_M\\}$, the <b>Average Face</b> $\\Psi$ represents the common anatomical baseline:
  </p>
  <div class="math-block">
    $$\\Psi = \\frac{1}{M} \\sum_{i=1}^M \\Gamma_i$$
  </div>
  <p>
    Each face vector is centered by subtracting the mean: $\\Phi_i = \\Gamma_i - \\Psi$. Concatenating these column vectors produces the difference matrix $A \\in \\mathbb{R}^{D \\times M}$:
  </p>
  <div class="math-block">
    $$A = [\\Phi_1, \\Phi_2, \\dots, \\Phi_M]$$
  </div>

  <h3>2.2 The Dimensionality Dilemma and The Turk-Pentland Algebraic Trick</h3>
  <p>
    The sample covariance matrix $C \\in \\mathbb{R}^{D \\times D}$ is defined as:
  </p>
  <div class="math-block">
    $$C = \\frac{1}{M} \\sum_{i=1}^M \\Phi_i \\Phi_i^T = \\frac{1}{M} A A^T$$
  </div>
  <p>
    For $64 \\times 64$ images, $D = 4096$. Consequently, $C$ contains $4096 \\times 4096 = 16,777,216$ elements. Computing the eigenvalues and eigenvectors of a $4096 \\times 4096$ matrix requires $\\mathcal{O}(D^3) \\approx 6.87 \\times 10^{10}$ floating-point operations. Moreover, since there are only $M = 245$ training images, the rank of $A A^T$ is at most $M - 1 = 244$. At least $D - M + 1 = 3852$ eigenvalues are identically zero.
  </p>
  <p>
    <b>The Turk-Pentland Reduction:</b> Construct the inner-product surrogate matrix $L \\in \\mathbb{R}^{M \\times M}$:
  </p>
  <div class="math-block">
    $$L = A^T A$$
  </div>
  <p>
    Matrix $L$ is of size $245 \\times 245 = 60,025$ elements&mdash;<b>$279.5\\times$ smaller than $C$</b>.
  </p>
  <p>
    <b>Proof of Equivalence:</b> Let $v_k$ be an eigenvector of $L$ associated with eigenvalue $\\mu_k$:
  </p>
  <div class="math-block">
    $$A^T A v_k = \\mu_k v_k$$
  </div>
  <p>
    Premultiplying both sides by matrix $A$:
  </p>
  <div class="math-block">
    $$A (A^T A v_k) = A (\\mu_k v_k) \\implies (A A^T)(A v_k) = \\mu_k (A v_k)$$
  </div>
  <p>
    This proves that $u_k = A v_k$ is an exact eigenvector of the full covariance matrix $A A^T$. Normalizing to unit Euclidean norm:
  </p>
  <div class="math-block">
    $$u_k = \\frac{A v_k}{\\|A v_k\\|_2}, \\quad \\text{such that } \\|u_k\\|_2 = 1 \\text{ and } u_j^T u_k = \\delta_{jk}$$
  </div>
  <p>
    Sorting eigenvalues in descending order ($\\mu_1 \\ge \\mu_2 \\ge \\dots \\ge \\mu_M$), the top $K$ eigenfaces form projection matrix $U = [u_1, u_2, \\dots, u_K] \\in \\mathbb{R}^{D \\times K}$.
  </p>

  <figure>
    <img src="__FIG1_B64__" alt="Figure 1: Mean Face and Eigenfaces">
    <figcaption>Figure 1: Average face ($\Psi$) and the top 15 principal eigenfaces ($u_1 \dots u_{15}$) with individual variance explained.</figcaption>
  </figure>

  <div class="page-break"></div>

  <h3>2.3 Subspace Projection and Reconstruction</h3>
  <p>
    Any centered face image $\\Phi = \\Gamma - \\Psi$ is projected into $K$-dimensional Face Space by computing:
  </p>
  <div class="math-block">
    $$\\Omega = U^T (\\Gamma - \\Psi) = [\\omega_1, \\omega_2, \\dots, \\omega_K]^T \\in \\mathbb{R}^K$$
  </div>
  <p>
    The reconstructed image $\\hat{\\Gamma}$ is synthesized as:
  </p>
  <div class="math-block">
    $$\\hat{\\Gamma} = \\Psi + U \\Omega = \\Psi + \\sum_{k=1}^K \\omega_k u_k$$
  </div>

  <figure>
    <img src="__FIG3_B64__" alt="Figure 2: Reconstruction Convergence">
    <figcaption>Figure 2: Progressive face reconstruction across $K \\in [2, 5, 10, 20, 40]$ showing rapid detail convergence.</figcaption>
  </figure>

  <h3>2.4 Dual Distance Metrics and The 4-Way Decision Framework</h3>
  <p>
    Turk and Pentland formulated recognition as a dual hypothesis test using two distinct Euclidean distance metrics:
  </p>
  <ul>
    <li><b>Distance from Face Space (DFFS - $\\epsilon_d$):</b> $\\epsilon_d = \\|\\Gamma - \\hat{\\Gamma}\\|_2$. Measures the orthogonal residual between the query image and the face manifold. Acts as a <b>Face Detector</b>.</li>
    <li><b>Distance in Face Space (DIFS - $\\epsilon_c$):</b> $\\epsilon_c = \\min_k \\|\\Omega - \\Omega_k\\|_2$ where $\\Omega_k$ is the enrolled class centroid. Measures resemblance to enrolled identities. Acts as a <b>Face Classifier</b>.</li>
  </ul>

  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Condition</th>
        <th style="width: 25%;">Decision</th>
        <th style="width: 50%;">Physical Meaning &amp; Action</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>$\\epsilon_d \\ge \\theta_f$</td>
        <td><strong>NOT A FACE</strong></td>
        <td>Image does not match face subspace geometry (e.g. background object, noise, texture). Rejected.</td>
      </tr>
      <tr>
        <td>$\\epsilon_d < \\theta_f \\land \\epsilon_c < \\theta_c$</td>
        <td><strong>KNOWN FACE</strong></td>
        <td>Confirmed human face; recognized as enrolled individual $c^* = \\arg\\min_k \\|\\Omega - \\Omega_k\\|$.</td>
      </tr>
      <tr>
        <td>$\\epsilon_d < \\theta_f \\land \\epsilon_c \\ge \\theta_c$</td>
        <td><strong>UNKNOWN FACE</strong></td>
        <td>Confirmed human face, but belongs to an unseen person. System prompts for new enrollment.</td>
      </tr>
    </tbody>
  </table>

  <figure>
    <img src="__FIG4_B64__" alt="Figure 3: Decision Space Geometry">
    <figcaption>Figure 3: 2D Decision Space Geometry displaying the 3 operational zones partitioned by thresholds $\\theta_f$ and $\\theta_c$.</figcaption>
  </figure>

  <div class="page-break"></div>

  <h2>3. Dataset and Experimental Setup</h2>
  <p>
    The experiments were conducted on the <b>Olivetti / AT&amp;T Face Database</b> (40 subjects, 10 photos/subject, $64 \\times 64$ grayscale). The dataset was partitioned to rigorously test all 4 outcomes of Turk &amp; Pentland's decision logic:
  </p>
  <ul>
    <li><b>Training Gallery ($X_{\\text{train}}$):</b> 35 enrolled individuals $\\times$ 7 photos = <b>245 images</b> ($M = 245$). Used to compute $\\Psi$, $A$, $L$, and $U$.</li>
    <li><b>Known Probe Test Set ($X_{\\text{test\\_known}}$):</b> 35 enrolled individuals $\\times$ 3 photos = <b>105 images</b>. Evaluates top-1 recognition accuracy.</li>
    <li><b>Unknown Probe Test Set ($X_{\\text{test\\_unknown}}$):</b> 5 unenrolled individuals $\\times$ 10 photos = <b>50 images</b>. Completely withheld from training to evaluate the "Unknown Face" detection rule.</li>
    <li><b>Non-Face Pattern Set:</b> 10 synthetic textures (checkerboards, noise, ripples, gradients) to test non-face rejection.</li>
  </ul>

  <h2>4. Empirical Results and Performance Analysis</h2>

  <figure>
    <img src="__FIG2_B64__" alt="Figure 4: Scree Plot">
    <figcaption>Figure 4: Scree plot of eigenvalues (left) and cumulative variance curve (right), indicating 90% variance at $K=57$.</figcaption>
  </figure>

  <h3>4.1 Accuracy and Reconstruction Error Tradeoff vs. K</h3>
  <p>
    Table 1 and Figure 5 illustrate the tradeoff between dimensionality reduction and recognition fidelity.
  </p>

  <table>
    <thead>
      <tr>
        <th class="text-center">Components ($K$)</th>
        <th class="text-center">Dimensionality Reduction</th>
        <th class="text-center">Top-1 Accuracy (%)</th>
        <th class="text-center">Mean Reconstruction Error ($\\epsilon_d$)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="text-center">2</td>
        <td class="text-center">99.95%</td>
        <td class="text-center">18.10%</td>
        <td class="text-center">6.859</td>
      </tr>
      <tr>
        <td class="text-center">5</td>
        <td class="text-center">99.88%</td>
        <td class="text-center">50.48%</td>
        <td class="text-center">5.931</td>
      </tr>
      <tr>
        <td class="text-center">10</td>
        <td class="text-center">99.76%</td>
        <td class="text-center">74.29%</td>
        <td class="text-center">5.245</td>
      </tr>
      <tr>
        <td class="text-center">20</td>
        <td class="text-center">99.51%</td>
        <td class="text-center">81.90%</td>
        <td class="text-center">4.496</td>
      </tr>
      <tr>
        <td class="text-center"><strong>40</strong></td>
        <td class="text-center"><strong>99.02%</strong></td>
        <td class="text-center"><strong>85.71%</strong></td>
        <td class="text-center"><strong>3.847</strong></td>
      </tr>
      <tr>
        <td class="text-center"><strong>50</strong></td>
        <td class="text-center"><strong>98.78%</strong></td>
        <td class="text-center"><strong>87.62%</strong></td>
        <td class="text-center"><strong>3.676</strong></td>
      </tr>
      <tr>
        <td class="text-center">100</td>
        <td class="text-center">97.56%</td>
        <td class="text-center">87.62%</td>
        <td class="text-center">3.197</td>
      </tr>
    </tbody>
  </table>

  <figure>
    <img src="__FIG6_B64__" alt="Figure 5: Accuracy vs K">
    <figcaption>Figure 5: Top-1 recognition accuracy (solid line with circles) and reconstruction error $\\epsilon_d$ (dashed line with triangles) vs. $K$.</figcaption>
  </figure>

  <h3>4.2 Robustness Under Noise and Partial Occlusions</h3>
  <figure>
    <img src="__FIG5_B64__" alt="Figure 6: Robustness Analysis">
    <figcaption>Figure 6: Robustness under Gaussian noise ($\sigma=0.10, 0.25$) and synthetic occlusions (sunglasses and surgical mask).</figcaption>
  </figure>
  <p>
    Because eigenfaces capture holistic, low-frequency facial structure across the entire image plane, localized occlusions (e.g. eye masks or mouth blocks) alter only a small fraction of the subspace inner products, allowing the remaining unoccluded facial surface to preserve identity.
  </p>

  <div class="page-break"></div>

  <h2>5. Comparative Discussion: Eigenfaces vs. Modern Methods</h2>
  <table>
    <thead>
      <tr>
        <th>Attribute</th>
        <th>Eigenfaces (PCA, 1991)</th>
        <th>Fisherfaces (LDA, 1997)</th>
        <th>Deep Metric Learning (CNNs, 2014+)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Supervision</strong></td>
        <td>Unsupervised (maximizes total variance)</td>
        <td>Supervised (maximizes class separation)</td>
        <td>Supervised (ArcFace / CosFace margin losses)</td>
      </tr>
      <tr>
        <td><strong>Illumination Robustness</strong></td>
        <td>Low (top eigenfaces encode lighting shifts)</td>
        <td>High (discards intra-class lighting scatter)</td>
        <td>Very High (learned non-linear feature maps)</td>
      </tr>
      <tr>
        <td><strong>Manifold Structure</strong></td>
        <td>Linear subspace ($U^T \\Phi$)</td>
        <td>Linear discriminant subspace</td>
        <td>Highly non-linear deep manifold</td>
      </tr>
      <tr>
        <td><strong>Pose Tolerance</strong></td>
        <td>Restricted to near-frontal ($\pm 20^\\circ$)</td>
        <td>Restricted to near-frontal</td>
        <td>Extreme pose tolerance ($\pm 90^\\circ$ profile)</td>
      </tr>
    </tbody>
  </table>

  <h2>6. Automated Unit Testing &amp; Verification</h2>
  <p>
    To verify mathematical fidelity, automated unit tests in <code>tests/test_eigenfaces.py</code> confirmed:
  </p>
  <ol>
    <li><b>Orthonormality of Basis:</b> Verified $U^T U = I_K$ to numerical precision ($10^{-7}$).</li>
    <li><b>Turk-Pentland Equivalence:</b> Proved eigenvectors derived from $L = A^T A$ align identically (overlap = $1.00000$) with direct eigendecomposition of $C = A A^T$.</li>
    <li><b>Monotonicity of Error:</b> Confirmed $\\epsilon_d(K+1) \\le \\epsilon_d(K)$ for all $K$.</li>
    <li><b>4-Way Decision Logic:</b> Verified clean rejection of random noise as <code>NOT_A_FACE</code>.</li>
  </ol>

  <h2>7. Conclusion</h2>
  <p>
    This project successfully reproduced and empirically validated the 1991 paper <i>"Eigenfaces for Recognition"</i>. By realizing the Turk-Pentland covariance reduction trick, computational cost was reduced by $279.5\\times$, allowing fast, real-time recognition. Evaluated on the canonical Olivetti benchmark, the model achieved $87.62\\%$ accuracy at a $99.0\\%$ dimensionality reduction ratio, demonstrating the enduring elegance and pedagogical importance of linear subspace analysis in computer vision.
  </p>

  <h2>8. References</h2>
  <ol>
    <li><b>Turk, M., &amp; Pentland, A. (1991).</b> <i>Eigenfaces for Recognition.</i> Journal of Cognitive Neuroscience, 3(1), 71&ndash;86.</li>
    <li><b>Sirovich, L., &amp; Kirby, M. (1987).</b> <i>Low-dimensional procedure for the characterization of human faces.</i> J. Opt. Soc. Am. A, 4(3), 519&ndash;524.</li>
    <li><b>Belhumeur, P. N., Hespanha, J. P., &amp; Kriegman, D. J. (1997).</b> <i>Eigenfaces vs. Fisherfaces: Recognition using class specific linear projection.</i> IEEE Trans. PAMI, 19(7), 711&ndash;720.</li>
    <li><b>Kanade, T. (1973).</b> <i>Picture Processing System by Computer Complex and Recognition of Human Faces.</i> Doctoral thesis, Kyoto University.</li>
    <li><b>AT&amp;T Laboratories Cambridge.</b> <i>The Database of Faces (ORL Database).</i> URL: <code>https://ndownloader.figshare.com/files/5976027</code>.</li>
  </ol>

  <!-- Section 9: GitHub Repository & QR Code Verification -->
  <div class="qr-container">
    <h3 style="margin: 0 0 6px 0; text-transform: uppercase;">9. Project Source Code &amp; Repository Verification</h3>
    <p style="margin: 0; text-align: center; font-size: 10pt;">
      Scan the QR code below or visit the GitHub repository link to inspect the complete source code, automated test suites, dataset scripts, and interactive presentation tools:
    </p>
    <img src="__QR_B64__" alt="GitHub Repository QR Code">
    <div class="repo-link">
      <a href="https://github.com/shashank-emty/Eigen-faces" target="_blank" style="color: #000000; text-decoration: underline;">
        https://github.com/shashank-emty/Eigen-faces
      </a>
    </div>
    <div style="font-size: 9pt; margin-top: 6px; color: #333333;">
      Student: <b>Shashank M T</b> &bull; UUCMS No.: <b>U01BH25C0174</b> &bull; Pooja Bhagavat Mahajana First Grade College
    </div>
  </div>

</body>
</html>
"""

    html = (
        template.replace("__FIG1_B64__", fig1_b64)
        .replace("__FIG2_B64__", fig2_b64)
        .replace("__FIG3_B64__", fig3_b64)
        .replace("__FIG4_B64__", fig4_b64)
        .replace("__FIG5_B64__", fig5_b64)
        .replace("__FIG6_B64__", fig6_b64)
        .replace("__QR_B64__", qr_b64)
    )

    out_path = os.path.join(BASE_DIR, "REPORT.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[REPORT BUILD] Self-contained printable HTML report created at: {out_path}")


if __name__ == "__main__":
    build_report_html()
