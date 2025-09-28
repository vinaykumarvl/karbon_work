from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

pdf_file = "data/icici/icici_sample.pdf"

c = canvas.Canvas(pdf_file, pagesize=letter)
c.setFont("Helvetica", 12)

c.drawString(100, 750, "Date       Description        Amount   Balance")
c.drawString(100, 730, "2025-01-01  Test Transaction   100      1000")

c.save()
print("✅ Better sample PDF created:", pdf_file)
