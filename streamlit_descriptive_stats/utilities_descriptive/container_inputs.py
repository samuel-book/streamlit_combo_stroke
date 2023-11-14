"""
All of the content for the Inputs section.
"""
# Imports
import streamlit as st
import numpy as np


def inputs_region_choice(df_stroke_team, existing_regions=[]):
    """
    Take user inputs for which regions to consider.

    The function finds all of the available regions in the main stats
    dataframe. Each region is given a checkbox so that the user can
    select it independently of the others. All of the selections are
    returned in one list.

    Inputs:
    -------
    df_stroke_team - pd.DataFrame. The descriptive statistics dataframe
                     that contains a column 'RGN11NM' of region names.
                     This name is from the Office for National
                     Statistics field: REGION / 2011 / NAME.
    containers     - list. A list of containers to place the multiple
                     select boxes into. If there are fewer containers
                     in the list than there are select boxes to draw,
                     then subsequent boxes are drawn starting from the
                     beginning of the list again.

    Returns:
    --------
    regions_selected - list. Contains one string per region selected
                       by the user.
    """
    # List of regions in the dataframe:
    region_list = sorted(list(set(
        df_stroke_team['RGN11NM'].squeeze().values
        )))

    regions_selected = st.multiselect(
        'Select region(s):',
        options=region_list,
        default=existing_regions
    )

    return regions_selected


def input_stroke_teams_to_highlight(
        df_stroke_team,
        regions_selected,
        all_teams_str,
        years_selected,
        existing_teams=[]
        ):
    """
    Create input widgets for stroke teams to highlight, split by year.

    Firstly, reduce the list of all stroke teams to just those in the
    regions selected by the user. Then create a separate input widget
    for each year in the data. Combine the inputs from all widgets
    into a single list of selected teams and years and return.

    Inputs:
    -------
    df_stroke_team   - pd.DataFrame. The hospital locations data.
                       Must contain columns for 'Stroke Team' and
                       'RGN11NM' (region name).
    regions_selected - list. Names of regions selected by the user.
    all_teams_str    - str. Name of the "all teams" group in the
                       descriptive stats dataframe.
    year_options     - list. Previously sorted set of items in the
                       "year" row of the descriptive stats dataframe.
    all_years_str    - str. Name of the "all years" group in the
                       year options (e.g. "2016 to 2021").
    containers       - list. Containers to place these widgets in.

    Returns:
    --------
    all_stroke_teams_selected - list. One string per stroke team and
                                year combination selected by the user.
                                e.g. "All E+W (2016)".
    """
    # Create the list of stroke teams in the selected regions.
    # Pull out any row of the dataframe that contains any of the
    # selected region names in any of its columns.
    stroke_team_list = (
        df_stroke_team['Stroke Team'][
            df_stroke_team.isin(regions_selected).any(axis=1)]
    )
    # Add on the "all of this region" teams:
    for region in regions_selected:
        stroke_team_list = np.append(f'All {region}', stroke_team_list)
    # Add on the "all teams" team:
    stroke_team_list = np.append(all_teams_str, stroke_team_list)

    # Input team names:
    # Use this callback function to update the highlighted team names
    # once the user selects something. This method prevents the problem
    # where streamlit doesn't process every second click on the widget.
    def update_teams():
        st.session_state['highlighted_teams_with_click_ds'] = (
            st.session_state['team_input_ds']
        )

    # Input widget:
    stroke_teams_selected = st.multiselect(
        'Pick teams in selected region(s):',
        options=stroke_team_list,
        default=existing_teams,
        key='team_input_ds',
        on_change=update_teams
        )

    # The select box displays just the name of the team.
    # Append the year to these names:
    all_stroke_teams_selected = [
        f'{t} ({year})'
        for year in years_selected
        for t in stroke_teams_selected
        ]
    all_stroke_teams_selected_without_year = (
        stroke_teams_selected * len(years_selected))

    return (
        all_stroke_teams_selected,
        all_stroke_teams_selected_without_year,
        stroke_teams_selected
    )
