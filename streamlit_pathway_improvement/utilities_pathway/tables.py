"""
Functions for writing tables on the pathway app.
"""
# ----- Imports -----
import streamlit as st
import pandas as pd

from utilities_pathway.fixed_params import \
    default_highlighted_team, display_name_of_default_highlighted_team

def show_data_for_team(team, df):
    if team == display_name_of_default_highlighted_team:
        team_filter = default_highlighted_team
    else:
        team_filter = team
    
    df_team = df[df['stroke_team'] == team_filter]
    # Only keep the columns we want:
    df_team = df_team[[
        'scenario',
        'Percent_Thrombolysis_(mean)',
        'Percent_Thrombolysis_(mean)_diff',
        'Baseline_good_outcomes_per_1000_patients_(mean)',
        'Additional_good_outcomes_per_1000_patients_(mean)',
        'Additional_good_outcomes_per_1000_patients_(mean)_diff'
        ]]
    
    # Rename the columns so they look nicer:
    df_team.rename(columns={
        'scenario': 'Scenario',
        'Percent_Thrombolysis_(mean)': 'Percent thrombolysis (mean)',
        'Percent_Thrombolysis_(mean)_diff': 'Change from base (percent thrombolysis)',
        'Baseline_good_outcomes_per_1000_patients_(mean)': 'Baseline good outcomes per 1000 patients (mean)',
        'Additional_good_outcomes_per_1000_patients_(mean)': 'Additional good outcomes per 1000 patients (mean)',
        'Additional_good_outcomes_per_1000_patients_(mean)_diff': 'Change from base (additional good outcomes)'
        }, inplace=True)

    # Rename values in the 'Scenario' column:
    df_team['Scenario'].replace({
        'base': 'Base',
        'speed': 'Speed',
        'onset': 'Onset',
        'benchmark': 'Benchmark',
        'speed_onset': 'Speed + Onset',
        'speed_benchmark': 'Speed + Benchmark',
        'onset_benchmark': 'Onset + Benchmark',
        'speed_onset_benchmark': 'Speed + Onset + Benchmark'
        }, inplace=True)
    
    # Set the 'scenario' column to be the index values:
    df_team = df_team.set_index('Scenario')

    # Make a style dictionary so all values are printed
    # with 2 decimal places.
    style_dict = {}
    for col in df_team.columns:
        style_dict[col] = '{:,.2f}'.format

    # Write to streamlit:
    st.dataframe(df_team.style.format(style_dict))


def show_data_for_all(df):
    display_columns = [
        'Percent thrombolysis (mean)',
        'Change from base (percent thrombolysis)',
        'Baseline good outcomes per 1000 patients (mean)',
        'Additional good outcomes per 1000 patients (mean)',
        'Change from base (additional good outcomes)'
        ]
    display_scenarios = [
        'Base',
        'Speed',
        'Onset',
        'Benchmark',
        'Speed + Onset',
        'Speed + Benchmark',
        'Onset + Benchmark',
        'Speed + Onset + Benchmark'
    ]

    # # User inputs for which columns to show:
    # columns_to_keep_display = st.multiselect(
    #     'Columns to show',
    #     display_columns,
    #     default=display_columns
    # )
    # columns_to_keep_display_sorted = [column for column in display_columns if column in columns_to_keep_display]
    # columns_to_keep_display = columns_to_keep_display_sorted
    columns_to_keep_display = display_columns
    # User inputs for which scenarios to show:
    scenarios_to_keep_display = st.multiselect(
        'Scenarios to include in the table',
        display_scenarios,
        default=display_scenarios
    )

    # Rename the columns so they look nicer:
    df.rename(columns={
        'stroke_team': 'Stroke team',
        'scenario': 'Scenario',
        'Percent_Thrombolysis_(mean)': 'Percent thrombolysis (mean)',
        'Percent_Thrombolysis_(mean)_diff': 'Change from base (percent thrombolysis)',
        'Baseline_good_outcomes_per_1000_patients_(mean)': 'Baseline good outcomes per 1000 patients (mean)',
        'Additional_good_outcomes_per_1000_patients_(mean)': 'Additional good outcomes per 1000 patients (mean)',
        'Additional_good_outcomes_per_1000_patients_(mean)_diff': 'Change from base (additional good outcomes)'
        }, inplace=True)
    
    # Only keep the columns we want:
    df = df[[
        'Stroke team',
        'Scenario',
        *columns_to_keep_display
        ]]
    
    # Rename values in the 'Scenario' column:
    # Use this rather indirect syntax to avoid SettingWithCopyWarning.
    replace_dict = {
        'base': 'Base',
        'speed': 'Speed',
        'onset': 'Onset',
        'benchmark': 'Benchmark',
        'speed_onset': 'Speed + Onset',
        'speed_benchmark': 'Speed + Benchmark',
        'onset_benchmark': 'Onset + Benchmark',
        'speed_onset_benchmark': 'Speed + Onset + Benchmark'
        }
    for i, key in enumerate(list(replace_dict.keys())):
        df.loc[df['Scenario'] == key, 'Scenario'] = list(replace_dict.values())[i]
    # Only keep the scenarios we want:
    df = df[df['Scenario'].isin(scenarios_to_keep_display)]

    # Rename default highlighted team in the 'stroke_team' column:
    df['Stroke team'].replace({
        default_highlighted_team: display_name_of_default_highlighted_team
        }, inplace=True)
    # Sort the dataframe by this column otherwise you can work out
    # the real name of the default highlighted team.
    df.sort_values(['Stroke team', 'Scenario'], inplace=True)

    # Set the 'stroke_team' column to be the index values:
    df = df.set_index('Stroke team')

    # Make a style dictionary so all values are printed
    # with 2 decimal places.
    style_dict = {}
    for col in df.columns:
        if col != 'Scenario':
            style_dict[col] = '{:,.2f}'.format

    # Write to streamlit:
    st.dataframe(df.style.format(style_dict))
