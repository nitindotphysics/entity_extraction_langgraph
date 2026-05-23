from docling.document_converter import (
    DocumentConverter
)

def build_document_representation(
    file_path
):

    converter = DocumentConverter()

    docling_result = converter.convert(
        file_path
    )

    markdown_content = (

        docling_result
        .document
        .export_to_markdown()
    )

    return {

        "document_metadata": {

            "parser":
                "docling"
        },

        "content_representation": {

            "markdown":
                markdown_content,

            "tables":
                [],

            "images":
                []
        }
    }