"""
Helper functions for plotting.
"""
import plotly.express as px
import plotly.graph_objects as go
import matplotlib
import numpy as np
import streamlit as st

from utilities_pathway.fixed_params import plain_str, bench_str, \
    display_name_of_default_highlighted_team, default_highlighted_team

# Functions:

def remove_old_colours_for_highlights(highlighted_teams_input):
    # Remove highlighted colours that are no longer needed:
    try:
        highlighted_teams_colours_before = \
            st.session_state['highlighted_teams_colours']
        highlighted_teams_colours = {}
        for team in highlighted_teams_input:
            try:
                highlighted_teams_colours[team] = \
                    highlighted_teams_colours_before[team]
            except KeyError:
                pass
        st.session_state['highlighted_teams_colours'] = \
            highlighted_teams_colours
    except KeyError:
        st.session_state['highlighted_teams_colours'] = {}


def choose_colours_for_highlights(highlighted_teams_list):

    highlighted_teams_colours = \
        st.session_state['highlighted_teams_colours']
    # Specify the indices to get a mix of colours:
    plotly_colours = px.colors.qualitative.Plotly
    # Pick out some colours we prefer (not too close to existing colours):
    inds_preferred = [1, 5, 4, 7, 8, 9, 6, 2, 3, 0]
    preferred_colours = np.array(plotly_colours)[inds_preferred]

    for i, leg_entry in enumerate(highlighted_teams_list):
        try:
            # Check if there's already a designated colour:
            colour = highlighted_teams_colours[leg_entry]
        except KeyError:
            if leg_entry == plain_str:
                colour = 'grey'
            elif leg_entry == bench_str:
                colour = 'Navy'
            else:
                # Pick a colour that hasn't already been used.
                unused_colours = list(np.setdiff1d(
                    preferred_colours,
                    list(highlighted_teams_colours.values())
                    ))
                if len(unused_colours) < 1:
                    # Select a colour from this list:
                    mpl_colours = list(matplotlib.colors.cnames.values())
                    colour = list(highlighted_teams_colours.values())[0]
                    while colour in list(highlighted_teams_colours.values()):
                        colour = mpl_colours[
                            np.random.randint(0, len(mpl_colours))]
                else:
                    success = 0
                    j = 0
                    while success < 1:
                        colour = preferred_colours[j]
                        if colour in highlighted_teams_colours.values():
                            j += 1
                        else:
                            success = 1

            # Add this to the dictionary:
            highlighted_teams_colours[leg_entry] = colour

    # Save the new colour dictionary to the session state:
    st.session_state['highlighted_teams_colours'] = highlighted_teams_colours


def find_offsets_for_scatter(n_points, y_gap=0.05, y_max=0.2, positive=False):
    """For scattering points on violin"""
    # Where to scatter the team markers:
    y_offsets_scatter = []  # [0.0]
    while len(y_offsets_scatter) < n_points:
        y_extra = np.arange(y_gap, y_max, y_gap)
        if positive is False:
            # Mix in the same values, but negative.
            y_extra = np.stack((
                y_extra, -y_extra
            )).T.flatten()
        y_offsets_scatter = np.append(y_offsets_scatter, y_extra)
        y_gap = 0.5 * y_gap
    return y_offsets_scatter


