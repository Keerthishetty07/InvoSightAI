from datetime import datetime

from ai_engine.ocr import extract_text
from .extractor import extract_invoice_data


def process_invoice(invoice):
    """
    Complete invoice processing pipeline:
    1. OCR
    2. Extract fields
    3. Save to database
    """

    print(">>> process_invoice() called")
    try:
        # Get uploaded file path
        file_path = invoice.uploaded_file.path

        # ---------------- OCR ----------------
        text = extract_text(file_path)

        invoice.ocr_text = text

        # ---------------- Extract Data ----------------
        data = extract_invoice_data(text)

        # Basic Details
        invoice.invoice_number = data.get("invoice_number", "")
        invoice.vendor = data.get("vendor", "")
        invoice.customer = data.get("customer", "")

        invoice.vendor_gstin = data.get("vendor_gstin", "")
        invoice.customer_gstin = data.get("customer_gstin", "")

        # ---------------- Invoice Date ----------------
        invoice_date = data.get("invoice_date", "")

        if invoice_date:

            date_formats = [
                "%d-%b-%Y",
                "%d/%m/%Y",
                "%d-%m-%Y",
            ]

            for fmt in date_formats:
                try:
                    invoice.invoice_date = datetime.strptime(
                        invoice_date,
                        fmt
                    ).date()
                    break
                except ValueError:
                    continue

        # ---------------- Amounts ----------------
        subtotal = data.get("subtotal", "")
        tax = data.get("tax", "")
        total = data.get("total", "")

        if subtotal:
            invoice.subtotal = float(
                subtotal.replace(",", "")
            )

        if tax:
            invoice.tax = float(
                tax.replace(",", "")
            )

        if total:
            invoice.total = float(
                total.replace(",", "")
            )

        # ---------------- Status ----------------
        invoice.status = "Processed"

    except Exception as e:

        invoice.status = "Failed"
        invoice.ocr_text = f"Error: {str(e)}"

    invoice.save()

    return invoice