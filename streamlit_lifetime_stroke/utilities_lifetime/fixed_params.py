"""
Define constants that will be used in multiple places throughout the
script but that only need to be defined once.
"""
import streamlit as st


def page_setup():
    """
    Set up the display in the tab in your browser.

    n.b. Set page to widescreen must be first call to st.
    """
    st.set_page_config(
        page_title='Lifetime outcomes',
        page_icon='💷',
        # layout='wide'
        )


# Colour scheme to match Excel hazard chart:
# #RRGGBB in hex.
colours_excel = [
    '#ffc000',   # mRS 0
    '#ed7d31',   # mRS 1
    '#a5a5a5',   # mRS 2
    '#b4c7e7',   # mRS 3
    '#5b9bd5',   # mRS 4
    '#70ad47',   # mRS 5
]
