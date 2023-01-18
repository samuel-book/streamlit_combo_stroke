import numpy as np
import streamlit as st
import plotly.graph_objects as go


def plot_bars_sorted_rank(df, scenario, scenario_for_rank):
    # Percentage thrombolysis use:
    custom_data = np.stack((
        # Name of the stroke team:
        df['stroke_team'][df['scenario'] == 'base'],
        # Effect of scenario:
        # (round this now so we can use the +/- sign format later)
        np.round(
            df['Percent_Thrombolysis_(mean)_diff']\
                [df['scenario'] == scenario], 1),
        # Final prob:
        # (round this now so we can use the +/- sign format later)
        df['Percent_Thrombolysis_(mean)'][df['scenario'] == scenario]
        ), axis=-1)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Sorted rank'][df['scenario'] == 'base'],
        y=df['Percent_Thrombolysis_(mean)'][df['scenario'] == 'base'],
        name='base',
        marker=dict(color='DarkGrey'),  #'rgba(0,0,0,0.5)'),
        customdata=custom_data
    ))

    # Update hover label info *before* adding traces that have
    # hoverinfo='skip', otherwise this step will overwrite them.
    # Change the hover format
    fig.update_layout(hovermode='x')

    if scenario == 'base':
        # Update hover label message:
        fig.update_traces(hovertemplate=(
            '%{customdata[0]}' +
            '<br>' +
            'Base probability: %{y:.1f}%'
            '<extra></extra>'
        ))
    else:
        # Update hover label message:
        fig.update_traces(hovertemplate=(
            '%{customdata[0]}' +
            '<br>' +
            'Base probability: %{y:.1f}%' +
            '<br>' +
            f'Effect of {scenario}: ' + '%{customdata[1]:+}%' +
            '<br>' +
            f'Final probability: ' + '%{customdata[2]:.1f}%'
            '<extra></extra>'
        ))
        # y_diffs = (
        #     df['Percent_Thrombolysis_(mean)'][df['scenario'] == scenario].values -
        #     df['Percent_Thrombolysis_(mean)'][df['scenario'] == 'base'].values
        # )
        # The differences are already in the dataframe:
        y_diffs = (
            df['Percent_Thrombolysis_(mean)_diff'][df['scenario'] == scenario]
        )
        
        
        leg_str = scenario.replace('_', '_<br>')
        fig.add_trace(go.Bar(
            x=df['Sorted rank'][df['scenario'] == scenario],
            y=y_diffs,
            name=f'difference due to<br>{leg_str}',
            marker=dict(color='rgba(255,0,0,0.3)'),
            # customdata=custom_data
            hoverinfo='skip'
        ))

    # Change the bar mode
    fig.update_layout(barmode='stack')

    fig.update_layout(
        title=f'{scenario}',
        xaxis_title=f'Rank sorted by {scenario_for_rank}',
        yaxis_title='Percent Thrombolysis (mean)',
        legend_title='Highlighted team'
    )


    fig.update_yaxes(range=[0, max(df['Percent_Thrombolysis_(mean)'])*1.05])
    fig.update_xaxes(range=[min(df['Sorted rank'])-1, max(df['Sorted rank'])+1])

    st.plotly_chart(fig, use_container_width=True)


def plot_bars_for_single_team(df, team):
    # # For y-limits:
    # # Find max y values across all teams.
    # max_percent_thrombolysis_mean = max(df['Percent_Thrombolysis_(mean)'])
    # max_additional_good_mean = max(df['Additional_good_outcomes_per_1000_patients_(mean)'])


    # max_percent_thrombolysis_mean_diff = max(np.abs(df['Percent_Thrombolysis_(mean)_diff'].values))
    # max_additional_good_mean_diff = max(np.abs(df['Additional_good_outcomes_per_1000_patients_(mean)_diff'].values))

    # Pick out just the data for the chosen team:
    df_here = df[df['stroke_team'] == team]
    cols_bar = st.columns(2)
    with cols_bar[0]:
        # Percentage thrombolysis use:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_here['scenario'],
            # y=df_here['Percent_Thrombolysis_(mean)'],
            y=df_here['Percent_Thrombolysis_(mean)_diff'],
        ))

        fig.update_xaxes(title='Scenario')
        fig.update_yaxes(title='DIFF Percent Thrombolysis (mean)')

        # fig.update_yaxes(range=[
        #     -max_percent_thrombolysis_mean_diff*1.05,
        #     +max_percent_thrombolysis_mean_diff*1.05
        #     ])

        st.plotly_chart(fig, use_container_width=True)

    with cols_bar[1]:
        # Additional good outcomes
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_here['scenario'],
            # y=df_here['Additional_good_outcomes_per_1000_patients_(mean)'],
            y=df_here['Additional_good_outcomes_per_1000_patients_(mean)_diff'],
            marker=dict(color='red')
        ))

        fig.update_xaxes(title='Scenario')
        fig.update_yaxes(title='DIFF Additional good outcomes<br>per 1000 patients<br>(mean)')

        # fig.update_yaxes(range=[
        #     -max_additional_good_mean_diff*1.05,
        #     +max_additional_good_mean_diff*1.05
        #     ])

        st.plotly_chart(fig, use_container_width=True)
