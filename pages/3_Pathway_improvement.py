import streamlit as st
import importlib

# Import the main demo page:
pathway_package = importlib.import_module(
    'streamlit_pathway_improvement.pages.2_Interactive_demo',
    package='2_Interactive_demo.py'
    )
# Run the main function:
pathway_package.main()
