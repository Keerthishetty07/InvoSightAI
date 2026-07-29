import os
import fitz
import easyocr

# Reader will be created only when needed
reader = None


def get_reader():
    global reader

    if reader is None:
        reader = easyocr.Reader(["en"], gpu=False)

    return reader


def extract_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_from_pdf(file_path)

    return extract_from_image(file_path)


def extract_from_image(image_path):

    reader = get_reader()

    results = reader.readtext(image_path)

    text = "\n".join(item[1] for item in results)

    text = text.replace("₹", "")
    text = text.replace("84,", "4,")
    text = text.replace("8,", "4,")

    return text


def extract_from_pdf(pdf_path):

    document = fitz.open(pdf_path)

    full_text = ""

    for page in document:

        pix = page.get_pixmap(dpi=250)

        image_path = "temp_page.png"

        pix.save(image_path)

        full_text += extract_from_image(image_path)
        full_text += "\n"

        if os.path.exists(image_path):
            os.remove(image_path)

    document.close()

    return full_text