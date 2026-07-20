"""Generate the REHS 2026 poster template (24x36 portrait, PowerPoint).

Layout follows the 2025 REHS poster (poster-bs/2025_REHS_presentation.pdf):
full-width horizontal bands, each with explanatory text on the left and
figures on the right -- NOT vertical columns.

Run:  python make_template.py
Out:  REHS2026-poster-template.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------------- palette
INK = RGBColor(0x1A, 0x1A, 0x1A)
NAVY = RGBColor(0x10, 0x2A, 0x54)
GREY = RGBColor(0x70, 0x70, 0x70)
BLUE_PANEL = RGBColor(0xDC, 0xE9, 0xF7)   # the light blue section bands
GREY_PANEL = RGBColor(0xE8, 0xE8, 0xE8)   # intro / abstract boxes
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LINK = RGBColor(0x1155, 0x00 + 0x77, 0xCC) if False else RGBColor(0x11, 0x55, 0xCC)

# ---------------------------------------------------------------- geometry
W, H = 24.0, 36.0
M = 0.6                                    # page margin
CW = W - 2 * M                             # content width

prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(H)
slide = prs.slides.add_slide(prs.slide_layouts[6])


def box(x, y, w, h, text, size, *, bold=False, color=INK, align=PP_ALIGN.LEFT,
        italic=False, space_after=8, line=1.1):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.margin_top = tf.margin_bottom = Inches(0.04)
    for i, chunk in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = chunk
        p.alignment = align
        p.space_after = Pt(space_after)
        p.line_spacing = line
        for r in p.runs:
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = color
            r.font.name = "Calibri"
    return tb


def rounded(x, y, w, h, fill):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y),
                               Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    s.line.fill.background()
    s.shadow.inherit = False
    s.adjustments[0] = 0.035          # gentle corner radius, like the 2025 poster
    return s


def framed(x, y, w, h, caption, size=15):
    """A figure placeholder with its caption underneath."""
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                               Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = WHITE
    s.line.color.rgb = GREY
    s.line.width = Pt(1)
    s.shadow.inherit = False
    box(x, y + h / 2 - 0.35, w, 0.7, "[ FIGURE ]", 16, color=GREY,
        align=PP_ALIGN.CENTER, italic=True, space_after=0)
    box(x, y + h + 0.04, w, 0.5, caption, size, color=INK, space_after=0)


def section(y, h, title, owner, body, figs, *, fill=BLUE_PANEL, refs=None):
    """A full-width band: title, text on the left, figures on the right."""
    rounded(M, y, CW, h, fill)
    box(M + 0.45, y + 0.18, CW - 0.9, 0.75, title, 38, bold=True, color=NAVY,
        space_after=0)
    box(M + 0.45, y + 0.95, CW - 0.9, 0.35, f"OWNER: {owner}", 17, bold=True,
        color=GREY, italic=True, space_after=0)
    tw = CW * 0.40
    box(M + 0.45, y + 1.35, tw, h - 2.05, body, 22, color=INK, space_after=7)
    if refs:
        box(M + 0.45, y + h - 0.58, tw, 0.45, refs, 18, color=LINK, space_after=0)
    fx = M + CW * 0.44
    fw = CW - (CW * 0.44) - 0.45
    for (rx, ry, rw, rh, cap) in figs:
        framed(fx + rx * fw, y + 1.35 + ry, rw * fw, rh, cap)


# ================================================================== header
box(M + 2.9, 0.25, CW - 5.8, 1.55,
    "AI-POWERED SUPPORT CHATBOT FOR HIGH-PERFORMANCE COMPUTING", 46,
    bold=True, color=INK, align=PP_ALIGN.CENTER, space_after=0, line=0.95)
box(M + 2.9, 1.88, CW - 5.8, 0.5,
    "BY STUDENT 1¹, STUDENT 2², STUDENT 3³, STUDENT 4⁴, "
    "STUDENT 5⁵, STUDENT 6⁶, STUDENT 7⁷", 27,
    bold=True, color=INK, align=PP_ALIGN.CENTER, space_after=0)
box(M + 2.9, 2.38, CW - 5.8, 0.4,
    "UNDER MENTORSHIP OF MOHAMMAD FIRAS SADA⁸", 24,
    bold=True, color=INK, align=PP_ALIGN.CENTER, space_after=0)
box(M + 2.9, 2.80, CW - 5.8, 0.7,
    "¹⁻⁷ [Your high schools, City, CA — one entry per student, "
    "matching the superscripts above];\n"
    "⁸ San Diego Supercomputer Center, University of California San Diego, "
    "La Jolla, CA 92093, USA", 16,
    color=INK, align=PP_ALIGN.CENTER, space_after=0)

# logo slots (drop real logos in on top of these)
for lx, cap in ((M + 0.1, "UCSD / SDSC\nlogo here"), (W - M - 2.6, "NRP\nlogo here")):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(lx), Inches(0.3),
                               Inches(2.5), Inches(2.5))
    s.fill.solid(); s.fill.fore_color.rgb = WHITE
    s.line.color.rgb = GREY; s.line.width = Pt(1); s.shadow.inherit = False
    box(lx, 1.35, 2.5, 0.8, cap, 15, color=GREY, align=PP_ALIGN.CENTER,
        italic=True, space_after=0)

# ==================================================== introduction | abstract
y = 3.55
hw = (CW - 0.4) / 2
rounded(M, y, hw, 3.7, GREY_PANEL)
box(M + 0.4, y + 0.18, hw - 0.8, 0.6, "INTRODUCTION", 34, bold=True, color=NAVY,
    space_after=0)
box(M + 0.4, y + 0.85, hw - 0.8, 2.7,
    "[OWNER: Student 7 — ~110 words]\n"
    "Set up the problem for someone who has never heard of NRP. What is the "
    "National Research Platform and who uses it? Why is finding an answer in "
    "technical documentation slow? What are large language models, and why "
    "can't you just ask ChatGPT about NRP? End on the gap your project fills.",
    22, color=INK)

rounded(M + hw + 0.4, y, hw, 3.7, GREY_PANEL)
box(M + hw + 0.8, y + 0.18, hw - 0.8, 0.6, "ABSTRACT", 34, bold=True,
    color=NAVY, space_after=0)
box(M + hw + 0.8, y + 0.85, hw - 0.8, 2.7,
    "[OWNER: Student 7 — ~110 words, five sentences, WRITTEN LAST]\n"
    "1 problem. 2 what we built. 3 how it works (retrieve, then generate). "
    "4 the result, with a real number from the evaluation. 5 what it means. "
    "Write this only after Student 6 has the evaluation number — an abstract "
    "without a number is just a description.",
    22, color=INK)

# ====================================================== 1. knowledge base
y = 7.40
section(y, 7.1, "BUILDING THE KNOWLEDGE BASE", "Students 1 & 2",
        "The chatbot's knowledge comes from the real NRP documentation, not "
        "from the language model's training.\n"
        "• [S1] Pages collected from the NRP docs, and how we cleaned them\n"
        "• [S1] Chunking: why we split pages into ~500-token pieces\n"
        "• [S2] Embeddings: text becomes numbers, similar meaning lands nearby\n"
        "• [S2] How search() returns the five closest chunks to a question",
        [(0.00, 0.0, 0.47, 2.5, "Figure 1. Ingest pipeline: docs → clean → chunk → embed → vector database."),
         (0.53, 0.0, 0.47, 2.5, "Figure 2. One example chunk, showing the text and its source URL."),
         (0.00, 2.9, 0.47, 2.1, "Figure 3. A real question and the three chunks retrieved for it."),
         (0.53, 2.9, 0.47, 2.1, "Figure 4. Table: pages collected, chunks produced, embedding model used.")],
        refs="References: https://nrp.ai/documentation/  |  https://docs.trychroma.com/")

# ====================================================== 2. RAG
y = 14.65
section(y, 7.1, "ANSWERING QUESTIONS WITH RAG", "Students 3 & 4",
        "Retrieval-Augmented Generation (RAG) puts the answer *into* the "
        "question before the model ever sees it.\n"
        "• [S3] The prompt: retrieved docs + question → a grounded answer\n"
        "• [S3] Why we tell the model to admit when the docs don't cover it\n"
        "• [S3] How each answer carries citations back to its NRP page\n"
        "• [S4] The interface: streaming answers, history, a sources list",
        [(0.00, 0.0, 0.47, 2.5, "Figure 5. The RAG loop: embed → search → build prompt → LLM → cited answer."),
         (0.53, 0.0, 0.47, 2.5, "Figure 6. The same question answered WITHOUT retrieval (wrong) and WITH it (correct)."),
         (0.00, 2.9, 1.00, 2.1, "Figure 7. The chatbot interface — a real question, a real answer, real citations. (Hero image: crop tight, pick a good question.)")],
        refs="References: Lewis et al., NeurIPS 2020  |  https://streamlit.io/")

# ====================================================== 3. deployment
y = 21.90
section(y, 5.6, "DEPLOYING ON THE NATIONAL RESEARCH PLATFORM", "Student 5",
        "The chatbot runs on the same cluster it answers questions about.\n"
        "• The path: browser → Ingress → Service → Pod → NRP LLM → back\n"
        "• Why the vector database lives on a PVC and survives a restart\n"
        "• Why the API token is a Secret, never baked into the image\n"
        "• The live public URL anyone can visit",
        [(0.00, 0.0, 0.47, 3.4, "Figure 8. System architecture on NRP: Ingress, Service, Pod, Secret, ConfigMap, PVC."),
         (0.53, 0.0, 0.47, 1.5, "Figure 9. kubectl get pods — the chatbot pod Running."),
         (0.53, 1.9, 0.47, 1.5, "Figure 10. QR code + live URL.")],
        refs="References: https://nrp.ai/  |  https://kubernetes.io/docs/")

# ====================================================== 4. evaluation
y = 27.65
section(y, 5.4, "EVALUATION: DOES IT WORK?", "Student 6",
        "We wrote 20 real NRP questions and graded every answer by hand.\n"
        "• Each question answered twice: once with retrieval, once without\n"
        "• The gap between those two scores is the evidence that RAG helps\n"
        "• Each miss classified: retrieval miss, or model miss\n"
        "• Limitations: 20 questions is a small set, and we wrote it",
        [(0.00, 0.0, 0.47, 3.4, "Figure 11. Score with retrieval vs. without — a bar chart beats a table."),
         (0.53, 0.0, 0.47, 3.4, "Figure 12. Breakdown of the failures: retrieval misses vs. model misses.")],
        refs="References: our evaluation set — eval/questions.jsonl in the project repo")

# ====================================================== 5. conclusions
y = 33.15
rounded(M, y, CW, 2.30, GREY_PANEL)
box(M + 0.45, y + 0.12, CW - 0.9, 0.55, "CONCLUSIONS & FUTURE WORK", 30,
    bold=True, color=NAVY, space_after=0)
cw2 = (CW - 1.4) / 2
box(M + 0.45, y + 0.68, cw2, 1.5,
    "[OWNER: Student 7 — 3 bullets]\n"
    "• What we built, and that it runs live on NRP\n"
    "• The one number showing retrieval helps\n"
    "• The most surprising thing we learned", 21, color=INK, space_after=3)
box(M + 0.45 + cw2 + 0.5, y + 0.68, cw2, 1.5,
    "FUTURE WORK\n"
    "• The improvement we would make first, and why\n"
    "• A capability we ran out of time for\n"
    "• How someone else could use or extend this", 21, color=INK,
    space_after=3)

box(M, H - 0.46, CW, 0.42,
    "ACKNOWLEDGMENTS: We thank the SDSC REHS program, the National Research "
    "Platform team, and our mentor.   Image credits: all figures and screenshots "
    "are our own unless credited beside the figure.", 15, color=GREY,
    align=PP_ALIGN.CENTER, space_after=0)

prs.save("REHS2026-poster-template.pptx")
print("wrote REHS2026-poster-template.pptx  (24 x 36 in, portrait, banded layout)")
