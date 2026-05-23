import requests
import streamlit as st
import pandas as pd

API_BASE_URL = (
    "http://127.0.0.1:8000"
)

def render_investigation_page():

    st.header(
        "Document Investigation Dashboard"
    )

    # ----------------------------------------
    # FETCH INVESTIGATION DATA
    # ----------------------------------------

    response = requests.get(

        f"{API_BASE_URL}/investigation-documents"
    )

    documents = response.json()

    # ----------------------------------------
    # EMPTY STATE
    # ----------------------------------------

    if not documents:

        st.info(
            "No investigation documents found"
        )

        return

    # ----------------------------------------
    # MASTER TABLE
    # ----------------------------------------

    st.subheader(
        "Investigation Registry"
    )

    for document in documents:

        # ----------------------------------------
        # SAFE VALUES
        # ----------------------------------------

        customer_name = (
            document.get(
                "customer_name"
            )
            or "N/A"
        )

        workflow_status = (
            document.get(
                "workflow_status"
            )
            or "UNKNOWN"
        )

        alert_count = (
            document.get(
                "alert_count"
            )
            or 0
        )

        transaction_count = (
            document.get(
                "transaction_count"
            )
            or 0
        )

        # ----------------------------------------
        # MASTER ROW TITLE
        # ----------------------------------------

        row_title = (

            f"""
            📄 {document['document_name']}
            | Customer: {customer_name}
            | Transactions: {transaction_count}
            | Alerts: {alert_count}
            | Status: {workflow_status}
            """
        )

        # ----------------------------------------
        # EXPANDABLE INVESTIGATION PANEL
        # ----------------------------------------

        with st.expander(
            row_title
        ):

            # ----------------------------------------
            # TOP METRICS
            # ----------------------------------------

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(

                "Document ID",

                document.get(
                    "document_id"
                )
            )

            col2.metric(

                "Transactions",

                transaction_count
            )

            col3.metric(

                "Alerts",

                alert_count
            )

            col4.metric(

                "Workflow Status",

                workflow_status
            )

            st.markdown("---")

            # ----------------------------------------
            # DOCUMENT METADATA
            # ----------------------------------------

            st.subheader(
                "Document Metadata"
            )

            metadata_df = pd.DataFrame([{

                "Document Name":

                    document.get(
                        "document_name"
                    ),

                "Workflow Run ID":

                    document.get(
                        "workflow_run_id"
                    ),

                "Extraction Required":

                    document.get(
                        "entities_extraction_required"
                    ),

                "Created At":

                    document.get(
                        "created_at"
                    )
            }])

            st.dataframe(

                metadata_df,

                width="stretch"
            )

            st.markdown("---")

            # ----------------------------------------
            # ALERTS SECTION
            # ----------------------------------------

            st.subheader(
                "Generated Alerts"
            )

            alerts = document.get(
                "alerts",
                []
            )

            if alerts:

                alerts_df = pd.DataFrame(
                    alerts
                )

                st.dataframe(

                    alerts_df,

                    width="stretch"
                )

            else:

                st.info(
                    "No alerts generated"
                )

            st.markdown("---")

            # ----------------------------------------
            # NORMALIZED ENTITIES
            # ----------------------------------------

            normalized_entities = document.get(
                "normalized_entities"
            )

            if normalized_entities:

                st.subheader(
                    "Customer & Account Information"
                )

                customer_entities = (

                    normalized_entities.get(
                        "customer_entities",
                        {}
                    )
                )

                account_entities = (

                    normalized_entities.get(
                        "account_entities",
                        {}
                    )
                )

                balance_entities = (

                    normalized_entities.get(
                        "balance_entities",
                        {}
                    )
                )

                entities_df = pd.DataFrame([{

                    "Customer Name":

                        customer_entities.get(
                            "customer_name"
                        ),

                    "Customer ID":

                        customer_entities.get(
                            "customer_id"
                        ),

                    "Account Number":

                        account_entities.get(
                            "account_number"
                        ),

                    "SWIFT Code":

                        account_entities.get(
                            "swift_code"
                        ),

                    "Opening Balance":

                        balance_entities.get(
                            "opening_balance"
                        ),

                    "Closing Balance":

                        balance_entities.get(
                            "closing_balance"
                        ),

                    "Currency":

                        balance_entities.get(
                            "currency"
                        )
                }])

                st.dataframe(

                    entities_df,

                    width="stretch"
                )

                st.markdown("---")

                # ----------------------------------------
                # TRANSACTIONS TABLE
                # ----------------------------------------

                st.subheader(
                    "Transactions"
                )

                transactions = (

                    normalized_entities.get(
                        "transaction_entities",
                        []
                    )
                )

                if transactions:

                    transactions_df = pd.DataFrame(
                        transactions
                    )

                    st.dataframe(

                        transactions_df,

                        width="stretch"
                    )

                else:

                    st.info(
                        "No transactions found"
                    )

            else:

                st.info(
                    "No normalized entities available for this document type"
                )