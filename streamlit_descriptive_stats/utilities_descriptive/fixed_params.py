import streamlit as st


def page_setup():
    # ----- Page setup -----
    # The following options set up the display in the tab in your browser. 
    # Set page to widescreen must be first call to st.
    st.set_page_config(
        page_title='Descriptive statistics',
        page_icon=':bar_chart:',
        layout='wide'
        )
    # n.b. this can be set separately for each separate page if you like.
