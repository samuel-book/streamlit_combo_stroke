"""
Plots for the descriptive stats demo.
"""
import streamlit as st
import plotly.graph_objs as go
import geojson
import numpy as np
import pandas as pd
from scipy.stats import linregress
# For clickable plotly events:
from streamlit_plotly_events import plotly_events

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


def plot_geography_pins(
        df_stroke_team,
        stroke_teams_selected,
        team_colours_dict
        ):
    """
    Plot a map of England and Wales with the stroke teams marked.

    This draws a shape for each region from a geojson that was created
    by combining all super-generalised LSOA shapes in each region.
    The markers are drawn using latitude and longitude coordinates that
    were generated from the stroke teams' postcodes. Most teams get a
    generic marker, but teams in the input list get their own colour.

    Inputs:
    -------
    df_stroke_team        - pd.DataFrame. Dataframe of team locations.
                            Must contain columns 'lat', 'long', and
                            'Stroke Team' for marker positions/labels.
    stroke_teams_selected - list. List of stroke teams to highlight.
    team_colours_dict     - dict. Keys are stroke teams, values are
                            colours to plot them in.
    """
    # Import geojson data:
    geojson_file = 'regions_EW.geojson'
    with open(dir + './data_descriptive/region_geojson/' + geojson_file) as f:
        geojson_ew = geojson.load(f)

    # Find extent of this geojson data.
    # This will be used later to set the plot's axis limits.
    coords = np.array(list(geojson.utils.coords(geojson_ew)))
    extent = [
        coords[:, 0].min(),
        coords[:, 0].max(),
        coords[:, 1].min(),
        coords[:, 1].max()
    ]

    # Get the names of the regions out of the geojson:
    region_list = []
    for feature in geojson_ew['features']:
        region = feature['properties']['RGN11NM']
        region_list.append(region)

    # Create a dummy dataframe of region names and some value for colours.
    df_regions = pd.DataFrame(region_list, columns=['RGN11NM'])
    df_regions['v'] = [0] * len(df_regions)  # Same value, same colour.

    # Plot:
    fig = go.Figure()
    # Sneakily make a slightly taller figure when there are more
    # highlighted teams selected. This is because the legend gets
    # taller and will start reducing the size of the map axes
    # unless more room is provided.
    fig_height = 500 + 20*len([t for t in stroke_teams_selected
                             if t[:4] != 'All '])
    fig.update_layout(
        width=500,
        height=fig_height,
        margin_l=0, margin_r=0, margin_t=0, margin_b=0
        )

    # Add region polygons:
    fig.add_trace(go.Choropleth(
        geojson=geojson_ew,
        locations=df_regions['RGN11NM'],
        z=df_regions['v'],
        featureidkey='properties.RGN11NM',
        colorscale=[
            [0.0, "rgba(0, 0, 0, 0)"],
            [1.0, "rgba(0, 0, 0, 0)"]],
        showscale=False,
        hoverinfo='skip',
        marker_line_color='DarkGrey'
    ))
    # The custom colour scale goes from transparent to transparent.
    # All of the plotted shapes will have no colour.

    # Add scatter markers for all non-selected hospitals:
    # Pull out any row of the dataframe that contains any of the
    # selected stroke team names in any of its columns.
    df_most_teams = (
        df_stroke_team[
            ~df_stroke_team.isin(stroke_teams_selected).any(axis=1)]
    )
    fig.add_trace(go.Scattergeo(
        lon=df_most_teams['long'],
        lat=df_most_teams['lat'],
        customdata=np.stack([df_most_teams['Stroke Team']], axis=-1),
        mode='markers',
        marker_color='Firebrick',
        marker_size=8,
        marker_symbol='cross',
        # showlegend=False
        name='Stroke teams'
    ))

    # Add scatter markers for the selected hospitals.
    # Remove any of the "all teams" or "all region" data:
    stroke_teams_highlighted = [t for t in stroke_teams_selected
                                if t[:4] != 'All ']
    for stroke_team in stroke_teams_highlighted:
        colour = team_colours_dict[stroke_team]
        df_this_team = (
            df_stroke_team[df_stroke_team['Stroke Team'] == stroke_team]
        )
        fig.add_trace(go.Scattergeo(
            lon=df_this_team['long'],
            lat=df_this_team['lat'],
            customdata=np.stack([df_this_team['Stroke Team']], axis=-1),
            mode='markers',
            marker_color=colour,
            marker_line_color='black',
            marker_line_width=1.0,
            marker_size=10,
            # showlegend=False
            name=stroke_team
        ))

    # Update geojson projection.
    # Projection options:
    #   august  eckert1  fahey  times  van der grinten
    # ^ these ones look ok by eye. There's a longer list in the docs.
    # (Seems that they don't work with plotly events?)
    fig.update_layout(
        geo_scope='europe',
        geo_projection=go.layout.geo.Projection(type='airy'),
        geo_lonaxis_range=[extent[0], extent[1]],
        geo_lataxis_range=[extent[2], extent[3]],
        # geo_resolution=50,
        geo_visible=False
    )
    # fig.update_geos(fitbounds="locations", visible=False)

    # Update hover info for scatter points:
    fig.update_traces(
        hovertemplate='%{customdata[0]}<extra></extra>',
        selector=dict(type='scattergeo')
    )
    # Move legend:
    fig.update_layout(legend=dict(x=0, y=0, yanchor='top'))

    # Add transparent background:
    fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))

    # # Remove some buttons from the mode bar (top corner on hover).
    # plotly_config = {
    #     'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    # }
    # st.plotly_chart(fig, config=plotly_config)
    # Write the plot to streamlit, and store the details of the last
    # marker that was clicked:
    selected_marker = plotly_events(
        fig, click_event=True, #key='waterfall_combo',
        override_height=fig_height, override_width='100%')
    callback_geography(
        selected_marker,
        stroke_teams_selected,
        stroke_teams_highlighted,
        df_stroke_team['Stroke Team'].squeeze()
        )
    st.caption('Locations of the stroke teams.')


