"""
Mock Test PDF Exporter — generates a realistic exam paper layout
with cover page, instructions, section-wise questions, and answer key.
"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    KeepTogether,
)
from reportlab.lib import colors
from config import GeneratedQuestion


def export_mock_test_pdf(
    questions: list[GeneratedQuestion],
    exam_name: str = "RBI Grade B",
    set_number: int = 1,
    time_minutes: int = 120,
    marks_per_question: float = 1.0,
    negative_marking: float = 0.25,
) -> bytes:
    """Generate a mock test PDF laid out like an actual exam paper.

    Args:
        questions: List of generated questions (in order).
        exam_name: Exam title for the cover page.
        set_number: Mock test set number.
        time_minutes: Total time allowed.
        marks_per_question: Marks for each correct answer.
        negative_marking: Marks deducted for wrong answer.

    Returns:
        PDF file as bytes.
    """
    if not questions:
        raise ValueError("Cannot generate a mock test PDF with zero questions.")

    output = io.BytesIO()
    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=20 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    cover_title = ParagraphStyle(
        "CoverTitle", parent=styles["Title"],
        fontSize=26, textColor=HexColor("#1a237e"),
        alignment=TA_CENTER, spaceAfter=8,
    )
    cover_sub = ParagraphStyle(
        "CoverSub", parent=styles["Heading2"],
        fontSize=16, textColor=HexColor("#37474f"),
        alignment=TA_CENTER, spaceAfter=6,
    )
    section_heading = ParagraphStyle(
        "SectionHeading", parent=styles["Heading2"],
        fontSize=15, textColor=HexColor("#ffffff"),
        alignment=TA_CENTER, spaceBefore=12, spaceAfter=6,
        backColor=HexColor("#1a237e"),
        borderPadding=(6, 8, 6, 8),
    )
    q_number_style = ParagraphStyle(
        "QNumber", parent=styles["Normal"],
        fontSize=10, textColor=HexColor("#1a237e"),
        fontName="Helvetica-Bold", spaceAfter=2,
    )
    q_text_style = ParagraphStyle(
        "QText", parent=styles["Normal"],
        fontSize=10, leading=14, spaceAfter=4,
        alignment=TA_JUSTIFY,
    )
    option_style = ParagraphStyle(
        "Option", parent=styles["Normal"],
        fontSize=9.5, leading=13, leftIndent=15, spaceAfter=1,
    )
    instr_style = ParagraphStyle(
        "Instruction", parent=styles["Normal"],
        fontSize=10, leading=14, spaceAfter=4,
    )
    instr_bold = ParagraphStyle(
        "InstrBold", parent=styles["Normal"],
        fontSize=10, leading=14, fontName="Helvetica-Bold",
        spaceAfter=4,
    )
    answer_style = ParagraphStyle(
        "Answer", parent=styles["Normal"],
        fontSize=9, leading=12,
    )
    heading_style = ParagraphStyle(
        "AnswerHeading", parent=styles["Heading2"],
        fontSize=16, textColor=HexColor("#1a237e"),
        spaceBefore=10, spaceAfter=8,
    )
    explanation_style = ParagraphStyle(
        "Explanation", parent=styles["Normal"],
        fontSize=8.5, leading=11, textColor=HexColor("#555555"),
        leftIndent=15,
    )

    elements = []

    # ── Cover Page ──────────────────────────────────────────────────
    elements.append(Spacer(1, 60))
    elements.append(Paragraph(f"{exam_name}", cover_title))
    elements.append(Paragraph(f"Predicted Mock Test — Set {set_number}", cover_sub))
    elements.append(Spacer(1, 20))

    # Summary box
    total_marks = len(questions) * marks_per_question
    sections_in_test = sorted(set(q.section for q in questions))
    section_counts = {}
    for q in questions:
        section_counts[q.section] = section_counts.get(q.section, 0) + 1

    summary_data = [
        ["Total Questions", str(len(questions))],
        ["Total Marks", str(int(total_marks))],
        ["Duration", f"{time_minutes} minutes"],
        ["Marking Scheme", f"+{marks_per_question} / −{negative_marking}"],
        ["Sections", str(len(sections_in_test))],
    ]
    for sec in sections_in_test:
        summary_data.append([f"  {sec}", f"{section_counts[sec]} Qs"])

    summary_table = Table(summary_data, colWidths=[200, 200])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), HexColor("#e8eaf6")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#c5cae9")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(summary_table)

    elements.append(PageBreak())

    # ── Instructions Page ───────────────────────────────────────────
    elements.append(Paragraph("General Instructions", heading_style))
    instructions = [
        f"1. This test contains <b>{len(questions)}</b> questions across "
        f"<b>{len(sections_in_test)}</b> section(s).",
        f"2. Total time allowed: <b>{time_minutes} minutes</b>.",
        f"3. Each correct answer carries <b>+{marks_per_question}</b> mark(s).",
        f"4. Each wrong answer carries a penalty of <b>−{negative_marking}</b> mark(s).",
        "5. There is <b>no penalty</b> for unanswered questions.",
        "6. Use of calculators is <b>NOT</b> permitted.",
        "7. Read each question carefully before answering.",
        "8. For Data Interpretation / Puzzle sets, the common data is provided "
        "before the questions — all questions in a set refer to the same data.",
        "9. Mark your answers clearly. Only one option is correct per question.",
        "10. Answer key and explanations are provided at the end of this paper.",
    ]
    for inst in instructions:
        elements.append(Paragraph(inst, instr_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "⏱ Suggested time allocation per section:",
        instr_bold,
    ))
    if time_minutes > 0 and section_counts:
        for sec in sections_in_test:
            sec_time = round(time_minutes * section_counts[sec] / len(questions))
            elements.append(Paragraph(
                f"  • {sec}: ~{sec_time} minutes ({section_counts[sec]} Qs)",
                instr_style,
            ))

    elements.append(PageBreak())

    # ── Questions ───────────────────────────────────────────────────
    q_number = 0
    current_section = None

    for q in questions:
        # Section header when section changes
        if q.section != current_section:
            current_section = q.section
            sec_count = section_counts.get(current_section, 0)
            # Section header as a colored table row
            sec_header_data = [[
                Paragraph(
                    f"{current_section}  ({sec_count} Questions)",
                    ParagraphStyle("SH", parent=styles["Normal"],
                                   fontSize=13, fontName="Helvetica-Bold",
                                   textColor=colors.white, alignment=TA_CENTER),
                )
            ]]
            sec_table = Table(sec_header_data, colWidths=[doc.width])
            sec_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#1a237e")),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]))
            elements.append(Spacer(1, 10))
            elements.append(sec_table)
            elements.append(Spacer(1, 8))

        q_number += 1

        # Question block (keep together to avoid page-split mid-question)
        q_elements = []
        q_elements.append(Paragraph(
            f"<b>Q.{q_number}</b>  <font size='8' color='#888888'>[{q.topic}]</font>",
            q_number_style,
        ))

        # Clean the question text for PDF (escape XML special chars)
        q_text = _escape_xml(q.text)
        q_elements.append(Paragraph(q_text, q_text_style))

        # Options
        for opt in q.options:
            q_elements.append(Paragraph(_escape_xml(str(opt)), option_style))
        q_elements.append(Spacer(1, 6))

        elements.append(KeepTogether(q_elements))

    elements.append(PageBreak())

    # ── Answer Key ──────────────────────────────────────────────────
    elements.append(Paragraph("Answer Key", heading_style))

    # Compact answer grid
    answer_letters = []
    for i, q in enumerate(questions, 1):
        letter = chr(ord('a') + q.correct_answer) if 0 <= q.correct_answer < len(q.options) else '?'
        answer_letters.append(f"Q.{i}: ({letter})")

    # Layout as a table grid (10 columns)
    cols = 5
    grid_rows = []
    row = []
    for i, a in enumerate(answer_letters):
        row.append(a)
        if len(row) >= cols:
            grid_rows.append(row)
            row = []
    if row:
        row.extend([""] * (cols - len(row)))
        grid_rows.append(row)

    if grid_rows:
        answer_table = Table(grid_rows, colWidths=[doc.width / cols] * cols)
        answer_table.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.3, HexColor("#cccccc")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f5f5f5")),
        ]))
        elements.append(answer_table)

    elements.append(PageBreak())

    # ── Detailed Solutions ──────────────────────────────────────────
    elements.append(Paragraph("Detailed Solutions", heading_style))

    for i, q in enumerate(questions, 1):
        letter = chr(ord('a') + q.correct_answer) if 0 <= q.correct_answer < len(q.options) else '?'
        sol_block = []
        sol_block.append(Paragraph(
            f"<b>Q.{i}</b> [{q.topic}] — Answer: <b>({letter})</b>",
            answer_style,
        ))
        if q.explanation:
            sol_block.append(Paragraph(
                _escape_xml(q.explanation),
                explanation_style,
            ))
        sol_block.append(Spacer(1, 4))
        elements.append(KeepTogether(sol_block))

    # Build PDF
    doc.build(elements)
    return output.getvalue()


def _escape_xml(text: str) -> str:
    """Escape XML special characters for ReportLab Paragraph."""
    if not text:
        return ""
    return (
        str(text).replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
