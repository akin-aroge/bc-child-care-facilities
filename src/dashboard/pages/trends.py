""" Trends page"""

import streamlit as st
from src.dashboard import utils as dash_utils
from src.dashboard import viz
from src.dashboard import stories


def main():

    sec_kpi()
    select_year = year_filter()
    select_service = service_filter()
    select_region = region_filter()

    df = dash_utils.filter_facility_df(
        year_filter=select_year,
        service_filter=select_service,
        region_filter=select_region,
    )
    sec_trend_view(df, col_to_view=select_service)


def year_filter():

    min_year = int(dash_utils.get_min_year())
    max_year = int(dash_utils.get_max_year())
    value = st.sidebar.slider(
        label="set year limits:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )
    return value


def service_filter():
    services = dash_utils.get_facility_df_services()

    select_service = st.sidebar.selectbox(
        "Select service to see trned:", options=services, index=0
    )
    # select_service = [select_service]
    return select_service


def region_filter():
    regions = dash_utils.get_facility_df_regions()

    select_region = st.sidebar.multiselect(
        label="select regions to view:", options=regions, default=regions
    )
    return select_region


def sec_kpi():

    col1, col2 = st.columns(2)
    cols_to_view = ["total_facilities", "total_spaces"]
    n_facilities, delta_facilities = dash_utils.get_last_facility_count_n_change(
        col_to_count=cols_to_view[0]
    )
    n_spaces, delta_spaces = dash_utils.get_last_facility_count_n_change(
        col_to_count=cols_to_view[1]
    )

    with col1:
        st.metric(
            label=f"Latest number of {cols_to_view[0]}",
            value=n_facilities,
            delta=int(delta_facilities),
        )
    with col2:
        st.metric(
            label=f"Latest number of {cols_to_view[1]}",
            value=n_spaces,
            delta=int(delta_spaces),
        )


def sec_trend_view(data, col_to_view):
    st.write(
        f"""
            ## Yearly trend in {col_to_view}.
            The plot shows the distribution of the demand by the month of the year.
            """
    )
    fig = viz.plot_fac_trend(data=data, y_col=col_to_view)
    view_delta = st.checkbox(label="view annual change", value=True)

    # if col_to_view in  ["total_spaces", "total_facilities"]:
    if view_delta:

        # create two columns to show growth
        col1, col2 = st.columns([1, 1])
        fig_delta = viz.plot_fac_delta(data=data, y_col=col_to_view)

        with col2:
            dash_utils.st_img_show(fig_delta)
        with col1:
            dash_utils.st_img_show(fig)
    else:
        dash_utils.st_img_show(fig)

    with st.expander("See remarks"):
        st.write(stories.ON_THE_TREND_IN_FACILITY_GROWTH)