def scatter_highlighted_teams(
        fig,
        df,
        scenarios,
        highlighted_teams_input,
        highlighted_colours,
        scenario_str,
        middle=0,
        horizontal=True,
        positive=True,
        y_gap=0.05,
        y_max=0.2,
        val_str='Percent_Thrombolysis_(mean)',
        row=None,
        col=None,
        add_to_legend=True,
        showlegend_scatter=True
        ):

    if horizontal is True:
        marker_increase = 'arrow-right'
        marker_decrease = 'arrow-left'
    else:
        marker_increase = 'arrow-up'
        marker_decrease = 'arrow-down'

    if 'Percent_Thrombolysis' in val_str:
        col_str = '!perc_thromb'
    else:
        col_str = '!add_good'

    # Where to put highlighted teams:
    y_offsets_scatter = find_offsets_for_scatter(len(highlighted_teams_input), y_gap, y_max, positive)

    # Store the symbols used in here so later we can add an extra
    # legend containing these markers.
    all_symbols = ['circle', marker_increase, marker_decrease]
    all_inds_used = []

    for t, team in enumerate(highlighted_teams_input):
        vals_teams = []
        prob_labels=[]
        rank_scenarios=[]
        symbols = ['circle']
        sizes = [4]  # Marker sizes

        all_inds_used.append(0)

        if team == display_name_of_default_highlighted_team:
            df_team = default_highlighted_team
        else:
            df_team = team

        for z, scenario in enumerate(scenarios):

            df_scenario = df[df['scenario'] == scenario]
            # Add scatter markers for highlighted teams
            # showlegend_scatter = False if x > 0 else True
            if scenario == 'base':
                prob_label = 'Base'
            else:
                prob_label = scenario_str  # + ' '
            prob_labels.append(prob_label)

            # Find HB name for this team:
            hb_team = df_scenario['HB_team']\
                [df_scenario['stroke_team'] == df_team].values[0]
            # Find colour before overwriting hb_team:
            colour = highlighted_colours[hb_team]
            if team == display_name_of_default_highlighted_team:
                hb_team = display_name_of_default_highlighted_team
            # Find sorted rank for this team in this scenario:
            rank_scenario = df_scenario['Sorted_rank!'+scenario+col_str]\
                [df_scenario['stroke_team'] == df_team].values[0]
            rank_scenarios.append(rank_scenario)

            val_team = df_scenario[val_str]\
                [df_scenario['stroke_team'] == df_team].values
            vals_teams.append(val_team[0])

            if z > 0:
                if val_team > vals_teams[0]:
                    symbols.append(marker_increase)
                    all_inds_used.append(1)
                else:
                    symbols.append(marker_decrease)
                    all_inds_used.append(2)
                sizes.append(8)

        all_inds_used = sorted(list(set(all_inds_used)))


        # Scatter on first violin:

        if len(prob_labels) > 1:
            custom_data = np.stack((
                [hb_team]*2,
                [prob_labels[0]]*2,
                [rank_scenarios[0]]*2,
                [vals_teams[0]]*2,
                [prob_labels[1]]*2,
                [rank_scenarios[1]]*2,
                [vals_teams[1]]*2,
                [vals_teams[1] - vals_teams[0]]*2,
                ['%' if 'Percent' in val_str else '']*2
            ), axis=-1)
        else:
            custom_data = np.stack((
                [hb_team]*2,
                [prob_labels[0]]*2,
                [rank_scenarios[0]]*2,
                [vals_teams[0]]*2,
                ['%' if 'Percent' in val_str else '']*2
            ), axis=-1)

        # x_teams = np.arange(len(scenarios)) + x_offsets_scatter[t]
        offs_teams = np.full(len(vals_teams), middle) + y_offsets_scatter[t]

        if horizontal is True:
            x_teams = vals_teams
            y_teams = offs_teams
        else:
            x_teams = offs_teams
            y_teams = vals_teams

        fig.add_trace(go.Scatter(
            x=x_teams,
            y=y_teams,
            name=hb_team,
            mode='markers+lines',
            marker=dict(color=colour,
                        symbol=symbols,
                        size=sizes,
                        line=dict(color='black', width=1.0)),
            showlegend=showlegend_scatter,
            legendgroup='2',
            customdata=custom_data
        ), row=row, col=col)

        # Second violin:
        # y_teams = np.arange(len(scenarios)) + y_offsets_scatter[t]
        # for s, scenario in enumerate(scenarios):
        #     if s > 0:
        #         custom_data_here = np.stack(
        #             np.transpose([
        #                 custom_data[s, :],
        #                 custom_data[s, :]
        #                 ]),
        #             axis=-1)
        #         # Scatter on second violin:
        #         fig.add_trace(go.Scatter(
        #             y=[y_teams[s]],
        #             x=[x_teams[s]],
        #             name='extra',  # hb_team,
        #             mode='markers',
        #             marker=dict(color=highlighted_colours[hb_team],
        #                         symbol=symbols[s],
        #                         size=sizes[s],
        #                         line=dict(color='black', width=1.0)),
        #             showlegend=False,
        #             customdata=custom_data_here
        #         ))



    return all_symbols, all_inds_used
