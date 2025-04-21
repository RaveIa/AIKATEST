from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap
import tempfile

def export_to_pdf(text, font_size=14):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=A4)

    width, height = A4
    margin = 50
    max_line_chars = 95  # ~ correspond à largeur utile A4
    line_height = font_size + 6
    y = height - margin

    c.setFont("Helvetica", font_size)

    for line in text.strip().split('\n'):
        if not line.strip():
            y -= line_height
            continue
        wrapped_lines = wrap(line.strip(), width=max_line_chars)
        for wline in wrapped_lines:
            c.drawString(margin, y, wline)
            y -= line_height
            if y < margin:
                c.showPage()
                c.setFont("Helvetica", font_size)
                y = height - margin

    c.save()
    return temp_file.name
