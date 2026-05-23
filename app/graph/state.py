from typing import TypedDict
from typing import Optional


class FinancialDocumentState(TypedDict):
    skip_processing: Optional[bool]
    
    file_path: str

    representation: Optional[dict]

    quality_report: Optional[dict]

    classification: Optional[dict]

    extracted_entities: Optional[dict]

    normalized_entities: Optional[dict]

    requires_ocr: Optional[bool]

    alerts: Optional[list]

    document_id: Optional[int]

    workflow_run_id: Optional[int]

    execution_order: Optional[int]

