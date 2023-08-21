import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from src import processing as proc


space_n_facility_col_names = ["total_spaces", "total_facilities"]

def plot_fac_trend(data:pd.DataFrame, y_col):
    """plots the time series of the facility counts"""

    fig, ax = plt.subplots(1,1)
    sns.lineplot(data=data, x='date', y=y_col, ls='-', hue='region', ax=ax)

    ax.legend()
    ax.grid()

    return fig

def plot_fac_delta(data:pd.DataFrame, y_col, **kwargs):
    """plots the time series of the facility changes from period to period."""

    # col_delta = proc.get_col_delta(data, y_col)
    # date
    
    regions = data['region'].unique()
    fig, ax = plt.subplots(1,1)
    delta_col_name = y_col+"_change"
    for region in regions[:]:

        region_df = data[data['region'] == region]
        region_df[delta_col_name] = region_df[y_col].diff()

        region_df = region_df.resample('Y', on='date',label='left', closed='right').sum()
        # ax.plot_date(data=region_df, x='date', y=y_col, ls='-', label=region)
        sns.lineplot(data=region_df, x='date', y=delta_col_name, ls='-', label=region)

    ax.legend()
    ax.grid()

    return fig