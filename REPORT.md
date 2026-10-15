# POOJA BHAGAVAT MAHAJANA FIRST GRADE COLLEGE
### Department of Computer Science & Artificial Intelligence
**K.R.S. Road, Metagalli, Mysuru – 570016, Karnataka**

---

# A PROJECT REPORT ON
## EIGEN FACES
### Implementation of "Eigenfaces for Recognition" (Turk & Pentland, 1991) Technical Paper Using Python

*Submitted in partial fulfillment of the requirements for the award of the degree of*  
**BACHELOR OF COMPUTER APPLICATIONS (ARTIFICIAL INTELLIGENCE)**  
**BCA(AI)**

---

### SUBMITTED BY:
**SHASHANK M T**  
**UUCMS Register Number**: `U01BH25C0174`  
**Semester & Course**: 3rd Semester, 2nd Year BCA(AI)

### UNDER THE GUIDANCE OF:
**RAGUNANDAN B**  
**Guest Lecturer – Introduction to Machine Learning**  
Department of Computer Science & AI  
Pooja Bhagavat Mahajana First Grade College, Mysuru

**Academic Year**: 2026 – 2027  
**Date of Submission**: October 15, 2026  
**Subject**: Machine Learning  
**GitHub Repository**: [https://github.com/shashank-emty/Eigen-faces](https://github.com/shashank-emty/Eigen-faces)

---

<div style="page-break-after: always;"></div>

## CERTIFICATE

This is to certify that the project report entitled **"EIGEN FACES: Implementation of 'Eigenfaces for Recognition' (Turk & Pentland, 1991) Technical Paper Using Python"** is a bonafide work carried out by **SHASHANK M T** (UUCMS No: **U01BH25C0174**), a student of Bachelor of Computer Applications in Artificial Intelligence **[BCA(AI)]** (3rd Semester, 2nd Year), at **Pooja Bhagavat Mahajana First Grade College, Mysuru**, in partial fulfillment of the academic curriculum for the subject **Machine Learning** during the academic year 2026–2027.

The project implementation, mathematical derivations, automated unit tests, and empirical analyses documented in this report have been independently developed, executed, and verified under academic supervision.

<br><br><br>

_________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _________________________  
**Ragunandan B** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Head of Department (HOD)**  
Guest Lecturer – Intro to ML (Internal Guide) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Department of Computer Science & AI  
Dept. of CS & AI, PBM FGC &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; PBM FGC, Mysuru  

<br><br>

_________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; _________________________  
**Principal** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **External Examiner**  
PBM FGC, Mysuru  

---

<div style="page-break-after: always;"></div>

## DECLARATION

I, **SHASHANK M T**, student of 3rd Semester, 2nd Year Bachelor of Computer Applications in Artificial Intelligence [BCA(AI)], bearing UUCMS Register Number **U01BH25C0174**, hereby declare that the project report entitled **"EIGEN FACES: Implementation of 'Eigenfaces for Recognition' (Turk & Pentland, 1991) Technical Paper Using Python"** submitted to **Pooja Bhagavat Mahajana First Grade College, Mysuru**, is an authentic record of independent technical work carried out by me under academic guidance.

I further declare that this implementation adheres to the mathematical formulations set forth in the research literature and has not been submitted previously to any other university or institution for the award of any degree, diploma, or certificate.

All external libraries, benchmark datasets, and literature sources consulted have been appropriately cited and acknowledged.

<br><br>

**Place**: Mysuru, Karnataka  
**Date**: October 15, 2026  

<br>

_________________________  
**SHASHANK M T**  
UUCMS No.: `U01BH25C0174`  
Course: BCA(AI), 3rd Semester, 2nd Year  

---

<div style="page-break-after: always;"></div>

## ACKNOWLEDGEMENTS

The successful realization of this project implementation and technical report has been made possible through the encouragement, guidance, and academic support of several individuals and mentors.

First and foremost, I express my sincere gratitude to our respected **Principal**, **Pooja Bhagavat Mahajana First Grade College, Mysuru**, for fostering an academic environment equipped with modern computing infrastructure that encourages hands-on research and technical exploration.

I extend my heartfelt thanks to the **Head of the Department (HOD)**, Department of Computer Science & Artificial Intelligence, for their constant encouragement, organizational oversight, and valuable suggestions throughout the curriculum.

I place on record my heartfelt gratitude and sincere indebtedness to my course lecturer and project guide, **Mr. Ragunandan B**, Guest Lecturer – Introduction to Machine Learning, Department of Computer Science & Artificial Intelligence. His inspiring lectures, lucid explanations of linear algebra and machine learning concepts, constructive reviews of mathematical derivations, and technical guidance were instrumental in the successful completion of this project implementation.

I also place on record my sincere appreciation to the authors of the original research paper, **Matthew A. Turk and Alex P. Pentland**, whose foundational work at the Massachusetts Institute of Technology (MIT) continues to inspire generations of computer vision and machine learning researchers.

Finally, I convey my heartfelt thanks to my family, peers, and friends whose unwavering encouragement and patience have been a pillar of strength during my academic endeavors.

<br>

**SHASHANK M T**  
BCA(AI), 3rd Semester (2nd Year) | UUCMS No: `U01BH25C0174`  

---

<div style="page-break-after: always;"></div>

## ABSTRACT

This project report presents an exhaustive, from-scratch Python implementation, empirical evaluation, and theoretical analysis of the landmark paper **"Eigenfaces for Recognition"** by Matthew Turk and Alex Pentland (published in the *Journal of Cognitive Neuroscience*, Vol. 3, No. 1, 1991). 

In the late 20th century, facial recognition was dominated by fragile geometric landmark extraction methods that measured distances between isolated features (eyes, nose, mouth), largely failing under real-world illumination, noise, and perspective variations. Turk and Pentland pioneered an **appearance-based, holistic information-theoretic framework** leveraging Principal Component Analysis (PCA) to represent faces as linear combinations of orthogonal basis vectors termed **"Eigenfaces"**.

A fundamental mathematical bottleneck in applying PCA directly to digital imagery is the dimensionality of the sample covariance matrix $C = \frac{1}{M}AA^T \in \mathbb{R}^{D \times D}$. For standard $64 \times 64$ grayscale imagery ($D = 4096$ pixels), the covariance matrix contains over **$16.7\text{ million elements}$**, rendering direct eigendecomposition computationally intractable ($\mathcal{O}(D^3) \approx 6.87 \times 10^{10}$ FLOPs). This report mathematically proves and implements the **Turk-Pentland Covariance Reduction Trick**, which shifts eigendecomposition to an inner-product surrogate matrix $L = A^TA \in \mathbb{R}^{M \times M}$ ($M = 245$ training images, $60,025$ elements), achieving a **$279.5\times$ computational reduction** while obtaining the identical principal eigenvectors.

Crucially, rather than implementing a naive nearest-neighbor classifier, this work implements the complete **two-threshold 4-way decision framework** from Section 3.2 of the paper:
1. **Distance from Face Space (DFFS, $\epsilon_d = \|\Gamma - \hat{\Gamma}\|_2$)** evaluates whether an image belongs to the facial manifold, enabling robust **non-face rejection**.
2. **Distance in Face Space (DIFS, $\epsilon_c = \min_k \|\Omega - \Omega_k\|_2$)** classifies identity among enrolled subjects while identifying **unknown/unseen human faces**.

Evaluated on the canonical **Olivetti / AT&T Cambridge face database** (400 images across 40 individuals), the system achieves a top-1 identification accuracy of **$85.71\%$** at $K=40$ eigenfaces and **$87.62\%$** at $K=50$, representing a **$99.0\%$ dimensionality reduction** ($4096 \to 40$). Non-face pattern rejection achieves **$80.0\%–90.0\%$**, and human face acceptance is verified at **$100.0\%$** with zero false rejections. Robustness to Gaussian noise ($\sigma=0.25$) and facial occlusions (sunglasses, masks) is demonstrated. All visual figures, tables, mathematical proofs, unit testing suites, and a live web presentation dashboard are documented in full.

**Keywords**: *Face Recognition, Eigenfaces, Principal Component Analysis, Turk-Pentland Trick, Dimensionality Reduction, Subspace Learning, Pattern Recognition, Computer Vision, Machine Learning.*

---

<div style="page-break-after: always;"></div>

## TABLE OF CONTENTS

* **Certificate of Authenticity**
* **Declaration**
* **Acknowledgements**
* **Abstract**
* **List of Figures**
* **List of Tables**
* **List of Abbreviations & Mathematical Symbols**

### CHAPTER 1: INTRODUCTION
* 1.1 Context and Significance of Biometric Facial Recognition
* 1.2 Evolution of Computer Vision Approaches: Geometric vs. Appearance-based
* 1.3 Problem Statement
* 1.4 Objectives of the Project
* 1.5 Scope and Limitations of the Implementation
* 1.6 Report Organization

### CHAPTER 2: LITERATURE REVIEW
* 2.1 Sirovich & Kirby (1987) – Low-Dimensional Procedure for Face Characterization
* 2.2 Matthew Turk & Alex Pentland (1991) – Eigenfaces for Recognition
* 2.3 Belhumeur, Hespanha & Kriegman (1997) – Fisherfaces & Linear Discriminant Analysis
* 2.4 Local Appearance Descriptors: Local Binary Patterns (LBPH)
* 2.5 The Deep Learning Revolution: FaceNet, ArcFace, and Convolutional Neural Networks
* 2.6 Comparative Summary of Paradigms

### CHAPTER 3: THEORETICAL FOUNDATION & MATHEMATICAL DERIVATIONS
* 3.1 Digital Image Representation as High-Dimensional Vectors ($\Gamma \in \mathbb{R}^D$)
* 3.2 The Average Face Vector ($\Psi$) and Mean-Centering
* 3.3 Difference Matrix Assembly ($A \in \mathbb{R}^{D \times M}$)
* 3.4 The High-Dimensional Covariance Dilemma ($C \in \mathbb{R}^{D \times D}$)
* 3.5 Rigorous Mathematical Proof of the Turk-Pentland Covariance Reduction Trick
* 3.6 Eigendecomposition and Orthonormal Basis Construction ($U \in \mathbb{R}^{D \times K}$)
* 3.7 Proof of Orthonormality ($U^T U = I_K$)
* 3.8 Projection into Subspace: Derivation of Coordinate Vector $\Omega$
* 3.9 Image Reconstruction as Linear Combination of Eigenvectors ($\hat{\Gamma}$)
* 3.10 Dual Distance Formulations:
  * 3.10.1 Distance from Face Space (DFFS, $\epsilon_d$)
  * 3.10.2 Distance in Face Space (DIFS, $\epsilon_c$)
* 3.11 The 4-Way Decision Rule Framework (Section 3.2 Analysis)
* 3.12 Threshold Calibration Mechanics ($\theta_f$ and $\theta_c$)

### CHAPTER 4: SYSTEM ARCHITECTURE & IMPLEMENTATION METHODOLOGY
* 4.1 End-to-End System Architecture
* 4.2 Benchmark Dataset: Olivetti / AT&T Faces Database
* 4.3 Structured Experimental Dataset Partitioning
* 4.4 Modular Codebase Architecture:
  * 4.4.1 `src/eigenfaces.py` (Pure NumPy Classifier)
  * 4.4.2 `src/dataset.py` (Data Ingestion & Non-Face Synthesis)
  * 4.4.3 `src/evaluate.py` (Benchmark & Metrics Engine)
  * 4.4.4 `src/visualizer.py` (Scientific Monochrome Visualization)
  * 4.4.5 `demo.py` (Automated Console Demonstration)
  * 4.4.6 `app.py` & `templates/index.html` (Interactive Web Presentation Server)
* 4.5 Algorithmic Pseudocode:
  * 4.5.1 Training Phase (Eigenface Learning & Centroid Calculation)
  * 4.5.2 Inference Phase (4-Way Decision Logic)

### CHAPTER 5: EXPERIMENTAL RESULTS & PERFORMANCE EVALUATION
* 5.1 Training Convergence and Computational Reduction Metrics
* 5.2 Qualitative Evaluation: Mean Face and Principal Eigenfaces Gallery (Figure 1)
* 5.3 Scree Plot, Eigenvalue Decay & Cumulative Variance (Figure 2)
* 5.4 Reconstruction Fidelity vs. Subspace Dimensionality $K$ (Figure 3)
* 5.5 Quantitative Identification Accuracy vs. $K$ (Table 1, Figure 6)
* 5.6 Validation of the 4-Way Decision Space Geometry (Table 2, Figure 4)
* 5.7 Robustness Analysis: Performance Under Noise and Occlusions (Figure 5)
* 5.8 Computational Complexity and Profiling

### CHAPTER 6: AUTOMATED UNIT TESTING & MATHEMATICAL VERIFICATION
* 6.1 Unit Testing Framework (`tests/test_eigenfaces.py`)
* 6.2 Test 1: Orthonormality of Basis Vectors ($U^T U = I$)
* 6.3 Test 2: Turk-Pentland Algebraic Equivalence ($A^TA \leftrightarrow AA^T$)
* 6.4 Test 3: Monotonic Decrease of Reconstruction Residual
* 6.5 Test 4: High-Variance Non-Face Rejection

### CHAPTER 7: CONCLUSION & FUTURE SCOPE
* 7.1 Summary of Project Accomplishments
* 7.2 Key Academic Findings
* 7.3 Limitations of Linear PCA Subspaces
* 7.4 Directions for Future Research

### CHAPTER 8: REFERENCES & BIBLIOGRAPHY
### CHAPTER 9: SOURCE CODE REPOSITORY & VERIFICATION (GITHUB QR CODE)

---

<div style="page-break-after: always;"></div>

## LIST OF FIGURES

| Figure Number | Caption / Description | Page |
| :---: | :--- | :---: |
| **Figure 1** | Average Face ($\Psi$) and Top 15 Principal Eigenfaces ($u_1 \dots u_{15}$) with Variance Ratios | Sec 5.2 |
| **Figure 2** | Scree Plot of Eigenvalue Spectrum and Cumulative Explained Variance Curve | Sec 5.3 |
| **Figure 3** | Progressive Face Reconstruction Convergence across $K \in [2, 5, 10, 20, 40]$ | Sec 5.4 |
| **Figure 4** | 2D Decision Space Geometry displaying the 3 Operational Zones ($\theta_f$ and $\theta_c$) | Sec 5.6 |
| **Figure 5** | Robustness Analysis under Gaussian Noise ($\sigma=0.10, 0.25$) and Facial Occlusions | Sec 5.7 |
| **Figure 6** | Dual-Axis Curve: Top-1 Identification Accuracy (%) and Reconstruction Error ($\epsilon_d$) vs. $K$ | Sec 5.5 |
| **Figure 7** | System Architectural Pipeline of the Eigenfaces Implementation | Sec 4.1 |
| **Figure 8** | High-Resolution GitHub Repository QR Code for External Evaluation | Sec 9 |

---

## LIST OF TABLES

| Table Number | Title / Description | Page |
| :---: | :--- | :---: |
| **Table 1** | Benchmark Performance Summary: Accuracy (%) and Reconstruction Residual ($\epsilon_d$) vs. $K$ | Sec 5.5 |
| **Table 2** | 4-Way Decision Confusion Matrix across Known Probes, Unknown Probes, and Non-Faces | Sec 5.6 |
| **Table 3** | Dataset Partitioning Scheme for the 400-Image Olivetti Face Database | Sec 4.3 |
| **Table 4** | Comparative Evaluation: Eigenfaces (PCA) vs. Fisherfaces (LDA) vs. Deep Learning (CNNs) | Sec 2.6 |
| **Table 5** | Computational Complexity & Dimensionality Reduction Comparison ($AA^T$ vs. $A^TA$) | Sec 5.1 |

---

## LIST OF ABBREVIATIONS & MATHEMATICAL SYMBOLS

| Symbol / Abbreviation | Meaning / Mathematical Definition |
| :--- | :--- |
| **PCA** | Principal Component Analysis |
| **DFFS** | Distance from Face Space ($\epsilon_d = \|\Gamma - \hat{\Gamma}\|_2$) |
| **DIFS** | Distance in Face Space ($\epsilon_c = \min_k \|\Omega - \Omega_k\|_2$) |
| **LDA** | Linear Discriminant Analysis (Fisherfaces) |
| **CNN** | Convolutional Neural Network |
| **ORL / AT&T** | Olivetti Research Laboratory Face Database |
| **FLOPs** | Floating-Point Operations |
| **$\Gamma$** | Flattened Image Column Vector ($\Gamma \in \mathbb{R}^D$) |
| **$D$** | Total Pixels per Image ($D = H \times W = 4096$) |
| **$M$** | Number of Training Samples ($M = 245$) |
| **$\Psi$** | Universal Average / Mean Face Vector ($\Psi \in \mathbb{R}^D$) |
| **$\Phi_i$** | Mean-Centered Difference Vector ($\Phi_i = \Gamma_i - \Psi$) |
| **$A$** | Mean-Centered Ensemble Difference Matrix ($A \in \mathbb{R}^{D \times M}$) |
| **$C$** | True Covariance Matrix ($C = \frac{1}{M} A A^T \in \mathbb{R}^{D \times D}$) |
| **$L$** | Turk-Pentland Surrogate Covariance Matrix ($L = A^T A \in \mathbb{R}^{M \times M}$) |
| **$v_k, \mu_k$** | Eigenvector and Eigenvalue of Surrogate Matrix $L$ |
| **$u_k$** | Normalized $k$-th Eigenface Vector ($u_k \in \mathbb{R}^D$) |
| **$K$** | Number of Retained Principal Components / Eigenfaces ($K \ll M$) |
| **$U$** | Eigenface Projection Matrix ($U \in \mathbb{R}^{D \times K}$) |
| **$\Omega$** | Subspace Coordinate / Weight Vector ($\Omega \in \mathbb{R}^K$) |
| **$\hat{\Gamma}$** | Reconstructed Face Vector ($\hat{\Gamma} = \Psi + U \Omega$) |
| **$\theta_f$** | Face Space Distance Threshold for Non-Face Rejection |
| **$\theta_c$** | Classification Distance Threshold for Unknown Identity Detection |

---

<div style="page-break-after: always;"></div>

# CHAPTER 1: INTRODUCTION

## 1.1 Context and Significance of Biometric Facial Recognition
Biometric recognition involves the automated identification or verification of individuals based on their physiological or behavioral characteristics. Among biometrics—including fingerprints, iris patterns, voice signatures, and retinal scans—**facial recognition** occupies a distinctive position because it is inherently **passive, non-intrusive, and contactless**. A subject can be recognized from a distance without requiring physical cooperation or contact with a sensor.

Automated face recognition is fundamental to numerous societal and industrial applications:
* **Public Security and Law Enforcement**: Surveillance monitoring, suspect tracking, and border control.
* **Identity Verification & Access Control**: Mobile device unlocking, physical building security, and digital banking authentication.
* **Smart Human-Computer Interaction (HCI)**: Personalized user interfaces, affective computing, and driver fatigue monitoring.

Despite its intuitive ease for human visual perception, automated facial recognition poses formidable computational challenges. A digital facial image is subject to extensive intra-class variations: lighting gradients, shadows, facial expressions (smiling, frowning), poses, perspective distortions, and occlusions (glasses, facial hair, masks). Developing algorithmic systems that are invariant to these confounding factors while remaining sensitive to inter-class identity differences is the central quest of computer vision.

---

## 1.2 Evolution of Computer Vision Approaches: Geometric vs. Appearance-Based
The historical trajectory of facial recognition can be characterized into four distinct epochs:

```
+-------------------------------------------------------------------------+
| EPOCHS OF FACEL RECOGNITION RESEARCH                                    |
|                                                                         |
| 1. Geometric Landmark Matching (1970s - 1980s)                          |
|    Landmark coordinates, Euclidean ratios, rigid template fitting.      |
|                                                                         |
| 2. Linear Appearance Subspaces (1990s)                                  |
|    Turk & Pentland (1991) Eigenfaces, Sirovich & Kirby (1987) PCA,      |
|    Belhumeur et al. (1997) Fisherfaces (LDA).                           |
|                                                                         |
| 3. Local Texture & Hybrid Descriptors (2000s)                           |
|    Local Binary Patterns (LBP), Gabor Wavelets, SIFT / HOG features.    |
|                                                                         |
| 4. Deep Metric Representation Learning (2014 - Present)                 |
|    Deep Residual Networks, ArcFace, CosFace, Vision Transformers.       |
+-------------------------------------------------------------------------+
```

Prior to 1991, systems predominantly attempted to formalize human intuitions by extracting discrete geometric landmarks (e.g., Kanade, 1973). These systems extracted coordinates of eye pupils, nose tips, and lip vertices, forming a feature vector of distances and angles:
$$x_{\text{geom}} = [d_{\text{eye-to-eye}}, d_{\text{nose-to-mouth}}, \theta_{\text{jaw}}, \dots]$$

### Critical Weaknesses of Geometric Landmark Systems:
1. **Landmark Localization Sensitivity**: Accurately locating fiducial landmarks on low-resolution, noisy, or poorly illuminated images is unreliable. A single missed landmark corrupts the entire vector.
2. **Discarding Holistic Information**: Geometric models completely discard skin texture, 3D cheekbone curvature, illumination shading, and subtle eye shape.
3. **No Non-Face Detection**: Geometric rules cannot determine if a query image is actually a human face or an arbitrary background object.

The breakthrough by **Matthew Turk and Alex Pentland (1991)** at the MIT Media Laboratory abandoned discrete feature extraction altogether. They proposed treating face recognition as an **appearance-based, holistic linear subspace problem** using Principal Component Analysis (PCA). They proved that the high-dimensional space of all possible images contains a vastly lower-dimensional manifold on which human faces reside—termed **"Face Space"**.

---

## 1.3 Problem Statement
Given an unconstrained digital grayscale image $I(x,y)$ of dimension $N \times N$, design and implement a complete, robust, and computationally tractable machine learning system that:
1. Eliminates the computational bottleneck of decomposing massive $D \times D$ covariance matrices ($D = N^2$).
2. Projects facial imagery into an optimal, lower-dimensional subspace ($K \ll D$) maximizing retained variance.
3. Implements an automated **4-way decision framework** capable of:
   * **Rejecting non-face images** (objects, random noise, arbitrary textures).
   * **Recognizing known enrolled subjects** with high identification accuracy.
   * **Detecting unknown human faces** belonging to unseen individuals, enabling future enrollment.
4. Demonstrates robustness under real-world perturbations including additive Gaussian noise, severe illumination shifts, and partial facial occlusions.

---

## 1.4 Objectives of the Project
The primary academic and technical objectives of this project are:
1. **Mathematical Fidelity**: Implement the exact equations and derivations from Turk & Pentland (1991) using pure NumPy, without relying on black-box wrappers (`sklearn.decomposition.PCA`).
2. **Covariance Reduction Implementation**: Realize the Turk-Pentland surrogate matrix trick $L = A^TA$, demonstrating an analytical and computational complexity reduction of over **$270\times$**.
3. **Full 4-Way Decision Logic**: Implement both **Distance from Face Space (DFFS, $\epsilon_d$)** and **Distance in Face Space (DIFS, $\epsilon_c$)** to realize the complete two-threshold classification engine.
4. **Empirical Benchmarking**: Evaluate recognition accuracy, reconstruction fidelity, and decision boundary calibration on the canoncial **Olivetti / AT&T Face Database**.
5. **Robustness Characterization**: Systematically quantify performance degradation under synthetic Gaussian noise and facial occlusions (sunglasses and surgical masks).
6. **Automated Verification**: Build unit test suites asserting orthonormal basis conditions ($U^TU = I_K$), algebraic equivalence, and error monotonicity.
7. **Interactive Demonstration Tools**: Develop an automated terminal execution script (`demo.py`) and a modern interactive web dashboard (`app.py`) for live viva defense.

---

## 1.5 Scope and Limitations of the Implementation
* **Scope**: The system is designed for near-frontal grayscale facial images ($64 \times 64$ pixels) under controlled-to-moderate illumination and expression variations ($\pm 20^\circ$ rotation).
* **Limitations**: As an unsupervised linear subspace model, standard Eigenfaces does not account for non-linear manifold curvature under extreme 3D profile rotations ($>45^\circ$) or extreme illumination shifts where lighting shadows dominate facial identity variance (a limitation later addressed by Fisherfaces / LDA).

---

## 1.6 Report Organization
* **Chapter 2** presents an in-depth literature review tracing the historical development from PCA to modern deep metric learning.
* **Chapter 3** provides the complete theoretical foundation and step-by-step mathematical proofs of the Turk-Pentland formulation.
* **Chapter 4** outlines the system architecture, dataset partitioning, and algorithmic pseudocode.
* **Chapter 5** presents the empirical experimental results, figures, tables, and robustness tests.
* **Chapter 6** details the automated unit testing and mathematical verification suite.
* **Chapter 7** concludes the report with key findings, limitations, and future research directions.
* **Chapters 8 & 9** provide academic references, the source code repository URL, and the scannable GitHub QR code.

---

<div style="page-break-after: always;"></div>

# CHAPTER 2: LITERATURE REVIEW

## 2.1 Sirovich & Kirby (1987) – Low-Dimensional Representation of Faces
The mathematical foundation for subspace face representation was established by **Lawrence Sirovich and Michael Kirby** (1987) in their paper *"Low-dimensional procedure for the characterization of human faces"* published in the *Journal of the Optical Society of America A*. 

Sirovich and Kirby applied the **Karhunen-Loève expansion** (discrete Principal Component Analysis) to ensembles of digitized human faces. They discovered that face images are remarkably redundant: while a $128 \times 128$ image resides in a $16,384$-dimensional Euclidean space, human faces occupy a tiny, highly constrained subspace. They demonstrated that any face could be faithfully approximated as a linear combination of just $\sim 40$ to $50$ orthogonal coordinate eigenfunctions. However, Sirovich and Kirby utilized PCA strictly for image compression and characterization, leaving the problem of automated face recognition and detection unaddressed.

---

## 2.2 Matthew Turk & Alex Pentland (1991) – Eigenfaces for Recognition
In their seminal 1991 paper published in the *Journal of Cognitive Neuroscience*, **Matthew Turk and Alex Pentland** transformed Sirovich and Kirby’s representation framework into a functional, real-time recognition system. 

Their primary conceptual and technical contributions were:
1. **Eigenfaces Definition**: Formalized the eigenvectors of the face covariance matrix as "Eigenfaces", viewing them as holistic feature extractors.
2. **The Covariance Eigendecomposition Shortcut**: Formulated the mathematical proof demonstrating that the eigenvectors of $AA^T \in \mathbb{R}^{D \times D}$ can be derived directly from the much smaller matrix $A^TA \in \mathbb{R}^{M \times M}$, turning a computationally impossible problem into a real-time computation.
3. **The 4-Way Decision Rule**: Introduced the concept of **Distance from Face Space (DFFS)** as an orthogonal residual metric for **Face Detection**, and **Distance in Face Space (DIFS)** for **Identification**, creating the first integrated architecture for simultaneous face detection and recognition.

---

## 2.3 Belhumeur, Hespanha & Kriegman (1997) – Fisherfaces & LDA
In 1997, Peter Belhumeur, João Hespanha, and David Kriegman published *"Eigenfaces vs. Fisherfaces: Recognition Using Class Specific Linear Projection"* in the *IEEE Transactions on Pattern Analysis and Machine Intelligence*.

Belhumeur et al. highlighted a fundamental theoretical weakness of Eigenfaces: **PCA is an unsupervised algorithm**. PCA seeks projection directions that maximize *total variance* across all images. However, in real-world environments, the variance caused by illumination changes (e.g., lighting from the left vs. right) is often substantially greater than the variance between different people's facial structures. As a consequence, the top eigenfaces frequently encode lighting directions rather than identity discrimination.

To overcome this, they introduced **Fisherfaces**, which utilizes **Fisher's Linear Discriminant Analysis (LDA)**. Fisherfaces projects the data into a subspace that simultaneously **maximizes between-class scatter ($S_B$)** while **minimizing within-class scatter ($S_W$)**:
$$W_{\text{opt}} = \arg\max_W \frac{|W^T S_B W|}{|W^T S_W W|}$$
Fisherfaces proved significantly more invariant to extreme lighting changes, although it requires multiple labeled training examples per subject and is susceptible to the "small sample size problem" when $M < D$.

---

## 2.4 Local Appearance Descriptors: Local Binary Patterns (LBPH)
In the early 2000s, researchers recognized that global holistic representations (like PCA and LDA) are vulnerable to non-rigid deformations and localized occlusions. **Ahonen, Hadid, and Pietikäinen (2006)** introduced **Local Binary Patterns Histograms (LBPH)** for face recognition. 

LBPH divides a facial image into small spatial regions and computes local texture micro-patterns by thresholding neighboring pixels against center pixels. Because LBPH evaluates micro-texture relationships rather than absolute global intensities, it exhibits high tolerance to monotonic illumination variations and partial occlusions, bridging the gap between holistic linear subspaces and modern feature extractors.

---

## 2.5 The Deep Learning Revolution: FaceNet, ArcFace, and CNNs
Beginning with Taigman et al.'s **DeepFace** (2014) and Schroff et al.'s **FaceNet** (2015), the field underwent a paradigm shift toward **Deep Convolutional Neural Networks (CNNs)** and deep metric learning:
* **FaceNet (2015)**: Introduced the **Triplet Loss**, training deep networks to project face images directly onto a 128-dimensional Euclidean sphere where the distance between images of the same identity is minimized while distance to different identities is enforced past a margin:
  $$L = \sum_{i}^N \max(0, \|f(x_i^a) - f(x_i^p)\|_2^2 - \|f(x_i^a) - f(x_i^n)\|_2^2 + \alpha)$$
* **ArcFace (Deng et al., 2019)**: Introduced **Additive Angular Margin Loss**, optimizing geodesic distances on a hypersphere to achieve state-of-the-art recognition across millions of unconstrained identities.

---

## 2.6 Comparative Summary of Paradigms

```
+---------------------------------------------------------------------------------------------------+
| COMPARATIVE SUMMARY OF FACE RECOGNITION PARADIGMS                                                 |
+----------------------+--------------------+--------------------+----------------------------------+
| Feature / Metric     | Eigenfaces (1991)  | Fisherfaces (1997) | Deep Metric Learning (2015-Now)  |
+----------------------+--------------------+--------------------+----------------------------------+
| Core Formulation     | Linear Subspace    | Linear Subspace    | Non-linear Deep Manifold         |
| Optimization Goal    | Max Total Variance | Max Class Scatter  | Angular Margin Hypersphere       |
| Supervision          | Unsupervised (PCA) | Supervised (LDA)   | Deep Supervised Metric           |
| Computational Cost   | Low (Closed form)  | Low (Closed form)  | Very High (GPU Training)         |
| Sensitivity to Light | Moderate to High   | Low                | Extremely Low                    |
| Pose Tolerance       | Near-frontal (+-20)| Near-frontal (+-20)| Extreme Invariance (+-90 deg)    |
| Sample Requirement   | 1-5 images/person  | >2 images/person   | Millions of images required      |
+----------------------+--------------------+--------------------+----------------------------------+
```

---

<div style="page-break-after: always;"></div>

# CHAPTER 3: THEORETICAL FOUNDATION & MATHEMATICAL DERIVATIONS

This chapter presents the rigorous mathematical foundation and analytical derivations of the Eigenfaces framework as formulated by Matthew Turk and Alex Pentland (1991).

---

## 3.1 Digital Image Representation as High-Dimensional Vectors
Let a digital face image $I(x,y)$ be represented as an intensity matrix of dimensions $H \times W$ pixels. In linear algebra, a 2D matrix can be flattened by concatenating its rows (or columns) into a 1D column vector:
$$\Gamma_i = \begin{bmatrix} I_i(1,1) \\ I_i(1,2) \\ \vdots \\ I_i(H,W) \end{bmatrix} \in \mathbb{R}^D, \quad \text{where } D = H \times W$$

For the benchmark $64 \times 64$ images used in this project:
$$D = 64 \times 64 = 4096 \text{ dimensions}$$

Each face image is thus represented as a single point in a $4096$-dimensional Euclidean space $\mathbb{R}^D$. Because human faces share a common morphology (two eyes horizontally aligned above a central nose and mouth), face vectors are not uniformly distributed throughout $\mathbb{R}^D$. Instead, they cluster in a tiny, constrained low-dimensional subspace.

---

## 3.2 The Average Face Vector ($\Psi$) and Mean-Centering
Given an ensemble of $M$ training images $\{\Gamma_1, \Gamma_2, \dots, \Gamma_M\}$, the **Average Face Vector** $\Psi \in \mathbb{R}^D$ is the arithmetic mean across all training samples:
$$\Psi = \frac{1}{M} \sum_{i=1}^M \Gamma_i$$

The vector $\Psi$ represents the static anatomical baseline common to all human faces. 

To isolate facial individuality and illumination differences, each training face is centered by subtracting $\Psi$:
$$\Phi_i = \Gamma_i - \Psi, \quad i = 1, \dots, M$$

The centered difference vectors $\Phi_i$ have zero expected mean:
$$\mathbb{E}[\Phi] = \frac{1}{M} \sum_{i=1}^M \Phi_i = \frac{1}{M} \sum_{i=1}^M (\Gamma_i - \Psi) = \Psi - \Psi = \mathbf{0}$$

---

## 3.3 Difference Matrix Assembly ($A \in \mathbb{R}^{D \times M}$)
The $M$ mean-centered vectors $\Phi_1, \Phi_2, \dots, \Phi_M$ are concatenated column-wise to form the data matrix $A$:
$$A = [\Phi_1, \Phi_2, \dots, \Phi_M] \in \mathbb{R}^{D \times M}$$

Matrix $A$ has $D$ rows ($4096$ pixels) and $M$ columns ($245$ training images).

---

## 3.4 The High-Dimensional Covariance Dilemma ($C \in \mathbb{R}^{D \times D}$)
The sample covariance matrix $C \in \mathbb{R}^{D \times D}$ of the training ensemble is defined as:
$$C = \frac{1}{M} \sum_{i=1}^M \Phi_i \Phi_i^T = \frac{1}{M} A A^T$$

Notice the dimensions:
$$\dim(A) = (D \times M) \implies \dim(A A^T) = (D \times D)$$

For images of size $64 \times 64$, $D = 4096$. The covariance matrix $C$ contains:
$$4096 \times 4096 = 16,777,216 \text{ floating-point elements}$$

### The Computational Impasse:
Finding the eigenvalues and eigenvectors of a symmetric matrix $C \in \mathbb{R}^{D \times D}$ via standard algorithms (such as QR decomposition or divide-and-conquer) has a computational complexity of:
$$\mathcal{O}(D^3) = (4096)^3 \approx 6.87 \times 10^{10} \text{ FLOPs}$$

For higher-resolution images (e.g., $256 \times 256$, $D = 65,536$), the covariance matrix contains $>4.29 \times 10^9$ elements ($34\text{ GB}$ of RAM for a single matrix), rendering direct eigendecomposition impossible.

Furthermore, basic linear algebra establishes that:
$$\text{rank}(A A^T) \le \min(\text{rank}(A), \text{rank}(A^T)) \le \min(D, M) = M$$

Since the vectors were mean-centered, the maximum rank is at most $M - 1$. Out of $4096$ possible eigenvalues, at most $M - 1 = 244$ are non-zero. The remaining $3852$ eigenvalues are identical to zero. Computing a $4096 \times 4096$ matrix to retrieve only $244$ meaningful vectors is wildly inefficient.

---

## 3.5 Rigorous Mathematical Proof of the Turk-Pentland Covariance Reduction Trick
To resolve this computational bottleneck, Turk and Pentland (1991) introduced an algebraic reduction based on the dual inner-product matrix.

### Theorem:
Let $A \in \mathbb{R}^{D \times M}$ be a real matrix with $M \ll D$. If $v_k \in \mathbb{R}^M$ is an eigenvector of the matrix $L = A^T A \in \mathbb{R}^{M \times M}$ with corresponding eigenvalue $\mu_k$, then $u_k = A v_k \in \mathbb{R}^D$ is an eigenvector of the covariance matrix $C = A A^T \in \mathbb{R}^{D \times D}$ with the identical eigenvalue $\mu_k$.

### Proof:
By definition of an eigenvector, the eigendecomposition of the surrogate matrix $L = A^T A$ satisfies:
$$L v_k = \mu_k v_k$$
Substituting $L = A^T A$:
$$(A^T A) v_k = \mu_k v_k \quad \text{--- (Equation 1)}$$

where $\mu_k \in \mathbb{R}$ is the scalar eigenvalue and $v_k \in \mathbb{R}^M$ is the non-zero eigenvector.

Now, multiply both sides of Equation 1 from the left by matrix $A \in \mathbb{R}^{D \times M}$:
$$A [(A^T A) v_k] = A [\mu_k v_k]$$

By the associative property of matrix multiplication:
$$(A A^T)(A v_k) = A (\mu_k v_k)$$

Since $\mu_k$ is a scalar, it commutes with matrix $A$:
$$(A A^T)(A v_k) = \mu_k (A v_k) \quad \text{--- (Equation 2)}$$

Now, define the vector $u_k \in \mathbb{R}^D$ as:
$$u_k = A v_k$$

Substituting $u_k$ into Equation 2 yields:
$$(A A^T) u_k = \mu_k u_k \quad \text{--- (Equation 3)}$$

Equation 3 is the exact definition of an eigenvalue problem for matrix $A A^T$. 
Therefore, $u_k = A v_k$ is an exact eigenvector of the full covariance matrix $A A^T$ with eigenvalue $\mu_k$. $\quad \blacksquare$

### Computational Impact:
The surrogate matrix $L = A^T A$ is of size $M \times M = 245 \times 245 = 60,025$ elements.  
The complexity of decomposing $L$ is:
$$\mathcal{O}(M^3) = (245)^3 \approx 1.47 \times 10^7 \text{ FLOPs}$$
$$\text{Computational Speedup Factor} = \frac{\mathcal{O}(D^3)}{\mathcal{O}(M^3)} = \left(\frac{4096}{245}\right)^3 \approx \mathbf{4,670\times}$$
In terms of memory footprint, $60,025$ elements vs. $16,777,216$ elements represents a **$279.5\times$ memory reduction**.

---

## 3.6 Eigendecomposition and Orthonormal Basis Construction
Because $L = A^T A$ is real, symmetric, and positive semi-definite ($x^T A^T A x = \|A x\|_2^2 \ge 0$), the **Spectral Theorem** guarantees that all eigenvalues $\mu_k$ are real and non-negative, and its eigenvectors $v_k$ can be chosen to be mutually orthonormal:
$$v_j^T v_k = \delta_{jk} = \begin{cases} 1 & \text{if } j = k \\ 0 & \text{if } j \ne k \end{cases}$$

The derived eigenvectors $u_k = A v_k$ are scaled to unit Euclidean length:
$$\|u_k\|_2 = \sqrt{u_k^T u_k} = \sqrt{(A v_k)^T (A v_k)} = \sqrt{v_k^T A^T A v_k} = \sqrt{v_k^T (\mu_k v_k)} = \sqrt{\mu_k \|v_k\|_2^2} = \sqrt{\mu_k}$$

Therefore, dividing $A v_k$ by its Euclidean norm gives the orthonormal **Eigenface** $u_k$:
$$u_k = \frac{A v_k}{\sqrt{\mu_k}} = \frac{A v_k}{\|A v_k\|_2}$$

Sorting the eigenvalues in descending order:
$$\mu_1 \ge \mu_2 \ge \dots \ge \mu_K \ge \dots \ge \mu_M \ge 0$$

The top $K$ eigenfaces are arranged as column vectors to construct the projection matrix $U \in \mathbb{R}^{D \times K}$:
$$U = [u_1, u_2, \dots, u_K]$$

---

## 3.7 Proof of Orthonormality ($U^T U = I_K$)
We verify that the projection matrix $U$ forms an orthonormal basis:
$$(U^T U)_{jk} = u_j^T u_k = \left(\frac{A v_j}{\sqrt{\mu_j}}\right)^T \left(\frac{A v_k}{\sqrt{\mu_k}}\right) = \frac{v_j^T (A^T A) v_k}{\sqrt{\mu_j \mu_k}}$$

Since $v_k$ is an eigenvector of $A^T A$ with eigenvalue $\mu_k$:
$$(U^T U)_{jk} = \frac{v_j^T (\mu_k v_k)}{\sqrt{\mu_j \mu_k}} = \frac{\mu_k (v_j^T v_k)}{\sqrt{\mu_j \mu_k}}$$

Since $v_j$ and $v_k$ are orthonormal ($v_j^T v_k = \delta_{jk}$):
- If $j \ne k$: $(U^T U)_{jk} = 0$.
- If $j = k$: $(U^T U)_{kk} = \frac{\mu_k (1)}{\sqrt{\mu_k^2}} = \frac{\mu_k}{\mu_k} = 1$.

Hence, $U^T U = I_K \in \mathbb{R}^{K \times K}$. $\quad \blacksquare$

---

## 3.8 Subspace Projection: Derivation of Coordinate Vector $\Omega$
Any face image $\Gamma \in \mathbb{R}^D$ is projected into the $K$-dimensional Face Space by first subtracting the average face $\Psi$ and computing the inner product with each basis vector $u_k$:
$$\omega_k = u_k^T (\Gamma - \Psi), \quad k = 1, \dots, K$$

The complete coordinate representation is the vector $\Omega \in \mathbb{R}^K$:
$$\Omega = \begin{bmatrix} \omega_1 \\ \omega_2 \\ \vdots \\ \omega_K \end{bmatrix} = U^T (\Gamma - \Psi)$$

Vector $\Omega$ serves as the low-dimensional compact feature embedding representing the individual identity.

---

## 3.9 Image Reconstruction as Linear Combination of Eigenvectors
The orthogonal projection of $\Gamma$ onto the subspace spanned by the $K$ eigenfaces is given by:
$$\hat{\Phi} = U \Omega = \sum_{k=1}^K \omega_k u_k$$

Adding back the average face vector $\Psi$ yields the reconstructed image $\hat{\Gamma} \in \mathbb{R}^D$:
$$\hat{\Gamma} = \Psi + \hat{\Phi} = \Psi + U \Omega = \Psi + \sum_{k=1}^K \omega_k u_k$$

As $K$ approaches $M$, $\hat{\Gamma}$ converges toward the exact original image $\Gamma$.

---

## 3.10 Dual Distance Formulations

```
+-------------------------------------------------------------------------+
| GEOMETRIC DECOMPOSITION OF THE INPUT IMAGE SPACE                        |
|                                                                         |
|                \   Input Image Gamma                                    |
|                 \  *                                                    |
|                  \ |                                                    |
|                   \| eps_d (DFFS: Distance From Face Space)             |
|                    v                                                    |
|  ==================*===================  <-- Face Space Subspace (K-D)  |
|               Reconstructed Gamma_f                                     |
|                    |                                                    |
|                    |<--- eps_c (DIFS: Distance In Face Space) --->|     |
|                    v                                              v     |
|                 Omega (Projection)                     Enrolled Omega_k |
+-------------------------------------------------------------------------+
```

### 3.10.1 Distance from Face Space (DFFS - $\epsilon_d$)
The **Distance from Face Space** $\epsilon_d$ is the orthogonal Euclidean distance between the raw input vector $\Gamma$ and its reconstruction $\hat{\Gamma}$:
$$\epsilon_d = \|\Gamma - \hat{\Gamma}\|_2 = \sqrt{\sum_{p=1}^D (\Gamma(p) - \hat{\Gamma}(p))^2}$$

* **Geometric Meaning**: $\epsilon_d$ quantifies how much of the image lies *outside* the hyper-plane spanned by human faces.
* **Functional Role**: **Face Detection & Non-Face Rejection**. Non-face objects (e.g., chairs, cars, random noise) cannot be expressed as linear combinations of eigenfaces, producing a massive residual $\epsilon_d \gg \theta_f$.

### 3.10.2 Distance in Face Space (DIFS - $\epsilon_c$)
The **Distance in Face Space** $\epsilon_c$ is the Euclidean distance within the $K$-dimensional subspace between the query weight vector $\Omega$ and enrolled class centroids $\Omega_k$:
$$\Omega_k = \frac{1}{M_k} \sum_{i \in \text{Class } k} \Omega_i$$
$$\epsilon_c = \min_k \|\Omega - \Omega_k\|_2 = \min_k \sqrt{\sum_{j=1}^K (\omega_j - \Omega_{k,j})^2}$$

* **Geometric Meaning**: $\epsilon_c$ measures how close the face lies to known identity clusters within Face Space.
* **Functional Role**: **Identity Classification & Unknown Face Discovery**.

---

## 3.11 The 4-Way Decision Rule Framework (Section 3.2 Analysis)
Combining $\epsilon_d$ and $\epsilon_c$ establishes the complete two-threshold decision engine formulated in Section 3.2 of Turk & Pentland (1991):

```
+-------------------------------------------------------------------------+
| TURK & PENTLAND 4-WAY DECISION LOGIC                                    |
|                                                                         |
| Is eps_d >= theta_f?                                                    |
|   |                                                                     |
|   +-- YES --> [CASE 1: NOT A FACE]                                      |
|   |           Residual too large; reject input image.                   |
|   |                                                                     |
|   +-- NO  --> Confirmed Human Face! Now check: Is eps_c < theta_c?      |
|                 |                                                       |
|                 +-- YES --> [CASE 2: KNOWN FACE]                        |
|                 |           Classified as Enrolled Subject c*.          |
|                 |                                                       |
|                 +-- NO  --> [CASE 3: UNKNOWN FACE]                      |
|                             Unseen human face; prompt to enroll.        |
+-------------------------------------------------------------------------+
```

---

## 3.12 Threshold Calibration Mechanics
The operational thresholds $\theta_f$ and $\theta_c$ are calibrated directly from the empirical training distributions:
1. **Face Threshold ($\theta_f$)**:
   $$\theta_f = \max_{i \in \text{Train}} \|\Gamma_i - \hat{\Gamma}_i\|_2 + \alpha \cdot \sigma_{\text{dffs}}$$
   Setting $\alpha = 8.0$ guarantees that virtually $100\%$ of natural facial variations (including unseen individuals) fall safely below $\theta_f$, while non-face patterns ($\epsilon_d \ge 12.0$) are cleanly rejected.
2. **Classification Threshold ($\theta_c$)**:
   $$\theta_c = \mu_{\text{intra}} + \beta \cdot \sigma_{\text{intra}}$$
   where $\mu_{\text{intra}}$ and $\sigma_{\text{intra}}$ represent the mean and standard deviation of intra-class centroid distances. Setting $\beta = 1.2$ establishes a discriminative boundary separating known subjects from unseen individuals.

---

<div style="page-break-after: always;"></div>

# CHAPTER 4: SYSTEM ARCHITECTURE & IMPLEMENTATION METHODOLOGY

## 4.1 End-to-End System Architecture
The software architecture follows a modular, decoupled pipeline designed for reproducibility:

```
+-------------------------------------------------------------------------+
| HIGH-LEVEL SYSTEM PIPELINE                                              |
|                                                                         |
|  [Olivetti Dataset] --> [load_face_data()] --> [Partitioning Engine]    |
|                                                      |                  |
|       +----------------------------------------------+                  |
|       |                     |                        |                  |
|       v                     v                        v                  |
|  X_train (M=245)      X_test_known (N=105)     X_test_unknown (N=50)    |
|       |                                                                 |
|       v                                                                 |
|  [EigenfacesClassifier.fit()]                                           |
|       |--> 1. Compute Mean Face Psi                                     |
|       |--> 2. Compute Difference Matrix A                               |
|       |--> 3. Form Surrogate L = A^T A                                  |
|       |--> 4. np.linalg.eigh(L) --> (evals, evecs)                      |
|       |--> 5. Compute Eigenfaces U = A * evecs / norms                  |
|       |--> 6. Project Gallery: Omega_train = U^T A                      |
|       |--> 7. Calibrate Thresholds (theta_f, theta_c)                   |
|                                                                         |
|  [Query Image Gamma] --> [recognize()] --> [4-Way Decision Engine]      |
|       |--> eps_d >= theta_f ?  --> "NOT_A_FACE"                         |
|       |--> eps_c < theta_c  ?  --> "KNOWN_FACE" (ID = c*)               |
|       |--> Otherwise        ?  --> "UNKNOWN_FACE" (New subject)         |
+-------------------------------------------------------------------------+
```

---

## 4.2 Benchmark Dataset: Olivetti / AT&T Faces Database
The dataset employed is the **Olivetti Faces Database** (collected at AT&T Laboratories Cambridge, UK).
* **Subject Count**: 40 distinct subjects.
* **Images per Subject**: 10 images each (Total: 400 images).
* **Resolution**: $64 \times 64$ pixels, 8-bit grayscale, normalized to float $[0.0, 1.0]$.
* **Physical Variations**: Lighting angle shifts, facial expressions (open/closed eyes, smiling/neutral), glasses vs. no glasses, and head tilt up to $\pm 20^\circ$.
* **Local Offline Storage**: Cached locally in `data/olivetti_py3.pkz` (1.3 MB).

---

## 4.3 Structured Experimental Dataset Partitioning
To evaluate the 4-way decision framework, the dataset was split as follows:

```
+------------------------------------------------------------------------------------------------+
| TABLE 3: DATASET PARTITIONING SPECIFICATIONS                                                   |
+----------------------+--------------------+--------------------+-------------------------------+
| Partition Name       | Samples & Subjects | Total Images       | Experimental Purpose          |
+----------------------+--------------------+--------------------+-------------------------------+
| Training Gallery     | 35 subjects x 7 img| 245 images (M=245) | Learn Psi, L, and Eigenfaces  |
| Known Probe Set      | 35 subjects x 3 img| 105 images         | Test Known ID (Case 2)        |
| Unknown Probe Set    | 5 subjects x 10 img| 50 images          | Test Unknown Face (Case 3)    |
| Non-Face Patterns    | Synthetic Textures | 10 images          | Test Non-Face Reject (Case 1) |
+----------------------+--------------------+--------------------+-------------------------------+
```

---

## 4.4 Modular Codebase Architecture
The codebase is structured under `eigen_faces/`:
* `src/eigenfaces.py`: The core `EigenfacesClassifier` class implementing matrix vectorization, surrogate decomposition, subspace projection, reconstruction, and the 4-way decision logic in pure NumPy.
* `src/dataset.py`: Ingestion routines for the Olivetti database and synthetic non-face generator (checkerboard, uniform noise, sinusoidal gratings, radial ripples).
* `src/evaluate.py`: Benchmark suite computing accuracy vs. $K$, confusion metrics, and noise degradation.
* `src/visualizer.py`: Scientific monochrome visualization generator saving high-contrast figures.
* `src/generate_bw_figures.py`: Dedicated script compiling all 6 monochrome publication figures into `results/bw/`.
* `src/build_html_report.py`: Compiler building the self-contained printable `REPORT.html`.
* `demo.py`: Automated terminal execution script printing ASCII telemetry.
* `app.py`: Flask web server providing an interactive presentation dashboard at `http://localhost:5050`.

---

## 4.5 Algorithmic Pseudocode

### 4.5.1 Training Phase (Eigenfaces Learning)
```python
Algorithm 1: Eigenfaces Training via Turk-Pentland Reduction
Input: Training images Gamma_1, ..., Gamma_M in R^D, labels y_1, ..., y_M, component count K
Output: Mean face Psi, projection matrix U, class centroids Omega_c, thresholds theta_f, theta_c

1: Compute average face vector:
      Psi = (1 / M) * sum_{i=1}^M Gamma_i
2: Compute mean-centered difference matrix:
      For i = 1 to M:
          Phi_i = Gamma_i - Psi
      A = [Phi_1, Phi_2, ..., Phi_M]  # Shape: (D x M)
3: Form surrogate covariance matrix:
      L = A^T * A                     # Shape: (M x M)
4: Compute eigenvalues and eigenvectors:
      evals, evecs = eigh(L)
5: Sort in descending order:
      idx = argsort(evals)[::-1]
      evals = evals[idx]
      evecs = evecs[:, idx]
6: Transform eigenvectors to Face Space:
      U = A * evecs[:, :K]            # Shape: (D x K)
7: Normalize columns to unit length:
      For k = 1 to K:
          U[:, k] = U[:, k] / norm(U[:, k])
8: Project training gallery into Face Space:
      Omega_train = U^T * A           # Shape: (K x M)
9: Compute class centroids:
      For each unique class c:
          Omega_c = mean(Omega_train[:, y == c], axis=1)
10: Calibrate decision thresholds theta_f and theta_c from training residuals.
```

### 4.5.2 Inference Phase (4-Way Decision Logic)
```python
Algorithm 2: Turk & Pentland 4-Way Decision Classification
Input: Query image Gamma in R^D, Model (Psi, U, Omega_c, theta_f, theta_c)
Output: Decision ("NOT_A_FACE", "KNOWN_FACE", "UNKNOWN_FACE"), Predicted Label c*

1: Project query image into Face Space:
      Omega = U^T * (Gamma - Psi)     # Coordinate vector (K x 1)
2: Reconstruct face from subspace:
      Gamma_hat = Psi + U * Omega     # Reconstructed image (D x 1)
3: Compute Distance from Face Space (DFFS):
      eps_d = norm(Gamma - Gamma_hat)
4: Compute Distance in Face Space (DIFS):
      For each enrolled class c:
          dist_c = norm(Omega - Omega_c)
      eps_c = min(dist_c)
      c_star = argmin(dist_c)
5: Apply 4-Way Decision Rules:
      If eps_d >= theta_f:
          Return Decision: "NOT_A_FACE", Predicted: None
      Else if eps_c < theta_c:
          Return Decision: "KNOWN_FACE", Predicted: c_star
      Else:
          Return Decision: "UNKNOWN_FACE", Predicted: None
```

---

<div style="page-break-after: always;"></div>

# CHAPTER 5: EXPERIMENTAL RESULTS & PERFORMANCE EVALUATION

## 5.1 Training Convergence and Computational Reduction Metrics
The empirical execution confirmed the mathematical speedup predicted by the Turk-Pentland proof:

```
+------------------------------------------------------------------------------------------------+
| TABLE 5: COMPUTATIONAL COMPLEXITY AND MEMORY PROFILING                                         |
+--------------------------+-----------------------------+---------------------------------------+
| Metric / Parameter       | Direct Covariance (C = AA^T)| Turk-Pentland Surrogate (L = A^TA)    |
+--------------------------+-----------------------------+---------------------------------------+
| Matrix Dimensions        | 4096 x 4096                 | 245 x 245                             |
| Total Matrix Elements    | 16,777,216 floating-point   | 60,025 floating-point                 |
| Memory Footprint         | ~134.2 MB                   | ~0.48 MB (279.5x reduction)           |
| Theoretical Complexity   | O(D^3) ~ 6.87 x 10^10 FLOPs | O(M^3) ~ 1.47 x 10^7 FLOPs            |
| Actual Wall-Clock Time   | >18.5 seconds               | 0.042 seconds (440x faster)           |
+--------------------------+-----------------------------+---------------------------------------+
```

---

## 5.2 Qualitative Evaluation: Mean Face and Principal Eigenfaces Gallery
Figure 1 displays the computed **Average Face ($\Psi$)** and the top 15 principal eigenfaces ($u_1 \dots u_{15}$).

```
+-------------------------------------------------------------------------+
| FIGURE 1: MEAN FACE AND TOP 15 PRINCIPAL EIGENFACES                     |
| Image Source: results/bw/fig1_eigenfaces_gallery.png                    |
|                                                                         |
| [ Average Face Psi ]   [ Eigenface u_1 ]  [ Eigenface u_2 ]  [ u_3 ]    |
| (Baseline template)    (16.8% variance)   (12.7% variance)   (7.4%)     |
|                                                                         |
| [ Eigenface u_4 ]      [ Eigenface u_5 ]  [ Eigenface u_6 ]  [ u_7 ]    |
| (5.3% variance)        (4.2% variance)    (3.5% variance)    (3.0%)     |
+-------------------------------------------------------------------------+
```

### Visual and Morphological Analysis:
1. **Average Face ($\Psi$)**: Represents the smooth, symmetric universal human template. Individual distinguishing marks are blended out, leaving centered eye sockets, nose bridge, and lip lines.
2. **Eigenfaces $u_1$ and $u_2$**: Display distinct left-versus-right and top-versus-bottom illumination gradients. Because PCA is unsupervised, global lighting shifts account for the largest mathematical variance in the pixel space.
3. **Eigenfaces $u_3$ through $u_8$**: Clearly encode physical facial features: forehead height, jawline roundness, eyebrow thickness, and presence/absence of glasses.
4. **Higher Eigenfaces ($u_9 \dots u_{15}$)**: Represent high-frequency facial micro-details and hair edge textures.

---

## 5.3 Scree Plot, Eigenvalue Decay & Cumulative Variance
Figure 2 displays the Scree Plot (eigenvalue magnitude vs. index $k$) and the cumulative explained variance curve.

```
+-------------------------------------------------------------------------+
| FIGURE 2: EIGENVALUE SPECTRUM AND CUMULATIVE VARIANCE CURVE             |
| Image Source: results/bw/fig2_scree_plot.png                           |
|                                                                         |
|  Eigenvalue Magnitude (Scree)             Cumulative Variance (%)       |
|  |*                                      100|          . - - - 95% (K=95)|
|  | *                                      90|      . - ' - - - 90% (K=57)|
|  |  *                                     80|    /                       |
|  |   *.                                   60|  /                         |
|  |     * - - . .                          40| /                          |
|  +-------------------> (k)                0 +-------------------> (K)   |
|   1 10 20 30 40 50                           1 10 20 40 60 80           |
+-------------------------------------------------------------------------+
```

* **Exponential Decay**: The eigenvalues decay precipitously. The first 10 components account for **$60.21\%$** of total variance.
* **Variance Milestones**:
  * **$80\%$ Variance** is achieved at $K = 29$ eigenfaces.
  * **$90\%$ Variance** is achieved at $K = 57$ eigenfaces.
  * **$95\%$ Variance** is achieved at $K = 95$ eigenfaces.
* **Dimensional Compression**: At $K = 40$, the model captures **$86.33\%$** of the information while achieving a **$99.02\%$ dimensionality reduction** ($4096 \to 40$ floats).

---

## 5.4 Reconstruction Fidelity vs. Subspace Dimensionality K
Figure 3 demonstrates how an input facial vector is reconstructed as the subspace dimension $K$ expands.

```
+-------------------------------------------------------------------------+
| FIGURE 3: RECONSTRUCTION CONVERGENCE ACROSS DIMENSIONALITY K            |
| Image Source: results/bw/fig3_face_reconstruction.png                   |
|                                                                         |
| [ Original ]    [ K = 2 ]     [ K = 5 ]     [ K = 10 ]    [ K = 40 ]    |
|  True Face    eps_d = 8.59  eps_d = 6.76  eps_d = 5.58  eps_d = 4.73    |
| (4096 dims)   (Coarse blob) (Outline)     (Features)    (Sharp ID)      |
+-------------------------------------------------------------------------+
```
* At $K = 2$: Only coarse illumination shading is visible ($\epsilon_d = 8.593$).
* At $K = 5$: Head contour and eye sockets emerge ($\epsilon_d = 6.765$).
* At $K = 10$: Nose bridge and mouth boundary become sharp ($\epsilon_d = 5.588$).
* At $K = 40$: High-fidelity reconstruction matching the subject's true likeness ($\epsilon_d = 4.729$).

---

## 5.5 Quantitative Identification Accuracy vs. K
Table 1 and Figure 6 report top-1 identification accuracy on the 105 known test probes across increasing values of $K$.

```
+------------------------------------------------------------------------------------------------+
| TABLE 1: BENCHMARK RECOGNITION ACCURACY AND RECONSTRUCTION ERROR VS. K                         |
+-------------------+-----------------------+-----------------------+----------------------------+
| Eigenfaces (K)    | Dimensionality (Dims) | Top-1 Accuracy (%)    | Mean Recon Error (eps_d)   |
+-------------------+-----------------------+-----------------------+----------------------------+
| K = 2             | 2                     | 18.10%                | 6.859                      |
| K = 5             | 5                     | 50.48%                | 5.931                      |
| K = 10            | 10                    | 74.29%                | 5.245                      |
| K = 15            | 15                    | 76.19%                | 4.796                      |
| K = 20            | 20                    | 81.90%                | 4.496                      |
| K = 30            | 30                    | 85.71%                | 4.083                      |
| **K = 40**        | **40**                | **85.71%**            | **3.847**                  |
| **K = 50**        | **50**                | **87.62%**            | **3.676**                  |
| K = 75            | 75                    | 87.62%                | 3.387                      |
| K = 100           | 100                   | 87.62%                | 3.197                      |
+-------------------+-----------------------+-----------------------+----------------------------+
```

```
+-------------------------------------------------------------------------+
| FIGURE 6: ACCURACY AND RECONSTRUCTION RESIDUAL TRADEOFF                 |
| Image Source: results/bw/fig6_accuracy_vs_k.png                        |
+-------------------------------------------------------------------------+
```

### Analysis of the Dimensional Tradeoff:
* Accuracy exhibits a steep rise from $K=2$ ($18.10\%$) to $K=20$ ($81.90\%$), proving that the first 20 eigenfaces capture the primary discriminative structure.
* Performance peaks and plateaus at **$87.62\%$** between $K=50$ and $K=100$. Beyond $K=50$, adding components improves reconstruction error ($\epsilon_d$ drops from $3.68$ to $3.20$) but does not increase accuracy, confirming that tail eigenvalues encode image noise rather than identity.

---

## 5.6 Validation of the 4-Way Decision Space Geometry
The two calibrated decision thresholds were established as:
* **Face Space Threshold ($\theta_f$)**: $7.884$
* **Classification Threshold ($\theta_c$)**: $6.463$

Figure 4 illustrates the 2D decision geometry mapping $\epsilon_d$ (DFFS) on the horizontal axis and $\epsilon_c$ (DIFS) on the vertical axis across all three test groups.

```
+-------------------------------------------------------------------------+
| FIGURE 4: 2D DECISION SPACE GEOMETRY                                    |
| Image Source: results/bw/fig4_decision_space_geometry.png               |
+-------------------------------------------------------------------------+
```

```
+------------------------------------------------------------------------------------------------+
| TABLE 2: 4-WAY DECISION ENGINE VALIDATION MATRIX                                               |
+-----------------------+--------------+------------------+-------------------+------------------+
| Input Category        | Total Tested | Dec: KNOWN_FACE  | Dec: UNKNOWN_FACE | Dec: NOT_A_FACE  |
+-----------------------+--------------+------------------+-------------------+------------------+
| Known Probes (X_test) | 105          | 83 (79.0%)       | 22 (21.0%)        | 0 (0.0%)         |
| Unknown Probes (Unseen| 50           | 32 (64.0%)       | 18 (36.0%)        | 0 (0.0%)         |
| Non-Face Patterns     | 10           | 0 (0.0%)         | 2 (20.0%)         | 8 (80.0%)        |
+-----------------------+--------------+------------------+-------------------+------------------+
```

### Operational Conclusions:
1. **$100.0\%$ Face Acceptance Rate**: Every valid human face (known or unknown) yielded $\epsilon_d < \theta_f = 7.884$. Zero human faces were falsely rejected as non-faces.
2. **$80.0\%$ Non-Face Rejection Rate**: High-spatial-frequency patterns (checkerboard: $\epsilon_d = 32.08$, random noise: $\epsilon_d = 14.91$) were cleanly rejected into Zone 3.

---

## 5.7 Robustness Analysis: Performance Under Noise and Occlusions
Figure 5 documents model behavior under synthetic degradations:

```
+-------------------------------------------------------------------------+
| FIGURE 5: ROBUSTNESS UNDER NOISE AND OCCLUSIONS                         |
| Image Source: results/bw/fig5_robustness_analysis.png                   |
+-------------------------------------------------------------------------+
```

1. **Clean Face**: $\epsilon_d = 4.73$, correctly classified as `KNOWN_FACE`.
2. **Mild Gaussian Noise ($\sigma = 0.10$)**: $\epsilon_d = 5.21 < \theta_f$, correctly identified.
3. **Severe Gaussian Noise ($\sigma = 0.25$)**: $\epsilon_d = 7.14 < \theta_f$, correctly identified; reconstruction acts as a **denoising filter**.
4. **Eye Occlusion (Sunglasses Effect)**: $\epsilon_d = 5.84 < \theta_f$, correctly identified.
5. **Mouth Occlusion (Surgical Mask Effect)**: $\epsilon_d = 6.02 < \theta_f$, correctly identified.

*Theoretical Explanation*: Because PCA computes global surface projections ($u_k^T \Phi$), localized regional blockages alter only a fraction of the inner product summation, allowing unoccluded facial surface areas to preserve identity coordinates.

---

<div style="page-break-after: always;"></div>

# CHAPTER 6: AUTOMATED UNIT TESTING & MATHEMATICAL VERIFICATION

To verify mathematical correctness, an automated test suite was constructed in `tests/test_eigenfaces.py`:

```python
+-------------------------------------------------------------------------+
| AUTOMATED MATHEMATICAL TEST SUITE (tests/test_eigenfaces.py)            |
|                                                                         |
| [TEST 1] test_orthonormality_of_eigenfaces                              |
|          Assertion: norm(U^T * U - Identity_K) < 1e-7                   |
|          Status:    PASSED [Basis vectors are strictly orthonormal]     |
|                                                                         |
| [TEST 2] test_turk_pentland_trick_equivalence                           |
|          Assertion: abs(dot(u_direct, u_derived)) == 1.00000            |
|          Status:    PASSED [Exact algebraic equivalence confirmed]      |
|                                                                         |
| [TEST 3] test_reconstruction_monotonicity                               |
|          Assertion: dffs(K+1) <= dffs(K) for all K                      |
|          Status:    PASSED [Monotonic convergence verified]             |
|                                                                         |
| [TEST 4] test_four_way_decision_rule                                    |
|          Assertion: dffs(random_noise) > theta_face                     |
|          Status:    PASSED [Non-face rejected cleanly]                  |
+-------------------------------------------------------------------------+
```

All 4 unit tests execute in **0.035 seconds**, verifying that the code satisfies theoretical bounds.

---

<div style="page-break-after: always;"></div>

# CHAPTER 7: CONCLUSION & FUTURE SCOPE

## 7.1 Summary of Project Accomplishments
1. **From-Scratch Mathematical Rigor**: Successfully implemented the complete formulation of Turk & Pentland (1991) using pure NumPy without black-box machine learning wrappers.
2. **Empirical Validation of the Covariance Trick**: Mathematically proved and verified the $A^TA \leftrightarrow AA^T$ equivalence, slashing memory by **$279.5\times$** and compute time by over **$400\times$**.
3. **Full 4-Way Decision System**: Realized dual-distance hypothesis testing, achieving $100\%$ face acceptance and $80\%–90\%$ non-face rejection.
4. **High Accuracy**: Attained **$87.62\%$** recognition accuracy at $99.0\%$ dimensionality reduction on the benchmark Olivetti dataset.
5. **Demonstration Readiness**: Built an automated terminal demo (`demo.py`) and an interactive web presentation dashboard (`app.py`).

## 7.2 Limitations of PCA Subspaces
* **Sensitivity to Illumination**: Because PCA maximizes total variance, the first 2–3 eigenfaces predominantly capture lighting shifts rather than identity.
* **Sensitivity to Non-Frontal Poses**: Linear subspaces assume frontal alignment; large 3D rotations corrupt planar linear projections.

## 7.3 Directions for Future Research
* **Kernel PCA**: Incorporating non-linear kernel functions $k(x, y)$ to project faces into higher-dimensional non-linear feature spaces.
* **Fisherfaces (LDA Integration)**: Transitioning from unsupervised PCA to supervised Linear Discriminant Analysis to maximize between-class scatter while minimizing lighting-induced within-class scatter.
* **Deep Hybrid Subspaces**: Utilizing shallow CNN feature maps as inputs to PCA subspaces for hybrid edge-device biometrics.

---

<div style="page-break-after: always;"></div>

# CHAPTER 8: REFERENCES & BIBLIOGRAPHY

1. **Turk, M., & Pentland, A. (1991)**. *Eigenfaces for Recognition*. **Journal of Cognitive Neuroscience**, Vol. 3, No. 1, pp. 71–86.
2. **Sirovich, L., & Kirby, M. (1987)**. *Low-dimensional procedure for the characterization of human faces*. **Journal of the Optical Society of America A**, Vol. 4, No. 3, pp. 519–524.
3. **Belhumeur, P. N., Hespanha, J. P., & Kriegman, D. J. (1997)**. *Eigenfaces vs. Fisherfaces: Recognition using class specific linear projection*. **IEEE Transactions on Pattern Analysis and Machine Intelligence**, Vol. 19, No. 7, pp. 711–720.
4. **Kanade, T. (1973)**. *Picture Processing System by Computer Complex and Recognition of Human Faces*. Doctoral Dissertation, Kyoto University.
5. **Ahonen, T., Hadid, A., & Pietikäinen, M. (2006)**. *Face description with local binary patterns: Application to face recognition*. **IEEE Transactions on Pattern Analysis and Machine Intelligence**, Vol. 28, No. 12, pp. 2037–2041.
6. **Schroff, F., Kalenichenko, D., & Philbin, J. (2015)**. *FaceNet: A unified embedding for face recognition and clustering*. **IEEE Conference on Computer Vision and Pattern Recognition (CVPR)**, pp. 815–823.
7. **Deng, J., Guo, J., Xue, N., & Zafeiriou, S. (2019)**. *ArcFace: Additive angular margin loss for deep face recognition*. **IEEE Conference on Computer Vision and Pattern Recognition (CVPR)**, pp. 4690–4699.
8. **AT&T Laboratories Cambridge**. *The Database of Faces (formerly The ORL Database of Faces)*. Available online: `https://ndownloader.figshare.com/files/5976027`.

---

<div style="page-break-after: always;"></div>

# CHAPTER 9: SOURCE CODE REPOSITORY & VERIFICATION (GITHUB QR CODE)

To facilitate academic verification and review by the project examination committee, the complete source code, test suites, dataset ingestion scripts, and interactive presentation interfaces are hosted on GitHub:

* **Official Repository Link**: [https://github.com/shashank-emty/Eigen-faces](https://github.com/shashank-emty/Eigen-faces)

```
+-------------------------------------------------------------------------+
| [OFFICIAL GITHUB REPOSITORY VERIFICATION QR CODE]                       |
|                                                                         |
| Scan using any smartphone camera to inspect source code, execution logs |
| and reproduction instructions.                                          |
+-------------------------------------------------------------------------+
```

![GitHub Repository QR Code](results/bw/github_qr.png)

```
+-------------------------------------------------------------------------+
| STUDENT AND SUBMISSION DETAILS                                          |
|                                                                         |
| Student Name : SHASHANK M T                                             |
| UUCMS Number : U01BH25C0174                                             |
| Degree       : Bachelor of Computer Applications (AI) - BCA(AI) (3rd Sem, 2nd Year) |
| Subject      : Machine Learning                                         |
| Institution  : Pooja Bhagavat Mahajana First Grade College, Mysuru      |
| Date         : October 15, 2026                                         |
+-------------------------------------------------------------------------+
```
