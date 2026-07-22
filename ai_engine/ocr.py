import os
import fitz
import easyocr
from PIL import Image

# Create EasyOCR reader once
reader = easyocr.Reader(["en"], gpu=False)


def extract_text(file_path):
    """
    Extract text from an image or PDF.
    Returns extracted text as one string.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_from_pdf(file_path)

    return extract_from_image(file_path)


def extract_from_image(image_path):

    results = reader.readtext(image_path)

    text = "\n".join([item[1] for item in results])
    text = text.replace("₹", "")
    text = text.replace("84,", "4,")
    text = text.replace("8,", "4,")

    return text


def extract_from_pdf(pdf_path):

    document = fitz.open(pdf_path)

    full_text = ""

    for page in document:

        pix = page.get_pixmap(dpi=300)

        image_path = "temp_page.png"

        pix.save(image_path)

        full_text += extract_from_image(image_path)

        full_text += "\n"

        if os.path.exists(image_path):
            os.remove(image_path)

    return full_text