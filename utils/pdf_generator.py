# utils/pdf_generator.py

from fpdf import FPDF
from datetime import datetime

def generate_invoice_pdf(cart, cashier_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Wholesale Clothing Store - Invoice", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Cashier: {cashier_name}", ln=2, align="L")
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=3, align="L")
    pdf.ln(10)

    pdf.cell(60, 10, txt="Product", border=1)
    pdf.cell(30, 10, txt="Qty", border=1)
    pdf.cell(40, 10, txt="Price", border=1)
    pdf.cell(40, 10, txt="Subtotal", border=1, ln=1)

    total = 0
    for item in cart:
        pdf.cell(60, 10, txt=item[1], border=1)
        pdf.cell(30, 10, txt=str(item[2]), border=1)
        pdf.cell(40, 10, txt=f"{item[3]:.2f}", border=1)
        pdf.cell(40, 10, txt=f"{item[4]:.2f}", border=1, ln=1)
        total += item[4]

    tax = total * 0.05
    grand_total = total + tax

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Subtotal: ₹{total:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"5% Tax: ₹{tax:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Total Amount: ₹{grand_total:.2f}", ln=1)

    pdf.output("invoice.pdf")
