import streamlit as st


def page_setup():
    # ----- Page setup -----
    # The following options set up the display in the tab in your browser.
    # Set page to widescreen must be first call to st.
    st.set_page_config(
        page_title='Pathway improvement',
        page_icon=':hospital:',
        # layout='wide'
        )
    # n.b. this can be set separately for each separate page if you like.

# How to label non-highlighted teams:
plain_str = 'Non-benchmark team'
bench_str = 'Benchmark team: \U00002605'

scenarios_dict = {
    'Base':'base',
    'Speed':'speed',
    'Onset':'onset',
    'Benchmark':'benchmark',
    'Speed + Onset':'speed_onset',
    'Speed + Benchmark':'speed_benchmark',
    'Onset + Benchmark':'onset_benchmark',
    'Speed + Onset + Benchmark':'speed_onset_benchmark'
    # 'same_patient_characteristics'
}
scenarios_dict2 = dict(zip(scenarios_dict.values(), scenarios_dict.keys()))
scenarios = list(scenarios_dict.values())
