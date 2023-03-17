import streamlit as st
import importlib

# Import the main demo page:
predict_package = importlib.import_module(
    'streamlit_stroke_treatment_ml.pages.2_🔮_Interactive_demo',
    package='2_🔮_Interactive_demo.py'
    )
# Run the main function:
predict_package.main()
