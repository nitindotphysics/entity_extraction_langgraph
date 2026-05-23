def analyze_document_quality(document_representation):

    markdown = (
        document_representation[
            "content_representation"
        ]["markdown"]
    )

    markdown_length = len(markdown)

    contains_tables = "|" in markdown

    contains_image_only = (
        markdown.strip() == "<!-- image -->"
    )

    meaningful_text = (
        markdown_length > 100
    )

    requires_ocr = False

    if contains_image_only:
        requires_ocr = True

    if markdown_length < 50:
        requires_ocr = True

    quality_report = {

        "markdown_length": markdown_length,

        "contains_tables": contains_tables,

        "contains_image_only": contains_image_only,

        "contains_meaningful_text": meaningful_text,

        "requires_ocr": requires_ocr
    }

    return quality_report