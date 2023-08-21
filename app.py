import streamlit as st
from src import constants as C
from src.dashboard.pages import trends
import src.processing as proc

APP_MODES = ["Facility Trends", "facility Map"]

def sec_update_data():
    # TODO
    is_update_data = st.sidebar.button("Update Data")
    if is_update_data:
        proc.get_dashboard_data(update=is_update_data)



def main():
    st.set_page_config(page_title="Electricy Demand Predition", layout="wide")
    sec_update_data()
    st.sidebar.title("What would you like to do?:")
    st.title("BC Child Care Facilities")
    st.caption(
        "Scource Code: [link](https://github.com/akin-aroge/bc-child-care-facilities)"
    )
    st.caption(
        f"Data Sources: [facility locations]({C.DATA_SOURCES['child care map data']}), \
            [facilities over time]({C.DATA_SOURCES['facilities and spaces over time']})"
    )

    app_mode = st.sidebar.selectbox("Choose the app mode", APP_MODES, index=0)
    if app_mode == "Facility Trends":
        trends.main()
        

if __name__ == "__main__":
    main()
