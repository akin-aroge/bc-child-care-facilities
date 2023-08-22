""" Trends page"""

import streamlit as st
from src.dashboard import utils as dash_utils
from src.dashboard import viz
from src.dashboard import stories


def main():
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
    # human_readable_services = [dash_utils.get_human_readable(item, item) for item in services]

    select_service = st.sidebar.selectbox(
        "Select service type:",
        options=services,
        index=0,
        format_func=lambda x: dash_utils.get_human_readable(x),
    )
    # select_service = [select_service]
    return select_service


def region_filter():
    regions = dash_utils.get_facility_df_regions()

    select_region = st.sidebar.multiselect(
        label="select regions to view:", options=regions, default=regions
    )
    return select_region


def sec_trend_view(data, col_to_view):
    st.write(
        f"""
            ## Facilities Annual Growth Trend
            The plot shows the growth trend of facilities.
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
        st.write(stories.ON_FACILITY_TRENDS)
