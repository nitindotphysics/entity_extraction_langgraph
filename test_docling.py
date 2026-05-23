import warnings

warnings.filterwarnings("ignore")

from app.processors.pdf.docling_processor import (
    process_pdf_with_docling
)

from app.processors.pdf.document_representation import (
    build_document_representation
)

from app.ingestion.file_discovery import (
    discover_pdfs
)


pdfs = discover_pdfs()

first_pdf = pdfs[6]

docling_result = process_pdf_with_docling(
    first_pdf["file_path"]
)

representation = build_document_representation(
    docling_result
)

# print(representation["markdown"])
print(representation)