import re

from .patterns import (
    GST_PATTERN,
    INVOICE_PATTERNS,
    DATE_PATTERNS,
    TOTAL_PATTERNS,
    TAXABLE_PATTERN,
    TOTAL_TAX_PATTERN
)


def search_patterns(patterns, text):

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return ""


def extract_invoice_data(text):

    data = {
        "invoice_number": "",
        "vendor": "",
        "customer": "",
        "vendor_gstin": "",
        "customer_gstin": "",
        "invoice_date": "",
        "subtotal": "",
        "tax": "",
        "total": "",
    }

    # Invoice Number
    data["invoice_number"] = search_patterns(
        INVOICE_PATTERNS,
        text
    )

    # Invoice Date
    data["invoice_date"] = search_patterns(
        DATE_PATTERNS,
        text
    )

    # GSTINs
    gstins = re.findall(GST_PATTERN, text)

    if len(gstins) >= 1:
        data["vendor_gstin"] = gstins[0]

    if len(gstins) >= 2:
        data["customer_gstin"] = gstins[1]

    # Taxable Amount
    taxable = re.search(TAXABLE_PATTERN, text, re.IGNORECASE)

    if taxable:
        data["subtotal"] = taxable.group(1)

    # Tax
    tax = re.search(TOTAL_TAX_PATTERN, text, re.IGNORECASE)

    if tax:
        data["tax"] = tax.group(1)

    # Grand Total
    data["total"] = search_patterns(
        TOTAL_PATTERNS,
        text
    )

    # Vendor (first non-empty line)
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if lines:
        data["vendor"] = lines[0]

    customer_match = re.search(
        r"M/S\s*\n(.+)",
        text,
        re.IGNORECASE
    )

    if customer_match:
        data["customer"] = customer_match.group(1).strip()

    return data