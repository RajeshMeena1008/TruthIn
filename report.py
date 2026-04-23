"""
report.py
Generates a downloadable PDF report using ReportLab or fpdf2.
Falls back to a text-based HTML pseudo-PDF if neither is available.
"""

import io
import datetime


def generate_pdf_report(food_name: str, nutrition: dict, score: int, classification: str, recommendations: list) -> bytes:
    """
    Generate a PDF report and return as bytes.
    Tries reportlab → fpdf2 → plain-text fallback.
    """
    try:
        return _generate_with_reportlab(food_name, nutrition, score, classification, recommendations)
    except ImportError:
        pass
    try:
        return _generate_with_fpdf(food_name, nutrition, score, classification, recommendations)
    except ImportError:
        pass
    return _generate_text_fallback(food_name, nutrition, score, classification, recommendations)


# ─── REPORTLAB ───────────────────────────────────────────────────────────────────
def _generate_with_reportlab(food_name, nutrition, score, classification, recommendations) -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.units import cm

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle("Title", parent=styles["Heading1"], fontSize=22, textColor=colors.HexColor("#00e5a0"), spaceAfter=4)
    story.append(Paragraph("🍎 FoodScan — Analysis Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.datetime.now().strftime('%B %d, %Y %H:%M')}", styles["Normal"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#333")))
    story.append(Spacer(1, 0.3*cm))

    # Product
    story.append(Paragraph(f"<b>Product:</b> {food_name}", styles["Normal"]))
    color_map = {"Healthy": "#00e5a0", "Moderate": "#ffd166", "Unhealthy": "#ff6b6b"}
    cls_color = color_map.get(classification, "#888")
    story.append(Paragraph(f'<b>Health Score:</b> <font color="{cls_color}"><b>{score}/100 — {classification}</b></font>', styles["Normal"]))
    story.append(Spacer(1, 0.4*cm))

    # Nutrition table
    story.append(Paragraph("<b>Nutrition Facts (per 100g)</b>", styles["Heading2"]))
    nutr_rows = [["Nutrient", "Value"]]
    key_map = {"calories": "Calories (kcal)", "fat": "Fat (g)", "sugar": "Sugar (g)",
               "protein": "Protein (g)", "sodium": "Sodium (mg)", "carbohydrates": "Carbohydrates (g)"}
    for k, label in key_map.items():
        val = nutrition.get(k, "N/A")
        nutr_rows.append([label, str(val)])

    t = Table(nutr_rows, colWidths=[9*cm, 7*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1e2330")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor("#00e5a0")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#161a23"), colors.HexColor("#1a1e2a")]),
        ("TEXTCOLOR", (0,1), (-1,-1), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#252b3b")),
        ("ROWHEIGHT", (0,0), (-1,-1), 22),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))

    # Recommendations
    if recommendations:
        story.append(Paragraph("<b>Recommendations</b>", styles["Heading2"]))
        for r in recommendations:
            story.append(Paragraph(f"• {r}", styles["Normal"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("<i>FoodScan— Powered by Deep Learning & OpenFoodFacts</i>", styles["Normal"]))

    doc.build(story)
    return buf.getvalue()


# ─── FPDF2 ───────────────────────────────────────────────────────────────────────
def _generate_with_fpdf(food_name, nutrition, score, classification, recommendations) -> bytes:
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(0, 229, 160)
    pdf.cell(0, 10, "FoodScan— Analysis Report", ln=True)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 6, f"Generated: {datetime.datetime.now().strftime('%B %d, %Y %H:%M')}", ln=True)
    pdf.ln(4)

    pdf.set_text_color(220, 220, 220)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"Product: {food_name}", ln=True)
    pdf.cell(0, 8, f"Health Score: {score}/100 — {classification}", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Nutrition Facts (per 100g):", ln=True)
    pdf.set_font("Helvetica", "", 10)
    key_map = {"calories": "Calories (kcal)", "fat": "Fat (g)", "sugar": "Sugar (g)",
               "protein": "Protein (g)", "sodium": "Sodium (mg)", "carbohydrates": "Carbohydrates (g)"}
    for k, label in key_map.items():
        val = nutrition.get(k, "N/A")
        pdf.cell(0, 6, f"  {label}: {val}", ln=True)
    pdf.ln(4)

    if recommendations:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, "Recommendations:", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for r in recommendations:
            # strip emoji for fpdf compatibility
            clean = r.encode("ascii", errors="replace").decode()
            pdf.multi_cell(0, 6, f"  * {clean}")

    return pdf.output()


# ─── TEXT FALLBACK ───────────────────────────────────────────────────────────────
def _generate_text_fallback(food_name, nutrition, score, classification, recommendations) -> bytes:
    """Return plain-text report as bytes (UTF-8)."""
    lines = [
        "FoodScan— Analysis Report",
        f"Generated: {datetime.datetime.now().strftime('%B %d, %Y %H:%M')}",
        "=" * 50,
        f"Product: {food_name}",
        f"Health Score: {score}/100 — {classification}",
        "",
        "Nutrition Facts (per 100g):",
    ]
    key_map = {"calories": "Calories (kcal)", "fat": "Fat (g)", "sugar": "Sugar (g)",
               "protein": "Protein (g)", "sodium": "Sodium (mg)", "carbohydrates": "Carbohydrates (g)"}
    for k, label in key_map.items():
        lines.append(f"  {label}: {nutrition.get(k, 'N/A')}")

    lines += ["", "Recommendations:"]
    for r in recommendations:
        lines.append(f"  * {r}")
    lines.append("\nFoodScan— Powered by Deep Learning & OpenFoodFacts")

    return "\n".join(lines).encode("utf-8")
