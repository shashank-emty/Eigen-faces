# Presentation & Viva Defense Guide: Eigen Faces (Turk & Pentland, 1991)

> **Presenter**: **Shashank M T** | **UUCMS No.**: **U01BH25C0174**  
> **Course Lecturer**: **Ragunandan B** (*Guest Lecturer – Introduction to Machine Learning*)  
> **Course**: **BCA(AI) – 3rd Semester, 2nd Year** | **Subject**: **Machine Learning**  
> **Institution**: **Pooja Bhagavat Mahajana First Grade College**  
> **Submission Date**: **October 15, 2026**  
> **GitHub Repository**: [https://github.com/shashank-emty/Eigen-faces](https://github.com/shashank-emty/Eigen-faces)  
> **Format**: Individual student presentation (for one-on-one viva and one-to-many committee evaluation).

---

## 1. Executive Summary for Evaluators

This project provides an exact, from-scratch implementation of the landmark 1991 paper by **Matthew Turk and Alex Pentland** (*Journal of Cognitive Neuroscience*, Vol. 3, No. 1, pp. 71–86).

### Key Architectural Strengths:
1. **Mathematical Fidelity**: No black-box machine learning shortcuts. Principal Component Analysis (PCA) and the **Turk-Pentland Dimensionality Reduction Trick** ($L = A^T A$) are implemented directly using linear algebra operations in NumPy.
2. **Complete 4-Way Decision Rule**: Unlike naive nearest-neighbor implementations that only classify known faces, this system implements the complete 2-threshold decision framework from Section 3.2:
   - **Case 1: Not a Face** ($\epsilon_d \ge \theta_f$) — Reject non-face inputs using Distance from Face Space.
   - **Case 2: Known Face** ($\epsilon_d < \theta_f$ and $\epsilon_c < \theta_c$) — Correctly recognize enrolled subjects.
   - **Case 3: Unknown Face** ($\epsilon_d < \theta_f$ and $\epsilon_c \ge \theta_c$) — Detect unseen individuals as human faces, enabling enrollment.
3. **Dual Demonstration Interfaces**:
   - **Console / Script Demo (`demo.py`)**: Runs an end-to-end benchmark with formatted ASCII telemetry and generates publication-grade figures in `results/`.
   - **Interactive Web App (`app.py`)**: A live GUI dashboard with an interactive reconstruction slider ($K \in [1, 50]$), probe selector, metric gauges, and embedded theory slides.

---

## 2. 10-Minute Slide-by-Slide Presentation Structure

| Slide / Time | Topic | Key Talking Points | Visual to Show |
| :--- | :--- | :--- | :--- |
| **Slide 1 (0:00 - 1:00)** | **Problem & Motivation** | • Traditional 1980s methods used geometric features (distance between eyes, nose bridge length), which were fragile and difficult to extract.<br>• Turk & Pentland proposed a *holistic information-theory approach* treating faces as 2D patterns. | Problem diagram / face grid |
| **Slide 2 (1:00 - 2:30)** | **Mathematical Subspace & Mean Face** | • Images of size $N \times N$ form vectors $\Gamma \in \mathbb{R}^D$ where $D = N^2$ ($64 \times 64 = 4096$).<br>• Average Face $\Psi = \frac{1}{M}\sum \Gamma_i$ captures the shared baseline template.<br>• Mean-centered matrix $A = [\Phi_1, \dots, \Phi_M]$ centers the distribution. | Mean Face $\Psi$ thumbnail |
| **Slide 3 (2:30 - 4:30)** | **The Turk-Pentland Covariance Trick** | • $C = \frac{1}{M} A A^T$ is $D \times D$ ($4096 \times 4096 = 16.7\text{M}$ entries) &rarr; Intractable!<br>• Compute surrogate $L = A^T A$ of size $M \times M$ ($245 \times 245 = 60,025$ entries).<br>• Proof: $A (A^T A v_k) = \mu_k (A v_k) \implies (A A^T)(A v_k) = \mu_k (A v_k)$.<br>• Eigenfaces are $u_k = \frac{A v_k}{\|A v_k\|_2}$. | Mathematical proof & Scree Plot |
| **Slide 4 (4:30 - 6:00)** | **Face Projection & Reconstruction** | • Project onto $K$ dimensions: $\Omega = U^T (\Gamma - \Psi)$.<br>• Reconstruct: $\hat{\Gamma} = \Psi + U \Omega$.<br>• Show that as $K$ increases from 2 to 40, facial features (eyes, nose, mouth) emerge sequentially. | Reconstruction at $K=2, 5, 10, 20, 40$ |
| **Slide 5 (6:00 - 7:30)** | **The 4-Way Decision Rule** | • Distance from Face Space (DFFS): $\epsilon_d = \|\Gamma - \hat{\Gamma}\|_2$.<br>• Distance in Face Space (DIFS): $\epsilon_c = \min_k \|\Omega - \Omega_k\|_2$.<br>• Show the 2D decision quadrant plot with thresholds $\theta_f$ and $\theta_c$. | Decision Space Geometry plot |
| **Slide 6 (7:30 - 8:45)** | **Live Demonstration** | • Run `demo.py` or demonstrate live on `http://localhost:5050`.<br>• Test: Known Face probe &rarr; Recognized.<br>• Test: Unseen individual &rarr; Unknown Face.<br>• Test: Checkerboard / Noise &rarr; Not a Face. | Live Web Dashboard |
| **Slide 7 (8:45 - 10:00)** | **Benchmarks & Conclusion** | • Accuracy reaches >87% with just 30–50 eigenfaces (98.8% dimensional compression).<br>• Non-face rejection rate: >70–90%.<br>• Discuss limitations: lighting sensitivity, solved later by Fisherfaces (LDA) and Deep CNNs. | Accuracy vs $K$ curve |

---

## 3. How to Demonstrate Live During Presentation

### Option A: Terminal Console Demo (Fast, 1-Click)
Run the automated end-to-end demonstration script:
```bash
source .venv/bin/activate
python demo.py
```
**What the audience will see**:
- Clean ASCII steps detailing image dimensionality ($D=4096$, $M=245$).
- Covariance matrix reduction factor ($279.5\times$ smaller).
- Step-by-step test cases for Enrolled Subject, Unenrolled Subject, and Non-Face Object.
- Benchmark accuracy table vs number of components $K$.
- Saved publication figures in `results/`.

### Option B: Interactive Web Dashboard (Ideal for Live Q&A / Projector)
Start the presentation server:
```bash
source .venv/bin/activate
python app.py
```
Open **`http://localhost:5050`** in any web browser.

**Demonstration Interactions**:
1. **Live Classification**: Click on the thumbnail probes on the left:
   - Select an **Enrolled Subject** &rarr; Shows green banner: `RECOGNIZED: KNOWN SUBJECT #X`, displays matched gallery photo.
   - Select an **Unenrolled Subject** &rarr; Shows blue banner: `DETECTED: UNKNOWN HUMAN FACE`, explaining that $\epsilon_d < \theta_f$ confirmed it is a human face, while $\epsilon_c \ge \theta_c$ verified it is not in the enrolled gallery.
   - Select a **Non-Face Pattern** (e.g. Checkerboard or Random Noise) &rarr; Shows red banner: `REJECTED: NOT A HUMAN FACE`, pointing to $\epsilon_d \ge \theta_f$.
2. **Reconstruction Slider**: Go to the **Face Reconstruction Lab** tab. Drag the $K$ slider from 1 up to 50 to visually demonstrate how eigenfaces progressively encode coarse lighting $\to$ face shape $\to$ fine facial details.
3. **Eigenfaces Gallery**: Show the 16 ghostly eigenfaces and explain how the earliest components capture dominant illumination and broad contours.

---

## 4. Viva Defense & Examination Q&A (Preparing for Difficult Questions)

### Q1: Why can we compute the eigenvectors of $A^T A$ instead of $A A^T$?
> **Answer**:
> Let $A$ be a $D \times M$ matrix where $D = 4096$ pixels and $M = 245$ images.
> The full covariance matrix $C = \frac{1}{M} A A^T$ is of size $D \times D = 4096 \times 4096$ ($16,777,216$ elements).
> Since $M \ll D$, the maximum rank of $A A^T$ is at most $M - 1$. This means at least $D - M + 1$ eigenvalues are zero.
> Consider the surrogate matrix $L = A^T A$, which is only $M \times M$ ($245 \times 245 = 60,025$ elements).
> Let $v_k$ be an eigenvector of $L$ with eigenvalue $\mu_k$:
> $$A^T A v_k = \mu_k v_k$$
> Multiplying both sides from the left by $A$:
> $$A (A^T A v_k) = A (\mu_k v_k) \implies (A A^T)(A v_k) = \mu_k (A v_k)$$
> Notice that $(A A^T)(u_k) = \mu_k (u_k)$ where $u_k = A v_k$.
> Thus, $A v_k$ is an exact eigenvector of the full covariance matrix $C = A A^T$! We simply normalize $u_k$ to unit length: $u_k = \frac{A v_k}{\|A v_k\|_2}$.

---

### Q2: Why do eigenfaces look like "ghostly" faces?
> **Answer**:
> Because eigenfaces are linear combinations of all faces in the training set:
> $$u_k = \sum_{i=1}^M v_{ki} \Phi_i$$
> Since each $\Phi_i$ is a centered face image, adding and subtracting them produces an image that retains basic facial geometry (eyes, nose, mouth regions) with high and low intensity variations representing facial features and lighting gradients.

---

### Q3: How are the thresholds $\theta_f$ and $\theta_c$ determined?
> **Answer**:
> In Section 3.2 and Section 4 of Turk & Pentland (1991):
> 1. **$\theta_f$ (Face Space Threshold)**: Evaluates the reconstruction residual $\epsilon_d = \|\Gamma - \hat{\Gamma}\|_2$. We measure the distribution of reconstruction errors across training face images ($\mu_{\text{dffs}}, \sigma_{\text{dffs}}$). The threshold is set with a statistical safety margin above the maximum training error ($\theta_f = \max(\epsilon_d) + c \cdot \sigma$) to ensure valid face variations are accepted while non-face patterns ($\epsilon_d \gg 15$) are rejected.
> 2. **$\theta_c$ (Classification Threshold)**: Evaluates the distance in face space between face weight vectors and class centroids. We compute the intra-class dispersion (distance between images of the same individual and their class centroid). $\theta_c$ is set above the typical intra-class distance. If an input probe's closest enrolled centroid exceeds $\theta_c$, the person is deemed an unknown/unseen individual.

---

### Q4: What is the difference between Distance From Face Space (DFFS) and Distance In Face Space (DIFS)?
> **Answer**:
> - **DFFS ($\epsilon_d$)**: The Euclidean distance between the input image and its orthogonal projection onto the $K$-dimensional face subspace ($\|\Gamma - \hat{\Gamma}\|_2$). It measures *whether the image belongs to the face manifold at all* (Face Detection).
> - **DIFS ($\epsilon_c$)**: The Euclidean distance within the $K$-dimensional subspace between the weight vector $\Omega$ and the closest enrolled class centroid $\Omega_k$. It measures *which known person the face resembles* (Face Identification).

---

### Q5: What are the main weaknesses of Eigenfaces, and how did subsequent algorithms improve upon them?
> **Answer**:
> 1. **PCA is Unsupervised**: PCA finds directions that maximize *total* variance across all images. However, in face recognition, variation caused by changes in lighting or shadows is often much larger than variation between different people's facial shapes.
> 2. **Belhumeur et al. (1997) introduced Fisherfaces (LDA)**: Linear Discriminant Analysis finds a subspace that maximizes *between-class scatter* while minimizing *within-class scatter*, making it significantly more robust to illumination changes.
> 3. **Nonlinear Manifold**: Face appearance under extreme angles or expressions forms a highly nonlinear manifold. Modern Convolutional Neural Networks (CNNs) and deep metric learning (e.g. ArcFace, FaceNet) replace linear PCA projections with deep nonlinear embedding functions.

---

## 5. Summary of Mathematical Formulas

| Concept | Equation |
| :--- | :--- |
| **Face Vector** | $\Gamma_i \in \mathbb{R}^D, \quad D = H \times W$ |
| **Mean Face** | $\Psi = \frac{1}{M}\sum_{i=1}^M \Gamma_i$ |
| **Mean-Centered Vector** | $\Phi_i = \Gamma_i - \Psi$ |
| **Data Matrix** | $A = [\Phi_1, \Phi_2, \dots, \Phi_M] \in \mathbb{R}^{D \times M}$ |
| **Surrogate Covariance** | $L = A^T A \in \mathbb{R}^{M \times M}$ |
| **Surrogate Eigendecomposition** | $L v_k = \mu_k v_k$ |
| **Eigenfaces** | $u_k = \frac{A v_k}{\|A v_k\|_2}, \quad k = 1, \dots, K$ |
| **Projection / Weights** | $\Omega = U^T (\Gamma - \Psi) \in \mathbb{R}^K$ |
| **Reconstruction** | $\hat{\Gamma} = \Psi + U \Omega = \Psi + \sum_{k=1}^K \omega_k u_k$ |
| **Distance from Face Space (DFFS)** | $\epsilon_d = \|\Gamma - \hat{\Gamma}\|_2$ |
| **Distance in Face Space (DIFS)** | $\epsilon_c = \min_k \|\Omega - \Omega_k\|_2$ |
| **Rejection Rule** | $\epsilon_d \ge \theta_f \implies \text{Not a Face}$ |
| **Recognition Rule** | $\epsilon_d < \theta_f \land \epsilon_c < \theta_c \implies \text{Known Face } c^*$ |
| **Discovery Rule** | $\epsilon_d < \theta_f \land \epsilon_c \ge \theta_c \implies \text{Unknown Face}$ |
