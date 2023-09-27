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
import numpy as np
import json
import plotly.graph_objs as go


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
# from utilities_descriptive.fixed_params import page_setup
# from utilities.inputs import \
#     write_text_from_file
# Containers:
# import utilities.container_inputs
# import utilities.container_results
# import utilities.container_details


def make_emoji_dict_by_team(
        year_options,
        stroke_team_list,
        stroke_team_list_years
        ):
    # Start with black circle for "all teams" group:
    emoji_teams_vals = ['⚫'] * len(year_options)
    # Cycle through these emoji for the other stroke teams:
    emoji_teams = ['🔴', '🟠', '🟡', '🟢', '🔵', '🟣'] # '🟤' '⚪' '⚫' ⏺
    for i in range(len(stroke_team_list)):
        emoji_teams_vals += [emoji_teams[i % len(emoji_teams)]] * len(year_options)
    # st.write(text_colours_vals)
    emoji_teams_dict = dict(zip(stroke_team_list_years, emoji_teams_vals))
    return emoji_teams_dict


def make_emoji_dict_by_region(
        emoji_regions_dict,
        year_options,
        stroke_team_list,
        stroke_team_list_years,
        region_list,
        all_regions_str = 'all E+W'
        ):

    # Start with "all teams" group:
    emoji_teams_vals = [emoji_regions_dict[all_regions_str]] * len(year_options)
    for i in range(len(stroke_team_list)):
        emoji_teams_vals += [emoji_regions_dict[region_list[i]]] * len(year_options)
    # st.write(text_colours_vals)
    emoji_teams_dict = dict(zip(stroke_team_list_years, emoji_teams_vals))
    return emoji_teams_dict


def build_lists_for_each_team_and_year(stroke_team_list, year_options, region_team_list):
    stroke_team_list_years = [
        f'{s} ({y})'
        for s in ['all E+W'] + stroke_team_list
        for y in year_options
    ]
    # Builds a list containing:
    # Team 1 (2016 to 2021)
    # Team 1 (2016)
    # Team 1 (2017)
    # ...
    # Team 1 (2021)
    # Team 2 (2016 to 2021)
    # Team 2 (2016)
    # Team 2 (2017)
    # ...
    # Team 2 (2021)
    # Similar for regions:
    region_team_list_years = [
        region
        for region in ['all E+W'] + region_team_list
        for y in year_options
    ]
    return stroke_team_list_years, region_team_list_years


def inputs_region_choice(region_list):
    cols_regions = st.columns(3)
    regions_selected_bool = []
    for r, region in enumerate(region_list):
        with cols_regions[r % len(cols_regions)]:
            region_bool = st.checkbox(region, key=region)
        regions_selected_bool.append(region_bool)
    regions_selected = list(np.array(region_list)[regions_selected_bool])
    return regions_selected


def reduce_big_lists_to_regions_selected(
        region_team_list_years,
        regions_selected,
        stroke_team_list_years,
        emoji_teams_dict
):
    full_list_regions_selected_bool = np.full(len(region_team_list_years), False)
    for region in ['all E+W'] + regions_selected:
        inds = np.where(np.array(region_team_list_years) == region)
        full_list_regions_selected_bool[inds] = True

    stroke_team_list_years_by_region_selected = (
        np.array(stroke_team_list_years)[full_list_regions_selected_bool]
    )
    # st.write(emoji_teams_dict.keys())
    # st.write(emoji_teams_dict.keys())
    emoji_teams_dict_by_region_selected = dict(
        zip(
            np.array(list(emoji_teams_dict.keys()))[full_list_regions_selected_bool],
            np.array(list(emoji_teams_dict.values()))[full_list_regions_selected_bool]
            )
        )
    return (stroke_team_list_years_by_region_selected,
            emoji_teams_dict_by_region_selected)


def plot_geography_pins(region_list, df_stroke_team):
    fig = go.Figure()

    fig.update_layout(
        width=500,
        height=500,
        margin_l=0, margin_r=0, margin_t=0, margin_b=0
        )

    # for region in region_list:
    geojson_file = 'regions_EW.geojson'  # 'region_' + region.replace(' ', '~') + '.geojson'
    with open('./data_descriptive/region_geojson/' + geojson_file) as f:
        geojson_ew = json.load(f)
    # Find extent of this geojson data.
    import geojson
    coords = np.array(list(geojson.utils.coords(geojson_ew)))
    extent = [
        coords[:, 0].min(),
        coords[:, 0].max(),
        coords[:, 1].min(),
        coords[:, 1].max()
    ]

    df_regions = pd.DataFrame(region_list, columns=['RGN11NM'])
    df_regions['v'] = [0] * len(df_regions) #np.arange(len(df_regions))
    
    # st.write(geojson_ew['features']['properties'])

    fig.add_trace(go.Choropleth(
        geojson=geojson_ew,
        locations=df_regions['RGN11NM'],
        z=df_regions['v'],
        featureidkey='properties.RGN11NM',
        # coloraxis="coloraxis",
        colorscale='Picnic',
        # autocolorscale=False
        showscale=False,
        hoverinfo='skip'
    ))

    fig.add_trace(go.Scattergeo(
        lon=df_stroke_team['long'],
        lat=df_stroke_team['lat'],
        customdata=np.stack([df_stroke_team['Stroke Team']], axis=-1),
        mode='text',
        text=df_stroke_team['emoji']
        # marker_color=df_stroke_team['RGN11NM']
    ))
    fig.update_layout(
        geo_scope='europe',
        geo_resolution=50,
        geo_projection=go.layout.geo.Projection(type = 'airy'),
        geo_lonaxis_range=[extent[0], extent[1]],
        geo_lataxis_range=[extent[2], extent[3]],
    )

    fig.update_traces(
        hovertemplate='%{customdata[0]}<extra></extra>',
        selector=dict(type='scattergeo')
    )
    fig.update_traces(
        hovertemplate='%{customdata[0]}<extra></extra>',
        selector=dict(type='scattergeo')
    )

    fig.update_geos(fitbounds="locations", visible=False)

    plotly_config = {
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    }
    st.plotly_chart(fig, config=plotly_config)
    st.caption('Locations of the stroke teams, colour-coded by region.')


