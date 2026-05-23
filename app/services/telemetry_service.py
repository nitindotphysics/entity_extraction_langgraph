from app.database.db import (
    SessionLocal
)

from app.database.models import (
    Document,
    WorkflowRun,
    NodeExecution,
    ExtractedEntities,
    NormalizedEntities,
    AlertEvent,
    DebugSnapshot
)

from sqlalchemy.exc import IntegrityError

def document_already_processed(

    document_hash
):

    db = SessionLocal()

    existing_document = db.query(
        Document
    ).filter(

        Document.document_hash == document_hash

    ).first()

    db.close()

    return existing_document


def create_document_record(

    file_name,
    document_hash,
    parser_used,
    ocr_used,
    file_size_kb=None,
    page_count=None,
    document_type="UNKNOWN",
    extraction_required=False
):

    db = SessionLocal()

    # document = Document(

    #     file_name=file_name,

    #     document_hash=document_hash,

    #     document_type=document_type,

    #     parser_used=parser_used,

    #     ocr_used=ocr_used
    # )

    document = Document(

        file_name=file_name,

        document_hash=document_hash,

        parser_used=parser_used,

        ocr_used=ocr_used,

        file_size_kb=file_size_kb,

        page_count=page_count,

        document_type=document_type,

        extraction_required=
            extraction_required
    )
    

    db.add(document)

    db.commit()

    db.refresh(document)

    db.close()

    return document.id

def create_workflow_run(

    document_id,
    workflow_status="RUNNING"
):

    db = SessionLocal()

    workflow_run = WorkflowRun(

        document_id=document_id,

        workflow_status=workflow_status
    )

    db.add(workflow_run)

    db.commit()

    db.refresh(workflow_run)

    db.close()

    return workflow_run.id

def log_node_execution(

    workflow_run_id,
    node_name,
    execution_status,
    execution_order
):

    db = SessionLocal()

    node_execution = NodeExecution(

        workflow_run_id=workflow_run_id,

        node_name=node_name,

        execution_status=execution_status,

        execution_order=execution_order
    )

    db.add(node_execution)

    db.commit()

    db.close()

def store_extracted_entities(

    workflow_run_id,
    entities
):

    db = SessionLocal()

    extracted = ExtractedEntities(

        workflow_run_id=workflow_run_id,

        entities_json=entities
    )

    db.add(extracted)

    db.commit()

    db.close()

def store_normalized_entities(

    workflow_run_id,
    normalized_entities
):

    db = SessionLocal()

    normalized = NormalizedEntities(

        workflow_run_id=workflow_run_id,

        normalized_json=normalized_entities
    )

    db.add(normalized)

    db.commit()

    db.close()

def store_alert_event(

    workflow_run_id,
    alert_type,
    alert_payload,
    delivery_channel,
    delivery_status
):

    db = SessionLocal()

    alert = AlertEvent(

        workflow_run_id=workflow_run_id,

        alert_type=alert_type,

        alert_payload=alert_payload,

        delivery_channel=delivery_channel,

        delivery_status=delivery_status
    )

    db.add(alert)

    db.commit()

    db.close()

def store_debug_snapshot(

    workflow_run_id,
    node_name,
    snapshot_type,
    snapshot_data
):

    db = SessionLocal()

    snapshot = DebugSnapshot(

        workflow_run_id=workflow_run_id,

        node_name=node_name,

        snapshot_type=snapshot_type,

        snapshot_data=snapshot_data
    )

    db.add(snapshot)

    db.commit()

    db.close()

def update_workflow_status(

    workflow_run_id,
    workflow_status
):

    db = SessionLocal()

    workflow = db.query(
        WorkflowRun
    ).filter(

        WorkflowRun.id == workflow_run_id

    ).first()

    workflow.workflow_status = (
        workflow_status
    )

    db.commit()

    db.close()

def update_alert_delivery_status(

    workflow_run_id,

    alert_type,

    delivery_channel,

    delivery_status
):

    db = SessionLocal()

    alert = db.query(
        AlertEvent
    ).filter(

        AlertEvent.workflow_run_id
        == workflow_run_id,

        AlertEvent.alert_type
        == alert_type

    ).first()

    if alert:

        alert.delivery_channel = (
            delivery_channel
        )

        alert.delivery_status = (
            delivery_status
        )

        db.commit()

    db.close()