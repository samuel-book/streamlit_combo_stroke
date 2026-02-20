"""
Streamlit app for the stroke outcome model.
"""
import streamlit as st

from utilities_top.fixed_params import page_setup
from utilities_top.inputs import write_text_from_file

page_setup()

st.markdown('# :hospital: Stroke Predictions')

st.markdown('''
## Summary

This app contains five demonstrations of modelling and analysis
of stroke treatment and outcomes:
''')

cols = st.columns(2)

with cols[0]:
    st.info(
        '''
**Descriptive statistics**

Describes the characteristics of the patients attending each stroke team.

+ __Inputs:__ Stroke team name or selected features
+ __Outputs:__ Statistics for that stroke team and features.
''', icon='📊')

with cols[1]:
    st.error(
        '''
**Pathway improvement**

Predict the change in thrombolysis use in each stroke team
with different scenarios.

+ __Inputs:__ Scenario type:
  + faster speed to treatment
  + more onset times known
  + match benchmark stroke teams.
+ __Outputs:__ Thrombolysis rate and additional good outcomes
for each stroke team.
''', icon='⏱️')

with cols[0]:
    st.error(
        '''
**Thrombolysis decisions**

Predict the probability of each stroke team providing thrombolysis
to a generated patient.

+ __Inputs:__ Patient details
+ __Outputs:__ Thrombolysis probability from each stroke team.
''', icon='🔮')

with cols[1]:
    st.info(
        '''
**Population outcomes**

Estimate the change in disability levels for a patient population
where some patients are treated at chosen times.

+ __Inputs:__ Times to treatment and the patient population:
  + proportions of stroke types
  + proportions treated
+ __Outputs:__ Population mean mRS and utility.
''', icon='📋')

with cols[0]:
    st.info(
        '''
**Lifetime mortality**

A lifetime economic stroke outcome model for predicting mortality
and lifetime secondary care use by patients who have been discharged
from stroke team following a stroke.

+ __Inputs:__ Patient age, sex, and mRS
+ __Outputs:__ Mortality with time, QALYs, resource use and costs.
''', icon='💷')

st.markdown('## Background information')

cols_stroke_types = st.columns(2)
with cols_stroke_types[0]:
    st.markdown('''
### Stroke types

Patients can have an ischaemic stroke, which is caused by a blood clot, or
a haemorrhaegic stroke, which is caused by a bleed in the brain.

Ischaemic stroke can be further defined by the location of the clot,
which is either:  
+ a large-vessel occlusion (__LVO__), or
+ a non-large-vessel occlusion (__nLVO__).
''')

with cols_stroke_types[1]:
    st.markdown('''
### Treatments
There are two types of treatment available for ischaemic stroke.
Both of these aim to achieve reperfusion, which is the restoration
of the blood supply to the cut-off areas of the brain.

Treatments:
+ intravenous thrombolysis (__IVT__), a clot-busting medication.
+ mechanical thrombectomy (__MT__), which physically removes the clot.

Limitations:
+ Patients with an LVO can be treated with IVT and/or MT.
+ Patients with an nLVO can be treated with IVT.

The benefit received by the patient decreases with time, with each
treatment having no effect after a specified duration
(6.3 hours for IVT, and 8 hours for MT).
''')

write_text_from_file('pages/text_for_pages/1_Intro.txt',
                     head_lines_to_skip=3)
