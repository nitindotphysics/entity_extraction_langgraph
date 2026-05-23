from pathlib import Path

import os
import json

from app.processors.pdf.docling_processor import (
    process_pdf_with_docling
)

from app.notifications.sms_service import (
    send_sms_notification
)

from app.notifications.email_service import (
    send_email_notification
)

from app.services.telemetry_service import (

    update_alert_delivery_status,

    document_already_processed,

    create_document_record,

    create_workflow_run,

    log_node_execution,

    store_extracted_entities,

    store_normalized_entities,

    store_alert_event,

    store_debug_snapshot,

    update_workflow_status
)

from app.alerts.alert_engine import (
    evaluate_alert_rules
)

from app.utils.hash_utils import (
    generate_document_hash
)

# ----------------------------------------
# DOCUMENT REPRESENTATION
# ----------------------------------------

from app.processors.pdf.document_representation import (
    build_document_representation
)

from app.quality.document_quality_analyzer import (
    analyze_document_quality
)

# ----------------------------------------
# OCR IMPORTS
# ----------------------------------------

from app.ocr.paddle_ocr_processor import (
    extract_text_with_ocr
)

from app.ocr.ocr_representation_builder import (
    build_ocr_representation
)

# ----------------------------------------
# CLASSIFICATION IMPORTS
# ----------------------------------------

from app.classification.document_classifier import (
    classify_document
)

# ----------------------------------------
# ENTITY EXTRACTION IMPORTS
# ----------------------------------------

from app.extraction.bank_statement_extractor import (
    extract_bank_statement_entities
)

from app.extraction.normalize_entities import (
    normalize_bank_statement_entities
)

# ----------------------------------------
# PARSE DOCUMENT NODE
# ----------------------------------------

def parse_document_node(state):

    state["execution_order"] = 1

    docling_result = (
        process_pdf_with_docling(
            state["file_path"]
        )
    )

    representation = (

        build_document_representation(

            state["file_path"]
        )
    )

    state["representation"] = (
        representation
    )

    document_hash = generate_document_hash(
        state["file_path"]
    )

    existing_document = (
        document_already_processed(
            document_hash
        )
    )

    if existing_document:

        print(
            "\nDOCUMENT ALREADY PROCESSED\n"
        )

        print(
            "SKIPPING WORKFLOW..."
        )

        state["skip_processing"] = True

        return state

    print("\nRUNNING: parse_document_node\n")

    print("\nCURRENT STATE:\n")
    print(state)

    # ----------------------------------------
    # BUILD DOCUMENT REPRESENTATION
    # ----------------------------------------

    representation = (
        build_document_representation(
            state["file_path"]
        )
    )

    state["representation"] = (
        representation
    )

    # ----------------------------------------
    # CREATE DOCUMENT RECORD
    # ----------------------------------------

    document_id = create_document_record(

        file_name=state["file_path"],

        document_hash=document_hash,

        document_type="UNKNOWN",

        parser_used="pymupdf",

        ocr_used=False,

        file_size_kb=round(

            os.path.getsize(
                state["file_path"]
            ) / 1024,

            2
        ),

        extraction_required=False
    )

    workflow_run_id = create_workflow_run(

        document_id=document_id
    )

    state["document_id"] = document_id

    state["workflow_run_id"] = workflow_run_id

    log_node_execution(

        workflow_run_id=workflow_run_id,

        node_name="parse_document_node",

        execution_status="SUCCESS",

        execution_order=state["execution_order"]
    )

    return state

# ----------------------------------------
# QUALITY CHECK NODE
# ----------------------------------------

def quality_check_node(state):

    state["execution_order"] += 1

    print("\nRUNNING: quality_check_node\n")

    print("\nCURRENT STATE:\n")
    print(state)

    quality_report = (
        analyze_document_quality(
            state["representation"]
        )
    )

    state["quality_report"] = (
        quality_report
    )

    state["requires_ocr"] = (
        quality_report["requires_ocr"]
    )

    log_node_execution(

        workflow_run_id=state["workflow_run_id"],

        node_name="quality_check_node",

        execution_status="SUCCESS",

        execution_order=state["execution_order"]
    )

    return state

# ----------------------------------------
# OCR NODE
# ----------------------------------------

def ocr_node(state):

    state["execution_order"] += 1

    print("\nRUNNING: ocr_node\n")

    print("\nCURRENT STATE:\n")
    print(state)

    ocr_text = extract_text_with_ocr(
        state["file_path"]
    )

    representation = (
        build_ocr_representation(
            ocr_text
        )
    )

    state["representation"] = (
        representation
    )

    log_node_execution(

        workflow_run_id=state["workflow_run_id"],

        node_name="ocr_node",

        execution_status="SUCCESS",

        execution_order=state["execution_order"]
    )

    return state

# ----------------------------------------
# CLASSIFICATION NODE
# ----------------------------------------

