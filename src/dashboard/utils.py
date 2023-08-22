""" dashboard utilities """

import pandas as pd
from src import utils
from src import processing as proc
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import streamlit as st
import numpy as np
import src.constants as C
import pickle

root_dir = utils.get_proj_root()

# year limits
# facility_df, locs_df = proc.get_raw_data(update=False)
# facility_df_ex_path = root_dir.joinpath("./data/raw/ccof_facilities_and_spaces_over_time.csv")

# def get_dashboard_data():
#     """Create the ehanced dataset for dashboard operations."""
#     # if refresh:
#     #     facility_df, locs_df = proc.get_raw_data(update=False)
#     #     facility_df_ex = proc.enhance_facility_df(facility_df=facility_df)
#     #     facility_df_ex.to_csv()
#     facility_df, locs_df = proc.get_raw_data(update=False)
#     facility_df_ex = proc.enhance_facility_df(facility_df=facility_df)
#     locs_df_ex = proc.enhance_facility_loc_df(facility_loc_df=locs_df)

#     return facility_df_ex, locs_df_ex

# TODO: this should not be here
facility_df_ex, locs_df_ex = proc.get_dashboard_data()


def get_facility_df_services():
    """Get the facilities care types"""
    return list(facility_df_ex.columns[3:15])


def get_facility_df_regions():
    """Get the different facility regions."""
    return list(facility_df_ex.region.unique())

def get_facility_loc_df_regions(facility_loc_ex_df:pd.DataFrame):
    """Get the different facility location regions."""
    return list(facility_loc_ex_df.region.unique())

def get_facility_loc_df_service_type(facility_loc_ex_df:pd.DataFrame):
    """Get the different facility location regions."""
    return list(facility_loc_ex_df.SERVICE_TYPE_CD.unique())

def get_max_year() -> int:
    """get maximum year."""
    max_year = facility_df_ex.date.dt.year.max()
    return max_year


def get_min_year() -> int:
    """get maximum year."""
    min_year = facility_df_ex.date.dt.year.min()
    return min_year


def get_date_count(data: pd.DataFrame, date: pd.Timestamp, col_name: str):
    """Get the total of the specified column for the given timestamp."""
    try:
        vals = data[data["date"] == date][col_name]
    except KeyError:
        print("date values not found.")
    return np.sum(vals)


def get_last_facility_count_n_change(col_to_count="total_facilities"):

    last_record_month = facility_df_ex["date"].max()
    second_to_last_record_month = last_record_month + pd.DateOffset(months=-1)
    last_record_month_facility_count = get_date_count(
        data=facility_df_ex, date=last_record_month, col_name=col_to_count
    )
    second_to_last_record_month_count = get_date_count(
        data=facility_df_ex, date=second_to_last_record_month, col_name=col_to_count
    )
    delta = last_record_month_facility_count - second_to_last_record_month_count

    return last_record_month_facility_count, delta


def st_img_show(fig: matplotlib.figure.Figure):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    st.image(buf)


def filter_facility_df(
    year_filter=None, service_filter=None, region_filter=None
) -> pd.DataFrame:

    """Apply filters to the facility dataframe"""
    df = facility_df_ex.copy()

    # filter year
    if year_filter is not None:
        min_year, max_year = year_filter

        year_mask = (df["date"] > str(min_year)) & (df["date"] < str(max_year + 1))
        df = df[year_mask]
    # print(df.head())

    if region_filter is not None:
        print(region_filter)
        region_mask = df["region"].apply(lambda x: x in region_filter)
        print(region_mask)
        df = df[region_mask]

    return df

def filter_facility_loc_df(data:pd.DataFrame, region_filter=None,
                           service_type_filter=None
) -> pd.DataFrame:

    """Apply filters to the facility dataframe"""
    df = data.copy()


    if region_filter is not None:
        region_mask = df["region"].apply(lambda x: x in region_filter)
        df = df[region_mask]

    if service_type_filter is not None:
        mask = df['SERVICE_TYPE_CD'].apply(lambda x: x in service_type_filter)
        df = df[mask]

    return df


def get_latlon_centroid(lat, lon) -> list:

    pos = np.stack([lat, lon], axis=1)
    centroid = pos.mean(axis=0)
    return centroid

def get_human_readable(input):

    value = C.NAME_MAPPINGS.get(input, input)
    return value




def save_value(value, fname):
    with open(fname, "wb") as f:
        pickle.dump(value, f)