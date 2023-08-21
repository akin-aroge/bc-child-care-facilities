import streamlit as st
from src import constants as C
from src.dashboard.pages import trends

APP_MODES = ["Facility Trends", "facility Map"]


def main():
    st.set_page_config(page_title="Electricy Demand Predition", layout="wide")
    st.sidebar.title("What would you like to do?:")
    st.title("BC Child Care Facilities")
    st.caption(
        "Scource Code: [link]()"
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
