import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pingouin import qqplot
from scipy.stats import shapiro
from math import ceil


def multi_boxplot(data: pd.DataFrame, x: str):

    analysis_cols = data.columns.drop(x)
    fig, axes = plt.subplots(nrows=1, ncols=len(analysis_cols), figsize=(5 * len(analysis_cols), 5))
    
    for index, col in enumerate(analysis_cols):
        sns.boxplot(x=x, y=col, data=data, hue=x, ax=axes[index])
        axes[index].tick_params(axis='x', labelsize=14)
        axes[index].set_xlabel(f"{x}", fontsize=14)
        axes[index].set_ylabel(f"{col}", fontsize=14)
        plt.tight_layout()

def is_norm(data: pd.DataFrame, by: str = None, ncol_fig: int = 4):

    categories = data[by].unique() if isinstance(by, str) else ['']
    nrow_fig = ceil(len(categories)*(len(data.columns) -1)/ncol_fig) if not len(categories)==1 else ceil(len(data.columns)/ncol_fig)
    fig, axes = plt.subplots(nrows=nrow_fig, ncols=ncol_fig, figsize=(5*ncol_fig, 5*nrow_fig))
    axes = axes.flatten()    
    counter = 0

    for name in categories:

        plot_data = data.query(f"{by} == '{name}'").drop(columns=[by]) if len(categories) > 1 else data
        ncol_plot_data: int = len(plot_data.columns)

        for index, col in enumerate(plot_data.columns):
            stat, pval = shapiro(plot_data[col])
            shapiro_info: str = f"    Shapiro-Wilk\n" +\
                                f"Statistic:  {stat:.5f}\n"+\
                                f"P-Value:    {pval:.5f}\n"
            axes_index = index + counter*ncol_plot_data
            qqplot(plot_data[col], ax=axes[axes_index])
            axes[axes_index].set(xlabel='', ylabel='')
            axes[axes_index].set_title(f'{name} {col}', fontsize=16)
            axes[axes_index].text(0.02, 0.98, shapiro_info, transform=axes[axes_index].transAxes,  ha='left', va='top')
        
        counter += 1

    [fig.delaxes(ax) for ax in axes[-ncol_fig:] if not ax.has_data()]
    fig.suptitle(f"Quantile-Quantile plots {'by '+ by if counter != 1 else ''}", fontsize=32)
    fig.supxlabel("Theoretical quantiles", fontsize=24)
    fig.supylabel("Ordered quantiles", fontsize=24)
    plt.subplots_adjust(top=.93, left=.06, bottom=0.05)
