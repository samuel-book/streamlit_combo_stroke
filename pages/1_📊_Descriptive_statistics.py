import streamlit as st
import importlib

# Import the main demo page:
descriptive_stats_module = importlib.import_module(
    'streamlit_descriptive_stats.pages.2_Interactive_demo',
    package='2_Interactive_demo.py'
    )
# Run the main function:
descriptive_stats_module.main()
