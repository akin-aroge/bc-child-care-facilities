import streamlit as st
from src import constants as C
from src.dashboard.pages import trends, distribution
import src.processing as proc
from src.dashboard import utils as dash_utils

APP_MODES = ["Facility Trends", "Facility Distribution"]

def sec_update_data():
    # TODO
    is_update_data = st.sidebar.button("Update data from source")
    if is_update_data:
        proc.get_dashboard_data(update=is_update_data)

def git_repo():
    st.caption(
    "Scource Code: [link](https://github.com/akin-aroge/bc-child-care-facilities)"
)
    
def data_sorce_link():
    st.caption(
        f"Data Sources: [Facility Locations]({C.DATA_SOURCES['child care map data']}), \
            [Regional Facility Numbers]({C.DATA_SOURCES['facilities and spaces over time']})"
    )    

def sec_links_caption():
    cols =  st.columns([0.1, 0.3, 0.6])
    with cols[0]:
        git_repo()
    with cols[1]:
        data_sorce_link()

def sec_synopsis():
    st.write(
        """
        A dashboard showing the trends and distribution of child care facility centers in BC.
"""
    )

def sec_kpi():

    col1, col2, col3 = st.columns([0.1, 0.4, 0.4])
    cols_to_view = ["total_facilities", "total_spaces"]
    n_facilities, delta_facilities = dash_utils.get_last_facility_count_n_change(
        col_to_count=cols_to_view[0]
    )
    n_spaces, delta_spaces = dash_utils.get_last_facility_count_n_change(
        col_to_count=cols_to_view[1]
    )

    with col1:
        st.write("Monthly Update:")
    with col2:
        st.metric(
            label=f"Latest number of toal facilities",
            value=n_facilities,
            delta=int(delta_facilities),
        )
    with col3:
        st.metric(
            label=f"Latest number of total spaces",
            value=n_spaces,
            delta=int(delta_spaces),
        )

def main():
    st.set_page_config(page_title="BC-ChildCare Facilities", layout="wide")
    sec_update_data()
    st.sidebar.title("What would you like to do?:")
    st.title("BC Child Care Facilities")
    sec_synopsis()
    sec_links_caption()

    sec_kpi()

    app_mode = st.sidebar.selectbox("Choose the app mode:", APP_MODES, index=0)
    if app_mode == "Facility Trends":
        trends.main()
    elif app_mode == 'Facility Distribution':
        distribution.main()

        

if __name__ == "__main__":
    main()
