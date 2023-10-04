"""
Descriptive statistics demo.

This app reads in a dataframe containing descriptive statistics
and displays selected parts of it nicely. The stats exist for
acute stroke teams in the SSNAP data.

The dataframe is created in a notebook that is also included in
the app's repository. The data that goes into it is secret.
"""
# ----- Imports -----
import streamlit as st
import pandas as pd


# Add an extra bit to the path if we need to.
# Try importing something as though we're running this from the same
# directory as the landing page.
try:
    from utilities_descriptive.fixed_params import page_setup
except ModuleNotFoundError:
    # If the import fails, add the landing page directory to path.
    # Assume that the script is being run from the directory above
    # the landing page directory, which is called
    # streamlit_lifetime_stroke.
    import sys
    sys.path.append('./streamlit_descriptive_stats/')
    # The following should work now:
    from utilities_descriptive.fixed_params import page_setup
try:
    test_file = pd.read_csv(
        './data_descriptive/stroke_teams.csv',
        index_col='stroke_team'
        )
    dir = './'
except FileNotFoundError:
    # If the import fails, add the landing page directory to path.
    # Assume that the script is being run from the directory above
    # the landing page directory, which is called
    # stroke_outcome_app.
    dir = 'streamlit_descriptive_stats/'

# Custom functions:
from utilities_descriptive.fixed_params import all_teams_str, all_years_str
import utilities_descriptive.container_inputs
import utilities_descriptive.container_results
import utilities_descriptive.container_plots
import utilities_descriptive.plot_utils


