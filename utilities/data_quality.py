import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
import general_tools as u_gt


def distplot_grid(df, cols, subplot_cols=4, figsize_multiplier=3):
    subplot_cols = subplot_cols
    subplot_rows = int(np.ceil(len(cols) / subplot_cols))

    default_fig_width, default_fig_height = plt.rcParams.get('figure.figsize')
    new_figsize = (figsize_multiplier * default_fig_width, default_fig_height * subplot_rows)
    _, axes = plt.subplots(subplot_rows, subplot_cols, figsize=new_figsize)
    for i in range(len(cols)):
        col = cols[i]
        
        if sum(~df[col].isna()) == 0:
            print('Alert:', col, 'is completely empty')
            continue
        
        subplot_row = i // subplot_cols
        subplot_col = i % subplot_cols
        subplot_index = (subplot_row, subplot_col)
        if subplot_rows == 1:
            subplot_index = subplot_col
        sns.distplot(u_gt.cap_and_log(df[col]), ax=axes[subplot_index])
