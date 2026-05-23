def build_ocr_representation(
    ocr_text
):

    representation = {

        "document_metadata": {
            "parser": "paddleocr"
        },

        "content_representation": {

            "markdown": ocr_text,

            "tables": [],

            "images": []
        }
    }

    return representation