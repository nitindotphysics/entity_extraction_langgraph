from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import JSON
from sqlalchemy import Text
from sqlalchemy import Boolean


from datetime import datetime

from app.database.db import Base

class Document(Base):

    __tablename__ = "documents"

    id = Column(

        Integer,

        primary_key=True,

        index=True
    )

    file_name = Column(
        String
    )

    document_hash = Column(

        String,

        unique=True
    )

    # ----------------------------------------
    # NEW METADATA FIELDS
    # ----------------------------------------

    parser_used = Column(
        String
    )

    ocr_used = Column(
        Boolean
    )

    file_size_kb = Column(
        Float
    )

    page_count = Column(
        Integer
    )

    document_type = Column(
        String
    )

    extraction_required = Column(
        Boolean
    )

    created_at = Column(

        DateTime,

        default=datetime.utcnow
    )

class WorkflowRun(Base):

    __tablename__ = "workflow_runs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    document_id = Column(
        Integer,
        ForeignKey("documents.id")
    )

    workflow_status = Column(String)

    failure_reason = Column(
        String,
        nullable=True
    )

    failed_node = Column(
        String,
        nullable=True
    )

    stack_trace = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class NodeExecution(Base):

    __tablename__ = "node_executions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    workflow_run_id = Column(
        Integer,
        ForeignKey("workflow_runs.id")
    )

    node_name = Column(String)

    execution_status = Column(String)

    execution_order = Column(Integer)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class ExtractedEntities(Base):

    __tablename__ = "extracted_entities"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    workflow_run_id = Column(
        Integer,
        ForeignKey("workflow_runs.id")
    )

    entities_json = Column(JSON)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class NormalizedEntities(Base):

    __tablename__ = "normalized_entities"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    workflow_run_id = Column(
        Integer,
        ForeignKey("workflow_runs.id")
    )

    normalized_json = Column(JSON)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class AlertEvent(Base):

    __tablename__ = "alert_events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    workflow_run_id = Column(
        Integer,
        ForeignKey("workflow_runs.id")
    )

    alert_type = Column(String)

    alert_payload = Column(JSON)

    delivery_channel = Column(String)

    delivery_status = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class DebugSnapshot(Base):

    __tablename__ = "debug_snapshots"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    workflow_run_id = Column(
        Integer,
        ForeignKey("workflow_runs.id")
    )

    node_name = Column(String)

    snapshot_type = Column(String)

    snapshot_data = Column(JSON)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )