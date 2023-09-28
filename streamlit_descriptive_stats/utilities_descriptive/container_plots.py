"""
Plots for the descriptive stats demo.
"""
import streamlit as st
import plotly.graph_objs as go
import geojson
import numpy as np
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


def plot_geography_pins(df_stroke_team):
    """
    Plot a map of England and Wales with the stroke teams marked.

    This draws a shape for each region from a geojson that was created
    by combining all super-generalised LSOA shapes in each region.
    The markers are drawn using latitude and longitude coordinates that
    were generated from the stroke teams' postcodes.

    Inputs:
    -------
    df_stroke_team - pd.DataFrame. Dataframe of hospital locations.
                     Must contain columns 'lat', 'long', and
                     'Stroke Team' for marker positions and labels.
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
    fig.update_layout(
        width=500,
        height=500,
        margin_l=0, margin_r=0, margin_t=0, margin_b=0
        )

    # Add region polygons:
    fig.add_trace(go.Choropleth(
        geojson=geojson_ew,
        locations=df_regions['RGN11NM'],
        z=df_regions['v'],
        featureidkey='properties.RGN11NM',
        colorscale='Picnic',
        showscale=False,
        hoverinfo='skip'
    ))
    # Add scatter markers for all hospitals:
    fig.add_trace(go.Scattergeo(
        lon=df_stroke_team['long'],
        lat=df_stroke_team['lat'],
        customdata=np.stack([df_stroke_team['Stroke Team']], axis=-1),
        mode='markers',
        # marker_color=df_stroke_team['RGN11NM']
    ))

    # Update geojson projection.
    # Projection options:
    #   august  eckert1  fahey  times  van der grinten
    # ^ these ones look ok by eye. There's a longer list in the docs.
    fig.update_layout(
        geo_scope='europe',
        geo_projection=go.layout.geo.Projection(type='times'),
        geo_lonaxis_range=[extent[0], extent[1]],
        geo_lataxis_range=[extent[2], extent[3]],
        # geo_resolution=50,
        geo_visible=False
    )
    fig.update_geos(fitbounds="locations", visible=False)

    # Update hover info for scatter points:
    fig.update_traces(
        hovertemplate='%{customdata[0]}<extra></extra>',
        selector=dict(type='scattergeo')
    )

    # Remove some buttons from the mode bar (top corner on hover).
    plotly_config = {
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    }
    st.plotly_chart(fig, config=plotly_config)
    st.caption('Locations of the stroke teams, colour-coded by region.')


def plot_violins(
        summary_stats_df,
        feature,
        year_options,
        stroke_teams_selected,
        all_years_str,
        all_teams_str
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
    year_options          - list. One string per year in the dataframe.
    stroke_teams_selected - list. Stroke teams to highlight.
    all_years_str         - str. Label of all years in the dataframe,
                            e.g. "2016 to 2021".
    all_teams_str         - str. Label of all teams in the dataframe,
                            e.g. "all E+W".
    """
    fig = go.Figure()

    fig.update_layout(
        width=1300,
        height=500,
        # margin_l=0, margin_r=0, margin_t=0, margin_b=0
        )

    # Rename the dataframe to keep code short:
    s = summary_stats_df.T
    # Remove "all teams" data:
    s = s[s['stroke_team'] != all_teams_str]

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

        # Draw a violin for this data:
        fig.add_trace(go.Violin(
            x=s['year'][s['year'] == year],
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
            x=[year]*3,
            y=[violin_vals.min(), violin_vals.max(), violin_vals.median()],
            line_color='black',
            marker=dict(size=20, symbol='line-ew-open'),
            # name='Final Probability',
            showlegend=False,
            hoverinfo='skip',
            ))

    # Highlight selected teams with scatter markers:
    for stroke_team in stroke_teams_selected:
        if stroke_team != all_teams_str:
            scatter_vals = s[(
                # (s['year'] == year) &
                (s['stroke_team'] == stroke_team)
                )]
            fig.add_trace(go.Scatter(
                x=scatter_vals['year'],
                y=scatter_vals[feature],
                mode='markers',
                name=stroke_team
            ))

    fig.update_layout(yaxis_title=feature)
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
