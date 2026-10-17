#!/usr/bin/env python3
"""
build_clean_pptx.py
Builds a comprehensive, audience-facing 16:9 widescreen presentation deck for the Eigenfaces Project.
Contains intuitive, detailed explanations of:
  - How Eigenfaces are mathematically and visually derived (the linear combination recipe)
  - How Projection and Reconstruction happen step-by-step
  - How the 4-Way Decision framework evaluates faces vs. non-faces and known vs. unknown
Designed for both the presenter to explain smoothly and the audience/evaluators to read effortlessly.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
OUTPUT_PPTX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "EigenFaces_Presentation.pptx")

# Palette: Academic Royal Navy, Clean Slate, Cyan, Amber & Emerald Accents
NAVY_DARK = RGBColor(15, 23, 42)       # Slate 900
NAVY_CARD = RGBColor(30, 41, 59)      # Slate 800
NAVY_ACCENT = RGBColor(37, 99, 235)   # Blue 600
CYAN_ACCENT = RGBColor(6, 182, 212)   # Cyan 500
AMBER_ACCENT = RGBColor(245, 158, 11) # Amber 500
EMERALD_ACCENT = RGBColor(16, 185, 129) # Emerald 500
ROSE_ACCENT = RGBColor(225, 29, 72)   # Rose 600

TEXT_WHITE = RGBColor(255, 255, 255)
TEXT_MUTED = RGBColor(148, 163, 184)  # Slate 400
TEXT_DARK = RGBColor(30, 41, 59)      # Slate 800
BG_LIGHT = RGBColor(248, 250, 252)    # Slate 50
CARD_BG = RGBColor(255, 255, 255)
CARD_BORDER = RGBColor(226, 232, 240)


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_bg(slide, color=BG_LIGHT):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.fill.background()
        return shape

    def add_header(slide, title_text, category="EIGENFACES • TURK & PENTLAND (1991)"):
        hdr_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.15))
        hdr_bg.fill.solid()
        hdr_bg.fill.fore_color.rgb = NAVY_DARK
        hdr_bg.line.fill.background()

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.13), Inches(13.333), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = NAVY_ACCENT
        line.line.fill.background()

        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.28))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = CYAN_ACCENT

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, NAVY_DARK)

    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = NAVY_ACCENT
    top_bar.line.fill.background()

    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.9), Inches(5.0), Inches(0.42))
    pill.fill.solid()
    pill.fill.fore_color.rgb = NAVY_CARD
    pill.line.color.rgb = CYAN_ACCENT
    pill.line.width = Pt(1)
    tf_p = pill.text_frame
    p_p = tf_p.paragraphs[0]
    p_p.text = "MACHINE LEARNING • TECHNICAL PAPER PRESENTATION"
    p_p.font.size = Pt(9.5)
    p_p.font.bold = True
    p_p.font.color.rgb = CYAN_ACCENT
    p_p.alignment = PP_ALIGN.CENTER

    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(2.0))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Eigenfaces for Recognition"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p2 = tf1.add_paragraph()
    p2.text = "Dimensionality Reduction, Subspace Modeling & 4-Way Decision Framework"
    p2.font.size = Pt(18)
    p2.font.color.rgb = TEXT_MUTED

    p3 = tf1.add_paragraph()
    p3.text = "Implementation of the Landmark Paper by Matthew Turk & Alex Pentland (1991)"
    p3.font.size = Pt(13)
    p3.font.color.rgb = CYAN_ACCENT

    # Presenter Card
    c_s = add_card(s1, Inches(1.0), Inches(3.8), Inches(5.4), Inches(3.0), NAVY_CARD, NAVY_ACCENT)
    tfs = c_s.text_frame
    tfs.word_wrap = True
    p = tfs.paragraphs[0]
    p.text = "PRESENTER"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT

    p = tfs.add_paragraph()
    p.text = "Shashank M T"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    details = [
        ("UUCMS Register No.", "U01BH25C0174"),
        ("Course / Degree", "BCA(AI) – 3rd Semester, 2nd Year"),
        ("Subject", "Machine Learning"),
        ("Institution", "Pooja Bhagavat Mahajana First Grade College"),
    ]
    for k, v in details:
        p = tfs.add_paragraph()
        p.text = f"•  {k}: {v}"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(226, 232, 240)

    # Faculty & Guide Card
    c_f = add_card(s1, Inches(6.8), Inches(3.8), Inches(5.5), Inches(3.0), NAVY_CARD, NAVY_ACCENT)
    tff = c_f.text_frame
    tff.word_wrap = True
    p = tff.paragraphs[0]
    p.text = "GUIDANCE & INSTITUTION"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT

    p = tff.add_paragraph()
    p.text = "Ragunandan B"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    f_details = [
        ("Designation", "Course Lecturer (Guest Lecturer – ML)"),
        ("Department", "Dept. of Computer Science & AI, PBM FGC"),
        ("Date", "October 15, 2026"),
        ("Repository", "github.com/shashank-emty/Eigen-faces"),
    ]
    for k, v in f_details:
        p = tff.add_paragraph()
        p.text = f"•  {k}: {v}"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(226, 232, 240)

    # =========================================================================
    # SLIDE 2: Problem & Motivation (The Paradigm Shift)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "Motivation & The Paradigm Shift in Face Recognition")

    # Left: The Old Way (Geometric)
    c_old = add_card(s2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tf_old = c_old.text_frame
    tf_old.word_wrap = True
    p = tf_old.paragraphs[0]
    p.text = "Traditional Approach (Pre-1991)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ROSE_ACCENT

    p = tf_old.add_paragraph()
    p.text = "Geometric Feature Extraction"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    old_points = [
        ("Manual Geometry Measurement", "Tried to measure distances between pupils, nose width, lip length, and jaw curvature."),
        ("High Sensitivity to Pose", "Even a small head tilt or rotation dramatically altered calculated distances."),
        ("Expression Sensitivity", "Smiling, blinking, or talking changed feature coordinates and broke matching."),
        ("Lighting Vulnerability", "Shadows caused edge detectors to miss feature boundaries entirely."),
        ("Conclusion", "Complex, slow, and brittle for automated real-time recognition.")
    ]
    for title, desc in old_points:
        p = tf_old.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK
        p = tf_old.add_paragraph()
        p.text = f"  {desc}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    # Right: The Breakthrough (Holistic)
    c_new = add_card(s2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tf_new = c_new.text_frame
    tf_new.word_wrap = True
    p = tf_new.paragraphs[0]
    p.text = "The Turk & Pentland Breakthrough (1991)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD_ACCENT

    p = tf_new.add_paragraph()
    p.text = "Holistic Information-Theoretic Approach"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    new_points = [
        ("Treat Whole Image as a Pattern", "Does not isolate eyes, nose, or mouth. Analyzes the face as a single 2D brightness distribution."),
        ("Subspace Information Coding", "Captures features that best account for the variation across the entire collection of faces."),
        ("Dimensionality Reduction", "Projects high-dimensional image space onto a tiny subspace spanning only the prominent variations."),
        ("Real-Time Execution", "Recognition reduces to a simple Euclidean distance calculation among a few dozen scalar weights."),
        ("Foundational Landmark", "Established the principle of appearance-based subspace learning in computer vision.")
    ]
    for title, desc in new_points:
        p = tf_new.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK
        p = tf_new.add_paragraph()
        p.text = f"  {desc}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 3: Mathematical Pipeline: Vectorization & Mean Centering
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "Mathematical Subspace: Image Vectorization & Mean Face")

    cards = [
        ("1. Image Vectorization",
         "From 2D Pixel Grid to High-Dimensional Vector",
         [
             "• Standard image dimensions: N × N = 64 × 64 pixels.",
             "• Unrolled into a single column vector: Γ ∈ ℝ^D, where D = 4,096.",
             "• Pixel values are normalized grayscale intensities in range [0, 1].",
             "• Every face is treated as a single point in a 4,096-dimensional space."
         ], Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), NAVY_ACCENT),

        ("2. The Average Face (Ψ)",
         "Capturing the Shared Baseline Geometry",
         [
             "• Mathematical definition:",
             "    Ψ = (1 / M) Σ Γ_i   (for i = 1 to M)",
             "• Captures common structural features shared across all human subjects (eyes, nose, forehead placement).",
             "• Visually appears as a smooth, blurry composite face.",
             "• Serves as the origin of the centered face coordinate system."
         ], Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4), AMBER_ACCENT),

        ("3. Mean-Centered Matrix (A)",
         "Isolating Distinguishing Variations",
         [
             "• Subtract the mean from each face:",
             "    Φ_i = Γ_i - Ψ",
             "• Removes common baseline; preserves only individual distinctiveness.",
             "• Stack centered vectors into matrix A:",
             "    A = [Φ_1, Φ_2, ..., Φ_M] ∈ ℝ^(D × M)",
             "• With D = 4,096 and M = 245, A is a 4,096 × 245 matrix."
         ], Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.4), EMERALD_ACCENT),
    ]

    for title, subtitle, bullets, left, top, width, height, accent in cards:
        card = add_card(s3, left, top, width, height)
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = accent

        p = tf.add_paragraph()
        p.text = subtitle
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

        for b in bullets:
            p = tf.add_paragraph()
            p.text = b
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 4: The Turk-Pentland Shortcut (The Covariance Reduction Trick)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "The Turk-Pentland Dimensionality Reduction Trick")

    c_left = add_card(s4, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tf_l = c_left.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "The Computational Roadblock"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ROSE_ACCENT

    p = tf_l.add_paragraph()
    p.text = "Full Covariance Matrix: C = (1/M) A A^T"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    items_l = [
        ("Dimensionality Crisis", "A is 4,096 × 245. Thus, C = A A^T has dimensions 4,096 × 4,096."),
        ("Massive Matrix Size", "Contains 4,096² = 16,777,216 floating-point values (~134 MB memory footprint)."),
        ("Cubic Complexity", "Computing eigenvectors of a 4,096 × 4,096 matrix requires O(D³) operations—intractable for real-time deployment."),
        ("Rank Deficiency", "Because we only have M = 245 sample images, the maximum rank of C is at most M - 1 = 244."),
        ("Redundant Computation", "Over 3,850 of the 4,096 eigenvalues are exactly zero! Direct calculation computes thousands of meaningless zeros.")
    ]
    for t, d in items_l:
        p = tf_l.add_paragraph()
        p.text = f"• {t}:"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK
        p = tf_l.add_paragraph()
        p.text = f"  {d}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    c_right = add_card(s4, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tf_r = c_right.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "The Turk-Pentland Algebraic Duality"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD_ACCENT

    p = tf_r.add_paragraph()
    p.text = "Surrogate Matrix: L = A^T A (279.5× Smaller)"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    proof_steps = [
        ("1. Compute Surrogate Matrix L", "L = A^T A of size 245 × 245 (only 60,025 elements)."),
        ("2. Solve Small Eigenproblem", "Let v_k be an eigenvector of L with eigenvalue μ_k:\n    A^T A v_k = μ_k v_k"),
        ("3. Pre-multiply Both Sides by A", "    A (A^T A v_k) = A (μ_k v_k)"),
        ("4. Re-associate Parentheses", "    (A A^T) (A v_k) = μ_k (A v_k)"),
        ("5. Exact Equivalence Established", "The vector u_k = A v_k is directly an eigenvector of the full covariance matrix C = A A^T!"),
        ("6. Orthonormalization", "Normalize to unit length: u_k = (A v_k) / ||A v_k||₂.")
    ]
    for t, d in proof_steps:
        p = tf_r.add_paragraph()
        p.text = f"• {t}:"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK
        p = tf_r.add_paragraph()
        p.text = f"  {d}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 5: How Eigenfaces Are Formed (The Recipe Behind Ghost Faces)
    # =========================================================================
    s5_form = prs.slides.add_slide(blank_layout)
    add_bg(s5_form)
    add_header(s5_form, "How Eigenfaces Are Formed: The Linear Combination Recipe")

    c1 = add_card(s5_form, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "1. Transforming Small Vectors Into Faces"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY_ACCENT

    p = tf_c1.add_paragraph()
    p.text = "Mathematical Recipe: u_k = A · v_k"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    form_steps = [
        ("The Eigenvector v_k as Blending Weights",
         "The small eigenvector v_k = [c₁, c₂, ..., c_M]^T contains M scalar numbers (one per training face). "
         "These numbers serve as mixing coefficients."),

        ("Linear Combination of All Training Faces",
         "Multiplying A by v_k produces:\n"
         "    u_k = Σ(i=1 to M) c_i · Φ_i\n"
         "In plain words: Eigenface k is formed by taking c₁ of Face 1, adding c₂ of Face 2, subtracting c₃ of Face 3, and so on across all 245 faces."),

        ("Why Do They Look Like 'Ghost' Faces?",
         "Because every Eigenface is literally a composite blending of 245 centered human faces. "
         "Adding and subtracting centered images reveals shared anatomical contours and lighting gradients while canceling individual skin textures.")
    ]
    for title, desc in form_steps:
        p = tf_c1.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK
        p = tf_c1.add_paragraph()
        p.text = f"  {desc}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    c2 = add_card(s5_form, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "2. Ordering by Variance & Feature Hierarchy"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = EMERALD_ACCENT

    p = tf_c2.add_paragraph()
    p.text = "Sorting Eigenfaces by Eigenvalues (λ₁ ≥ λ₂ ≥ ... ≥ λ_M)"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    hierarchy_steps = [
        ("Unit Normalization",
         "Each raw Eigenface is normalized to unit length:\n"
         "    u_k = u_k / ||u_k||₂\n"
         "Ensures all basis vectors form an orthonormal basis (u_i^T · u_j = 0 when i ≠ j)."),

        ("Eigenfaces 1 – 2 (Primary Illumination)",
         "Correspond to the largest eigenvalues. Capture the dominant global lighting directions (light from left vs. light from right)."),

        ("Eigenfaces 3 – 10 (Macro Facial Anatomy)",
         "Capture broad geometric variations: jawline width, forehead height, cheekbone structure, and hairline curvature."),

        ("Eigenfaces 11 – 40 (Micro Facial Features)",
         "Encode localized distinguishing traits: eye shapes, nose bridge contours, lip fullness, and eyebrows."),

        ("Eigenfaces 41+ (Noise & Redundancy)",
         "Represent negligible variance, pixel quantization noise, or camera artifacts—safely discarded during dimensionality reduction.")
    ]
    for title, desc in hierarchy_steps:
        p = tf_c2.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK
        p = tf_c2.add_paragraph()
        p.text = f"  {desc}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 6: Eigenfaces Gallery & Eigenvalue Spectrum
    # =========================================================================
    s6_vis = prs.slides.add_slide(blank_layout)
    add_bg(s6_vis)
    add_header(s6_vis, "Eigenfaces Gallery & Eigenvalue Spectrum Analysis")

    gallery_img = os.path.join(RESULTS_DIR, "01_eigenfaces_gallery.png")
    if os.path.exists(gallery_img):
        s6_vis.shapes.add_picture(gallery_img, Inches(0.8), Inches(1.45), Inches(5.6), Inches(4.2))

    c_gal = add_card(s6_vis, Inches(0.8), Inches(5.75), Inches(5.6), Inches(1.3))
    tf_g = c_gal.text_frame
    tf_g.word_wrap = True
    p = tf_g.paragraphs[0]
    p.text = "Visual Anatomy of Top 16 Eigenfaces"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_ACCENT
    p = tf_g.add_paragraph()
    p.text = "• The first 4 eigenfaces show strong left/right and top/bottom lighting gradients.\n• Components 5-16 reveal distinct eye socket hollows, nose bridges, and jaw shapes.\n• Each image is an orthonormal basis vector spanning the face subspace."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_DARK

    scree_img = os.path.join(RESULTS_DIR, "02_eigenvalue_scree_plot.png")
    if os.path.exists(scree_img):
        s6_vis.shapes.add_picture(scree_img, Inches(6.8), Inches(1.45), Inches(5.7), Inches(4.2))

    c_scr = add_card(s6_vis, Inches(6.8), Inches(5.75), Inches(5.7), Inches(1.3))
    tf_s = c_scr.text_frame
    tf_s.word_wrap = True
    p = tf_s.paragraphs[0]
    p.text = "Eigenvalue Spectrum (Scree Analysis)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = EMERALD_ACCENT
    p = tf_s.add_paragraph()
    p.text = "• Rapid exponential drop in eigenvalue magnitude confirms high data redundancy.\n• First 10 components account for ~65% of total dataset variance.\n• Top 40 components capture >88% of variance, discarding high-frequency noise."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 7: How Projection & Reconstruction Happen in Practice
    # =========================================================================
    s7_ops = prs.slides.add_slide(blank_layout)
    add_bg(s7_ops)
    add_header(s7_ops, "How Projection & Reconstruction Work in Practice")

    # Math Card Top
    c_math = add_card(s7_ops, Inches(0.8), Inches(1.4), Inches(11.73), Inches(1.55))
    tf_m = c_math.text_frame
    tf_m.word_wrap = True
    p = tf_m.paragraphs[0]
    p.text = "1. Projection (Encoding) vs. 2. Reconstruction (Synthesis)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_ACCENT

    p = tf_m.add_paragraph()
    p.text = "• How Projection Happens:  Ω = U_K^T · (Γ - Ψ) = [ω₁, ω₂, ..., ω_K]^T ∈ ℝ^K"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    p = tf_m.add_paragraph()
    p.text = "  To encode a new face Γ: (1) Subtract Average Face Ψ. (2) Take dot product with each Eigenface u_k to compute weight ω_k = u_k^T · (Γ - Ψ). This compresses 4,096 raw pixels into a tiny vector of K scalar weights (e.g. K = 40)."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_DARK

    p = tf_m.add_paragraph()
    p.text = "• How Reconstruction Happens:  Γ̂ = Ψ + U_K · Ω = Ψ + Σ(k=1 to K) ω_k · u_k"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    p = tf_m.add_paragraph()
    p.text = "  To rebuild the face: Start with Average Face Ψ, then add each Eigenface scaled by its weight. Layer by layer, the unique face reappears."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_DARK

    recon_img = os.path.join(RESULTS_DIR, "03_face_reconstruction.png")
    if os.path.exists(recon_img):
        s7_ops.shapes.add_picture(recon_img, Inches(0.8), Inches(3.1), Inches(11.73), Inches(4.1))

    # =========================================================================
    # SLIDE 8: How the 4-Way Decision Rule Works in Practice
    # =========================================================================
    s8_dec = prs.slides.add_slide(blank_layout)
    add_bg(s8_dec)
    add_header(s8_dec, "How Classification Happens: The 4-Way Decision Rule")

    c_dist = add_card(s8_dec, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.7))
    tf_d = c_dist.text_frame
    tf_d.word_wrap = True
    p = tf_d.paragraphs[0]
    p.text = "The Two Fundamental Questions & Distances"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY_ACCENT

    p = tf_d.add_paragraph()
    p.text = "Why naive nearest-neighbor fails on non-faces / strangers"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    decision_items = [
        ("Question 1: 'Is this input a human face?'",
         "Tested via Distance From Face Space (DFFS, ε_d):\n"
         "    ε_d = ||Γ - Γ̂||₂ (Reconstruction Residual)\n"
         "Because Eigenfaces are derived solely from human faces, they CANNOT accurately reconstruct arbitrary objects (e.g. coffee mug, dog, checkerboard). "
         "If ε_d ≥ θ_f: The system immediately rejects: REJECTED (NOT A FACE)."),

        ("Question 2: 'If it is a face, whose face is it?'",
         "Tested via Distance In Face Space (DIFS, ε_c):\n"
         "    ε_c = min_k ||Ω - Ω_k||₂ (Subspace Euclidean Distance)\n"
         "We measure the distance between the probe's weight vector Ω and the enrolled class centroids Ω_k."),

        ("Case 2: Known Enrolled Subject",
         "If ε_d < θ_f AND ε_c < θ_c:\n"
         "Matched to enrolled class with minimal distance → RECOGNIZED (KNOWN FACE)."),

        ("Case 3: Unseen Human Stranger (Open-Set)",
         "If ε_d < θ_f AND ε_c ≥ θ_c:\n"
         "Confirmed human face, but exceeds threshold for all known users → DETECTED (UNKNOWN VISITOR). Enables automated biometric enrollment.")
    ]
    for title, desc in decision_items:
        p = tf_d.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK
        p = tf_d.add_paragraph()
        p.text = f"  {desc}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    dec_img = os.path.join(RESULTS_DIR, "04_decision_space_geometry.png")
    if os.path.exists(dec_img):
        s8_dec.shapes.add_picture(dec_img, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.7))

    # =========================================================================
    # SLIDE 9: Experimental Setup & Dataset Split
    # =========================================================================
    s9_setup = prs.slides.add_slide(blank_layout)
    add_bg(s9_setup)
    add_header(s9_setup, "Experimental Setup & Open-Set Evaluation Protocol")

    setup_cards = [
        ("The AT&T / Olivetti Dataset",
         "400 Normalized Facial Images",
         [
             "• 40 distinct individuals (subjects s1 through s40).",
             "• 10 images per subject under controlled conditions.",
             "• Variations: Minor tilt, lighting changes, facial expressions (open/closed eyes, smiling), eyeglasses.",
             "• Normalized dimensions: 64 × 64 pixels (grayscale)."
         ], Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), NAVY_ACCENT),

        ("Open-Set Subspace Partition",
         "Gallery, Known Probes & Unseen Subjects",
         [
             "• Enrolled Subjects (35 individuals):",
             "    - 7 images/subject for training (M = 245 gallery faces).",
             "    - 3 images/subject for testing (105 known probes).",
             "",
             "• Unseen / Open-Set Subjects (5 individuals):",
             "    - Completely held out from training (50 unknown faces).",
             "    - Tests false acceptance vs valid stranger enrollment."
         ], Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4), AMBER_ACCENT),

        ("Synthetic Non-Face Benchmark",
         "Testing False Positive Rejection",
         [
             "• 20 synthetic non-face test images generated:",
             "    - Regular checkerboards of varying frequencies.",
             "    - High-frequency Gaussian white noise.",
             "    - Uniform black / white / gradient fields.",
             "",
             "• Purpose: Verifies whether DFFS threshold (θ_f) properly rejects non-face objects rather than assigning a random identity."
         ], Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.4), ROSE_ACCENT),
    ]

    for title, subtitle, bullets, left, top, width, height, accent in setup_cards:
        card = add_card(s9_setup, left, top, width, height)
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = accent

        p = tf.add_paragraph()
        p.text = subtitle
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

        for b in bullets:
            p = tf.add_paragraph()
            p.text = b
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 10: Empirical Results & Performance Benchmark
    # =========================================================================
    s10_res = prs.slides.add_slide(blank_layout)
    add_bg(s10_res)
    add_header(s10_res, "Empirical Results: Accuracy, Compression & Robustness")

    acc_img = os.path.join(RESULTS_DIR, "06_accuracy_vs_k.png")
    if os.path.exists(acc_img):
        s10_res.shapes.add_picture(acc_img, Inches(0.8), Inches(1.45), Inches(5.6), Inches(4.2))

    c_acc = add_card(s10_res, Inches(0.8), Inches(5.75), Inches(5.6), Inches(1.3))
    tf_a = c_acc.text_frame
    tf_a.word_wrap = True
    p = tf_a.paragraphs[0]
    p.text = "Recognition Accuracy vs Number of Components (K)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_ACCENT
    p = tf_a.add_paragraph()
    p.text = "• Accuracy rises sharply from 62% at K = 2 to >88% at K = 25.\n• Plateaus between K = 35 and K = 50 at ~90% accuracy.\n• Higher components add marginal discriminative power while capturing noise."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_DARK

    rob_img = os.path.join(RESULTS_DIR, "05_robustness_analysis.png")
    if os.path.exists(rob_img):
        s10_res.shapes.add_picture(rob_img, Inches(6.8), Inches(1.45), Inches(5.7), Inches(4.2))

    c_rob = add_card(s10_res, Inches(6.8), Inches(5.75), Inches(5.7), Inches(1.3))
    tf_r = c_rob.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Noise Perturbation & Occlusion Tolerance"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = EMERALD_ACCENT
    p = tf_r.add_paragraph()
    p.text = "• System remains stable under moderate Gaussian noise (σ ≤ 0.15).\n• Reconstructive projection acts as an intrinsic low-pass filter.\n• Degrades gracefully under center occlusions up to 25% area."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 11: Comparative Evolution: 1991 to Present
    # =========================================================================
    s11_comp = prs.slides.add_slide(blank_layout)
    add_bg(s11_comp)
    add_header(s11_comp, "Comparative Analysis: Evolution of Face Recognition")

    cols = [
        ("1. Eigenfaces (PCA)",
         "Turk & Pentland (1991)",
         [
             "• Paradigm: Unsupervised linear dimensionality reduction.",
             "• Objective: Maximizes total variance across all images.",
             "• Training Speed: Instantaneous (~0.14 s on CPU).",
             "• Data Required: 5–10 samples per subject.",
             "• Strengths: Mathematically transparent, lightweight, zero GPU needed.",
             "• Weakness: Sensitive to extreme illumination and pose changes."
         ], Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.4), NAVY_ACCENT),

        ("2. Fisherfaces (LDA)",
         "Belhumeur et al. (1997)",
         [
             "• Paradigm: Supervised linear discriminant analysis.",
             "• Objective: Maximizes between-class scatter while minimizing within-class scatter.",
             "• Training Speed: Very fast (<1 s).",
             "• Illumination Invariance: Discards top 3 eigenvectors to eliminate lighting variations.",
             "• Strengths: More robust to shadows and lighting than standard PCA.",
             "• Weakness: Suffers from Small Sample Size (SSS) problem if M < D."
         ], Inches(4.8), Inches(1.5), Inches(3.6), Inches(5.4), AMBER_ACCENT),

        ("3. Deep Embeddings",
         "FaceNet / ArcFace (2015+)",
         [
             "• Paradigm: Deep Convolutional Neural Networks (CNNs).",
             "• Objective: Non-linear metric learning on hyperspherical embeddings.",
             "• Training Speed: Compute-intensive (hours/days on GPU clusters).",
             "• Data Required: Millions of images (MS-Celeb-1M, VGGFace2).",
             "• Strengths: Invariant to extreme poses, occlusions, and expressions.",
             "• Weakness: Black-box nature, heavy computational demands."
         ], Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.4), EMERALD_ACCENT),
    ]

    for title, subtitle, bullets, left, top, width, height, accent in cols:
        card = add_card(s11_comp, left, top, width, height)
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = accent

        p = tf.add_paragraph()
        p.text = subtitle
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

        for b in bullets:
            p = tf.add_paragraph()
            p.text = b
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 12: Real-Time Demonstration Interfaces
    # =========================================================================
    s12_demo = prs.slides.add_slide(blank_layout)
    add_bg(s12_demo)
    add_header(s12_demo, "Demonstration Interfaces: CLI Benchmark & Web GUI")

    c_app = add_card(s12_demo, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    tf_app = c_app.text_frame
    tf_app.word_wrap = True
    p = tf_app.paragraphs[0]
    p.text = "Interactive Web Dashboard (app.py)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY_ACCENT

    p = tf_app.add_paragraph()
    p.text = "Live Interactive Demonstration Interface"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    app_features = [
        ("Live Probe Classification", "Clickable gallery of enrolled subjects, open-set strangers, and synthetic non-faces."),
        ("Visual Status Banners", "Instant color-coded decision outcomes:\n  • Green: Recognized Enrolled Subject\n  • Blue: Detected Unenrolled Stranger\n  • Red: Rejected Non-Face Pattern"),
        ("Face Reconstruction Lab", "Interactive slider dynamically adjusts K ∈ [1, 50], visually showing facial details emerging in real time."),
        ("Dual Metric Gauges", "Real-time readout of ε_d (DFFS) and ε_c (DIFS) against calibrated thresholds θ_f and θ_c.")
    ]
    for title, desc in app_features:
        p = tf_app.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK
        p = tf_app.add_paragraph()
        p.text = f"  {desc}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    c_cli = add_card(s12_demo, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tf_cli = c_cli.text_frame
    tf_cli.word_wrap = True
    p = tf_cli.paragraphs[0]
    p.text = "Automated Terminal Benchmark (demo.py)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD_ACCENT

    p = tf_cli.add_paragraph()
    p.text = "End-to-End Command-Line Pipeline"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    cli_features = [
        ("Pure NumPy Architecture", "100% from-scratch linear algebra without scikit-learn PCA black-boxes."),
        ("Diagnostic Telemetry", "Outputs detailed matrix dimensions, reduction factors (279.5×), and eigen-decomposition timings."),
        ("Automated Evaluation", "Executes 4-way decision matrix across all probe sets and outputs confusion statistics."),
        ("Publication-Grade Plots", "Automatically generates all 6 analytical figures in the results/ directory.")
    ]
    for title, desc in cli_features:
        p = tf_cli.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK
        p = tf_cli.add_paragraph()
        p.text = f"  {desc}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 13: Summary & Academic Takeaways
    # =========================================================================
    s13_conc = prs.slides.add_slide(blank_layout)
    add_bg(s13_conc, NAVY_DARK)

    top_b = s13_conc.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    top_b.fill.solid()
    top_b.fill.fore_color.rgb = CYAN_ACCENT
    top_b.line.fill.background()

    t_box = s13_conc.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(1.1))
    tf = t_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Summary of Contributions & Academic Takeaways"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    p = tf.add_paragraph()
    p.text = "Eigenfaces (Turk & Pentland, 1991) Implementation"
    p.font.size = Pt(14)
    p.font.color.rgb = CYAN_ACCENT

    c_conc = add_card(s13_conc, Inches(1.0), Inches(2.1), Inches(11.33), Inches(4.7), NAVY_CARD, NAVY_ACCENT)
    tf_c = c_conc.text_frame
    tf_c.word_wrap = True

    conclusions = [
        ("1. Mathematical Rigor", "Implemented exact PCA and Turk-Pentland surrogate trick (L = A^T A) using pure linear algebra in NumPy, reducing computation by 279.5×."),
        ("2. High Compression Ratio", "Compressed 4,096-pixel facial images into 40 scalar weights (99.02% reduction) while preserving ~90% recognition accuracy."),
        ("3. Complete 4-Way Decision Framework", "Dual thresholds (θ_f and θ_c) accurately discriminate between enrolled subjects, unknown human strangers, and non-face objects."),
        ("4. Edge Computing Suitability", "Instantaneous CPU training (~0.14 s) and microsecond inference make it ideal for embedded biometric IoT devices."),
        ("5. Open-Source Verification", "Fully reproducible codebase with CLI benchmarks, interactive GUI dashboard, and comprehensive test suite.")
    ]

    for title, desc in conclusions:
        p = tf_c.add_paragraph()
        p.text = f"•  {title}:"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = AMBER_ACCENT

        p = tf_c.add_paragraph()
        p.text = f"   {desc}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_WHITE

    p_end = tf_c.add_paragraph()
    p_end.text = "\nThank You! Ready for Questions & Discussion."
    p_end.font.size = Pt(16)
    p_end.font.bold = True
    p_end.font.color.rgb = CYAN_ACCENT
    p_end.alignment = PP_ALIGN.CENTER

    prs.save(OUTPUT_PPTX)
    print(f"Presentation saved successfully to: {OUTPUT_PPTX}")


if __name__ == "__main__":
    build_deck()
