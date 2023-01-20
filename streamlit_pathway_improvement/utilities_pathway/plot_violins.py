import streamlit as st
import plotly.graph_objects as go
import numpy as np

from utilities_pathway.fixed_params import scenarios, scenarios_dict2
from utilities_pathway.plot_utils import scatter_highlighted_teams


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


def plot_violins(df, scenarios, highlighted_teams_input=[], highlighted_colours={}, n_teams='all'):
    fig = go.Figure()

    # If there's only one scenario, remove repeats from the list:
    if len(list(set(scenarios))) == 1:
        scenarios = [scenarios[0]]

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

    scatter_highlighted_teams(fig, df, scenarios, highlighted_teams_input, highlighted_colours, scenario_str, middle=0, horizontal=False)

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



def plot_violins_half(df, scenarios, highlighted_teams_input=[], highlighted_colours={}, n_teams='all'):
    fig = go.Figure()

    # If there's only one scenario, remove repeats from the list:
    if len(list(set(scenarios))) == 1:
        scenarios = [scenarios[0]]

    # med_vals = df['Percent_Thrombolysis_(mean%)'].values
    scenario_str_list = []

    for s, scenario in enumerate(scenarios):
        y = 0

        scenario_str = scenarios_dict2[scenario]
        scenario_str_list.append(scenario_str)

        df_scenario = df[df['scenario'] == scenario]
        med_vals = df_scenario['Percent_Thrombolysis_(mean)'].values

        fig.add_trace(go.Violin(
            x=med_vals,
            y0=y, # [y]*len(med_vals),
            name='violin',
            points=False,
            marker=dict(color='grey'),
            showlegend=False,
            hoverinfo='skip',
            side='positive',
            scalemode='count'
            ))

        # Add scatter markers and line for the min/max/median:
        x_vals = [
            np.max(med_vals),
            np.median(med_vals),
            np.min(med_vals)
            ]
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=[y]*len(x_vals),
            name='violin',
            line_color='black',
            marker=dict(size=20, symbol='line-ns-open'),
            mode='markers+lines',
            showlegend=False,
            hoverinfo='skip',
        ))

    scatter_highlighted_teams(fig, df, scenarios, highlighted_teams_input, highlighted_colours, scenario_str, middle=0, horizontal=True)

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


    fig.update_yaxes(range=[0, 1])
    # fig.update_yaxes(
    #     tickmode='array',
    #     tickvals=np.arange(len(scenarios)),
    #     ticktext=scenario_str_list
    # )
    fig.update_xaxes(range=[-2, max(df['Percent_Thrombolysis_(mean)'])+5])

    fig.update_layout(
        title='Violins for all teams',
        yaxis_title='Scenario',
        xaxis_title='Percent Thrombolysis (mean)',
        legend_title='Highlighted team'
    )

    st.plotly_chart(fig, use_container_width=True)
