import pandas as pd

import matplotlib.pyplot as plt
from seaborn import boxplot
from pingouin import qqplot
from scipy.stats import shapiro
from math import ceil

def pretty_df(df_data: pd.DataFrame) -> pd.DataFrame:
    df_data.columns = [col_name.replace('_',' ').title() for col_name in df_data.columns] 
    df_data = df_data.apply(lambda col: col.apply(lambda x: x.replace('_',' ').title()) if col.dtype == 'object' else col)
    return df_data    

def multi_boxplot(df_data: pd.DataFrame, x: str) -> None:

    analysis_cols = df_data.columns.drop(x)
    fig, axes = plt.subplots(nrows=1, ncols=len(analysis_cols), figsize=(5*len(analysis_cols), 5))
    
    for index, col in enumerate(analysis_cols):
        boxplot(x=x, y=col, data=df_data, hue=x, ax=axes[index])
        axes[index].tick_params(axis='x', labelsize=14)
        axes[index].set_xlabel(f"{x}", fontsize=14)
        axes[index].set_ylabel(f"{col}", fontsize=14)
        plt.tight_layout()

def is_norm(df_data: pd.DataFrame, by: str = None, ncol_fig: int = 4, main_label: bool = True) -> None:

    categories = df_data[by].unique() if isinstance(by, str) else ['']
    nrow_fig = ceil(len(categories)*(len(df_data.columns) -1)/ncol_fig) if not len(categories)==1 else ceil(len(df_data.columns)/ncol_fig) 
    fig, axes = plt.subplots(nrows=nrow_fig, ncols=ncol_fig, figsize=(5*ncol_fig, 5*nrow_fig), constrained_layout=True)
    axes = axes.flatten()    
    counter = 0

    for counter, name in enumerate(categories):

        plot_data = df_data.query(f"{by} == '{name}'").drop(columns=[by]) if len(categories) > 1 else df_data
        ncol_plot_data: int = len(plot_data.columns)

        for index, col in enumerate(plot_data.columns):
            stat, pval = shapiro(plot_data[col])
            shapiro_info: str = f"    Shapiro-Wilk\n" +\
                                f"Statistic:  {stat:.5f}\n"+\
                                f"P-Value:    {pval:.5f}\n"
            axes_index = index + counter*ncol_plot_data
            qqplot(plot_data[col], ax=axes[axes_index])
            axes[axes_index].set_title(f'{name} {col}', fontsize=16)
            axes[axes_index].text(0.02, 0.98, shapiro_info, transform=axes[axes_index].transAxes,  ha='left', va='top')
        
    [fig.delaxes(ax) for ax in axes[-ncol_fig:] if not ax.has_data()]
    print(counter)
    if main_label:
        fig.suptitle(f"Quantile-Quantile plots {'by '+ by if counter != 0 else ''}", fontsize=28)
        fig.supxlabel("Theoretical quantiles", fontsize=24)
        fig.supylabel("Ordered quantiles", fontsize=24)
        [ax.set(xlabel='', ylabel='') for ax in axes]
    else:
        [ax.set_title("Q-Q plot for " + ax.get_title(), fontsize=14) for ax in axes]
    

