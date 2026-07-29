import requests

import os
OCR_API_KEY = os.environ.get("OCR_API_KEY")  # we'll fix this in Step 4
OCR_API_URL = "https://api.ocr.space/parse/image"

def extract_text(file_path):
    """
    Sends an image or PDF to the OCR.space API and returns the extracted text.
    """
    with open(file_path, "rb") as f:
        response = requests.post(
            OCR_API_URL,
            files={"file": f},
            data={
                "apikey": OCR_API_KEY,
                "language": "eng",
                "OCREngine": 2,  # better accuracy engine
            },
        )

    result = response.json()

    if result.get("IsErroredOnProcessing"):
        raise RuntimeError(f"OCR failed: {result.get('ErrorMessage')}")

    parsed_text = ""
    for parsed_result in result.get("ParsedResults", []):
        parsed_text += parsed_result.get("ParsedText", "")

    return parsed_text