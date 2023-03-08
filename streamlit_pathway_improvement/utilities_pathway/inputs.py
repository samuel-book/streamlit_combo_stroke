import streamlit as st
import pandas as pd
import numpy as np


# For importing data:
try:
    stroke_teams_test = pd.read_csv('./data_pathway/scenario_results.csv')
    dir = './'
except FileNotFoundError:
    dir = 'streamlit_pathway_improvement/'

from utilities_pathway.fixed_params import \
    plain_str, bench_str, scenarios, scenarios_dict, \
    default_highlighted_team, display_name_of_default_highlighted_team


def write_text_from_file(filename, head_lines_to_skip=0):
    """
    Write text from 'filename' into streamlit.
    Skip a few lines at the top of the file using head_lines_to_skip.
    """
    # Open the file and read in the contents,
    # skipping a few lines at the top if required.
    with open(filename, 'r', encoding="utf-8") as f:
        text_to_print = f.readlines()[head_lines_to_skip:]

    # Turn the list of all of the lines into one long string
    # by joining them up with an empty '' string in between each pair.
    text_to_print = ''.join(text_to_print)

    # Write the text in streamlit.
    st.markdown(f"""{text_to_print}""")


def import_lists_from_data():
    """
    """
    df = pd.read_csv(
        dir + 'data_pathway/scenario_results.csv',
        # index_col=index_col,
        header='infer'
        )

    # Pull out the list of stroke teams:
    stroke_teams_list = sorted(set(df['stroke_team'].to_numpy()))

    # # Remove "same patient characteristics" scenario:
    # df = df[
    #     df['scenario'].str.contains('same_patient_characteristics') == False
    #     ]

    return stroke_teams_list  #, scenarios


def import_stroke_data(stroke_teams_list, scenarios, highlighted_teams_input):
    """

    --- Columns in the imported data: ---
    Baseline_good_outcomes_(median)
    Baseline_good_outcomes_per_1000_patients_(low_5%)
    Baseline_good_outcomes_per_1000_patients_(high_95%)
    Baseline_good_outcomes_per_1000_patients_(mean)
    Baseline_good_outcomes_per_1000_patients_(stdev)
    Baseline_good_outcomes_per_1000_patients_(95ci)
    Percent_Thrombolysis_(median%)
    Percent_Thrombolysis_(low_5%)
    Percent_Thrombolysis_(high_95%)
    Percent_Thrombolysis_(mean)
    Percent_Thrombolysis_(stdev)
    Percent_Thrombolysis_(95ci)
    Additional_good_outcomes_per_1000_patients_(median)
    Additional_good_outcomes_per_1000_patients_(low_5%)
    Additional_good_outcomes_per_1000_patients_(high_95%)
    Additional_good_outcomes_per_1000_patients_(mean)
    Additional_good_outcomes_per_1000_patients_(stdev)
    Additional_good_outcomes_per_1000_patients_(95ci)
    Onset_to_needle_(mean)
    calibration
    scenario
    stroke_team
    """
    df = pd.read_csv(
        dir + 'data_pathway/scenario_results.csv',
        # index_col=index_col,
        header='infer'
        )

    # Remove "same patient characteristics" scenario:
    df = df[
        df['scenario'].str.contains('same_patient_characteristics') == False
        ]

    # Import benchmark info.
    benchmark_df = import_benchmark_data()
    # Make list of benchmark rank:
    # (original data is sorted alphabetically by stroke team)
    benchmark_rank_list = \
        benchmark_df.sort_values('stroke_team')['Rank'].to_numpy()
    # Indices of benchmark data at the moment:
    inds_benchmark = np.where(benchmark_rank_list <= 30)[0]
    # Convert this to a column for the dataframe:
    benchmark_col = np.tile(benchmark_rank_list, len(scenarios))
    # Add to the dataframe:
    df['Benchmark_rank'] = benchmark_col

    # Update the "Highlighted teams" column:
    # Label benchmarks:
    # table[np.where(table[:, 7] <= 30), 6] = 'Benchmark'
    highlighted_teams_list = np.array(
        ['-' for team in stroke_teams_list], dtype=object)
    # Combo highlighted and benchmark:
    hb_teams_list = np.array(
        [plain_str for team in stroke_teams_list], dtype=object)
    hb_teams_list[inds_benchmark] = bench_str
    # Put in selected Highlighteds (overwrites benchmarks):
    hb_teams_input = [plain_str, bench_str]
    for team in highlighted_teams_input:
        if team == display_name_of_default_highlighted_team:
            team = default_highlighted_team
        ind_t = np.argwhere(np.array(stroke_teams_list) == team)[0][0]
        # inds_highlighted.append(ind_t)
        highlighted_teams_list[ind_t] = team
        if ind_t in inds_benchmark:
            team = team + ' \U00002605'
        hb_teams_list[ind_t] = team
        hb_teams_input.append(team)

    # Add the short list of names to the session_state so we can
    # retrieve it immediately when the script is re-run:
    st.session_state['hb_teams_input'] = hb_teams_input
    # Add the full list to the dataframe:
    hb_teams_col = np.tile(hb_teams_list, len(scenarios))
    df['HB_team'] = hb_teams_col

    # Reduce this dataframe to just the important features:
    key_features = [
        'Baseline_good_outcomes_per_1000_patients_(mean)',
        'Percent_Thrombolysis_(mean)',
        'Additional_good_outcomes_per_1000_patients_(mean)',
        'scenario',
        'stroke_team',
        'Benchmark_rank',
        'HB_team'
    ]
    df = df[key_features].copy()

    # Add some new columns.
    # Data for the new columns will be put in these lists.
    # Initialise as all zero for the difference between base and base.
    diff_perc_thromb = [0] * len(stroke_teams_list)
    diff_additional_good = [0] * len(stroke_teams_list)
    # Define some bits to stop the following lines being really long:
    d = df['scenario'] == 'base'
    p_str = 'Percent_Thrombolysis_(mean)'
    a_str = 'Additional_good_outcomes_per_1000_patients_(mean)'
    for scenario in scenarios[1:]:
        # Find a shorter dataframe containing just this scenario:
        df_here = df[df['scenario'] == scenario]
        # Find lists of the differences from base:
        diff_p = df_here[p_str].values - df[p_str][d].values
        diff_a = df_here[a_str].values - df[a_str][d].values
        # Add to the existing lists:
        diff_perc_thromb = np.concatenate((diff_perc_thromb, diff_p))
        diff_additional_good = np.concatenate((diff_additional_good, diff_a))
    # Add these new columns to the dataframe:
    df[p_str + '_diff'] = diff_perc_thromb
    df[a_str + '_diff'] = diff_additional_good


    return df


