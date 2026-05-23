from docling.document_converter import DocumentConverter


converter = DocumentConverter()


def process_pdf_with_docling(pdf_path):

    result = converter.convert(pdf_path)

    return result