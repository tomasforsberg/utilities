import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import general_tools as u_gt

def apply_potential_transformation(df, col, transformations):
    transformation = None
    # Check to see if this is a "apply to all except..." 
    # or "apply to these..." case
    if transformations.get('type', 'standard') == 'exception':
        # There is a list of columns to be excluded,
        # and a transformation that should be applied to all other
        if col not in transformations['exceptions']:
            transformation = transformations['transformation']
    else:
        # There are column name keys with a transformation value
        # associated with them, for the ones that should be transformed
        if col in transformations:
            transformation = transformations[col]

    if transformation == 'log':
        return u_gt.cap_and_log(df[col])
    elif transformation is None:
        return df[col]
    else:
        print('No support for transformation', transformation)
        return df[col]

# Two alternatives for transformations apart from not passing it at all:
# transformations = {
#     'type': 'exception',
#     'transformation': 'log',
#     'exceptions': ['forecast_price_energy_p1', 'forecast_price_energy_p2', 'forecast_price_pow_p1']
# }
# transformations = {
#     'forecast_base_bill_ele': 'log',
#     'forecast_bill_12m': 'log'
# }
def distplot_grid(df, cols, subplot_cols=4, figsize_multiplier=3, transformations=None):
    subplot_cols = subplot_cols
    subplot_rows = int(np.ceil(len(cols) / subplot_cols))

    default_fig_width, default_fig_height = plt.rcParams.get('figure.figsize')
    new_figsize = (figsize_multiplier * default_fig_width, default_fig_height * subplot_rows)
    fig, axes = plt.subplots(subplot_rows, subplot_cols, figsize=new_figsize)
    fig.tight_layout(pad=3)
    for i in range(len(cols)):
        col = cols[i]
        
        if sum(~df[col].isna()) == 0:
            print('Alert:', col, 'is completely empty')
            continue
        
        series_to_plot = df[col]
        if transformations is not None:
            series_to_plot = apply_potential_transformation(df, col, transformations)

        # Calculate inter quartile range, and use this in the outlier threshold
        non_null_series = df[~pd.isna(df[col])][col]
        quartile_25 = np.quantile(non_null_series, 0.25)
        quartile_75 = np.quantile(non_null_series, 0.75)
        IQR = quartile_75 - quartile_25
        lower_threshold = quartile_25 - IQR * 1.5
        upper_threshold = quartile_75 + IQR * 1.5

        # Apply threshold filter to calculate outliers
        number_of_outliers = len(non_null_series[
            (non_null_series < lower_threshold) | 
            (non_null_series > upper_threshold)
            ])
        outlier_percentage = 100 * (number_of_outliers / len(non_null_series))

        subplot_row = i // subplot_cols
        subplot_col = i % subplot_cols
        subplot_index = (subplot_row, subplot_col)
        if subplot_rows == 1:
            subplot_index = subplot_col
        
        axes[subplot_index].set_title('#: ' + str(number_of_outliers) + 
                                    ' / ' + str(len(non_null_series)) +
                                    ' -> {:.2f} %'.format(outlier_percentage))
        sns.distplot(series_to_plot, ax=axes[subplot_index])

def apply_transformations(df, cols, transformations):
    return df[cols].apply(lambda col: apply_potential_transformation(df, col.name, transformations))

def quantile_describe(df):
    return df.describe().T.drop(columns=['count', 'mean', 'std'])
