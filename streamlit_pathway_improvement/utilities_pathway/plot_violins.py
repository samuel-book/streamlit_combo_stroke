import streamlit as st
import plotly.graph_objects as go
import numpy as np

from utilities_pathway.fixed_params import scenarios, scenarios_dict2

def box_and_whisker(df, scenarios):
    # Box and whisker plot:
    fig = go.Figure()

    med_vals = df['Percent_Thrombolysis_(median%)'].values
    for x, scenario in enumerate(scenarios):

        df_scenario = df[df['scenario'] == scenario]
        med_vals = df_scenario['Percent_Thrombolysis_(median%)'].values

        fig.add_trace(go.Box(
            y=med_vals,
            x=[scenario]*len(med_vals),
            name=scenario,
            boxpoints=False,
            marker=dict(color='grey'),
            showlegend=False
            ))

    st.plotly_chart(fig, use_container_width=True)



def find_offsets_for_scatter(n_points, y_gap=0.05, y_max=0.2):
    """For scattering points on violin"""
    # Where to scatter the team markers:
    y_offsets_scatter = []  # [0.0]
    while len(y_offsets_scatter) < n_points:
        y_extra = np.arange(y_gap, y_max, y_gap)
        y_extra = np.stack((
            y_extra, -y_extra
        )).T.flatten()
        y_offsets_scatter = np.append(y_offsets_scatter, y_extra)
        y_gap = 0.5 * y_gap
    return y_offsets_scatter


