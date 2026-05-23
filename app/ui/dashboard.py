import streamlit as st

from components.upload import (
    render_upload_page
)

from components.investigation import (
    render_investigation_page
)

from components.observability import (
    render_observability_page
)

# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------

st.set_page_config(

    page_title="Financial Document AI",

    layout="wide"
)

# ----------------------------------------
# TITLE
# ----------------------------------------

st.title(
    "Financial Document Intelligence Platform"
)

st.markdown("---")

# ----------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------

page = st.sidebar.radio(

    "Navigation",

    [

        "Upload Center",

        "Investigation Dashboard",

        "Observability Logs"
    ]
)

# ----------------------------------------
# ROUTING
# ----------------------------------------

if page == "Upload Center":

    render_upload_page()

elif page == "Investigation Dashboard":

    render_investigation_page()

elif page == "Observability Logs":

    render_observability_page()