def callback_geography(
        selected_bar,
        stroke_teams_selected,
        stroke_teams_highlighted,
        stroke_teams_all
        ):
    """
    # When the script is re-run, this value of selected bar doesn't
    # change. So if the script is re-run for another reason such as
    # a streamlit input widget being changed, then the selected bar
    # is remembered and it looks indistinguishable from the user
    # clicking the bar again. To make sure we only make updates if
    # the user actually clicked the bar, compare the current returned
    # bar details with the details of the last bar *before* it was
    # changed.
    # When moved to or from the highlighted list, the bar is drawn
    # as part of a different trace and so its details such as
    # curveNumber change.
    # When the user clicks on the same bar twice in a row, we do want
    # the bar to change. For example, a non-highlighted bar might have
    # curveNumber=0, then when clicked changes to curveNumber=1.
    # When clicked again, the last_changed_bar has curveNumber=0,
    # but selected_bar has curveNumber=1. The bar details have changed
    # and so the following loop still happens despite x and y being
    # the same.
    """
    try:
        # Pull the details out of the last bar that was changed
        # (moved to or from the "highlighted" list due to being
        # clicked on) out of the session state:
        last_changed_bar = st.session_state['last_changed_marker_ds']
    except KeyError:
        # Invent some nonsense. It doesn't matter whether it matches
        # the default value of selected_bar before anything is clicked.
        last_changed_bar = [0]

    if selected_bar != last_changed_bar:
        # If the selected bar doesn't match the last changed bar,
        # then we need to update the graph and store the latest
        # clicked bar.
        try:
            # If a bar has been clicked, then the following line
            # will not throw up an IndexError:
            c = selected_bar[0]['curveNumber']
            p = selected_bar[0]['pointIndex']

            # List of all non-highlighted teams:
            stroke_teams_not_highlighted = [
                t for t in stroke_teams_all
                if t not in stroke_teams_selected
                ]
            if c > 1:
                # This is a highlighted team.
                team_selected = stroke_teams_highlighted[c - 2]
            else:
                team_selected = stroke_teams_not_highlighted[p]

            # Check if the newly-selected team is already in the list.
            if team_selected in stroke_teams_selected:
                # Remove this team from the list.
                stroke_teams_selected.remove(team_selected)
            else:
                # Add the newly-selected team to the list.
                stroke_teams_selected.append(team_selected)
            # Add this new list to the session state so that
            # streamlit can access it immediately on the next re-run.
            st.session_state['highlighted_teams_with_click_ds'] = \
                (stroke_teams_selected)

            # Keep a copy of the bar that we've just changed,
            # and put it in the session state so that we can still
            # access it once the script is re-run:
            st.session_state['last_changed_marker_ds'] = selected_bar.copy()

            # Re-run the script to get immediate feedback in the
            # multiselect input widget and the graph colours:
            st.experimental_rerun()

        except IndexError:
            # Nothing has been clicked yet, so don't change anything.
            pass


