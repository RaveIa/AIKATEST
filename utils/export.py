
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile

def export_to_pdf(text):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=A4)
    width, height = A4
    y = height - 50
    for line in text.split("\n"):
        c.setFont("Helvetica", 14)
        c.drawString(50, y, line[:100])
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()
    return temp_file.name
