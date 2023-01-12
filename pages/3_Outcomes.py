import streamlit as st
import importlib

# Import the main demo page:
outcome_package = importlib.import_module(
    'stroke_outcome_app.pages.2_Interactive_demo',
    package='2_Interactive_demo.py'
    )
# Run the main function:
outcome_package.main()
