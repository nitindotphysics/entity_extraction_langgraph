import fitz   # PyMuPDF


def extract_pdf_text(pdf_path):

    doc = fitz.open(pdf_path)

    extracted_pages = []

    for page_number in range(len(doc)):

        page = doc[page_number]

        text = page.get_text()

        page_data = {
            "page_number": page_number + 1,
            "text": text
        }

        extracted_pages.append(page_data)

    doc.close()

    return extracted_pages