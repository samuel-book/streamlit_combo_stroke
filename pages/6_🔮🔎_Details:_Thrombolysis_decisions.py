import streamlit as st
import importlib

# Import the main demo page:
predict_package = importlib.import_module(
    'streamlit_stroke_treatment_ml.pages.3_🔎_Details',
    package='3_🔎_Details.py'
    )
# Run the main function:
predict_package.main()
