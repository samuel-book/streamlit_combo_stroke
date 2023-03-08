import streamlit as st
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

from utilities_pathway.fixed_params import scenarios_dict2, plotly_colours, \
    bench_str, plain_str
from utilities_pathway.plot_utils import scatter_highlighted_teams

def plot_hist(
        df, scenarios, highlighted_teams_input=[], highlighted_colours={}, n_teams='all', df_column='Percent_Thrombolysis_(mean)', y_title='Thrombolysis use (%)'
        ):

    # if 'Percent_Thrombolysis' in df_column:
    #     col_str = '!perc_thromb'
    # else:
    #     col_str = '!add_good'

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

    hist_colours = ['grey', plotly_colours[0]]

    fig = go.Figure()

    all_symbol_inds_used = []

    # showlegend = False if c > 0 else True
    for s, scenario in enumerate(scenarios):
        # Pull out just the data for this scenario:
        df_scenario = df[df['scenario'] == scenario]
        # Draw the histogram:
        fig.add_trace(go.Histogram(
            x=df_scenario[df_column],
            xbins=dict(
                start=0,
                end=35,
                size=1),
            autobinx=False,
            marker=dict(
                color=hist_colours[s],
                opacity=0.5,
                line=dict(
                    width=1.0,
                    color=hist_colours[s]
                    )
                ),
            name=scenarios_str_list[s],
            showlegend=True, #showlegend,
            legendgroup='2',
        ))

    # Reduce opacity:
    # fig.update_traces(opacity=0.5, row=1, col=col)
    fig.update_yaxes(title='Number of teams')

    scenario_str = scenarios_dict2[scenario]
    symbols_legend, symbol_inds_used = scatter_highlighted_teams(
        fig,
        df,
        scenarios,
        highlighted_teams_input,
        highlighted_colours,
        scenario_str,
        middle=0,
        horizontal=True,
        y_gap=2,
        y_max=30,
        val_str=df_column,
        add_to_legend=True, #add_to_legends[c],
        showlegend_scatter=True, #add_to_legends[c]
        )
    all_symbol_inds_used += symbol_inds_used

    all_symbol_inds_used = sorted(list(set(all_symbol_inds_used)))
    all_symbols_used = np.array(symbols_legend)[all_symbol_inds_used]

    # Add secret extra scatter points for a second legend:
    # symbols_legend = ['circle', marker_increase, marker_decrease]
    # Check which symbols were used in the previous steps
    # for drawing the highlighted teams.
    inds_to_draw = []
    for i, symbol in enumerate(symbols_legend):
        if symbol in all_symbols_used:
            # If it's been plotted, draw it on this legend.
            inds_to_draw.append(i)

    s_label = '+<br>Benchmark'.join(scenario_str.split('+ Benchmark'))
    names = [
        'Base',
        f'Increase with<br>{s_label}',
        f'Decrease with<br>{s_label}'
        ]
    sizes = [4, 8, 8]
    for s in inds_to_draw:
        fig.add_trace(go.Scatter(
            x=[-100],
            y=[-100],
            mode='markers',
            marker=dict(color='white', symbol=symbols_legend[s], size=sizes[s],
                line=dict(color='black', width=1.0)),
            name=names[s],
            legendgroup='1',
            hoverinfo='skip',
            visible='legendonly'
        ), row=None, col=None)

    fig.update_layout(legend_tracegroupgap=50)


    # Make both histograms share an x-axis
    # (otherwise default is like two sets of bar charts)
    fig.update_layout(barmode='overlay')

    # Legend:
    # fig.update_layout(legend_title='Scenario')
    # Move legend to within the axis area to disguise the fact
    # it changes width depending on which labels it contains.
    fig.update_layout(legend=dict(
        orientation='h', #'h',
        yanchor='top',
        y=-0.2,
        # xanchor='right',
        # x=1.5
    ))

    # Manually set the legend entry width to ensure that the
    # legend is split into two columns no matter what entries
    # it contains.
    fig.update_layout(legend_entrywidth=0.48)
    fig.update_layout(legend_entrywidthmode='fraction',)

    # fig.update_yaxes(range=[0, 30]) # , row=1, col=1)

    fig.update_xaxes(title=y_title)
    fig.update_yaxes(range=[0, 33])
    fig.update_xaxes(range=[0, 34])

    # Make hover text show all traces in one label:
    fig.update_layout(hovermode='closest') # 'x unified')
    # Don't shorten the names of the traces:
    fig.update_layout(hoverlabel=dict(namelength=-1))
    # Set hover template for scatter points:
    if len(scenarios) > 1:
        ht_scatter = (
            'Team %{customdata[0]}' +
            '<br>' +
            'Base value: %{customdata[3]:.2f}%{customdata[8]}' +
            '<br>' +
            'Effect of %{customdata[4]}: %{customdata[7]:.2f}%{customdata[8]}' +
            '<br>' +
            '%{customdata[4]} value: %{customdata[6]}%{customdata[8]}' +
            '<extra></extra>'
        )
    else:
        # If we're only showing the base scenario,
        # don't include any information about the change due to
        # the (non-existent) chosen scenario.
        ht_scatter = (
            'Team %{customdata[0]}' +
            '<br>' +
            'Base value: %{customdata[3]:.2f}%{customdata[4]}' +
            '<extra></extra>'
        )
    # Update the hover template only for the bars that aren't
    # marking the changes, i.e. the bars that have the name
    # in the legend that we defined earlier.
    fig.for_each_trace(
        lambda trace: trace.update(hovertemplate=ht_scatter)
        # if trace.marker.color != change_colour
        if trace.name not in scenarios_str_list
        else (),
    )


    # custom_data = np.stack((
    #     [hb_team]*2,
    #     [prob_labels[0]]*2,
    #     [rank_scenarios[0]]*2,
    #     [vals_teams[0]]*2,
    #     [prob_labels[1]]*2,
    #     [rank_scenarios[1]]*2,
    #     [vals_teams[1]]*2

    hb_teams_input = st.session_state['hb_teams_input']

    # Mess with the height of the plot - 
    # depends on how much is in the legend.
    height = 300  # 500 for similar height to arrow plot
    if len(scenarios) > 1:
        # More than just base.
        n_extra = len(scenarios[1].split('_'))
        if n_extra == 1:
            # base + 1 other
            height += 20
        elif n_extra == 2:
            height += 35
        elif n_extra == 3:
            height += 50
    height += 10 * len(hb_teams_input)
    # Reduce size of figure by adjusting margins:
    fig.update_layout(
        margin=dict(
            # l=0,
            # r=0,
            b=0,
            t=0, #40,
            # pad=0
        ),
        height=height
        )


    # Disable zoom and pan:
    fig.update_layout(
        # Left subplot:
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True),
        # # Right subplot:
        # xaxis2=dict(fixedrange=True),
        # yaxis2=dict(fixedrange=True)
        )

    # Turn off legend click events
    # (default is click on legend item, remove that item from the plot)
    fig.update_layout(legend_itemclick=False)
    # Only change the specific item being clicked on, not the whole
    # legend group:
    # # fig.update_layout(legend=dict(groupclick="toggleitem"))

    # Options for the mode bar.
    # (which doesn't appear on touch devices.)
    plotly_config = {
        # Mode bar always visible:
        # 'displayModeBar': True,
        # Plotly logo in the mode bar:
        'displaylogo': False,
        # Remove the following from the mode bar:
        'modeBarButtonsToRemove': [
            'zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale',
            'lasso2d'
            ],
        # Options when the image is saved:
        'toImageButtonOptions': {'height': None, 'width': None},
        }

    # Write to streamlit:
    st.plotly_chart(fig, use_container_width=True, config=plotly_config)
