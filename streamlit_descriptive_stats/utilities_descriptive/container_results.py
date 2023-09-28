"""
All of the content for the Results section.
"""
import streamlit as st


def check_teams_in_stats_df(
        summary_stats_df,
        stroke_teams_selected,
        container_warnings
        ):
    """
    Remove any selected teams and years that aren't in the data.

    If all of the selected teams and years exist in the descriptive
    stats dataframe, then return a shorter dataframe of just those
    teams and years. If some of them are missing, then check each
    team and year combo in turn to root out the missing ones.
    Return a dataframe of only the combos that exist and print a
    warning message about those that don't.

    Inputs:
    -------
    summary_stats_df      - pd.DataFrame. The descriptive stats data.
    stroke_teams_selected - list. One string per team and year combo
                            selected by the user.
    container_warnings    - streamlit container. Where to print any
                            warnings about missing data.

    Returns:
    --------
    df_to_show - pd.DataFrame. A subset of data from the input
                 dataframe that covers only the selected team and
                 year combinations.
    """
    try:
        # Smaller dataframe of only selected teams:
        df_to_show = summary_stats_df[stroke_teams_selected]
    except KeyError:
        # Remove teams that aren't in the dataframe.
        # Keep the valid ones in here:
        reduced_teams_to_show = []
        # Keep the invalid ones in here:
        missing_teams = []
        # Set up for printing a nice warning message:
        show_warning = False
        warning_str = 'There is no data for '

        # Sort the teams into the valid and invalid lists:
        for team in stroke_teams_selected:
            try:
                summary_stats_df[team]
                reduced_teams_to_show.append(team)
            except KeyError:
                show_warning = True
                missing_teams.append(team)

        # The dataframe containing only the valid teams:
        df_to_show = summary_stats_df[reduced_teams_to_show]

        # If there were missing teams (should always be True),
        # show the message.
        if show_warning is True:
            # Create a warning message to print.
            # e.g. "There is no data for {1}, {2} or {3}."
            warning_str = (
                warning_str +
                ', '.join(missing_teams[:-1])
                )
            if len(missing_teams) > 1:
                warning_str += ' or '
            warning_str = (
                warning_str + missing_teams[-1] + '.'
            )
            # Display the warning:
            with container_warnings:
                st.warning(warning_str, icon='⚠️')

    return df_to_show