def add_sorted_rank_column_to_df(df, scenario_for_rank, n_teams, n_scenarios, col_to_sort='Percent_Thrombolysis_(mean)'):
    if col_to_sort == 'Percent_Thrombolysis_(mean)':
        col_short = '!perc_thromb'
    else:
        col_short = '!add_good'
    scenario_for_name = scenario_for_rank + col_short
    if '!' in scenario_for_rank:
        scenario_for_rank = '!'.join(scenario_for_rank.split('!')[:-1])
        col_to_sort += '_diff'

    # Add sorted base rank:
    # Make a new "Index" column that ranks the teams alphabetically
    # (or default input order). Each team gets the same index value
    # across all of these different scenarios.
    index_original_col = np.tile(np.arange(n_teams), n_scenarios)
    df['Index'] = index_original_col
    # Sort the values by the mean percent of thrombolysis column
    # in the "base" scenario.
    # Extract the values for just this scenario:
    df_base = df[df['scenario'] == scenario_for_rank].copy()
    # Sort with largest value at the top:
    df_sorted_rank = df_base.sort_values(col_to_sort, ascending=False)
    # Add rank, largest value = 1, smallest = 132 (or number of teams).
    df_sorted_rank['Rank'] = np.arange(1, n_teams + 1)
    # Now re-sort back to the starting order...
    df_sorted_rank = df_sorted_rank.sort_values('Index')
    # ... and these are the ranks for all of the teams:
    df_sorted_rank_index = df_sorted_rank['Rank'].values
    # Copy this multiple times, one set for each scenario:
    sorted_rank_col = np.tile(df_sorted_rank_index, n_scenarios)
    # Add this column to the main data frame:

    df['Sorted_rank!' + scenario_for_name] = sorted_rank_col
    return df


def inputs_for_bar_chart():

    # Set value=True in these checkboxes
    # to have them ticked by default.
    st.markdown('Show difference due to:')
    scenarios_picked = []
    if st.checkbox('Speed', value=True):
        scenarios_picked.append('Speed')
    if st.checkbox('Onset', value=True):
        scenarios_picked.append('Onset')
    if st.checkbox('Benchmark', value=True):
        scenarios_picked.append('Benchmark')

    if len(scenarios_picked) == 0:
        scenario = 'base'
    else:
        scenario = ''
        if 'Speed' in scenarios_picked:
            scenario += '_speed'
        if 'Onset' in scenarios_picked:
            scenario += '_onset'
        if 'Benchmark' in scenarios_picked:
            scenario += '_benchmark'
        # Remove initial underscore:
        scenario = scenario[1:]

    # scenario_for_rank = st.radio(
    #     'Sort ranked values by this:',
    #     options=[
    #         'Base value',
    #         'Final value',
    #         f'Effect of scenario'
    #         ],#{scenario}'],
    #     horizontal=True
    #     )

    # if scenario_for_rank == 'Base value':
    #     scenario_for_rank = 'base'
    # elif scenario_for_rank == 'Final value':
    #     scenario_for_rank = scenario
    # else:
        # scenario_for_rank = scenario + '!diff'
    return scenario  #, scenario_for_rank


def import_benchmark_data():
    all_teams_and_probs = pd.read_csv(
        dir + 'data_pathway/hospital_10k_thrombolysis.csv')
    # Add an index row to rank the teams:
    all_teams_and_probs['Rank'] = \
        np.arange(1, len(all_teams_and_probs['stroke_team'])+1)
    return all_teams_and_probs


def highlighted_teams(stroke_teams_list):
    try:
        # If we've already selected highlighted teams using the
        # clickable plotly graphs, then load that list:
        existing_teams = st.session_state['highlighted_teams_with_click']
    except KeyError:
        # Make a dummy list so streamlit behaves as normal:
        existing_teams = [display_name_of_default_highlighted_team]

    # Swap out the default highlighted team's name for
    # the label chosen in fixed_params.
    teams_input_list = stroke_teams_list.copy()
    # Remove the chosen default team...
    teams_input_list.remove(default_highlighted_team)
    # ... and add the new name to the start of the list.
    teams_input_list = [display_name_of_default_highlighted_team] + \
                       teams_input_list

    highlighted_teams_input = st.multiselect(
        'Stroke teams to highlight:',
        teams_input_list,
        # help='Pick up to 9 before the colours repeat.',
        key='highlighted_teams',
        default=existing_teams
    )
    return highlighted_teams_input
