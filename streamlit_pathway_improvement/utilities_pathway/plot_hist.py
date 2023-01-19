import streamlit as st
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

from utilities_pathway.fixed_params import scenarios_dict2, plotly_colours

def plot_hist(
        df, scenarios, highlighted_teams_input=[], highlighted_colours={}, n_teams='all'
        ):

    # If only 'base' is in the list, remove repeats:
    if len(list(set(scenarios))) == 1:
        scenarios = [scenarios[0]]

    # Sort out labels for legend:
    scenarios_str_list = []
    for s in scenarios:
        s_label = scenarios_dict2[s]
        if '+' in s_label:
            s_label = '(' + s_label + ')'
            # Onset + Speed + Benchmark is too long, so move the
            # "+ Benchmark" onto its own line.
            s_label = ' +<br>'.join(s_label.split('+'))
        scenarios_str_list.append(s_label)


    subplot_titles = [
        'Thrombolysis use (%)',
        'Additional good outcomes<br>per 1000 admissions'
    ]
    fig = make_subplots(rows=1, cols=2, subplot_titles=subplot_titles)

    cols = [1, 2]
    x_data_strs = [
        'Percent_Thrombolysis_(mean)',
        'Additional_good_outcomes_per_1000_patients_(mean)'
        ]
    for c, col in enumerate(cols):
        showlegend = False if c > 0 else True
        for s, scenario in enumerate(scenarios):
            # Pull out just the data for this scenario:
            df_scenario = df[df['scenario'] == scenario]
            # Draw the histogram:
            fig.add_trace(go.Histogram(
                x=df_scenario[x_data_strs[c]],
                xbins=dict(
                    start=0,
                    end=35,
                    size=1),
                autobinx=False,
                marker=dict(
                    color=plotly_colours[s],
                    opacity=0.5,
                    line=dict(
                        width=1.0,
                        color=plotly_colours[s]
                        )
                    ),
                name=scenarios_str_list[s],
                showlegend=showlegend
            ),
            row=1, col=col)

        # Reduce opacity:
        # fig.update_traces(opacity=0.5, row=1, col=col)
        fig.update_yaxes(title='Number of hospitals', row=1, col=col)


    # Make both histograms share an x-axis
    # (otherwise default is like two sets of bar charts)
    fig.update_layout(barmode='overlay')

    # Legend:
    fig.update_layout(legend_title='Scenario')
    # Move legend to within the axis area to disguise the fact
    # it changes width depending on which labels it contains.
    fig.update_layout(legend=dict(
        # orientation='v', #'h',
        yanchor='top',
        y=1,
        xanchor='right',
        x=1.25
    ))


    fig.update_xaxes(title='Thrombolysis use (%)', row=1, col=1)
    fig.update_yaxes(range=[0, 30], row=1, col=1)
    fig.update_xaxes(range=[0, 34], row=1, col=1)

    fig.update_xaxes(
        title='Additional good outcomes<br>per 1000 admissions',
        row=1, col=2
        )
    fig.update_yaxes(range=[0, 33], row=1, col=2)
    fig.update_xaxes(range=[0, 34], row=1, col=2)

    fig.update_layout(hovermode='x unified')

    # Write to streamlit:
    st.plotly_chart(fig, use_container_width=True)