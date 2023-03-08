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

import plotly.graph_objects as go
# For importing colours:
import plotly.express as px
import matplotlib

# Add an extra bit to the path if we need to.
# Try importing something as though we're running this from the same
# directory as the landing page.
try:
    from utilities_pathway.fixed_params import page_setup
except ModuleNotFoundError:
    # If the import fails, add the landing page directory to path.
    # Assume that the script is being run from the directory above
    # the landing page directory, which is called
    # streamlit_pathway_improvement.
    import sys
    sys.path.append('./streamlit_pathway_improvement/')

# Custom functions:
from utilities_pathway.fixed_params import \
    page_setup, scenarios, scenarios_dict, plotly_colours, \
    default_highlighted_team, display_name_of_default_highlighted_team
import utilities_pathway.inputs
import utilities_pathway.plot_bars
import utilities_pathway.plot_violins
import utilities_pathway.plot_hist
from utilities_pathway.plot_utils import \
    remove_old_colours_for_highlights, choose_colours_for_highlights
from utilities_pathway.tables import show_data_for_team, show_data_for_all


def main():
    # ###########################
    # ##### START OF SCRIPT #####
    # ###########################
    page_setup()

    # Title:
    st.markdown('# :stopwatch: Pathway improvement')
    st.markdown('''
        We can see the effect of making changes to the pathway by running the same patient information multiple times with minor tweaks.
        ''')

    # Method
    col_ratio = [6, 7]
    cols_base = st.columns(col_ratio)
    cols_speed = st.columns(col_ratio)
    cols_onset = st.columns(col_ratio)
    cols_benchmark = st.columns(col_ratio)

    image_files = [
        'SAMueL2_model_base.png',
        'SAMueL2_model_speed.png',
        'SAMueL2_model_onset.png',
        'SAMueL2_model_benchmark.png',
    ]
    for i, image_file in enumerate(image_files):
        cols = [cols_base, cols_speed, cols_onset, cols_benchmark][i]
        with cols[0]:
            if i > 0:
                st.markdown('###  ')  # Match the headers in other column.
            # Draw the image with the basic model summary.
            try:
                st.image('./utilities_pathway/' + image_file)
            except (FileNotFoundError, st.runtime.media_file_storage.MediaFileStorageError):
                # Add an extra bit to the path for the combo app.
                st.image('./streamlit_pathway_improvement/' +
                        'utilities_pathway/' + image_file)


    # Pathway descriptions from the SAMueL book:
    # https://samuel-book.github.io/samuel-1/pathway_sim/scenario_analysis.html
    with cols_base[1]:
        st.markdown('### Base')
        st.markdown('''
            Uses the hospitals' recorded pathway statistics in SSNAP (same as validation notebook)
            ''')
    with cols_speed[1]:
        st.markdown('### Speed')
        st.markdown('''
            Sets 95\% of patients having a scan within 4 hours of arrival, and all patients have 15 minutes arrival to scan and 15 minutes scan to needle.
            ''')
    with cols_onset[1]:
        st.markdown('### Onset')
        st.markdown('''
            Sets the proportion of patients with a known onset time of stroke to the national upper quartile if currently less than the national upper quartile (leave any greater than the upper national quartile at their current level).
            ''')
    with cols_benchmark[1]:
        st.markdown('### Benchmark')
        st.markdown('''
            The benchmark thrombolysis rate takes the likelihood to give thrombolysis for patients scanned within 4 hours of onset from the majority vote of the 30 hospitals with the highest predicted thrombolysis use in a standard 10k cohort set of patients. These are from Random Forests models.
            ''')
    st.markdown('-' * 50)


    with st.sidebar:
        st.markdown('# Inputs')
        # st.markdown('### Highlighted teams')
        # container_highlighted_input = st.container()
        st.markdown('### Scenarios')
        container_scenario_input = st.container()


    # st.markdown('''
    #     ## :chart_with_upwards_trend: Effect of changing scenario
    # ''')
    # tabs_results = st.tabs(['Highlighted teams', 'All teams'])


    st.markdown('## :chart_with_upwards_trend: How could your team improve?')
    container_highlighted_teams = st.container()

    st.markdown('-'*50)
    st.markdown('## :abacus: How are the other teams affected?')
    st.info(''.join([
        'The scenario shown in these graphs ',
        'can be changed in the left sidebar.'
    ]), icon='ℹ️')
    st.markdown(''.join([
        'We can see the general pattern from changing scenario using histograms.'
    ]))


    container_histograms = st.container()

    st.markdown(''.join([
        'We can see the typical effect of this scenario ',
        'by plotting the original and final values for each team ',
        'separately.'
    ]))
    # container_sort_input = st.container()
    container_arrows = st.container()


    # ###########################
    # ########## SETUP ##########
    # ###########################

    stroke_teams_list = utilities_pathway.inputs.\
        import_lists_from_data()

    # User inputs:
    # with container_sort_input:
        # st.markdown('__:warning: TO DO:__ implement sorting better.')
    with st.sidebar:
        scenario = utilities_pathway.inputs.inputs_for_bar_chart()

    with container_highlighted_teams:
        # Receive the user inputs now and show this container now:
        # with container_bar_chart:
        # st.markdown(''.join([
        #     'To highlight stroke teams on the following charts, ',
        #     'select them in this box. ',
        #     '__:warning: TO DO:__ make charts clickable.'
        #     # ' or click on them in the charts.'
        # ]))
        # Pick teams to highlight on the bar chart:
        highlighted_teams_input = utilities_pathway.inputs.\
            highlighted_teams(stroke_teams_list)


    # #######################################
    # ########## MAIN CALCULATIONS ##########
    # #######################################

    with container_scenario_input:
        df = utilities_pathway.inputs.\
            import_stroke_data(
                stroke_teams_list, scenarios, highlighted_teams_input
                )

    # Sort the data according to this input:
    for col in ['Percent_Thrombolysis_(mean)', 'Additional_good_outcomes_per_1000_patients_(mean)']:
        for each_scenario in scenarios: #+ [scenario_for_rank]:
            df = utilities_pathway.inputs.add_sorted_rank_column_to_df(
                df, each_scenario, len(stroke_teams_list), len(scenarios), col)

    # Find colour lists for plotting (saved to session state):
    hb_teams_input = st.session_state['hb_teams_input']
    remove_old_colours_for_highlights(hb_teams_input)
    choose_colours_for_highlights(hb_teams_input)

    highlighted_colours = st.session_state['highlighted_teams_colours']

    # ###########################
    # ######### RESULTS #########
    # ###########################


    # with tabs_results[0]:
    with container_highlighted_teams:
        # Bar chart for individual team:
        if len(highlighted_teams_input) < 1:
            st.caption('No teams are highlighted.')
        else:
            st.markdown(''.join([
                'These charts show the effect of changing scenario ',
                'on the percentage of patients thrombolysed ',
                'and on the number of additional good outcomes. '
            ]))
            for team in highlighted_teams_input:
                cols_single_bars = st.columns(2)
                # Find the colour used to highlight this team:
                try:
                    bar_colour = highlighted_colours[team]
                except KeyError:
                    bar_colour = highlighted_colours[default_highlighted_team]
                with cols_single_bars[0]:
                    utilities_pathway.plot_bars.plot_bars_for_single_team(
                            df, team,
                            df_column='Percent_Thrombolysis_(mean)',
                            y_label='Thrombolysis use (%)',
                            bar_colour=bar_colour  #plotly_colours[0]
                            )
                    # Write an empty header for breathing room;
                    st.markdown('# ')
                with cols_single_bars[1]:
                    utilities_pathway.plot_bars.\
                        plot_bars_for_single_team(
                            df, team,
                            df_column='Additional_good_outcomes_per_1000_patients_(mean)',
                            y_label='Additional good outcomes<br>per 1000 admissions',
                            bar_colour=bar_colour  # plotly_colours[1]
                            )
                    # Write an empty header for breathing room;
                    st.markdown('# ')

                # Offer up a table:
                if st.checkbox(f'Show table of data for {team}'):
                    show_data_for_team(team, df)


    with container_histograms:
        cols_perc = st.columns(2)
        with cols_perc[0]:
            utilities_pathway.plot_hist.plot_hist(
                df,
                ['base', scenario],
                highlighted_teams_input,
                highlighted_colours,
                len(stroke_teams_list),
                df_column='Percent_Thrombolysis_(mean)', 
                y_title='Thrombolysis use (%)'
            )
        with cols_perc[1]:
            utilities_pathway.plot_hist.plot_hist(
                df,
                ['base', scenario],
                highlighted_teams_input,
                highlighted_colours,
                len(stroke_teams_list),
                df_column='Additional_good_outcomes_per_1000_patients_(mean)', 
                y_title='Additional good outcomes<br>per 1000 admissions'
            )

    with container_arrows:
        cols_add = st.columns(2)
        with cols_add[0]:
            utilities_pathway.plot_bars.plot_scatter_sorted_rank(
                df,
                scenario,
                scenario_for_rank='base!perc_thromb',
                n_teams=len(stroke_teams_list),
                y_str='Percent_Thrombolysis_(mean)',
                showlegend_col=True
                )

        with cols_add[1]:
            utilities_pathway.plot_bars.plot_scatter_sorted_rank(
                df,
                scenario,
                scenario_for_rank='base!add_good',
                n_teams=len(stroke_teams_list),
                y_str='Additional_good_outcomes_per_1000_patients_(mean)',
                showlegend_col=True
                )

    # Table of results
    st.markdown('### Table of all results')
    st.markdown('''
        This table contains the data for all teams and all scenarios. 
        It can be copied and pasted into other applications, 
        for example Excel.
        ''')
    show_data_for_all(df)
    

    # ----- The end! -----


if __name__ == '__main__':
    main()