def plot_violins(
        summary_stats_df,
        feature,
        feature_display_name,
        year_options,
        stroke_teams_selected,
        all_years_str,
        all_teams_str,
        team_colours_dict
        ):
    """
    Plot violins of this feature in each year.

    Plot one violin per year in the descriptive stats dataframe.
    The data shown is chosen with the "feature" picked previously.
    Also mark on the positions of some highlighted teams in all years.

    Inputs:
    -------
    summary_stats_df      - pd.DataFrame. Descriptive stats dataframe.
    feature               - str. Name of the row of data to plot.
    feature_display_name  - str. How to print the feature name.
    year_options          - list. One string per year in the dataframe.
    stroke_teams_selected - list. Stroke teams to highlight.
    all_years_str         - str. Label of all years in the dataframe,
                            e.g. "2016 to 2021".
    all_teams_str         - str. Label of all teams in the dataframe,
                            e.g. "all E+W".
    team_colours_dict     - dict. Keys are stroke teams, values are
                            colours to plot them in.
    """
    fig = go.Figure()

    fig.update_layout(
        width=1300,
        height=500,
        # margin_l=0, margin_r=0, margin_t=0, margin_b=0
        )

    # Rename the dataframe to keep code short:
    s = summary_stats_df.T
    # Remove "all teams" and "all of this region" data:
    s = s[~s.stroke_team.str.startswith(('All '))]

    for y, year in enumerate(year_options):
        # Plot violins in grey except for the "all years" violin,
        # which looks different to separate it off from the rest.
        if year == all_years_str:
            colour = 'Thistle'
        else:
            colour = 'Grey'

        # Include "to numeric" in case some of the numbers
        # are secretly strings (despite my best efforts).
        violin_vals = pd.to_numeric(s[feature][s['year'] == year])
        # x_vals = [y]

        # Draw a violin for this data:
        fig.add_trace(go.Violin(
            x=[y]*len(violin_vals),
            y=violin_vals,
            name=year,
            line=dict(color=colour),
            points=False,
            hoveron='points',
            showlegend=False
            ))

        # Add three scatter markers for min/max/median
        # with vertical line connecting them:
        fig.add_trace(go.Scatter(
            x=[y]*3,
            y=[violin_vals.min(), violin_vals.max(), violin_vals.median()],
            line_color='black',
            marker=dict(size=20, symbol='line-ew-open'),
            # name='Final Probability',
            showlegend=False,
            hoverinfo='skip',
            ))

    # Highlight selected teams with scatter markers.
    # Remove any of the "all teams" or "all region" data:
    stroke_teams_selected = [t for t in stroke_teams_selected
                             if t[:4] != 'All ']

    # Create some extra offsets from the centre of the violin
    # to prevent the scatter markers all overlapping:
    y_gap = 0.025
    y_max = 0.15
    # Where to scatter the team markers:
    y_offsets_scatter = []
    while len(y_offsets_scatter) < len(set(stroke_teams_selected)):
        y_extra = np.arange(y_gap, y_max, y_gap)
        y_extra = np.stack((
            y_extra, -y_extra
        )).T.flatten()
        y_offsets_scatter = np.append(y_offsets_scatter, y_extra)
        y_gap = 0.5 * y_gap

    for i, stroke_team in enumerate(set(stroke_teams_selected)):
        if stroke_team != all_teams_str:
            scatter_vals = s[(
                (s['stroke_team'] == stroke_team)
                )]
            # Just in case the years are out of order:
            x_vals = []
            for year in year_options:
                inds = np.where(scatter_vals['year'] == year)[0]
                if len(inds) > 0:
                    x_vals.append(inds[0])
                else:
                    x_vals.append(np.NaN)
            x_vals = np.array(x_vals) + y_offsets_scatter[i]
            fig.add_trace(go.Scatter(
                x=x_vals,
                y=scatter_vals[feature],
                mode='markers',
                name=stroke_team,
                marker_color=team_colours_dict[stroke_team],
                marker_line_color='black',
                marker_line_width=1.0,
                hovertemplate='%{y}'
            ))

    fig.update_layout(yaxis_title=feature_display_name)
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=np.arange(len(year_options)),
            ticktext=[str(y) for y in year_options]
        ))
    # Move legend to bottom
    fig.update_layout(legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.2,
        xanchor='right',
        x=0.9,
        # itemwidth=50
    ))

    plotly_config = {
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    }
    st.plotly_chart(fig, config=plotly_config)