def plot_violins(df, scenarios, highlighted_teams_input=[], highlighted_colours={}, n_teams='all'):
    fig = go.Figure()

    # If there's only one scenario, remove repeats from the list:
    if len(list(set(scenarios))) == 1:
        scenarios = [scenarios[0]]

    x_offsets_scatter = find_offsets_for_scatter(len(highlighted_teams_input))

    # med_vals = df['Percent_Thrombolysis_(mean%)'].values
    scenario_str_list = []
    
    for x, scenario in enumerate(scenarios):

        scenario_str = scenarios_dict2[scenario]
        scenario_str_list.append(scenario_str)

        df_scenario = df[df['scenario'] == scenario]
        med_vals = df_scenario['Percent_Thrombolysis_(mean)'].values

        fig.add_trace(go.Violin(
            y=med_vals,
            x=[x]*len(med_vals),
            name='violin',
            points=False,
            marker=dict(color='grey'),
            showlegend=False,
            hoverinfo='skip'
            ))

        # Add scatter markers and line for the min/max/median:
        y_vals = [
            np.max(med_vals),
            np.median(med_vals),
            np.min(med_vals)
            ]
        fig.add_trace(go.Scatter(
            y=y_vals,
            x=[x]*len(y_vals),
            name='violin',
            line_color='black',
            marker=dict(size=20, symbol='line-ew-open'),
            mode='markers+lines',
            showlegend=False,
            hoverinfo='skip',
        ))



    if len(highlighted_teams_input) > 0:
        # Add secret extra scatter points for a second legend:
        symbols = ['circle', 'triangle-up', 'triangle-down']
        s_label = '+<br>Benchmark'.join(scenario_str.split('+ Benchmark'))
        names = [
            'Base',
            f'Increase with {s_label}',
            f'Decrease with {s_label}'
            ]
        for s in range(3):
            fig.add_trace(go.Scatter(
                x=[-100],
                y=[-100],
                mode='markers',
                marker=dict(color='white', symbol=symbols[s],
                    line=dict(color='black', width=1.0)),
                name=names[s],
                legendgroup='1',
                hoverinfo='skip'
            ))

        fig.update_layout(legend_tracegroupgap=50)

    for t, team in enumerate(highlighted_teams_input):
        y_teams = []
        prob_labels=[]
        rank_scenarios=[]
        symbols = ['circle']
        sizes = [6]  # Marker sizes

        for x, scenario in enumerate(scenarios):

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
                [df_scenario['stroke_team'] == team].values[0]
            # Find sorted rank for this team in this scenario:
            rank_scenario = df_scenario['Sorted_rank!'+scenario]\
                [df_scenario['stroke_team'] == team].values[0]
            rank_scenarios.append(rank_scenario)

            y_team = df_scenario['Percent_Thrombolysis_(mean)']\
                [df_scenario['stroke_team'] == team].values
            y_teams.append(y_team[0])

            if x > 0:
                if y_team > y_teams[0]:
                    symbols.append('triangle-up')
                else:
                    symbols.append('triangle-down')
                sizes.append(10)


        # Scatter on first violin:
        
        if len(prob_labels) > 1:
            custom_data = np.stack((
                [hb_team]*2,
                [prob_labels[0]]*2,
                [rank_scenarios[0]]*2,
                [y_teams[0]]*2,
                [prob_labels[1]]*2,
                [rank_scenarios[1]]*2,
                [y_teams[1]]*2
            ), axis=-1)
        else:
            custom_data = np.stack((
                [hb_team]*2,
                [prob_labels[0]]*2,
                [rank_scenarios[0]]*2,
                [y_teams[0]]*2
            ), axis=-1)

        # x_teams = np.arange(len(scenarios)) + x_offsets_scatter[t]
        x_teams = np.full(len(scenarios), 0) + x_offsets_scatter[t]
        fig.add_trace(go.Scatter(
            y=y_teams,
            x=x_teams,
            name=hb_team,
            mode='markers+lines',
            marker=dict(color=highlighted_colours[hb_team],
                        symbol=symbols,
                        size=sizes,
                        line=dict(color='black', width=1.0)),
            # showlegend=showlegend_scatter,
            legendgroup='2',
            customdata=custom_data
        ))

        
        x_teams = np.arange(len(scenarios)) + x_offsets_scatter[t]
        for s, scenario in enumerate(scenarios):
            if s > 0:
                custom_data_here = np.stack(
                    np.transpose([
                        custom_data[s, :],
                        custom_data[s, :]
                        ]),
                    axis=-1)
                # Scatter on second violin:
                fig.add_trace(go.Scatter(
                    y=[y_teams[s]],
                    x=[x_teams[s]],
                    name='extra',  # hb_team,
                    mode='markers',
                    marker=dict(color=highlighted_colours[hb_team],
                                symbol=symbols[s],
                                size=sizes[s],
                                line=dict(color='black', width=1.0)),
                    showlegend=False,
                    customdata=custom_data_here
                ))


    # Update the hover text for the scatter points:
    ht =(
        '%{customdata[0]}' +
        '<br>' +
        # 'Effect of %{y}: %{customdata[1]:>+.2f}%' +
        # 'Effect of %{customdata[4]}: %{customdata[1]:>+.2f}%' +
        # '<br>' +
        '%{customdata[4]}: %{y:.2f}%' +
        '<br>' +
        'Rank for %{customdata[4]}: %{customdata[5]} of ' +
        f'{n_teams}' + ' teams' +
        '<extra></extra>'
        )
    # Update the hover template only for the bars that aren't
    # marking the changes, i.e. the bars that have the name
    # in the legend that we defined earlier.
    fig.for_each_trace(
        lambda trace: trace.update(hovertemplate=ht)
        if trace.name != 'violin'
        else (),
    )

    # Update the hover text for the scatter points:
    ht2 =(
        '%{customdata[0]}' +
        '<br>' +
        'Rank for %{customdata[1]}: %{customdata[2]} of ' +
        f'{n_teams}' + ' teams' +
        '<br>' +
        # 'Effect of %{y}: %{customdata[1]:>+.2f}%' +
        # 'Effect of %{customdata[4]}: %{customdata[1]:>+.2f}%' +
        # '<br>' +
        '%{customdata[1]}: %{customdata[3]:.2f}%' +
        '<br>'
    )
    if len(scenarios) > 1:
        ht2 += (
        '%{customdata[4]}: %{customdata[6]:.2f}%'
        )
    ht2 += (
        # '<br>' +
        # 'Rank for %{customdata[2]}: %{customdata[4]} of ' +
        # f'{n_teams}' + ' teams' +
        '<extra></extra>'
        )
    # Update the hover template only for the bars that aren't
    # marking the changes, i.e. the bars that have the name
    # in the legend that we defined earlier.
    fig.for_each_trace(
        lambda trace: trace.update(hovertemplate=ht2)
        if ((trace.name != 'extra') & (trace.name != 'violin'))
        else (),
    )


    fig.update_xaxes(range=[-0.5, len(scenarios)-0.5])
    fig.update_xaxes(
        tickmode='array',
        tickvals=np.arange(len(scenarios)),
        ticktext=scenario_str_list
    )
    fig.update_yaxes(range=[-2, max(df['Percent_Thrombolysis_(mean)'])+5])

    fig.update_layout(
        title='Violins for all teams',
        xaxis_title='Scenario',
        yaxis_title='Percent Thrombolysis (mean)',
        legend_title='Highlighted team'
    )

    st.plotly_chart(fig, use_container_width=True)
