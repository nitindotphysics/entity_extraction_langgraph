import requests
import streamlit as st
import pandas as pd

API_BASE_URL = (
    "http://127.0.0.1:8000"
)

def render_upload_page():

    st.header(
        "Batch Upload & Processing Center"
    )

    st.markdown(
        """
        Upload one or more financial documents
        for automated processing.
        """
    )

    # ----------------------------------------
    # MULTI FILE UPLOAD
    # ----------------------------------------

    uploaded_files = st.file_uploader(

        "Upload PDF Documents",

        type=["pdf"],

        accept_multiple_files=True
    )

    # ----------------------------------------
    # PROCESS BUTTON
    # ----------------------------------------

    if uploaded_files:

        st.info(

            f"{len(uploaded_files)} file(s) selected"
        )

        if st.button(
            "Process Documents"
        ):

            processing_results = []

            progress_bar = st.progress(0)

            total_files = len(
                uploaded_files
            )

            for index, uploaded_file in enumerate(
                uploaded_files
            ):

                with st.spinner(

                    f"Processing {uploaded_file.name}"
                ):

                    files = {

                        "file": (

                            uploaded_file.name,

                            uploaded_file,

                            "application/pdf"
                        )
                    }

                    response = requests.post(

                        f"{API_BASE_URL}/process-document",

                        files=files
                    )

                    result = response.json()

                    processing_results.append({

                        "document_name":

                            uploaded_file.name,

                        "status":

                            result.get(
                                "status"
                            ),

                        "workflow_run_id":

                            result.get(
                                "workflow_run_id"
                            ),

                        "document_type":

                            result.get(
                                "document",
                                {}
                            ).get(
                                "document_type"
                            ),

                        "alert_count":

                            result.get(
                                "alerts",
                                {}
                            ).get(
                                "count"
                            )
                    })

                progress_bar.progress(

                    (index + 1)
                    / total_files
                )

            st.success(
                "Batch processing completed"
            )

            # ----------------------------------------
            # RESULTS TABLE
            # ----------------------------------------

            st.subheader(
                "Processing Results"
            )

            results_df = pd.DataFrame(
                processing_results
            )

            st.dataframe(

                results_df,

                # use_container_width=True
                width="stretch"
            )