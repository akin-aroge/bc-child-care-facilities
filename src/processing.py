"""routings for processing data"""

import pandas as pd
from src import constants as C
from src import utils
from urllib.error import HTTPError


root_dir = utils.get_proj_root()
facility_loc_path_local = root_dir.joinpath("./data/raw/childcare_locations.csv")
facility_time_path_local = root_dir.joinpath(
    "./data/raw/ccof_facilities_and_spaces_over_time.csv"
)

facility_loc_path_web = C.DATA_SOURCES["child care map data"]
facility_time_path_web = C.DATA_SOURCES["facilities and spaces over time"]


def get_raw_data(update=False):
    """get raw data."""

    if not update:
        try:
            locs_df = pd.read_csv(facility_loc_path_local)
            facility_df = pd.read_csv(facility_time_path_local)
        except FileNotFoundError:
            # TODO:
            return_val = _pull_data_from_web()
            if return_val is False:
                pass
            else:
                facility_df, locs_df = return_val
                facility_df.to_csv(facility_time_path_local, index=False)
                locs_df.to_csv(facility_loc_path_local, index=False)
    else:
        return_val = _pull_data_from_web()
        if return_val is False:
            pass
        else:
            facility_df, locs_df = return_val

            facility_df.to_csv(facility_time_path_local, index=False)
            locs_df.to_csv(facility_loc_path_local, index=False)

    # to ensure always reading from local store
    facility_df = pd.read_csv(facility_time_path_local)
    locs_df = pd.read_csv(facility_loc_path_local)

    return (facility_df, locs_df)


def _pull_data_from_web():

    try:

        locs_df = pd.read_csv(facility_loc_path_web)
        facility_df = pd.read_csv(facility_time_path_web)

        return (facility_df, locs_df)
    except HTTPError:
        return False
        # pass


def enhance_facility_df(facility_df: pd.DataFrame) -> pd.DataFrame:
    """Add new columns to dataset."""

    df = (
        facility_df.assign(date=pd.to_datetime(facility_df["ym"], format="%Y%m"))
        .pipe(_get_col_diffs, col_to_diff="total_facilities")
        .pipe(_get_col_diffs, col_to_diff="total_spaces")
        .assign(space_per_fac=lambda x: x["total_spaces"] / x["total_facilities"])
        .pipe(_get_col_diffs, col_to_diff="space_per_fac")
    )

    return df


def enhance_facility_loc_df(facility_loc_df: pd.DataFrame) -> pd.DataFrame:
    """Add new columns to dataset."""
    df = (
        facility_loc_df
        # .assign(region=lambda x: cities_regions_map[x['CITY']])
        .query("IS_DUPLICATE == 'N'").assign(
            region=facility_loc_df["CITY"]
            .str.lower()
            .apply(lambda x: C.CITIES_REGIONS_MAP.get(x, "other"))
        )
    )
    return df


def get_location_dashboard_data(update=False):
    """get dashboard data for the facility locations"""

    facility_df, locs_df = get_raw_data(update=update)
    return locs_df


def get_dashboard_data(update=False):
    """Create the ehanced dataset for dashboard operations."""
    # if refresh:
    #     facility_df, locs_df = proc.get_raw_data(update=False)
    #     facility_df_ex = proc.enhance_facility_df(facility_df=facility_df)
    #     facility_df_ex.to_csv()
    # TODO: separate facility and location dataset retrieval
    facility_df, locs_df = get_raw_data(update=update)
    facility_df_ex = enhance_facility_df(facility_df=facility_df)
    locs_df_ex = enhance_facility_loc_df(facility_loc_df=locs_df)

    return facility_df_ex, locs_df_ex


def _get_group_diffs(group_df, col_to_diff: str):

    group_df[col_to_diff + "_growth"] = group_df[col_to_diff].diff()

    return group_df


def _get_col_diffs(df: pd.DataFrame, col_to_diff: str):

    df = df.groupby("region").apply(_get_group_diffs, col_to_diff=col_to_diff)

    return df


# def get_col_delta(df:pd.DataFrame, col_to_diff:str):
#     """Return the diffs of a specific column (while considering the region grouping)."""

#     df = df.groupby('region').apply(_get_group_diffs, col_to_diff=col_to_diff)
#     delta_col_name = col_to_diff+'_growth'

#     return df['delta_col_name']
