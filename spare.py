#num_fig: int = counter*(len(data.columns)-1) if counter !=1 else len(data.columns)
#[axes[i].set_xticklabels([]) for i in range(num_fig - ncol_fig)]
#[axes[i].set_yticklabels([]) for i in range(num_fig) if i % ncol_fig]
#[ax.tick_params(axis='x', labelsize=14) for ax in axes]