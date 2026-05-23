from langgraph.graph import (
    StateGraph,
    END
)

from app.graph.state import (
    FinancialDocumentState
)

from app.graph.nodes import (
    parse_document_node,
    quality_check_node,
    ocr_node,
    classification_node,
    extraction_node,
    alert_check_node,
    sms_alert_node,
    email_alert_node,
    finalize_workflow_node
)

# create graph
workflow = StateGraph(
    FinancialDocumentState
)

# add nodes
workflow.add_node(
    "parse_document",
    parse_document_node
)

workflow.add_node(
    "quality_check",
    quality_check_node
)

workflow.add_node(
    "ocr_node",
    ocr_node
)

workflow.add_node(
    "classification",
    classification_node
)

workflow.add_node(
    "extraction",
    extraction_node
)

workflow.add_node(
    "alert_check",
    alert_check_node
)

workflow.add_node(
    "sms_alert",
    sms_alert_node
)

workflow.add_node(
    "email_alert",
    email_alert_node
)

workflow.add_node(

    "finalize_workflow",

    finalize_workflow_node
)

# ----------------------------------------
# ROUTING FUNCTIONS
# ----------------------------------------

# route based on OCR requirement
def route_ocr(state):

    if state["requires_ocr"]:

        return "ocr_node"

    return "classification"


# route based on classification
def route_classification(state):

    document_type = state[
        "classification"
    ]["document_type"]

    if document_type == "bank_statement":

        return "extraction"

    return "finalize_workflow"


# route based on alerts
def route_alerts(state):

    if len(state["alerts"]) > 0:

        return "sms_alert"

    return "finalize_workflow"


# route based on duplicate processing
def route_duplicate_processing(state):

    if state.get("skip_processing"):

        return END

    return "quality_check"


# ----------------------------------------
# ENTRY POINT
# ----------------------------------------

workflow.set_entry_point(
    "parse_document"
)

# ----------------------------------------
# PARSE -> DUPLICATE CHECK
# ----------------------------------------

workflow.add_conditional_edges(

    "parse_document",

    route_duplicate_processing,

    {
        "quality_check": "quality_check",

        END: END
    }
)

# ----------------------------------------
# QUALITY -> OCR / CLASSIFICATION
# ----------------------------------------

workflow.add_conditional_edges(

    "quality_check",

    route_ocr,

    {
        "ocr_node": "ocr_node",

        "classification": "classification"
    }
)

# OCR -> CLASSIFICATION
workflow.add_edge(

    "ocr_node",

    "classification"
)

# ----------------------------------------
# CLASSIFICATION -> EXTRACTION / END
# ----------------------------------------

workflow.add_conditional_edges(

    "classification",

    route_classification,

    {
        "extraction": "extraction",

        "finalize_workflow":
            "finalize_workflow"
    }
)

# EXTRACTION -> ALERT CHECK
workflow.add_edge(

    "extraction",

    "alert_check"
)

# ----------------------------------------
# ALERT CHECK -> SMS / END
# ----------------------------------------

workflow.add_conditional_edges(

    "alert_check",

    route_alerts,

    {
        "sms_alert": "sms_alert",

        "finalize_workflow":
            "finalize_workflow"
    }
)

# SMS -> EMAIL
workflow.add_edge(

    "sms_alert",

    "email_alert"
)

# EMAIL -> END
workflow.add_edge(

    "email_alert",

    "finalize_workflow"
)

# finalise to end
workflow.add_edge(

    "finalize_workflow",

    END
)

# compile graph
graph = workflow.compile()