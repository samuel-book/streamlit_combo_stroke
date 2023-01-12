import streamlit as st
import importlib

# Import the main demo page:
lifetime_module = importlib.import_module(
    'streamlit_lifetime_stroke.pages.2_Interactive_demo',
    package='2_Interactive_demo.py'
    )
# Run the main function:
lifetime_module.main()
