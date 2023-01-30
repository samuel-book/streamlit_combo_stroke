import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utilities_pathway.fixed_params import scenarios, scenarios_dict2, \
    display_name_of_default_highlighted_team, default_highlighted_team


def plot_two_scatter_sorted_rank(df, scenario, scenario_for_rank, y_strs, n_teams='all'):
    cols = [1, 2]
    showlegends = [True, False]

    subplot_titles = [
        'Thrombolysis use (%)',
        'Additional good outcomes<br>per 1000 admissions'
    ]
    fig = make_subplots(rows=1, cols=2, subplot_titles=subplot_titles)
    
    for i in [0, 1]:
        plot_scatter_sorted_rank(
            df,
            scenario,
            scenario_for_rank,
            n_teams,
            y_str=y_strs[i],
            col=cols[i],
            row=1,
            fig=fig,
            showlegend_col=showlegends[i]
            )

    # To match histograms:
    fig.update_xaxes(range=[0, 34], row=1, col=1)
    fig.update_xaxes(range=[0, 34], row=1, col=2)


    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
        

def plot_scatter_sorted_rank(df_all, scenario, scenario_for_rank, n_teams='all', y_str='Percent_Thrombolysis_(mean)', col=None, row=None, fig=None, showlegend_col=False):
    if fig is None:
        fig = go.Figure()
    
    if y_str == 'Percent_Thrombolysis_(mean)':
        y_label = 'Thrombolysis use (%)'
    else:
        y_label = 'Additional good outcomes<br>per 1000 admissions'

    # Use this string for labels:
    scenario_str = scenarios_dict2[scenario]
    scenario_for_rank_str = scenarios_dict2[scenario_for_rank.split('!')[0]]
    # List of all the separate traces:
    hb_teams_input = st.session_state['hb_teams_input']
    highlighted_colours = st.session_state['highlighted_teams_colours']

    # change_colour = 'rgba(255,255,255,0.8)'

    for n, name in enumerate(hb_teams_input):

        if default_highlighted_team in name:
            display_name = display_name_of_default_highlighted_team
        else:
            display_name = name

        df = df_all[df_all['HB_team'] == name]

        if default_highlighted_team in name:
            name_arr = (
                [display_name_of_default_highlighted_team] *
                len(df['stroke_team'][df['scenario'] == 'base'])
            )
        else:
            name_arr = df['stroke_team'][df['scenario'] == 'base']

        colour = highlighted_colours[name]

        # Percentage thrombolysis use:
        custom_data = np.stack((
            # Name of the stroke team:
            name_arr,
            # Effect of scenario:
            # (round this now so we can use the +/- sign format later)
            np.round(
                df[y_str + '_diff']\
                    [df['scenario'] == scenario], 1),
            # Base prob:
            # (round this now so we can use the +/- sign format later)
            df[y_str][df['scenario'] == 'base'],
            # Final prob:
            # (round this now so we can use the +/- sign format later)
            df[y_str][df['scenario'] == scenario],
            # Base rank:
            df['Sorted_rank!base'][df['scenario'] == 'base'],
            # Final rank:
            df['Sorted_rank!'+scenario][df['scenario'] == 'base']
            ), axis=-1)


        # Setup assuming scenario == 'base':
        x_for_scatter = df['Sorted_rank!'+scenario_for_rank][df['scenario'] == 'base']
        y_for_scatter = df[y_str][df['scenario'] == 'base']
        mode = 'markers'
        symbols = 'circle'
        leg_str_full = 'dummy'  # Is this needed?
        size = 4

        if scenario != 'base':
            y_scenario = (
                df[y_str][df['scenario'] == scenario]
            )
            # The differences are already in the dataframe:
            y_diffs = (
                df[y_str + '_diff'][df['scenario'] == scenario]
            )

            # Base symbols:
            symbols = ['circle'] * len(x_for_scatter)
            # Scenario symbols: 
            symbols_scen = np.full(len(symbols), 'circle', dtype='U20')
            symbols_scen[np.where(y_diffs >= 0)] = 'arrow-right'
            symbols_scen[np.where(y_diffs < 0)] = 'arrow-left'
            symbols = np.array([symbols, symbols_scen])

            x_for_scatter = np.array([x_for_scatter, x_for_scatter])
            y_for_scatter = np.array([y_for_scatter, y_scenario])

            mode = 'markers+lines'


            leg_str = scenario_str.replace('+ ', '+<br>')
            leg_str_full = f'Difference due to<br>"{leg_str}"'


        if scenario == 'base':
            fig.add_trace(go.Scatter(
                y=x_for_scatter,
                x=y_for_scatter,
                name=display_name,
                mode=mode,
                # width=1,
                marker=dict(color=colour, symbol=symbols, size=size),
                    # line=dict(color=colour)),  #'rgba(0,0,0,0.5)'),
                customdata=custom_data,
                showlegend=showlegend_col
            ),
                row=row, col=col
            )
        else:
            for t, team in enumerate(range(x_for_scatter.shape[1])):
                showlegend = True if (t == 0 and showlegend_col is True) else False


                # st.write(custom_data)
                custom_data_here = custom_data[t, :]
                # st.text(custom_data_here)
                custom_data_here = np.transpose(np.stack((custom_data_here, custom_data_here), axis=-1))
                # st.text(custom_data_here)
                # st.text(custom_data_here[:, 0])

                fig.add_trace(go.Scatter(
                    y=x_for_scatter[:, t],
                    x=y_for_scatter[:, t],
                    name=display_name,
                    mode=mode,
                    # width=1,
                    marker=dict(color=colour, symbol=symbols[:, t], size=[4, 8]),
                        # line=dict(color=colour)),  #'rgba(0,0,0,0.5)'),
                    customdata=custom_data_here,
                    showlegend=showlegend
                ),
                    row=row, col=col)



    # Update hover label info *before* adding traces that have
    # hoverinfo='skip', otherwise this step will overwrite them.
    # Change the hover format
    fig.update_layout(hovermode='closest')
    # # Reduce hover distance to prevent multiple labels popping
    # # up for each x:
    # fig.update_layout(hoverdistance=1)
    # ^ this isn't good enough - still get three labels

    # Define the hover template:
    if scenario == 'base':
        # No change bars here.
        ht = (
            '%{customdata[0]}' +
            '<br>' +
            'Base probability: %{customdata[2]:.1f}%' +
            '<br>' +
            'Rank: %{y} of ' + f'{n_teams} teams'
            '<extra></extra>'
        )
    else:
        # Add messages to reflect the change bars.
        ht = (
            '%{customdata[0]}' +
            '<br>' +
            'Base probability: %{customdata[2]:.1f}%' +
            '<br>' +
            f'Effect of {scenario_str}: ' + '%{customdata[1]:+}%' +
            '<br>' +
            f'Final probability: ' + '%{customdata[3]:.1f}%' +
            '<br>' +
            'Base rank: %{customdata[4]} of ' + f'{n_teams} teams'
            '<br>' +
            f'{scenario_str} rank:' + ' %{customdata[5]} of ' + f'{n_teams} teams'
            '<extra></extra>'
        )

    # Update the hover template only for the bars that aren't
    # marking the changes, i.e. the bars that have the name
    # in the legend that we defined earlier.
    fig.for_each_trace(
        lambda trace: trace.update(hovertemplate=ht)
        # if trace.marker.color != change_colour
        if trace.name != leg_str_full
        else (),
    )

    # fig.update_layout(
    #     title=f'{scenario_str}',
    #     yaxis_title=f'Rank sorted by {scenario_for_rank_str}',
    #     xaxis_title=y_label,
    #     legend_title='Highlighted team',
    #     row=row, col=col
    # )
    fig.update_yaxes(title=f'Rank sorted by {scenario_for_rank_str}', row=row, col=col)
    fig.update_xaxes(title=y_label, row=row, col=col)
    # fig.update_layout(legend_title='Highlighted team')

    # Format legend so newest teams appear at bottom:
    fig.update_layout(legend=dict(traceorder='normal'))
    # Set margins to the same as the histogram:
    fig.update_layout(margin=dict(    
            l=0,
            r=0,
            # b=0,
            # t=40,
            pad=0
        ))
    # Set legend location to the same as the histogram:
    fig.update_layout(legend=dict(
        # orientation='h', #'h',
        yanchor='top',
        y=1,
        xanchor='right',
        x=1.5
    ))


    # fig.update_xaxes(range=[0, max(df_all[y_str])*1.05], row=row, col=col)
    fig.update_yaxes(range=[
        min(df_all['Sorted_rank!'+scenario_for_rank])-1,
        max(df_all['Sorted_rank!'+scenario_for_rank])+1
        ][::-1], row=row, col=col)

    # This simulates grid lines but makes the plot slow to display:
    # # Plot vertical lines:
    # for x in np.arange(0, 35):
    #     fig.add_vline(x=x, line=dict(color='grey'), opacity=0.1, layer='below')

    # # 23rd Jan 2023 - minor ticks currently don't show up in Streamlit
    # fig.update_xaxes(minor=dict(
    #     # ticklen=6,
    #     # tickcolor="black",
    #     # tickmode='array',
    #     # tickvals=np.arange(0, 35),
    #     # ticktext=['' for t in np.arange(0, 35)],
    #     ticks='outside',
    #     tick0=0,
    #     dtick=1,
    #     showgrid=True,
    #     gridcolor='magenta',
    #     gridwidth=1
    #     ), col=col, row=row)
    # fig.update_yaxes(minor_ticks="inside")


