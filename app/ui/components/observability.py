import requests
import streamlit as st
import pandas as pd

API_BASE_URL = (
    "http://127.0.0.1:8000"
)

def render_observability_page():

    st.header(
        "Engineering Observability Dashboard"
    )

    # ----------------------------------------
    # FETCH DATA
    # ----------------------------------------

    response = requests.get(

        f"{API_BASE_URL}/observability-logs"
    )

    data = response.json()

    metrics = data["metrics"]

    workflow_runs = data[
        "workflow_runs"
    ]

    node_executions = data[
        "node_executions"
    ]

    alert_events = data[
        "alert_events"
    ]

    # ----------------------------------------
    # KPI METRICS
    # ----------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(

        "Workflow Runs",

        metrics[
            "total_workflows"
        ]
    )

    col2.metric(

        "Node Executions",

        metrics[
            "total_node_executions"
        ]
    )

    col3.metric(

        "Alert Events",

        metrics[
            "total_alerts"
        ]
    )

    col4.metric(

        "Failed Nodes",

        # metrics[
        #     "failed_node_executions"
        # ]
        metrics.get(
            "failed_node_executions",
            0
        )
    )

    st.markdown("---")

    # ----------------------------------------
    # WORKFLOW RUNS
    # ----------------------------------------

    st.subheader(
        "Workflow Runs"
    )

    workflows_df = pd.DataFrame(
        workflow_runs
    )

    st.dataframe(

        workflows_df,

        width="stretch"
    )

    st.markdown("---")

    # ----------------------------------------
    # NODE EXECUTIONS
    # ----------------------------------------

    st.subheader(
        "Node Executions"
    )

    nodes_df = pd.DataFrame(
        node_executions
    )

    st.dataframe(

        nodes_df,

        width="stretch"
    )

    st.markdown("---")

    # ----------------------------------------
    # ALERT EVENTS
    # ----------------------------------------

    st.subheader(
        "Alert Events"
    )

    alerts_df = pd.DataFrame(
        alert_events
    )

    st.dataframe(

        alerts_df,

        width="stretch"
    )