from app.services.telemetry_service import (

    create_document_record,

    create_workflow_run,

    log_node_execution,

    store_extracted_entities,

    store_normalized_entities,

    store_alert_event,

    store_debug_snapshot,

    update_workflow_status
)


print("\nCREATING DOCUMENT RECORD...\n")


document_id = create_document_record(

    file_name="bank_statement_1.pdf",

    document_type="bank_statement",

    parser_used="docling",

    ocr_used=False
)

print("DOCUMENT ID:", document_id)


print("\nCREATING WORKFLOW RUN...\n")


workflow_run_id = create_workflow_run(

    document_id=document_id
)

print("WORKFLOW RUN ID:", workflow_run_id)


print("\nLOGGING NODE EXECUTIONS...\n")


log_node_execution(

    workflow_run_id=workflow_run_id,

    node_name="parse_document_node",

    execution_status="SUCCESS",

    execution_order=1
)


log_node_execution(

    workflow_run_id=workflow_run_id,

    node_name="classification_node",

    execution_status="SUCCESS",

    execution_order=2
)


print("\nSTORING EXTRACTED ENTITIES...\n")


store_extracted_entities(

    workflow_run_id=workflow_run_id,

    entities={

        "customer_name": "Alice Brown",

        "amount": "90000"
    }
)


print("\nSTORING NORMALIZED ENTITIES...\n")


store_normalized_entities(

    workflow_run_id=workflow_run_id,

    normalized_entities={

        "customer_name": "Alice Brown",

        "amount": 90000.0
    }
)


print("\nSTORING ALERT EVENT...\n")


store_alert_event(

    workflow_run_id=workflow_run_id,

    alert_type="HIGH_VALUE_TRANSACTION",

    alert_payload={

        "amount": 90000
    },

    delivery_channel="SMS",

    delivery_status="SENT"
)


print("\nSTORING DEBUG SNAPSHOT...\n")


store_debug_snapshot(

    workflow_run_id=workflow_run_id,

    node_name="classification_node",

    snapshot_type="RAW_LLM_RESPONSE",

    snapshot_data={

        "response": "bank_statement"
    }
)


print("\nUPDATING WORKFLOW STATUS...\n")


update_workflow_status(

    workflow_run_id=workflow_run_id,

    workflow_status="SUCCESS"
)


print("\nALL TELEMETRY TESTS COMPLETED\n")