def main():
    # ###########################
    # ##### START OF SCRIPT #####
    # ###########################
    page_setup()

    # Title:
    st.markdown('# 📊 Descriptive statistics')

    # ###########################
    # ########## SETUP ##########
    # ###########################

    all_regions_str = 'all E+W'

    # Import list of all stroke teams:
    df_stroke_team = pd.read_csv(
        dir + './data_descriptive/hospitals_and_lsoas_descriptive_stats.csv',
        index_col=False).sort_values('Stroke Team')

    # List of stroke teams
    stroke_team_list = list(df_stroke_team['Stroke Team'].squeeze().values)

    # List of regions
    region_list = sorted(list(set(df_stroke_team['RGN11NM'].squeeze().values)))
    region_team_list = list(df_stroke_team['RGN11NM'].squeeze().values)

    region_list = [
        'North East',
        'North West',
        'Yorkshire and The Humber',
        'East Midlands',
        'West Midlands',
        'Wales',
        'South West',
        'South East',
        'East of England',
        'London',
    ]
    # Use these emoji for the regions:
    emoji_teams = [
        '',  # for "all regions"
        '🔴', '🟠', '🟡', '🟢', '🔵', '🟣', '🟤', '⚪', '⚫', '🩵'
        ]
    # st.write('''
    # 🟥🟧🟨🟩🟦🟪🟫⬜⬛  
    # 🔴🟠🟡🟢🔵🟣🟤⚪⚫  
    # ❤️🧡💛💚💙🩵💜🤎🖤🩶🤍  
    # ''')
    region_set = [all_regions_str] + region_list
    emoji_regions_dict = dict(zip(region_set, emoji_teams))

    df_stroke_team['emoji'] = [emoji_regions_dict[region] for region in df_stroke_team['RGN11NM']]

    cols_regions = st.columns([0.6, 0.4])
    with cols_regions[1]:
        # Plot the team locations
        plot_geography_pins(region_list, df_stroke_team)

    # Add in all the year options:
    year_options = ['2016 to 2021', '2016', '2017',
                    '2018', '2019', '2020', '2021']

    stroke_team_list_years, region_team_list_years = (
        build_lists_for_each_team_and_year(
            stroke_team_list, year_options, region_team_list)
    )

    emoji_teams_dict = make_emoji_dict_by_region(
        emoji_regions_dict,
        year_options,
        stroke_team_list,
        stroke_team_list_years,
        region_team_list
        )

    with cols_regions[0]:
        # Select a region:
        st.markdown('Show teams from these regions:')
        regions_selected = inputs_region_choice(region_list)

    # Reduce the big lists to only regions selected:
    (stroke_team_list_years_by_region_selected,
     emoji_teams_dict_by_region_selected
     ) = reduce_big_lists_to_regions_selected(
        region_team_list_years,
        regions_selected,
        stroke_team_list_years,
        emoji_teams_dict
        )


    with cols_regions[0]:
        # Use the format function in the multiselect to change how
        # the team names are displayed without changing their names
        # in the underlying data.
        # Because the current ordering of the list is by team and then
        # by year, this also visually breaks up the list into groups of
        # each team.
        stroke_teams_selected = st.multiselect(
            'Stroke team',
            options=stroke_team_list_years_by_region_selected,
            default='all E+W (2016 to 2021)',
            format_func=(lambda x: f'{emoji_teams_dict_by_region_selected[x]} {x}')
            )

        limit_to_4hr = st.toggle('Limit to arrival within 4hr')

    if limit_to_4hr:
        summary_stats_file = 'summary_stats_4hr.csv'
    else:
        summary_stats_file = 'summary_stats.csv'

    summary_stats_df = pd.read_csv(
        dir + './data_descriptive/' + summary_stats_file, index_col=0
    )

    # Find which teams are in the stroke teams options but
    # are not in the stats dataframe:
    missing_teams_list = (
        set(stroke_team_list_years) -
        set(summary_stats_df.columns)
    )

    teams_to_show = stroke_teams_selected

    # ###########################
    # ######### RESULTS #########
    # ###########################
    st.header('Results')

    try:
        df_to_show = summary_stats_df[teams_to_show]
    except KeyError:
        # Remove teams that aren't in the dataframe:
        reduced_teams_to_show = []
        for team in teams_to_show:
            if team in missing_teams_list:
                st.markdown(f':warning: There is no data for {team}.')
            else:
                reduced_teams_to_show.append(team)
        df_to_show = summary_stats_df[reduced_teams_to_show]

    row_order = [
        'count',
        'age',
        'male',
        'infarction',
        'stroke severity',
        'onset-to-arrival time',
        'onset known',
        'arrive in 4  hours',
        'precise onset known',
        'onset during sleep',
        'use of AF anticoagulants',
        'prior disability',
        'prestroke mrs 0-2',
        'arrival-to-scan time',
        'thrombolysis',
        'scan-to-thrombolysis time',
        'death',
        'discharge disability',
        'increased disability due to stroke',
        'mrs 5-6',
        'mrs 0-2'
    ]
    df_to_show = df_to_show.loc[row_order]
    st.table(df_to_show)

    # ----- The end! -----


if __name__ == '__main__':
    main()
