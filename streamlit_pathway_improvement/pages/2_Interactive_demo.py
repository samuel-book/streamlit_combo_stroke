"""
Streamlit app template.

Because a long app quickly gets out of hand,
try to keep this document to mostly direct calls to streamlit to write
or display stuff. Use functions in other files to create and
organise the stuff to be shown. In this example, most of the work is
done in functions stored in files named container_(something).py
"""
# ----- Imports -----
import streamlit as st
import pandas as pd

# Add an extra bit to the path if we need to.
# Try importing something as though we're running this from the same
# directory as the landing page.
try:
    from utilities_pathway.fixed_params import page_setup
except ModuleNotFoundError:
    # If the import fails, add the landing page directory to path.
    # Assume that the script is being run from the directory above
    # the landing page directory, which is called
    # streamlit_pathway_improvement.
    import sys
    sys.path.append('./streamlit_pathway_improvement/')

# For importing data:
try:
    stroke_teams_test = pd.read_csv('./data_pathway/scenario_results.csv')
    dir = './'
except FileNotFoundError:
    dir = 'streamlit_pathway_improvement/'


# Custom functions:
from utilities_pathway.fixed_params import page_setup
from utilities_pathway.inputs import \
    write_text_from_file


# ###########################
# ##### START OF SCRIPT #####
# ###########################
page_setup()

# Title:
st.markdown('# Pathway improvement')


# ###########################
# ########## SETUP ##########
# ###########################

df = pd.read_csv(
    dir + 'data_pathway/scenario_results.csv',
    # index_col=index_col,
    header='infer'
    )

# Baseline_good_outcomes_(median)
# Baseline_good_outcomes_per_1000_patients_(low_5%)
# Baseline_good_outcomes_per_1000_patients_(high_95%)
# Baseline_good_outcomes_per_1000_patients_(mean)
# Baseline_good_outcomes_per_1000_patients_(stdev)
# Baseline_good_outcomes_per_1000_patients_(95ci)
# Percent_Thrombolysis_(median%)
# Percent_Thrombolysis_(low_5%)
# Percent_Thrombolysis_(high_95%)
# Percent_Thrombolysis_(mean)
# Percent_Thrombolysis_(stdev)
# Percent_Thrombolysis_(95ci)
# Additional_good_outcomes_per_1000_patients_(median)
# Additional_good_outcomes_per_1000_patients_(low_5%)
# Additional_good_outcomes_per_1000_patients_(high_95%)
# Additional_good_outcomes_per_1000_patients_(mean)
# Additional_good_outcomes_per_1000_patients_(stdev)
# Additional_good_outcomes_per_1000_patients_(95ci)
# Onset_to_needle_(mean)
# calibration
# scenario
# stroke_team

# Pull out the list of stroke teams:
stroke_team_list = sorted(set(df['stroke_team'].to_numpy()))

# Select a team
team_input = st.selectbox(
    'Pick a team',
    stroke_team_list
    )

# Pick out just the data for the chosen team:
df_here = df[df['stroke_team'] == team_input]



# ###########################
# ######### RESULTS #########
# ###########################

# Make a bar chart of the mean values:
import plotly.graph_objects as go

cols_bar = st.columns(2)
with cols_bar[0]:
    # Percentage thrombolysis use:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_here['scenario'],
        y=df_here['Percent_Thrombolysis_(mean)']
    ))

    fig.update_xaxes(title='Scenario')
    fig.update_yaxes(title='Percent Thrombolysis (mean)')

    st.plotly_chart(fig, use_container_width=True)

with cols_bar[1]:
    # Additional good outcomes 
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_here['scenario'],
        y=df_here['Additional_good_outcomes_per_1000_patients_(mean)'],
        marker=dict(color='red')
    ))

    fig.update_xaxes(title='Scenario')
    fig.update_yaxes(title='Additional_good_outcomes_per_1000_patients_(mean)')

    st.plotly_chart(fig, use_container_width=True)


st.write('Full data for this team: ')
st.write(df_here)

# ----- The end! -----
