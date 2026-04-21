"""
PDF Report Exporter — generates a formatted PDF report using reportlab.
"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)
from reportlab.lib import colors
import pandas as pd
from config import CategorizedQuestion
from analyzers.frequency import build_frequency_matrix
from analyzers.trends import analyze_trends
from analyzers.predictor import predict_topic_distribution


def export_to_pdf(
    categorized: list[CategorizedQuestion],
    predictions: list[dict] | None = None,
    sample_questions: dict[str, list[str]] | None = None,
    exam_name: str = "Exam",
) -> bytes:
    """
    Generate a formatted PDF report.

    Returns:
        PDF file contents as bytes
    """
    output = io.BytesIO()
    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=25 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=HexColor("#1a237e"),
        spaceAfter=20,
    )
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=16,
        textColor=HexColor("#283593"),
        spaceBefore=20,
        spaceAfter=10,
    )
    subheading_style = ParagraphStyle(
        "CustomSubHeading",
        parent=styles["Heading3"],
        fontSize=13,
        textColor=HexColor("#3949ab"),
        spaceBefore=12,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        spaceAfter=6,
    )
    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
    )

    elements = []

    # --- Title Page ---
    elements.append(Spacer(1, 80))
    elements.append(Paragraph(f"{exam_name}", title_style))
    elements.append(Paragraph("Previous Year Paper Analysis Report", heading_style))

    years = sorted(set(cq.question.year for cq in categorized))
    elements.append(Paragraph(
        f"Based on {len(categorized)} questions from {len(years)} years "
        f"({years[0]}–{years[-1]})" if years else "No data",
        body_style,
    ))
    elements.append(PageBreak())

    # --- Executive Summary ---
    elements.append(Paragraph("Executive Summary", heading_style))

    freq = build_frequency_matrix(categorized, group_by="topic")
    trends = analyze_trends(categorized)

    sections = set(cq.section for cq in categorized)
    topics = set(cq.topic for cq in categorized)

    elements.append(Paragraph(
        f"This report analyzes <b>{len(categorized)}</b> questions from "
        f"<b>{len(years)}</b> years of {exam_name} papers, covering "
        f"<b>{len(sections)}</b> sections and <b>{len(topics)}</b> topics.",
        body_style,
    ))

    elements.append(Paragraph(
        f"<b>Difficulty Trend:</b> {trends.get('difficulty_trend', 'N/A')}",
        body_style,
    ))

    # Top 5 topics summary
    if not freq.empty:
        elements.append(Paragraph("Top 5 High-Probability Topics:", subheading_style))
        for i, (idx, row) in enumerate(freq.head(5).iterrows()):
            section, topic = idx
            elements.append(Paragraph(
                f"{i+1}. <b>{topic}</b> ({section}) — "
                f"Score: {row['ProbabilityScore']:.0f}, "
                f"Total: {int(row['Total'])} Qs, "
                f"Consistency: {row['ConsistencyPct']:.0f}%",
                body_style,
            ))

    elements.append(PageBreak())

    # --- Frequency Matrix Table ---
    elements.append(Paragraph("Topic Frequency Matrix", heading_style))

    if not freq.empty:
        year_cols = [c for c in freq.columns if c.isdigit()]
        display_cols = year_cols + ["Total", "Percentage", "ProbabilityScore"]

        # Build table data
        table_data = [["Section", "Topic"] + display_cols]
        for (section, topic), row in freq.iterrows():
            table_row = [
                Paragraph(section, small_style),
                Paragraph(topic, small_style),
            ]
            for col in display_cols:
                val = row[col]
                if col == "Percentage":
                    table_row.append(f"{val:.1f}%")
                elif col == "ProbabilityScore":
                    table_row.append(f"{val:.0f}")
                else:
                    table_row.append(str(int(val)))
            table_data.append(table_row)

        col_widths = [70, 90] + [40] * len(display_cols)
        # Ensure total width fits page
        total_width = sum(col_widths)
        page_width = A4[0] - 40 * mm
        if total_width > page_width:
            scale = page_width / total_width
            col_widths = [w * scale for w in col_widths]

        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a237e")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (2, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#f5f5f5")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        elements.append(table)

    elements.append(PageBreak())

    # --- Trend Analysis ---
    elements.append(Paragraph("Trend Analysis", heading_style))

    if trends.get("rising_topics"):
        elements.append(Paragraph("Rising Topics (increasing frequency):", subheading_style))
        for t in trends["rising_topics"][:5]:
            elements.append(Paragraph(
                f"• {t['section']} > <b>{t['topic']}</b> — "
                f"Change: {t['change_pct']:+.0f}%",
                body_style,
            ))

    if trends.get("falling_topics"):
        elements.append(Paragraph("Falling Topics (decreasing frequency):", subheading_style))
        for t in trends["falling_topics"][:5]:
            elements.append(Paragraph(
                f"• {t['section']} > <b>{t['topic']}</b> — "
                f"Change: {t['change_pct']:+.0f}%",
                body_style,
            ))

    if trends.get("new_topics"):
        elements.append(Paragraph("New Topics (appeared only recently):", subheading_style))
        for t in trends["new_topics"]:
            elements.append(Paragraph(
                f"• {t['section']} > <b>{t['topic']}</b> ({t['count']} questions)",
                body_style,
            ))

    elements.append(PageBreak())

    # --- Predictions ---
    if predictions:
        elements.append(Paragraph("Predicted Topic Distribution", heading_style))
        elements.append(Paragraph(
            "Based on historical frequency, consistency, and recent trends:",
            body_style,
        ))

        pred_data = [["Rank", "Section", "Topic", "Expected Qs", "Score", "Trend"]]
        for i, p in enumerate(predictions[:15], 1):
            pred_data.append([
                str(i),
                p["section"],
                p["topic"],
                str(p["predicted_count"]),
                f"{p['probability_score']:.0f}",
                p["trend"],
            ])

        pred_table = Table(pred_data, colWidths=[30, 100, 110, 55, 45, 55], repeatRows=1)
        pred_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#548235")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#f5f5f5")]),
        ]))
        elements.append(pred_table)
        elements.append(PageBreak())

    # --- Sample Questions ---
    if sample_questions:
        elements.append(Paragraph("Sample Questions for Top Topics", heading_style))

        for key, questions in list(sample_questions.items())[:10]:
            elements.append(Paragraph(f"<b>{key}</b>", subheading_style))
            for i, q in enumerate(questions[:3], 1):
                # Truncate long questions
                q_display = q[:500] + "..." if len(q) > 500 else q
                elements.append(Paragraph(f"Q{i}: {q_display}", body_style))
            elements.append(Spacer(1, 10))

    # --- Study Priority ---
    elements.append(PageBreak())
    elements.append(Paragraph("Recommended Study Priority", heading_style))
    elements.append(Paragraph(
        "Based on the analysis, here is the recommended priority order for preparation:",
        body_style,
    ))

    if not freq.empty:
        for section_name in sorted(sections):
            section_topics = freq.loc[
                freq.index.get_level_values("section") == section_name
            ]
            if section_topics.empty:
                continue

            elements.append(Paragraph(f"<b>{section_name}</b>", subheading_style))
            for i, ((_, topic), row) in enumerate(section_topics.head(5).iterrows(), 1):
                priority = "MUST DO" if i <= 2 else ("HIGH" if i <= 4 else "MEDIUM")
                elements.append(Paragraph(
                    f"  {i}. [{priority}] {topic} — "
                    f"Probability: {row['ProbabilityScore']:.0f}, "
                    f"Consistency: {row['ConsistencyPct']:.0f}%",
                    body_style,
                ))

    # Build PDF
    doc.build(elements)
    return output.getvalue()
