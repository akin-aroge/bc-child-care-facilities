"""distribution page"""

import streamlit as st
import streamlit_folium as st_folium
from src.dashboard import utils as dash_utils
from src.dashboard import viz
from src.dashboard import stories
import src.processing as proc
from .trends import region_filter


@st.cache_data
def get_data():
    data = proc.get_location_dashboard_data()
    data = proc.enhance_facility_loc_df(data)
    return data


data = get_data()


def sec_page_title():
    st.write(
        """
        ## Distribution of Facility Centres
        """
    )


def main():
    sec_page_title()
    select_region = region_filter()
    select_service_type = service_type_filter()
    data = proc.enhance_facility_loc_df(get_data())
    print("before", data.head())
    data = dash_utils.filter_facility_loc_df(
        data=data, region_filter=select_region, service_type_filter=select_service_type
    )
    print("after", data.head())
    sec_dist_view(data=data)
    sec_map_view(data=data)


def service_type_filter():
    service_types = dash_utils.get_facility_loc_df_service_type(facility_loc_ex_df=data)
    selections = st.sidebar.multiselect(
        label="select service type:", options=service_types, default=service_types
    )
    return selections


def region_filter():
    regions = dash_utils.get_facility_loc_df_regions(facility_loc_ex_df=data)

    select_region = st.sidebar.multiselect(
        label="select regions to view:", options=regions, default=regions
    )
    return select_region


def sec_map_view():
    pass


def sec_dist_view(data):

    cols_to_view_by_options = ["CITY", "region"]  # TODO: centralize these
    col_to_view_by = st.radio(
        label="View by:",
        options=cols_to_view_by_options,
        format_func=lambda x: dash_utils.get_human_readable(x),
    )
    # top_n = st.number_input(label='Show top values:', min_value=2, max_value=50, value=10)

    fancy_col_to_view_by = dash_utils.get_human_readable(col_to_view_by)
    # st.write(
    #     f"""
    #         #### Distribution of Locations by {fancy_col_to_view_by}
    #         """
    # )

    # cols_to_view_by_options = ['CITY', 'region']  # TODO: centralize these
    # col_to_view_by = st.radio(label="View by:", options=cols_to_view_by_options)
    cols = st.columns([0.1, 0.5])
    with cols[0]:
        top_n = st.number_input(
            label="Show top values:", min_value=2, max_value=50, value=10
        )
    if col_to_view_by == "CITY":
        fig = viz.plot_distribution(
            data=data, group_col_name=col_to_view_by, top_n=top_n
        )
    elif col_to_view_by == "region":
        fig = viz.plot_distribution_by_region(data=data, top_n=top_n)

    dash_utils.st_img_show(fig)

    with st.expander("See remarks"):
        st.write(stories.ON_FACILITY_DISTRIBUTION)


def sec_map_view(data):

    st.write(
        f"""
        ## Map of Facility Locations
        """
    )
    st.caption("*click on location to view details* ")
    m = viz.plot_facility_map(data=data)
    st_folium.folium_static(m)
