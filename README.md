# Eigenfaces for Recognition (Turk & Pentland, 1991) — Python Implementation

A mathematically rigorous, from-scratch Python implementation of the seminal paper:
> **Matthew Turk and Alex Pentland (1991)**. *"Eigenfaces for Recognition"*. **Journal of Cognitive Neuroscience**, Vol. 3, No. 1, pp. 71–86.

Designed specifically for individual student project demonstration, oral viva defense, and classroom presentation.

---

## 🌟 Key Features

1. **Pure Linear Algebra Implementation**:
   - Zero reliance on `sklearn.decomposition.PCA` or black-box libraries for the core model.
   - Exact implementation of the **Turk-Pentland Covariance Reduction Trick** ($L = A^T A$ instead of $C = A A^T$).
2. **Complete 4-Way Decision Rule (Section 3.2)**:
   - Calculates both **Distance from Face Space (DFFS)** $\epsilon_d$ and **Distance in Face Space (DIFS)** $\epsilon_c$.
   - Rejects non-face images (noise, textures, objects).
   - Identifies known enrolled individuals.
   - Detects unseen individuals as unknown human faces.
3. **Dual Demonstration Interfaces**:
   - **Terminal Console Script (`demo.py`)**: Runs an automated pipeline with formatted ASCII telemetry, benchmark tables, and plot generation.
   - **Interactive Web Presentation Dashboard (`app.py`)**: A modern local web app featuring a live $K$-slider for face reconstruction, interactive probe selection, real-time gauges, and embedded slide notes.
4. **Publication-Grade Visualizations (`results/`)**:
   - Eigenfaces Gallery (Mean Face $\Psi$ and top 15 eigenfaces $u_k$).
   - Scree Plot & Cumulative Variance Explained curve.
   - Face Reconstruction convergence across $K \in [2, 5, 10, 20, 40]$.
   - 2D Decision Space Geometry with quadrant boundaries.
   - Perturbation & Robustness Analysis under Gaussian noise and occlusions (sunglasses/mask).
   - Accuracy vs. $K$ dimensional tradeoff curve.

## ⚡ Super Simple Quickstart