def plot_bars_for_single_team(df, team):

    t_str = 'Percent_Thrombolysis_(mean)'
    t_label = 'Thrombolysis use (%)'

    o_str = 'Additional_good_outcomes_per_1000_patients_(mean)'
    o_label = 'Additional good outcomes<br>per 1000 admissions'

    # For y-limits:
    # Find max y values across all teams.
    max_percent_thrombolysis_mean = max(df[t_str])
    min_percent_thrombolysis_mean = 0
    max_additional_good_mean = max(df[o_str])
    min_additional_good_mean = 0

    scenarios_str_list = []
    for s in scenarios:
        s_label = scenarios_dict2[s]
        if '+' in s_label:
            s_label = '(' + s_label + ')'
        if len(s_label) > 20:
            # Onset + Speed + Benchmark is too long, so move the
            # "+ Benchmark" onto its own line.
            s_label = ' +<br> Benchmark'.join(s_label.split(' + Benchmark'))
        scenarios_str_list.append(s_label)

    if team == display_name_of_default_highlighted_team:
        df_team = default_highlighted_team
    else:
        df_team = team

    # Pick out just the data for the chosen team:
    df_here = df[df['stroke_team'] == df_team]
    # Pick out base values:
    base_percent_thromb_here = df_here[t_str][df_here['scenario'] == 'base'].values[0]
    base_additional_good_here = df_here[o_str][df_here['scenario'] == 'base'].values[0]


    subplot_titles = [
        t_label,
        o_label
    ]
    fig = make_subplots(rows=1, cols=2, subplot_titles=subplot_titles)

    fig.update_layout(title='<b>Team ' + team)  # <b> for bold

    # --- Percentage thrombolysis use ---
    diff_vals_mean = np.round(df_here[t_str + '_diff'].values, 1)[1:]
    sign_list_mean = np.full(diff_vals_mean.shape, '+')
    sign_list_mean[np.where(diff_vals_mean < 0)[0]] = '-'
    bar_text_mean = []
    for i, diff in enumerate(diff_vals_mean):
        diff_str = ''.join([sign_list_mean[i], str(diff)])
        bar_text_mean.append(diff_str)
    bar_text_mean = [np.round(base_percent_thromb_here, 1).astype(str)] + bar_text_mean

    custom_data_mean = np.stack((
        # Difference between this scenario and base:
        np.round(df_here[t_str + '_diff'], 1),
        # Base value:
        np.full(
            df_here['scenario'].values.shape, 
            df_here[t_str]\
                [df_here['scenario'] == 'base']
            ),
        # Text for top of bars:
        bar_text_mean
    ), axis=-1)

    fig.add_trace(go.Bar(
        x=df_here['scenario'],
        y=df_here[t_str],
        customdata=custom_data_mean,
        showlegend=False
    ),
        row=1, col=1)

    fig.update_yaxes(title=t_label, row=1, col=1)

    fig.update_yaxes(range=[
        min_percent_thrombolysis_mean*1.1,
        max_percent_thrombolysis_mean*1.1
        ],
        row=1, col=1)


    # --- Additional good outcomes ---
    diff_vals_add = np.round(df_here[o_str + '_diff'].values, 1)[1:]
    sign_list_add = np.full(diff_vals_add.shape, '+')
    sign_list_add[np.where(diff_vals_add < 0)[0]] = '-'
    bar_text_add = []
    for i, diff in enumerate(diff_vals_add):
        diff_str = ''.join([sign_list_add[i], str(diff)])
        bar_text_add.append(diff_str)
    bar_text_add = [np.round(base_additional_good_here, 1).astype(str)] + bar_text_add

    custom_data_add = np.stack((
        # Difference between this scenario and base:
        np.round(df_here[o_str + '_diff'], 1),
        # Base value:
        np.full(
            df_here['scenario'].values.shape,
            df_here[o_str]\
                [df_here['scenario'] == 'base']
            ),
        # Text for top of bars:
        bar_text_add
    ), axis=-1)

    fig.add_trace(go.Bar(
        x=df_here['scenario'],
        # y=df_here[o_str],
        y=df_here[o_str],
        # marker=dict(color='red'),
        customdata=custom_data_add,
        showlegend=False
    ), row=1, col=2)

    fig.update_yaxes(title=o_label.split('<br>')[0], row=1, col=2)

    # Update y-axis limits with breathing room for labels above bars.
    fig.update_yaxes(range=[
        min_additional_good_mean*1.1,
        max_additional_good_mean*1.1
        ],
        row=1, col=2)

    # Shared formatting:
    cols = [1, 2]
    base_values = [base_percent_thromb_here, base_additional_good_here]
    for c, col in enumerate(cols):
        # Add some extra '%' for the first subplot but not the second.
        perc_str = '%' if col == 1 else ''
        # Update x-axis title and tick labels:
        fig.update_xaxes(title='Scenario', row=1, col=col)
        fig.update_xaxes(
            tickmode='array',
            tickvals = np.arange(len(scenarios_str_list)),
            ticktext=scenarios_str_list,
            tickangle=90,
            row=1, col=col
        )
        # Draw a horizontal line at the base value:
        fig.add_hline(
            y=base_values[c],
            line=dict(color='silver', width=1.0),
            layer='above',  # Puts it above the bars
            row=1, col=col)
        # Write the size of each bar within the bar:
        fig.update_traces(text='%{customdata[2]}', row=1, col=col)
        # Set text position to "auto" so it sits inside the bar if there's
        # room, and outside the bar if there's not enough room.
        # For everything inside and auto-size the text, use "inside".
        fig.update_traces(textposition='outside', row=1, col=col)
        # Explicitly ask for + and - signs:
        fig.update_traces(texttemplate='%{customdata[2]}' + perc_str, row=1, col=col)
        # Update hover template:
        fig.update_traces(hovertemplate=(
            # 'Value for %{x}: %{y}%' +
            'Value: %{y}' + perc_str +
            '<br>' +
            'Difference from base: %{customdata[0]:+}' + perc_str +
            '<br>' +
            '<extra></extra>'
        ),
            row=1, col=col)

    # Write to streamlit:
    st.plotly_chart(fig, use_container_width=True)