def main():
    # ###########################
    # ##### START OF SCRIPT #####
    # ###########################
    page_setup()

    # Title:
    st.markdown('# 📊 Descriptive statistics')
    st.markdown(''.join([
        'Use this tool to compare multiple stroke teams\' ',
        'performances and the characteristics of their patients.'
        ]))

    # Build up the page layout:
    _ = """
    +-----------------------------------------------------------------+
    | 📊 Descriptive statistics                                       |
    | An introductory sentence.                                       |
    |                                                                 |
    +----------cols_inputs_map[0]----------+---cols_inputs_map[1]-----+
    |                                      |                          |
    |       container_input_regions        |                          |
    |                                      |      container_map       |
    |        container_input_teams         |                          |
    +--------------------------------------+--------------------------+
    |                       container_warnings                        |
    |                                                                 |
    |                   container_input_4hr_toggle                    |
    |                                                                 |
    |                        container_results                        |
    |                                                                 |
    |                        container_violins                        |
    |                                                                 |
    |                        container_scatter                        |
    |                                                                 |
    |                        container_details                        |
    +-----------------------------------------------------------------+
    """
    cols_inputs_map = st.columns([0.6, 0.4])
    with cols_inputs_map[0]:
        st.markdown('## Select stroke team data')
        container_input_regions = st.container()
    with cols_inputs_map[0]:
        container_input_teams = st.container()
    with cols_inputs_map[1]:
        container_map = st.container()

    container_warnings = st.container()
    container_input_4hr_toggle = st.container()
    container_results_table = st.container()
    container_violins = st.container()
    container_scatter = st.container()
    container_details = st.container()

    # Each team input box:
    with container_input_teams:
        # st.markdown('### Select stroke teams')
        cols_t = st.columns([0.4, 0.2, 0.2, 0.2])
        with cols_t[0]:
            st.markdown('### Teams:')
        with cols_t[1]:
            st.markdown('### Years:')
        for col in cols_t[2:]:
            with col:
                # Unicode looks-like-a-space character
                # for vertical alignment with the other columns
                # that have text in.
                st.markdown('### \U0000200B')
        containers_list_team_inputs = [
            cols_t[0],             # All years
            cols_t[1], cols_t[2],  # 2016, 2017
            cols_t[3], cols_t[1],  # 2018, 2019
            cols_t[2], cols_t[3],  # 2020, 2021
            cols_t[1]
        ]

    with container_input_regions:
        st.markdown('### Filter by region')
        containers_list_region_inputs = st.columns(3)

    # ###########################
    # ########## SETUP ##########
    # ###########################

    # Decide which descriptive stats file to use:
    with container_input_4hr_toggle:
        limit_to_4hr = st.toggle('Limit to arrival within 4hr')
    if limit_to_4hr:
        summary_stats_file = 'summary_stats_4hr.csv'
    else:
        summary_stats_file = 'summary_stats.csv'
    # Read in the data:
    summary_stats_df = pd.read_csv(
        f'{dir}/data_descriptive/{summary_stats_file}',
        index_col=0
        )

    # Import list of all stroke teams:
    df_stroke_team = pd.read_csv(
        f'{dir}/data_descriptive/hospitals_and_lsoas_descriptive_stats.csv',
        index_col=False
        ).sort_values('Stroke Team')

    # List of years in the data:
    year_options = sorted(set(summary_stats_df.loc['year']))
    # Move the "all years" option to the front of the list:
    year_options.remove(all_years_str)
    year_options = [all_years_str] + year_options

    # Pull in the list of stroke teams that have already been selected.
    try:
        # If we've already selected highlighted teams using the
        # clickable plotly graphs, then load that list:
        existing_teams = st.session_state['highlighted_teams_with_click_ds']
    except KeyError:
        # Make a dummy list so streamlit behaves as normal:
        existing_teams = []
    # Check which regions those existing teams belong in:
    existing_regions = []
    for team in existing_teams:
        if team[:4] != 'All ':
            region = df_stroke_team['RGN11NM'][df_stroke_team['Stroke Team'] == team].squeeze()
            if region not in existing_regions:
                existing_regions.append(region)

    with container_input_regions:
        # Select regions:
        regions_selected = utilities_descriptive.container_inputs.\
            inputs_region_choice(
                df_stroke_team,
                containers_list_region_inputs,
                existing_regions
                )
        # Remove teams that aren't in the selected regions:
        existing_teams_selected_regions = []
        for team in existing_teams:
            if team[:4] != 'All ':
                region = df_stroke_team['RGN11NM'][df_stroke_team['Stroke Team'] == team].squeeze()
                if region in regions_selected:
                    existing_teams_selected_regions.append(team)
            else:
                region = team.split('All ')[1]
                if region in regions_selected:
                    existing_teams_selected_regions.append(team)

    st.session_state['highlighted_teams_with_click_ds'] = (
        existing_teams_selected_regions
    )

    with container_input_teams:
        # Select stroke teams:
        stroke_teams_selected, stroke_teams_selected_without_year, short_stroke_teams_selected_without_year = \
            utilities_descriptive.container_inputs.\
            input_stroke_teams_to_highlight(
                df_stroke_team,
                regions_selected,
                all_teams_str,
                year_options,
                all_years_str=all_years_str,
                containers=containers_list_team_inputs,
                existing_teams=existing_teams_selected_regions
                )

    # Update the colours assigned to the selected teams.
    # These functions update the colours dict in the session state...
    utilities_descriptive.plot_utils.remove_old_colours_for_highlights(
        stroke_teams_selected_without_year)
    utilities_descriptive.plot_utils.choose_colours_for_highlights(
        stroke_teams_selected_without_year)
    # ... and this line pulls out the results of those functions:
    team_colours_dict = st.session_state['highlighted_teams_colours_ds']
    # List of the team colours in the same order as the teams list
    # (used for adding colours to the table).
    team_colours = [team_colours_dict[t] for t
                    in stroke_teams_selected_without_year]

    # Now use these colours in drawing the map:
    with container_map:
        # Plot the team locations
        utilities_descriptive.container_plots.\
            plot_geography_pins(
                df_stroke_team,
                short_stroke_teams_selected_without_year,
                team_colours_dict
                )

    # ###########################
    # ######### RESULTS #########
    # ###########################

    # Check that all of the requested data exists.
    # Remove any teams that don't exist and print a warning message.
    df_to_show = utilities_descriptive.container_results.\
        check_teams_in_stats_df(
            summary_stats_df,
            stroke_teams_selected,
            container_warnings
        )

    # Update the order of the rows to this:
    index_names = {
        'count': 'Count',
        'age': 'Average age',
        'male': 'Male',
        'infarction': 'Infarction',
        'stroke_severity': 'Stroke severity',
        'afib_anticoagulant': 'AF anticoagulants',
        'prior_disability': 'Average pre-stroke disability',
        'prestroke_mrs_0-2': 'Pre-stroke mRS 0-2',
        'onset_known': 'Onset known',
        'precise_onset_known': 'Precise onset known',
        'onset_during_sleep': 'Onset during sleep',
        'onset_to_arrival_time': 'Onset-to-arrival time (minutes)',
        'arrive_in_4_hours': 'Arrive within 4 hours',
        'arrival_to_scan_time': 'Arrival-to-scan time (minutes)',
        'thrombolysis': 'Thrombolysis',
        'scan_to_thrombolysis_time': 'Scan-to-thrombolysis time (minutes)',
        'death': 'Death',
        'discharge_disability': 'Average discharge disability',
        'increased_disability_due_to_stroke':
            'Increased disability due to stroke',
        'mrs_5-6': 'Discharge disability 5-6',
        'mrs_0-2': 'Discharge disability 0-2'
    }
    inverse_index_names = dict(zip(index_names.values(), index_names.keys()))
    # Reduce the dataframe to only these rows, in that order:
    df_to_show = df_to_show.loc[list(index_names.keys())]
    # Convert all string values to numeric:
    # (when imported, the dataframe contained strings in the stroke_team
    # column. Now that's gone, it's all numeric data.)
    df_to_show = df_to_show.apply(pd.to_numeric)

    # Change format to percentage:
    rows_percentage = [
        'male', 'infarction', 'afib_anticoagulant',
        'prestroke_mrs_0-2', 'onset_known', 'precise_onset_known',
        'onset_during_sleep', 'arrive_in_4_hours', 'thrombolysis',
        'death', 'mrs_5-6', 'mrs_0-2'
    ]
    for row in rows_percentage:
        df_to_show.loc[row] = df_to_show.loc[row].apply('{:.1%}'.format)
    # Change format to integer:
    df_to_show.loc['count'] = df_to_show.loc['count'].apply('{:.0f}'.format)
    # Change format of time rows:
    rows_time = [
        'onset_to_arrival_time',
        'arrival_to_scan_time',
        'scan_to_thrombolysis_time'
    ]
    for row in rows_time:
        df_to_show.loc[row] = df_to_show.loc[row].apply('{:.0f}'.format)
    # Change format of float rows:
    rows_float = [
        'age', 'stroke_severity', 'prior_disability',
        'discharge_disability', 'increased_disability_due_to_stroke'
    ]
    for row in rows_float:
        df_to_show.loc[row] = df_to_show.loc[row].apply('{:.2f}'.format)

    # Update index names.
    df_to_show.index = index_names.values()

    # Apply styles to the table:
    df_to_show = utilities_descriptive.container_results.\
        apply_styles_to_dataframe(df_to_show, team_colours)

    # Draw in streamlit:
    with container_results_table:
        st.header('Results')
        st.table(df_to_show)

    # #########################
    # ######### PLOTS #########
    # #########################

    with container_violins:
        st.header('One feature over time')
        st.markdown('Compare one feature across multiple years.')

        # User inputs for which feature to plot:
        feature_display = st.selectbox(
            'Pick a feature to plot',
            options=index_names.values(),
            # default='count'
        )
        # Convert this to actual feature name:
        feature = inverse_index_names[feature_display]

        utilities_descriptive.container_plots.plot_violins(
            summary_stats_df,
            feature,
            feature_display,
            year_options,
            stroke_teams_selected_without_year,
            all_years_str,
            all_teams_str,
            team_colours_dict
            )

    with container_scatter:
        st.header('Relation between two features')
        st.markdown('Compare the variation of two features across hospitals.')
        cols_scatter_inputs = st.columns(3)
        # Pick two features to scatter:
        with cols_scatter_inputs[0]:
            x_feature_display_name = st.selectbox(
                'Feature for x-axis',
                options=index_names.values()
            )
            x_feature_name = inverse_index_names[x_feature_display_name]

        with cols_scatter_inputs[1]:
            y_feature_display_name = st.selectbox(
                'Feature for y-axis',
                options=index_names.values()
            )
            y_feature_name = inverse_index_names[y_feature_display_name]

        with cols_scatter_inputs[2]:
            year_restriction = st.selectbox(
                'Years to show',
                options=year_options
            )

        utilities_descriptive.container_plots.scatter_fields(
            x_feature_name,
            y_feature_name,
            year_restriction,
            summary_stats_df,
            stroke_teams_selected_without_year,
            team_colours_dict,
            x_feature_display_name,
            y_feature_display_name,
            )

    with container_details:
        st.markdown(
            '''
## Where do these numbers come from?

### Original data

We start with a large dataset of a few hundreds of thousands of patients who attended stroke units across England and Wales.
The data is limited to patients with out-of-hospital onset who arrive by ambulance.
The data comes from the Sentinel Stroke National Audit Programme (SSNAP).

We keep a copy of this original data and also create a subset that contains only patients who have known onset time and who arrived at hospital within four hours of stroke onset.
Which of these two datasets is shown in the app is controlled with a "limit to 4hrs" toggle button.

### Calculating the statistics

The large dataset is broken down into smaller groups depending on which team(s) are being considered.
For the "All England & Wales" group we use the full dataset.
For "All South West" we use only patients who attended teams in the South West, and so on.
When a specific team name is given, we use only patients who attended that team.

One of these smaller groups will still contain many patients.
We show the total number in the group with the "count" row in the table.
For all of the other rows in the table, we wish to show an average value across all of these patients.
For properties involving time ('onset_to_arrival_time', 'arrival_to_scan_time', 'scan_to_thrombolysis_time') we take the median time.
For all other properties, we take the mean value across all patients.
'''
        )

    # ----- The end! -----


if __name__ == '__main__':
    main()
