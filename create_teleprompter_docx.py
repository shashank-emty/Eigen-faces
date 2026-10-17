#!/usr/bin/env python3
"""
create_teleprompter_docx.py
Generates a clean, teleprompter-styled scrollable Word (.docx) document
with punchy, one-line-per-concept bullet points for presenting the Eigenfaces project.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUTPUT_DOCX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "EigenFaces_Teleprompter_Script.docx")


def create_document():
    doc = docx.Document()

    # Set margins for comfortable scrolling
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Helper colors
    NAVY = RGBColor(15, 23, 42)
    BLUE = RGBColor(37, 99, 235)
    GRAY = RGBColor(100, 116, 139)
    DARK = RGBColor(30, 41, 59)
    GREEN = RGBColor(16, 185, 129)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t = p_title.add_run("EIGENFACES PRESENTATION: TELEPROMPTER SCRIPT")
    run_t.font.name = "Arial"
    run_t.font.size = Pt(20)
    run_t.font.bold = True
    run_t.font.color.rgb = BLUE

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_s = p_sub.add_run("One-Line Speaking Prompts • Scroll As You Present")
    run_s.font.name = "Arial"
    run_s.font.size = Pt(12)
    run_s.font.italic = True
    run_s.font.color.rgb = GRAY

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Presentation sections
    slides_data = [
        (
            "SLIDE 1: TITLE & INTRODUCTION",
            [
                "Good morning respected lecturer and evaluators, my name is Shashank M T.",
                "Today I am presenting my project on Eigenfaces for Face Recognition, based on the landmark 1991 paper by Turk and Pentland.",
                "The entire system is built from scratch in Python using pure linear algebra without any machine learning shortcuts."
            ]
        ),
        (
            "SLIDE 2: MOTIVATION & THE PARADIGM SHIFT",
            [
                "Before 1991, computers tried measuring physical distances—like eye-to-eye width or nose length.",
                "That old geometric method failed whenever someone smiled, turned their head, or lighting changed.",
                "Turk and Pentland introduced a breakthrough: treat the entire face as a single 2D pattern of pixels.",
                "Because all human faces share basic structure, we only need to capture the differences that make each face unique."
            ]
        ),
        (
            "SLIDE 3: MATHEMATICAL SUBSPACE & MEAN FACE",
            [
                "Every 64 by 64 photo is flattened into a single column of 4,096 pixel numbers.",
                "We calculate the Average Face (Psi) by averaging all 245 training photos together.",
                "The Average Face acts as our baseline, capturing generic human anatomy.",
                "We subtract the Average Face from each photo so we are left with only distinctive individual variations."
            ]
        ),
        (
            "SLIDE 4: THE TURK-PENTLAND COVARIANCE SHORTCUT",
            [
                "To find the principal components, standard PCA requires a 4,096 by 4,096 covariance matrix.",
                "That matrix has 16.7 million numbers—which is computationally intractable on normal hardware.",
                "Since we only have 245 images, Turk and Pentland flipped the multiplication to a tiny 245 by 245 matrix.",
                "That surrogate matrix is 279.5 times smaller and solves in milliseconds.",
                "Multiplying the small eigenvectors by our data matrix recovers the exact eigenvectors of the giant matrix."
            ]
        ),
        (
            "SLIDE 5: HOW EIGENFACES ARE FORMED (THE GHOST FACE RECIPE)",
            [
                "Each small eigenvector is a recipe of 245 numbers telling us how much of each training face to blend.",
                "Multiplying by matrix A literally blends all 245 training faces together into one image.",
                "That is why Eigenfaces look like glowing, ghostly faces—they are composite blends of all human subjects.",
                "Eigenfaces 1 and 2 capture major lighting directions.",
                "Eigenfaces 3 to 10 capture broad facial shapes and jawlines.",
                "Eigenfaces 11 to 40 capture fine details like eyes, noses, and lips."
            ]
        ),
        (
            "SLIDE 6: EIGENFACES GALLERY & SCREE SPECTRUM",
            [
                "Here is our visual gallery of the top 16 ghost-like Eigenfaces.",
                "Our scree plot shows eigenvalues dropping exponentially.",
                "The first 40 Eigenfaces capture over 88% of all facial variation across the dataset.",
                "The remaining hundreds of components only contain camera noise and are safely discarded."
            ]
        ),
        (
            "SLIDE 7: PROJECTION & PROGRESSIVE RECONSTRUCTION",
            [
                "To encode a face, we take dot products with each Eigenface to get just 40 scalar weights (Omega).",
                "This achieves a 99% data compression—compressing 4,096 raw pixels into just 40 numbers.",
                "To rebuild the face, we start with the Average Face and add each Eigenface weighted by those numbers.",
                "With 2 Eigenfaces the reconstruction is blurry; by 40 Eigenfaces the person's face snaps into clear focus."
            ]
        ),
        (
            "SLIDE 8: THE 4-WAY DECISION RULE",
            [
                "Naive systems only do nearest-neighbor and falsely match non-faces to real people.",
                "Our system asks Question 1: 'Is it a human face?' by checking reconstruction error (epsilon_d).",
                "Because Eigenfaces only know how to build faces, random objects like cups or dogs produce huge errors and get rejected.",
                "Question 2: 'Who is it?' checks distance to known people in face space (epsilon_c).",
                "Zone 1 (Bottom-Left): Enrolled subject recognized successfully.",
                "Zone 2 (Top-Left): Human face detected, but an unseen stranger—triggering enrollment.",
                "Zone 3 (Top-Right): Not a face, completely far from all face space.",
                "Zone 4 (Bottom-Right): Not a face whose projection accidentally matched someone—safely rejected by epsilon_d."
            ]
        ),
        (
            "SLIDE 9: EXPERIMENTAL SETUP & DATASET",
            [
                "We evaluated using 400 facial images from the benchmark AT&T / Olivetti dataset.",
                "We partitioned 35 enrolled individuals (245 training images and 105 test probes).",
                "We reserved 5 individuals completely unseen (50 unknown faces) to evaluate stranger detection.",
                "We benchmarked 20 synthetic non-face patterns to verify false-positive rejection."
            ]
        ),
        (
            "SLIDE 10: EMPIRICAL RESULTS & ROBUSTNESS",
            [
                "Our classifier reaches approximately 90% recognition accuracy with just 40 Eigenfaces.",
                "Non-face rejection rate exceeds 85% with zero false rejections of real faces.",
                "The model is robust to moderate Gaussian noise and tolerates facial occlusions up to 25%."
            ]
        ),
        (
            "SLIDE 11: COMPARATIVE EVOLUTION (1991 TO PRESENT)",
            [
                "Eigenfaces (PCA, 1991) is unsupervised, maximizes total variance, and trains instantly in 0.14 seconds.",
                "Fisherfaces (LDA, 1997) was invented to discard lighting variations by maximizing between-class scatter.",
                "Modern Deep CNNs (FaceNet, 2015+) use deep neural networks for wild, uncontrolled selfies.",
                "Eigenfaces remains ideal for lightweight, privacy-preserving edge devices and embedded microcontrollers."
            ]
        ),
        (
            "SLIDE 12: DEMONSTRATION INTERFACES",
            [
                "We built an automated CLI benchmark script (demo.py) that runs diagnostics and generates publication figures.",
                "We also created an interactive Web Dashboard (app.py) running on localhost port 5050.",
                "The web dashboard shows real-time Green (Known), Blue (Stranger), and Red (Not a Face) decision banners."
            ]
        ),
        (
            "SLIDE 13: CONCLUSION & SUMMARY",
            [
                "In summary, we implemented an exact, from-scratch realization of Turk and Pentland's landmark 1991 paper.",
                "We achieved 99% data compression and ~90% accuracy using pure NumPy linear algebra.",
                "Thank you for your time and attention; I am now ready for your questions."
            ]
        ),
    ]

    for title, lines in slides_data:
        # Slide Header Banner
        p_hdr = doc.add_paragraph()
        p_hdr.paragraph_format.space_before = Pt(14)
        p_hdr.paragraph_format.space_after = Pt(4)
        p_hdr.paragraph_format.keep_with_next = True
        run_h = p_hdr.add_run(f"▶  {title}")
        run_h.font.name = "Arial"
        run_h.font.size = Pt(13)
        run_h.font.bold = True
        run_h.font.color.rgb = BLUE

        # Bullet lines
        for line in lines:
            p_line = doc.add_paragraph()
            p_line.paragraph_format.left_indent = Inches(0.25)
            p_line.paragraph_format.space_before = Pt(3)
            p_line.paragraph_format.space_after = Pt(4)
            p_line.paragraph_format.line_spacing = 1.15

            run_bullet = p_line.add_run("•  ")
            run_bullet.font.name = "Arial"
            run_bullet.font.size = Pt(11.5)
            run_bullet.font.bold = True
            run_bullet.font.color.rgb = GREEN

            run_text = p_line.add_run(line)
            run_text.font.name = "Arial"
            run_text.font.size = Pt(11.5)
            run_text.font.color.rgb = DARK

        # Small divider line
        p_div = doc.add_paragraph()
        p_div.paragraph_format.space_before = Pt(2)
        p_div.paragraph_format.space_after = Pt(8)
        run_d = p_div.add_run("―" * 45)
        run_d.font.color.rgb = GRAY
        run_d.font.size = Pt(8)

    doc.save(OUTPUT_DOCX)
    print(f"Teleprompter document created successfully: {OUTPUT_DOCX}")


if __name__ == "__main__":
    create_document()
