# GSTIN
GST_PATTERN = r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[A-Z0-9]\b"

# Invoice Number
INVOICE_PATTERNS = [
    r"Invoice\s*No\.?[_:\- ]*\n?\s*([A-Z0-9\-\/]+)",
    r"Invoice\s*Number[_:\- ]*\n?\s*([A-Z0-9\-\/]+)",
    r"Invoice\s*No[_:\- ]*\n?\s*([A-Z0-9\-\/]+)",
]

# Invoice Date
DATE_PATTERNS = [
    r"Invoice\s*Date[_:\- ]*\n?\s*(\d{2}-[A-Za-z]{3}-\d{4})",
    r"Invoice\s*Date[_:\- ]*\n?\s*(\d{2}/\d{2}/\d{4})",
    r"Invoice\s*Date[_:\- ]*\n?\s*(\d{2}-\d{2}-\d{4})",
]

# Total Amount
TOTAL_PATTERNS = [
    r"Total\s*Amount\s*After\s*Tax[_:\- ]*\n?\s*[₹$]?\s*([\d,]+\.\d{2})",
    r"Grand\s*Total[_:\- ]*\n?\s*[₹$]?\s*([\d,]+\.\d{2})",
    r"Total[_:\- ]*\n?\s*[₹$]?\s*([\d,]+\.\d{2})",
]

# Taxable Amount
TAXABLE_PATTERN = (
    r"Taxable\s*Amount[_:\- ]*\n?\s*([\d,]+\.\d{2})"
)

# Total Tax
TOTAL_TAX_PATTERN = (
    r"Total\s*Tax[_:\- ]*\n?\s*([\d,]+\.\d{2})"
)