The entire project is structured to be extremely simple and self-contained:
1. **Main Code**: [`main.py`](file:///Users/emty/balls/eigen_faces/main.py) contains all algorithms, PCA calculations, Turk-Pentland trick, and test cases in a single, clean file.
2. **Dataset**: `data/olivetti_py3.pkz` is bundled locally inside the project (400 face photos, 40 subjects, 64x64).
3. **Interactive Showcase**: [`index.html`](file:///Users/emty/balls/eigen_faces/index.html) can be opened in any web browser to showcase the code, algorithms, and visual graphs.

### Run in Terminal:
```bash
python3 main.py
```

### View Project & Code Showcase:
Simply double-click [`index.html`](file:///Users/emty/balls/eigen_faces/index.html) or open it in your browser!

---

## 📁 Simple Project Structure

```
eigen_faces/
├── main.py                   # ⭐ Main code with all algorithms (Turk & Pentland 1991)
├── index.html                # ⭐ Standalone HTML showcase for code, math & graphs
├── data/
│   └── olivetti_py3.pkz      # ⭐ Bundled AT&T / Olivetti Face Dataset (offline)
├── results/
│   └── bw/                   # High-contrast figures (Eigenfaces gallery, scree plot, etc.)
├── REPORT.html               # Comprehensive print-ready university report (B&W compatible)
├── REPORT.md                 # Markdown version of full university report
└── requirements.txt          # Python dependencies (numpy, scipy, scikit-learn, joblib)
```

---

## 🚀 Quickstart & Execution

### 1. Activate Environment
```bash
cd /Users/emty/balls/eigen_faces
source .venv/bin/activate
```

### 2. Run Automated Console Demo
```bash
python demo.py
```
This script will execute all technical steps, print benchmark tables to the console, and generate all figures in `results/`.

### 3. Launch Interactive Web Presentation Dashboard
```bash
python app.py
```
Then open **[http://localhost:5050](http://localhost:5050)** in your browser.

### 4. Run Unit Tests (Mathematical Verification)
```bash
python -m unittest tests/test_eigenfaces.py
```
Verifies:
- Orthonormality of eigenfaces ($U^T U = I$)
- Exact mathematical equivalence between $A^T A$ and $A A^T$
- Monotonic decrease of reconstruction error with increasing $K$
- Face vs. non-face rejection behavior

---

## 📐 Mathematical Formulation

### 1. Centering & The Covariance Dilemma
Given $M$ training images flattened into column vectors $\Gamma_i \in \mathbb{R}^D$ where $D = N \times N$:
$$\Psi = \frac{1}{M}\sum_{i=1}^M \Gamma_i, \qquad \Phi_i = \Gamma_i - \Psi$$
$$A = [\Phi_1, \Phi_2, \dots, \Phi_M] \in \mathbb{R}^{D \times M}$$

The sample covariance matrix is $C = \frac{1}{M} A A^T \in \mathbb{R}^{D \times D}$.  
For $64 \times 64$ images, $D = 4096$, so $C$ contains over $16.7$ million elements.

### 2. Turk-Pentland Dimensionality Reduction Trick
Instead of decomposing $C$, compute the eigenvectors $v_k$ of the $M \times M$ matrix $L = A^T A$:
$$A^T A v_k = \mu_k v_k$$
Multiply both sides by $A$:
$$A (A^T A v_k) = \mu_k (A v_k) \implies (A A^T)(A v_k) = \mu_k (A v_k)$$
Hence, $u_k = A v_k$ are the true eigenvectors of $C = A A^T$.  
Normalizing to unit length:
$$u_k = \frac{A v_k}{\|A v_k\|_2}, \qquad k = 1, \dots, K$$

### 3. Face Space Projection & Reconstruction
$$\Omega = U^T (\Gamma - \Psi) \in \mathbb{R}^K, \qquad \hat{\Gamma} = \Psi + U \Omega = \Psi + \sum_{k=1}^K \omega_k u_k$$

### 4. 4-Way Decision Rule
- **Distance from Face Space (DFFS)**: $\epsilon_d = \|\Gamma - \hat{\Gamma}\|_2$
- **Distance in Face Space (DIFS)**: $\epsilon_c = \min_k \|\Omega - \Omega_k\|_2$

$$\begin{cases}
\epsilon_d \ge \theta_f & \implies \textbf{Not a Face (Reject)} \\
\epsilon_d < \theta_f \land \epsilon_c < \theta_c & \implies \textbf{Known Face } c^* = \arg\min_k \epsilon_k \\
\epsilon_d < \theta_f \land \epsilon_c \ge \theta_c & \implies \textbf{Unknown Face (Enrollment candidate)}
\end{cases}$$

---

## 📊 Empirical Results (Olivetti / AT&T Faces Benchmark)

- **Dataset**: 40 subjects, 10 images each (64 $\times$ 64 pixels).
- **Partition**: 35 enrolled subjects (7 train, 3 test each = 245 train, 105 test), 5 unseen subjects (50 probe images for unknown face testing).
- **Dimensionality Reduction**: $4096 \to 40$ dimensions (**99.0% compression ratio**).
- **Cumulative Variance at $K=40$**: **86.33%** (95% reached at $K=95$).
- **Top-1 Recognition Accuracy vs $K$**:
  - $K = 2$: 18.10%
  - $K = 10$: 74.29%
  - $K = 20$: 81.90%
  - $K = 40$: **85.71%**
  - $K = 50$: **87.62%**
- **Face Detection Acceptance Rate**: 100.0%
- **Non-Face Rejection Rate**: >70.0% - 90.0%

---

## 🎓 Preparing for Your Presentation & Viva

See the detailed **[PRESENTATION_GUIDE.md](file:///Users/emty/balls/eigen_faces/PRESENTATION_GUIDE.md)** for:
- Slide-by-slide 10-minute script.
- Answers to typical examiner questions (e.g., *Why $A^T A$ instead of $A A^T$?*, *Eigenfaces vs. Fisherfaces*, *Why do eigenfaces look ghostly?*).
- Mathematical proof derivations.

### 📽️ Presentation Slides (2 Ready-to-Use Formats)

1. **Widescreen PowerPoint Presentation (`EigenFaces_Presentation.pptx`)**:
   - 13 comprehensive, publication-quality 16:9 slides.
   - Includes full presenter and institutional metadata (Shashank M T, UUCMS No. U01BH25C0174, BCA(AI), Pooja Bhagavat Mahajana First Grade College, Course Lecturer Ragunandan B).
   - High-resolution figures embedded directly from `results/`.
   - Regenerate anytime with:
     ```bash
     python generate_pptx.py
     ```
   - Open on Mac:
     ```bash
     open EigenFaces_Presentation.pptx
     ```

2. **Interactive Browser Slide Deck (`slides.html`)**:
   - Open instantly in any browser:
     ```bash
     open slides.html
     ```
   - Keyboard arrows (◄ / ►) or Space to advance.
   - Press **F** for Fullscreen mode.
   - Press **N** to show/hide Speaker Notes & Viva Defense talking points.
   - Press **P** or click the print icon to export directly as a 16:9 PDF.
   - Live rendered KaTeX formulas ($L = A^T A$, $\epsilon_d$, $\epsilon_c$).
