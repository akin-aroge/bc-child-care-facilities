import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import seaborn as sns
from src import processing as proc
from src import constants as C
from src.dashboard import utils as dash_utils
import folium


space_n_facility_col_names = ["total_spaces", "total_facilities"]


def plot_fac_trend(data: pd.DataFrame, y_col):
    """plots the time series of the facility counts"""

    fig, ax = plt.subplots(1, 1)
    sns.lineplot(data=data, x="date", y=y_col, ls="-", hue="region", ax=ax)

    ax.legend()
    ax.grid()
    xlabel = "Date"
    ylabel = f"# of {dash_utils.get_human_readable(y_col)}"
    # ylabel = dash_utils.get_human_readable(y_col)
    label_axes(ax=ax, x_label=xlabel, y_label=ylabel)

    return fig


def plot_fac_delta(data: pd.DataFrame, y_col, **kwargs):
    """plots the time series of the facility changes from period to period."""

    # col_delta = proc.get_col_delta(data, y_col)
    # date

    regions = data["region"].unique()
    fig, ax = plt.subplots(1, 1)
    delta_col_name = y_col + "_change"
    for region in regions[:]:

        region_df = data[data["region"] == region]
        region_df[delta_col_name] = region_df[y_col].diff()

        region_df = region_df.resample(
            "Y", on="date", label="left", closed="right"
        ).sum()
        # ax.plot_date(data=region_df, x='date', y=y_col, ls='-', label=region)
        sns.lineplot(data=region_df, x="date", y=delta_col_name, ls="-", label=region)

    ax.legend()
    ax.grid()

    xlabel = "Date"
    ylabel = f"Change in # of {dash_utils.get_human_readable(y_col)}"
    # ylabel = dash_utils.get_human_readable(y_col)
    label_axes(ax=ax, x_label=xlabel, y_label=ylabel)

    return fig


def plot_distribution(
    data: pd.DataFrame, group_col_name: str, top_n: int = 10
) -> matplotlib.figure.Figure:
    """plot the distribution of child care facilities"""

    agg_col_name = "city_perc"
    temp_df = (
        data.query("IS_DUPLICATE == 'N'")
        .loc[:, [group_col_name]]
        .groupby(group_col_name)
        .apply(lambda x: x.count() * 100.0 / len(data.query("IS_DUPLICATE == 'N'")))
        .rename(columns={group_col_name: agg_col_name})
        .sort_values(by=agg_col_name, ascending=False)
    )

    fig, ax = plt.subplots()
    # temp_df[:top_n].plot.bar(ax=ax)
    try:
        sns.barplot(
            data=temp_df.reset_index()[:top_n],
            x=group_col_name,
            y=agg_col_name,
            color="#1f77b4",
            ax=ax,
        )
        label_axes(ax=ax, x_label="City", y_label="Percentage of Total Facilities")
    except:
        pass
    ax.tick_params(
        axis="x", labelrotation=45,
    )
    return fig


def plot_distribution_by_region(
    data: pd.DataFrame, top_n: int = 10
) -> matplotlib.figure.Figure:
    """plot the distribution of child care facilities"""

    agg_col_name = "city_perc"
    group_col_name = "region"
    cities_regions_map = C.CITIES_REGIONS_MAP
    temp_df = (
        data.query("IS_DUPLICATE == 'N'")
        .assign(
            region=data["CITY"]
            .str.lower()
            .apply(lambda x: cities_regions_map.get(x, "other"))
        )
        .loc[:, [group_col_name]]
        .groupby(group_col_name)
        .apply(lambda x: x.count() * 100.0 / len(data.query("IS_DUPLICATE == 'N'")))
        .rename(columns={group_col_name: agg_col_name})
        .sort_values(by=agg_col_name, ascending=False)
    )

    fig, ax = plt.subplots()
    try:
        sns.barplot(
            data=temp_df.reset_index()[:top_n],
            x=group_col_name,
            y=agg_col_name,
            color="#1f77b4",
            ax=ax,
        )
        # temp_df[:top_n].plot.bar(ax=ax)
    except:
        pass
    label_axes(ax=ax, x_label="Region", y_label="Percentage of Total Facilities")
    ax.tick_params(
        axis="x", labelrotation=45,
    )

    return fig


def plot_facility_map(data: pd.DataFrame):
    """create map pllot of facility locations."""

    lat = data["LATITUDE"].values
    lon = data["LONGITUDE"].values
    if data.empty:
        centroid = C.BC_CENTRE_LAT_LON
    else:
        centroid = dash_utils.get_latlon_centroid(lat=lat, lon=lon)
    m = folium.Map(location=centroid, tiles="OpenStreetMap", zoom_start=9)

    # data.reset_index(inplace=True)
    # n_rows = data.shape[0]
    # for i in range(n_rows):
    #     row = data[]
    for i, idx in enumerate(data.index):
        row = data[data.index == idx]

        name = row["NAME"].iloc[0]
        address = row["ADDRESS_1"].iloc[0]
        city = row["CITY"].iloc[0]
        phone = row["PHONE"].iloc[0]
        popup = folium.Popup(
            f"""
            name: {name} <br>
            address: {address} <br>
            phone: {phone}
            """
        )
        folium.CircleMarker(
            location=[row.LATITUDE, row.LONGITUDE], popup=popup, radius=2
        ).add_to(m)

    return m


def label_axes(ax, x_label, y_label, title=None):
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
