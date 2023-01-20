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
    page_setup, scenarios, scenarios_dict
import utilities_pathway.inputs
import utilities_pathway.plot_bars
import utilities_pathway.plot_violins
import utilities_pathway.plot_hist
from utilities_pathway.plot_utils import \
    remove_old_colours_for_highlights, choose_colours_for_highlights


def main():
    # ###########################
    # ##### START OF SCRIPT #####
    # ###########################
    page_setup()

    # Title:
    st.markdown('# Pathway improvement')
    st.warning(''.join([
        ':warning: __Work in progress__ ',
        'This app runs but still needs explanatory text, ',
        'and not all of these test plots will be in the final version. '
        ]))

    container_highlighted_input = st.container()

    tabs_results = st.tabs(['All teams', 'Highlighted teams'])
    with tabs_results[0]:
        container_hist = st.container()
        container_violin = st.container()
        container_sort_input = st.container()
        container_bar = st.container()




    # ###########################
    # ########## SETUP ##########
    # ###########################

    stroke_teams_list = utilities_pathway.inputs.\
        import_lists_from_data()

    # User inputs:
    with container_sort_input:
        scenario, scenario_for_rank = utilities_pathway.inputs.\
            inputs_for_bar_chart()

    with container_highlighted_input:
        # Receive the user inputs now and show this container now:
        # with container_bar_chart:
        st.markdown(''.join([
            'To highlight stroke teams on the following charts, ',
            'select them in this box. ',
            '__TO DO:__ make charts clickable.'
            # ' or click on them in the charts.'
        ]))
        # Pick teams to highlight on the bar chart:
        highlighted_teams_input = utilities_pathway.inputs.\
            highlighted_teams(stroke_teams_list)


    # #######################################
    # ########## MAIN CALCULATIONS ##########
    # #######################################

    df = utilities_pathway.inputs.\
        import_stroke_data(
            stroke_teams_list, scenarios, highlighted_teams_input
            )

    # Sort the data according to this input:
    for each_scenario in scenarios + [scenario_for_rank]:
        df = utilities_pathway.inputs.add_sorted_rank_column_to_df(
            df, each_scenario, len(stroke_teams_list), len(scenarios))

    # Find colour lists for plotting (saved to session state):
    hb_teams_input = st.session_state['hb_teams_input']
    remove_old_colours_for_highlights(hb_teams_input)
    choose_colours_for_highlights(hb_teams_input)

    highlighted_colours = st.session_state['highlighted_teams_colours']


    # ###########################
    # ######### RESULTS #########
    # ###########################

    with container_hist:
        # Histogram
        utilities_pathway.plot_hist.plot_hist(
            df,
            ['base', scenario],
            highlighted_teams_input,
            highlighted_colours,
            len(stroke_teams_list)
        )

    with container_bar:
        # st.write('Ranked bar chart:')
        # st.write('(hard to see negative changes)')
        # # Make a bar chart of the mean values:
        # utilities_pathway.plot_bars.plot_bars_sorted_rank(
        #     df,
        #     scenario,
        #     scenario_for_rank,
        #     len(stroke_teams_list)
        #     )

        st.write('Non-ranked scatter:')
        # Make a scatter chart of the mean values:
        utilities_pathway.plot_bars.plot_scatter_base_vs_scenario(
            df,
            scenario,
            scenario_for_rank,
            len(stroke_teams_list)
            )

        st.write('Ranked scatter:')
        # Make a scatter chart of the mean values:
        utilities_pathway.plot_bars.plot_scatter_sorted_rank(
            df,
            scenario,
            scenario_for_rank,
            len(stroke_teams_list)
            )

        st.write('Ranked bar:')
        # Make a bar+scatter chart of the mean values:
        utilities_pathway.plot_bars.plot_bar_scatter_sorted_rank(
            df,
            scenario,
            scenario_for_rank,
            len(stroke_teams_list)
            )


    with tabs_results[1]:
        # Bar chart for individual team:
        for team in highlighted_teams_input:
            utilities_pathway.plot_bars.plot_bars_for_single_team(df, team)

    with container_violin:
        # Violin plot:
        utilities_pathway.plot_violins.plot_violins(
            df,
            ['base', scenario],
            highlighted_teams_input,
            highlighted_colours,
            len(stroke_teams_list)
            )

    # ----- The end! -----


if __name__ == '__main__':
    main()