def classification_node(state):

    state["execution_order"] += 1

    print("\nRUNNING: classification_node\n")

    print("\nCURRENT STATE:\n")
    print(state)

    classification = classify_document(
        state["representation"]
    )

    state["classification"] = (
        classification
    )

    log_node_execution(

        workflow_run_id=state["workflow_run_id"],

        node_name="classification_node",

        execution_status="SUCCESS",

        execution_order=state["execution_order"]
    )

    return state

# ----------------------------------------
# EXTRACTION NODE
# ----------------------------------------

def extraction_node(state):

    state["execution_order"] += 1

    print("\nRUNNING: extraction_node\n")

    print("\nCURRENT STATE:\n")
    print(state)

    entities = (
        extract_bank_statement_entities(
            state["representation"]
        )
    )

    normalized_entities = (
        normalize_bank_statement_entities(
            entities
        )
    )

    state["extracted_entities"] = (
        entities
    )

    store_extracted_entities(

        workflow_run_id=state["workflow_run_id"],

        entities=entities
    )

    state["normalized_entities"] = (
        normalized_entities.model_dump()
    )

    store_normalized_entities(

        workflow_run_id=state["workflow_run_id"],

        normalized_entities=normalized_entities.model_dump(
            mode="json"
        )
    )

    log_node_execution(

        workflow_run_id=state["workflow_run_id"],

        node_name="extraction_node",

        execution_status="SUCCESS",

        execution_order=state["execution_order"]
    )

    return state

# ----------------------------------------
# ALERT CHECK NODE
# ----------------------------------------

def alert_check_node(state):

    state["execution_order"] += 1

    alerts = evaluate_alert_rules(

        state[
            "normalized_entities"
        ]
    )

    state["alerts"] = alerts

    for alert in alerts:

        store_alert_event(

            workflow_run_id=state["workflow_run_id"],

            alert_type=alert.get("alert_type"),

            alert_payload=json.loads(

                json.dumps(

                    alert,

                    default=str
                )
            ),

            delivery_channel="PENDING",

            delivery_status="PENDING"
        )

    log_node_execution(

        workflow_run_id=state["workflow_run_id"],

        node_name="alert_check_node",

        execution_status="SUCCESS",

        execution_order=state["execution_order"]
    )

    return state

# def alert_check_node(state):

#     alerts = []

#     transactions = state[
#         "normalized_entities"
#     ]["transaction_entities"]

#     for transaction in transactions:

#         if transaction["amount"] > 50000:

#             alerts.append({

#                 "type": "HIGH_VALUE_TRANSACTION",

#                 "transaction": transaction
#             })

#     state["alerts"] = alerts

#     return state

# ----------------------------------------
# SMS ALERT NODE
# ----------------------------------------

def sms_alert_node(state):

    state["execution_order"] += 1

    print(
        "\nRUNNING: sms_alert_node\n"
    )

    for alert in state["alerts"]:

        response = (
            send_sms_notification(
                alert
            )
        )

        update_alert_delivery_status(

            workflow_run_id=state[
                "workflow_run_id"
            ],

            alert_type=alert.get("alert_type"),

            delivery_channel="SMS",

            delivery_status=response[
                "delivery_status"
            ]
        )

    log_node_execution(

        workflow_run_id=state[
            "workflow_run_id"
        ],

        node_name="sms_alert_node",

        execution_status="SUCCESS",

        execution_order=state[
            "execution_order"
        ]
    )

    return state

# ----------------------------------------
# EMAIL ALERT NODE
# ----------------------------------------

def email_alert_node(state):

    state["execution_order"] += 1

    print(
        "\nRUNNING: email_alert_node\n"
    )

    for alert in state["alerts"]:

        response = (
            send_email_notification(
                alert
            )
        )

        update_alert_delivery_status(

            workflow_run_id=state[
                "workflow_run_id"
            ],

            alert_type=alert.get("alert_type"),

            delivery_channel="EMAIL",

            delivery_status=response[
                "delivery_status"
            ]
        )

    log_node_execution(

        workflow_run_id=state[
            "workflow_run_id"
        ],

        node_name="email_alert_node",

        execution_status="SUCCESS",

        execution_order=state[
            "execution_order"
        ]
    )

    return state

# ----------------------------------------
# FINALIZE WORKFLOW NODE
# ----------------------------------------

def finalize_workflow_node(state):

    print(
        "\nRUNNING: finalize_workflow_node\n"
    )

    update_workflow_status(

        workflow_run_id=state[
            "workflow_run_id"
        ],

        workflow_status="SUCCESS"
    )

    log_node_execution(

        workflow_run_id=state[
            "workflow_run_id"
        ],

        node_name="finalize_workflow_node",

        execution_status="SUCCESS",

        execution_order=state[
            "execution_order"
        ] + 1
    )

    return state