def scatter_fields(
        x_feature_name,
        y_feature_name,
        year_restriction,
        df,
        stroke_teams_selected,
        team_colours_dict,
        x_feature_display_name,
        y_feature_display_name,
        ):
    """

    feature_display_name  - str. How to print the feature name.
    """
    df = df.T

    # Mask by selected year:
    df = df[df['year'] == year_restriction]

    # Remove "All teams" fields:
    # Pull out any row of the dataframe that contains any of the
    # selected stroke team names in any of its columns.
    stroke_teams_named_all = [t for t in set(df['stroke_team'])
                              if t[:4] == 'All ']
    df = df[~df.isin(stroke_teams_named_all).any(axis=1)]

    # Create the line of best fit:
    lobf = linregress(
        list(df[x_feature_name].astype(float).values),
        list(df[y_feature_name].astype(float).values)
        )

    fig = go.Figure()

    # Quick attempt to get near-square axis:
    fig.update_layout(
        width=800,
        height=500,
        # margin_l=0, margin_r=0, margin_t=0, margin_b=0
        )

    # Plot the line of best fit:
    lobf_name = (
        f'{lobf.intercept:.3f} + ' +
        f'({x_feature_display_name}) × ({lobf.slope:.3f})'
        )
    fig.add_trace(go.Scatter(
        x=df[x_feature_name],
        y=lobf.intercept + lobf.slope * df[x_feature_name].astype(float),
        name=lobf_name,
        hoverinfo='skip',
        marker_color='silver'
    ))

    # Pull out any row of the dataframe that contains any of the
    # selected stroke team names in any of its columns.
    mask_most_teams = ~df.isin(stroke_teams_selected).any(axis=1)
    # Plot all teams that are not highlighted:
    fig.add_trace(go.Scatter(
        x=df[x_feature_name][mask_most_teams],
        y=df[y_feature_name][mask_most_teams],
        mode='markers',
        text=df['stroke_team'][mask_most_teams],
        name='Stroke teams',
        marker_color='grey',
        marker_line_color='black',
        marker_line_width=1.0,
        hovertemplate='(%{x}, %{y})<extra>%{text}</extra>'
    ))

    # Plot highlighted teams:
    # Remove any of the "all teams" or "all region" data:
    stroke_teams_selected = [t for t in stroke_teams_selected
                             if t[:4] != 'All ']
    for stroke_team in stroke_teams_selected:
        mask_team = df['stroke_team'] == stroke_team
        fig.add_trace(go.Scatter(
            x=df[x_feature_name][mask_team],
            y=df[y_feature_name][mask_team],
            mode='markers',
            name=df['stroke_team'][mask_team].squeeze(),
            text=[df['stroke_team'][mask_team].squeeze()],
            marker_color=team_colours_dict[stroke_team],
            marker_line_color='black',
            marker_line_width=1.0,
            hovertemplate='(%{x}, %{y})<extra>%{text}</extra>'
        ))

    # Figure format:
    fig.update_layout(
        xaxis_title=x_feature_display_name,
        yaxis_title=y_feature_display_name
    )
    plotly_config = {
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    }
    st.plotly_chart(fig, config=plotly_config)
