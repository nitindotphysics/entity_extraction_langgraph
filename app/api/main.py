import shutil

import traceback

from pathlib import Path

from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from app.graph.workflow import (
    graph
)

from app.database.db import (
    SessionLocal
)

from app.database.models import (
    WorkflowRun,
    NodeExecution,
    AlertEvent,
    Document,
    NormalizedEntities
)

# ----------------------------------------
# CREATE FASTAPI APP
# ----------------------------------------

app = FastAPI(

    title="Financial Document AI"
)

# ----------------------------------------
# HEALTH API
# ----------------------------------------

@app.get("/health")
def health_check():

    return {

        "status": "healthy"
    }

# ----------------------------------------
# PROCESS DOCUMENT API
# ----------------------------------------

@app.post("/process-document")
async def process_document(

    file: UploadFile = File(...)
):

    # validate pdf

    if not file.filename.endswith(".pdf"):

        return {

            "error":
            "Only PDF files supported"
        }

    # create temp directory

    Path(
        "data/temp"
    ).mkdir(

        parents=True,

        exist_ok=True
    )

    # save uploaded file

    temp_file_path = Path(

        f"data/temp/{file.filename}"
    )

    with open(
        temp_file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # initial graph state

    initial_state = {

        "skip_processing": False,

        "file_path":
            str(temp_file_path),

        "representation": None,

        "quality_report": None,

        "classification": None,

        "extracted_entities": None,

        "normalized_entities": None,

        "requires_ocr": None,

        "alerts": [],

        "document_id": None,

        "workflow_run_id": None,

        "execution_order": 0
    }

    # invoke workflow

    # final_state = graph.invoke(
    #     initial_state
    # )
    try:

        final_state = graph.invoke(
            initial_state
        )

    # except Exception as e:

    #     print(
    #         f"\nWORKFLOW FAILED:\n{e}\n"
    #     )

    #     db = SessionLocal()

    #     workflow_run_id = initial_state.get(
    #         "workflow_run_id"
    #     )

    #     if workflow_run_id:

    #         workflow = db.query(
    #             WorkflowRun
    #         ).filter(

    #             WorkflowRun.id
    #             == workflow_run_id

    #         ).first()

    #         if workflow:

    #             workflow.workflow_status = (
    #                 "FAILED"
    #             )

    #             db.commit()

    #     db.close()

    #     raise e


    except Exception as e:

        print(
            f"\nWORKFLOW FAILED:\n{e}\n"
        )

        stack_trace = traceback.format_exc()

        db = SessionLocal()

        workflow_run_id = initial_state.get(
            "workflow_run_id"
        )

        if workflow_run_id:

            workflow = db.query(
                WorkflowRun
            ).filter(

                WorkflowRun.id
                == workflow_run_id

            ).first()

            if workflow:

                workflow.workflow_status = (
                    "FAILED"
                )

                workflow.failure_reason = (
                    str(e)
                )

                # ----------------------------------------
                # DETECT FAILED NODE
                # ----------------------------------------

                failed_node = None

                if "parse_document_node" in stack_trace:

                    failed_node = (
                        "parse_document_node"
                    )

                elif "quality_check_node" in stack_trace:

                    failed_node = (
                        "quality_check_node"
                    )

                elif "classification_node" in stack_trace:

                    failed_node = (
                        "classification_node"
                    )

                elif "extraction_node" in stack_trace:

                    failed_node = (
                        "extraction_node"
                    )

                elif "alert_check_node" in stack_trace:

                    failed_node = (
                        "alert_check_node"
                    )

                elif "sms_alert_node" in stack_trace:

                    failed_node = (
                        "sms_alert_node"
                    )

                elif "email_alert_node" in stack_trace:

                    failed_node = (
                        "email_alert_node"
                    )

                workflow.failed_node = (
                    failed_node
                )

                workflow.stack_trace = (
                    stack_trace
                )

                db.commit()

        db.close()

        raise e
    # duplicate document response

    if final_state.get(
        "skip_processing"
    ):

        return {

            "status":
                "SKIPPED",

            "message":
                "Document already processed",

            "skip_processing":
                True,

            "file_name":
                file.filename
        }

    # successful workflow response

    return {

        "status": "SUCCESS",

        "workflow_run_id":

            final_state.get(
                "workflow_run_id"
            ),

        "document": {

            "file_name":
                file.filename,

            "document_type":

                final_state.get(
                    "classification",
                    {}
                ).get(
                    "document_type"
                )

                if final_state.get(
                    "classification"
                )

                else None,

            "ocr_used":

                final_state.get(
                    "requires_ocr"
                )
        },

        "alerts": {

            "count":

                len(
                    final_state.get(
                        "alerts",
                        []
                    )
                ),

            "items": [

                alert.get(
                    "rule_name"
                )

                for alert in final_state.get(
                    "alerts",
                    []
                )
            ]
        },

        "extraction_summary": {

            "customer_name":

                final_state.get(
                    "normalized_entities",
                    {}
                ).get(
                    "customer_entities",
                    {}
                ).get(
                    "customer_name"
                )

                if final_state.get(
                    "normalized_entities"
                )

                else None,

            "account_number":

                final_state.get(
                    "normalized_entities",
                    {}
                ).get(
                    "account_entities",
                    {}
                ).get(
                    "account_number"
                )

                if final_state.get(
                    "normalized_entities"
                )

                else None,

            "transaction_count":

                len(

                    final_state.get(
                        "normalized_entities",
                        {}
                    ).get(
                        "transaction_entities",
                        []
                    )
                )

                if final_state.get(
                    "normalized_entities"
                )

                else 0
        }
    }

# ----------------------------------------
# WORKFLOW STATUS API
# ----------------------------------------

@app.get(
    "/workflow-status/{workflow_run_id}"
)
def get_workflow_status(

    workflow_run_id: int
):

    db = SessionLocal()

    workflow = db.query(
        WorkflowRun
    ).filter(

        WorkflowRun.id
        == workflow_run_id

    ).first()

    if not workflow:

        db.close()

        return {

            "error":
            "Workflow not found"
        }

    node_executions = db.query(
        NodeExecution
    ).filter(

        NodeExecution.workflow_run_id
        == workflow_run_id

    ).order_by(

        NodeExecution.execution_order
    ).all()

    response = {

        "workflow_run_id":

            workflow.id,

        "workflow_status":

            workflow.workflow_status,

        "created_at":

            workflow.created_at,

        "nodes_executed": [

            {

                "node_name":

                    node.node_name,

                "execution_status":

                    node.execution_status,

                "execution_order":

                    node.execution_order,

                "created_at":

                    node.created_at
            }

            for node in node_executions
        ]
    }

    db.close()

    return response

# ----------------------------------------
# ALERTS API
# ----------------------------------------

@app.get("/alerts")
def get_alerts():

    db = SessionLocal()

    alerts = db.query(
        AlertEvent
    ).all()

    response = [

        {

            "id":

                alert.id,

            "workflow_run_id":

                alert.workflow_run_id,

            "alert_type":

                alert.alert_type,

            "alert_payload":

                alert.alert_payload,

            "delivery_channel":

                alert.delivery_channel,

            "delivery_status":

                alert.delivery_status,

            "created_at":

                alert.created_at
        }

        for alert in alerts
    ]

    db.close()

    return response

# ----------------------------------------
# DOCUMENTS API
# ----------------------------------------

@app.get("/documents")
def get_documents():

    db = SessionLocal()

    documents = db.query(
        Document
    ).all()

    response = [

        {

            "id":

                document.id,

            "file_name":

                document.file_name,

            "document_hash":

                document.document_hash,

            "created_at":

                document.created_at
        }

        for document in documents
    ]

    db.close()

    return response

# ----------------------------------------
# INVESTIGATION DOCUMENTS API
# ----------------------------------------

# @app.get(
#     "/investigation-documents"
# )
# def get_investigation_documents():

#     db = SessionLocal()

#     documents = db.query(
#         Document
#     ).all()

#     response = []

#     for document in documents:

#         workflow = db.query(
#             WorkflowRun
#         ).filter(

#             WorkflowRun.document_id
#             == document.id

#         ).order_by(

#             WorkflowRun.id.desc()
#         ).first()

#         normalized_entities = None

#         if workflow:

#             normalized_entity_record = db.query(
#                 NormalizedEntity
#             ).filter(

#                 NormalizedEntity.workflow_run_id
#                 == workflow.id

#             ).first()

#             if normalized_entity_record:

#                 normalized_entities = (

#                     normalized_entity_record
#                     .normalized_json
#                 )

#         alerts = []

#         if workflow:

#             alert_records = db.query(
#                 AlertEvent
#             ).filter(

#                 AlertEvent.workflow_run_id
#                 == workflow.id

#             ).all()

#             alerts = [

#                 {

#                     "alert_type":

#                         alert.alert_type,

#                     "alert_message":

#                         alert.alert_payload.get(
#                             "alert_message"
#                         ),

#                     "channel":

#                         alert.delivery_channel,

#                     "status":

#                         alert.delivery_status
#                 }

#                 for alert in alert_records
#             ]

#         customer_name = None

#         account_number = None

#         transaction_count = 0

#         if normalized_entities:

#             customer_name = (

#                 normalized_entities.get(
#                     "customer_entities",
#                     {}
#                 ).get(
#                     "customer_name"
#                 )
#             )

#             account_number = (

#                 normalized_entities.get(
#                     "account_entities",
#                     {}
#                 ).get(
#                     "account_number"
#                 )
#             )

#             transaction_count = len(

#                 normalized_entities.get(
#                     "transaction_entities",
#                     []
#                 )
#             )

#         response.append({

#             "document_id":

#                 document.id,

#             "document_name":

#                 Path(
#                     document.file_name
#                 ).name,

#             "document_hash":

#                 document.document_hash,

#             "workflow_run_id":

#                 workflow.id

#                 if workflow

#                 else None,

#             "workflow_status":

#                 workflow.workflow_status

#                 if workflow

#                 else None,

#             "entities_extraction_required":

#                 normalized_entities
#                 is not None,

#             "customer_name":

#                 customer_name,

#             "account_number":

#                 account_number,

#             "transaction_count":

#                 transaction_count,

#             "alert_count":

#                 len(alerts),

#             "alerts":

#                 alerts,

#             "normalized_entities":

#                 normalized_entities,

#             "created_at":

#                 document.created_at
#         })

#     db.close()

#     return response

@app.get(
    "/investigation-documents"
)

def get_investigation_documents():

    db = SessionLocal()

    response = []

    documents = db.query(
        Document
    ).all()

    for document in documents:

        try:

            workflow = db.query(
                WorkflowRun
            ).filter(

                WorkflowRun.document_id
                == document.id

            ).order_by(

                WorkflowRun.id.desc()

            ).first()

            normalized_entities = None

            if workflow:

                normalized_entity_record = db.query(
                    NormalizedEntities
                ).filter(

                    NormalizedEntities.workflow_run_id
                    == workflow.id

                ).first()

                if normalized_entity_record:

                    normalized_entities = (
                        normalized_entity_record
                        .normalized_json
                    )

            alerts = []

            if workflow:

                alert_records = db.query(
                    AlertEvent
                ).filter(

                    AlertEvent.workflow_run_id
                    == workflow.id

                ).all()

                alerts = [

                    {

                        "alert_type":

                            alert.alert_type,

                        "alert_message":

                            alert.alert_payload.get(
                                "alert_message"
                            )

                            if alert.alert_payload

                            else None,

                        "channel":

                            alert.delivery_channel,

                        "status":

                            alert.delivery_status
                    }

                    for alert in alert_records
                ]

            customer_name = None
            account_number = None
            transaction_count = 0

            if normalized_entities:

                customer_name = (

                    normalized_entities.get(
                        "customer_entities",
                        {}
                    ).get(
                        "customer_name"
                    )
                )

                account_number = (

                    normalized_entities.get(
                        "account_entities",
                        {}
                    ).get(
                        "account_number"
                    )
                )

                transaction_count = len(

                    normalized_entities.get(
                        "transaction_entities",
                        []
                    )
                )

            response.append({

                "document_id":

                    document.id,

                "document_name":

                    Path(
                        document.file_name
                    ).name

                    if document.file_name

                    else "Unknown",

                "document_hash":

                    document.document_hash,

                "workflow_run_id":

                    workflow.id
                    if workflow
                    else None,

                "workflow_status":

                    workflow.workflow_status
                    if workflow
                    else None,

                "entities_extraction_required":

                    normalized_entities
                    is not None,

                "customer_name":

                    customer_name,

                "account_number":

                    account_number,

                "transaction_count":

                    transaction_count,

                "alert_count":

                    len(alerts),

                "alerts":

                    alerts,

                "normalized_entities":

                    normalized_entities,

                "created_at":

                    document.created_at
            })

        except Exception as e:

            print(
                f"INVESTIGATION API ERROR: {e}"
            )

    db.close()

    return response

# ----------------------------------------
# OBSERVABILITY LOGS API
# ----------------------------------------

@app.get(
    "/observability-logs"
)
def get_observability_logs():

    db = SessionLocal()

    workflow_runs = db.query(
        WorkflowRun
    ).all()

    workflow_data = [

        {

            "workflow_run_id":

                workflow.id,

            "document_id":

                workflow.document_id,

            "workflow_status":

                workflow.workflow_status,

            "created_at":

                workflow.created_at
        }

        for workflow in workflow_runs
    ]

    node_executions = db.query(
        NodeExecution
    ).all()

    node_data = [

        {

            "workflow_run_id":

                node.workflow_run_id,

            "node_name":

                node.node_name,

            "execution_status":

                node.execution_status,

            "execution_order":

                node.execution_order,

            "created_at":

                node.created_at
        }

        for node in node_executions
    ]

    alert_events = db.query(
        AlertEvent
    ).all()

    alert_data = [

        {

            "alert_id":

                alert.id,

            "workflow_run_id":

                alert.workflow_run_id,

            "alert_type":

                alert.alert_type,

            "delivery_channel":

                alert.delivery_channel,

            "delivery_status":

                alert.delivery_status,

            "created_at":

                alert.created_at
        }

        for alert in alert_events
    ]

    db.close()

    return {

        # "metrics": {

        #     "total_workflows":

        #         len(workflow_data),

        #     "total_node_executions":

        #         len(node_data),

        #     "total_alerts":

        #         len(alert_data)
        # },
        "metrics": {

            "total_workflows":

                len(workflow_data),

            "total_node_executions":

                len(node_data),

            "total_alerts":

                len(alert_data),

            "failed_node_executions":

                len(

                    [

                        node

                        for node in node_data

                        if node[
                            "execution_status"
                        ] == "FAILED"
                    ]
                )
        },

        "workflow_runs":

            workflow_data,

        "node_executions":

            node_data,

        "alert_events":

            alert_data
    }


# ----------------------------------------
# ROOT API
# ----------------------------------------

@app.get("/")
def root():

    return {

        "message":
            "Financial Document AI API Running"
    }