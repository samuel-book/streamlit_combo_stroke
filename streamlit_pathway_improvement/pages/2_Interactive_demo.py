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
    st.markdown(
        '''
        We can simulate various pathways
        to see the effect on thrombolysis rate and additional good outcomes.

        A patient has an additional good outcome if they were thrombolysed and
        had a post-stroke modified Rankin Scale (mRS) of 0 or 1,
        and without thrombolysis their mRS would have been higher than 1.
        ''')
    # st.markdown('')  # Breathing room
    st.markdown('We use the data set __SSNAP Subset 📈 HP1__ (~119,000 patients) which has the following properties:')
    st.markdown(
        '''

        | | |
        | --- | --- |
        | ✨ Cleaned | 📅 Calendar years 2019 and 2020 |
        | 🚑 Ambulance arrivals | 🏥 Grouped by stroke team |
        | 👥 Teams with over 250 admissions | 🧠 Grouped by stroke type |
        | 💉 Teams with at least 10 thrombolysis | |
        '''
        )

    tabs_method = st.tabs([
        'Scenarios',
        'Pathway method',
        'Outcome measure',
        'Simulating many patients'
        ])
    with tabs_method[0]:
        # Method
        cols_scenarios = st.columns(2)

        # Pathway descriptions from the SAMueL book:
        # https://samuel-book.github.io/samuel-1/pathway_sim/scenario_analysis.html
        with cols_scenarios[0]:
            st.info('''
                __Base__  
                Use the recorded stroke team performance data.
                ''')
        with cols_scenarios[0]:
            st.error('''
                __Speed__  
                Change the details of the arrival to scan times.

                For the subgroup of patients who have arrived within 4 hours of onset,
                set the _chance of having arrival to scan time under 4 hours_ to 95%.
                For patients who are scanned within 4 hours of arrival,
                set both _arrival to scan_ and _scan to needle_ times to 15 minutes exactly.
                ''')
        with cols_scenarios[1]:
            st.error('''
                __Onset__  
                Change the chance of having a known onset time.

                The target value is the upper quartile of the _proportions of patients with known onset time_ across all stroke teams.
                The _chance of having a known onset time_ is set to either the target value or the original value, whichever is larger.
                ''')
        with cols_scenarios[1]:
            st.info('''
                __Benchmark__  
                Change the chance of receiving thrombolysis.

                🪝🐤🦆 For the subgroup of patients who have enough time left for thrombolysis,
                update the _chance of receiving thrombolysis_ to the benchmark target for this stroke team.
                The benchmark target is the thrombolysis rate of the stroke team's original patients according to the majority vote of the benchmark teams.
                ''')

    with tabs_method[1]:
        st.markdown(
            '''
            Each patient goes through the following processes
            to find their final onset-to-needle time.  
            The actual numbers used in the checks
            _"Is the number smaller than... ?"_ vary by stroke team.
            '''
            )
        with st.expander('Is onset time known?'):
            image_file = 'flowchart_onset-known.png'
            try:
                st.image('./utilities_pathway/' + image_file)
                path_to_images = './utilities_pathway/'
            except (FileNotFoundError, st.runtime.media_file_storage.MediaFileStorageError):
                # Add an extra bit to the path for the combo app.
                st.image('./streamlit_pathway_improvement/' +
                        'utilities_pathway/' + image_file)
                path_to_images = './streamlit_pathway_improvement/utilities_pathway/'
        with st.expander('Calculate onset-to-arrival time'):
            image_file = 'flowchart_onset-to-arrival.png'
            st.image(f'{path_to_images}/{image_file}')
        with st.expander('Calculate arrival-to-scan time'):
            image_file = 'flowchart_arrival-to-scan.png'
            st.image(f'{path_to_images}/{image_file}')
        with st.expander('Is there enough time for treatment?'):
            image_file = 'flowchart_onset-to-scan.png'
            st.image(f'{path_to_images}/{image_file}')
        with st.expander('Is this patient treated?'):
            st.markdown(
                '''
                This step is carried out only for patients who have
                enough time left for treatment.
                ''')
            image_file = 'flowchart_treated.png'
            st.image(f'{path_to_images}/{image_file}')
        with st.expander('Calculate scan-to-needle time'):
            st.markdown(
                '''
                This step is carried out only for patients who
                receive treatment.
                ''')
            image_file = 'flowchart_scan-to-needle.png'
            st.image(f'{path_to_images}/{image_file}')
        st.markdown(
            '''
            The final treatment time is the sum of the onset-to-arrival,
            arrival-to-scan, and scan-to-needle times.
            ''')

    with tabs_method[2]:
        st.markdown(
            '''
            We calculate the mRS distribution at any treatment time
            using the _"stroke-outcome"_ model.
            ''',
            help='''More details are available at [this link](
            https://samuel-book.github.io/samuel-2/outcome_modelling/intro.html
            ).'''
        )
        st.markdown(
            '''
            This image shows results for Patient "A" who
            had an nLVO and was treated two hours after stroke onset.
            '''
        )
        image_file = 'good_outcome_example.png'
        st.image(f'{path_to_images}/{image_file}')
        st.markdown(
            '''
            The patient was randomly assigned a fixed probability of 0.55.
            The horizontal line at probability=0.55 marks which mRS bin
            the patient falls into in any mRS distribution.

            + The treated mRS is 1.
              + At time 2 hours the horizontal line is in the green bin.
            + The no-treatment mRS is 2.
              + In the "No treatment" distribution the horizontal line
                is in the red bin.

            The treatment has changed the expected outcome
            from "bad" (mRS=2 or higher) to "good" (mRS=1 or lower),
            so this patient counts towards "additional good outcomes".
            '''
        )

    with tabs_method[3]:
        st.markdown(
            '''
            Each stroke team has a different set of patient statistics.
            These include proportions, for example how many patients
            have known onset times, and distributions, for example
            the expected values of arrival-to-scan times.

            We calculate the results for a stroke team by
            simulating many cohorts of patients attending the team.
            We use one cohort per year and the number of patients in
            a cohort is the same as the average number of admissions
            to the stroke team in a year.
            The proportions of patients who have LVOs and nLVOs are
            also drawn from the average hospital data.

            The random elements in the simulation include whether a patient
            meets certain criteria, for example whether the onset time
            is known, and the specific timings chosen for a patient,
            which are usually drawn from a distribution of times.
            This means that two cohorts will contain different data.

            The pre-stroke mRS scores for the patients are generated by
            randomly selecting a "fixed probability" for each patient.
            The method from the "Outcome measure" tab shows how this is
            converted to post-stroke mRS scores.

            The simulations run for 100 years per team and the results
            below are the average results across the 100 trials.
            '''
        )

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
        df_on_import = utilities_pathway.inputs.\
            import_stroke_data(
                stroke_teams_list, scenarios, highlighted_teams_input
                )
        df = df_on_import.copy()

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
                    try:
                        bar_colour = highlighted_colours[team + ' \U00002605']
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
                if st.checkbox(f'Show table of data for Team {team}'):
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
    st.markdown(
        '''
        This table contains the data shown here for all teams
        and all scenarios. The complete data
        including standard deviation and confidence intervals
        is available from the download button below.
        '''
        )
    show_data_for_all(df)
    st.download_button(
        'Download complete data',
        df_on_import.to_csv(index=False),
        file_name='stroke_pathway_results.csv'
    )


    # ----- The end! -----


if __name__ == '__main__':
    main()
