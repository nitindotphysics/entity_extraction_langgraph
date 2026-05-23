import fitz
from PIL import Image
import numpy as np

from paddleocr import PaddleOCR


ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en'
)


def extract_text_with_ocr(pdf_path):

    doc = fitz.open(pdf_path)

    full_ocr_text = ""

    for page_number in range(len(doc)):

        page = doc[page_number]

        matrix = fitz.Matrix(2, 2)

        pix = page.get_pixmap(
            matrix=matrix
        )

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        img_array = np.array(img)

        result = ocr.ocr(img_array)

        page_text = ""

        if result and len(result) > 0:

            recognized_texts = result[0].get(
                "rec_texts",
                []
            )

            for text in recognized_texts:

                page_text += text + "\n"

        full_ocr_text += (
            f"\n--- PAGE {page_number + 1} ---\n"
        )

        full_ocr_text += page_text

    doc.close()

    return full_ocr_text