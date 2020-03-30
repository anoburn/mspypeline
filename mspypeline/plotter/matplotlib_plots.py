import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from adjustText import adjust_text


FIG_FORMAT = ".pdf"


def save_volcano_results(
        volcano_data: pd.DataFrame, unique_g1: pd.Series = None, unique_g2: pd.Series = None, g1: str = "group1",
        g2: str = "group2", col: str = "adjpval", intensity_label: str = "", save_path=os.getcwd(),
        show_suptitle: bool = True, fchange_threshold: float = 2, scatter_size: float = 10,
        n_labelled_proteins: int = 10
):
    """
    Saves multiple csv files and images containing the information of the volcano plot

    Parameters
    ----------
    volcano_data:
        DataFrame containing data for the volcano plot with columns logFC and column specified under col. THe index
        should be protein names or gene names
    unique_g1
        Series containing intensities of proteins or genes unique to group one
    unique_g2
        Series containing intensities of proteins or genes unique to group two
    g1
        Name of group one
    g2
        Name of group two
    col
        Column name containing p values
    intensity_label
        From which intensities were the fold changes calculated
    save_path
        path under which the results will be saved
    show_suptitle
        Should the figure title be shown
    fchange_threshold
        Minimum fold change threshold to be labelled significant
    scatter_size
        size of the points in the scatter plots
    n_labelled_proteins
        number of points that will be marked in th plot


    """
    plt.close("all")

    col_mapping = {"adjpval": "adjusted p value", "pval": "unadjusted p value"}

    # save all values
    volcano_data.to_csv(os.path.join(save_path,
                                  f"volcano_plot_data_{g1}_vs_{g2}_full_{col_mapping[col].replace(' ', '_')}.csv"))
    # save significant values
    volcano_data[volcano_data[col] < 0.05].to_csv(
        os.path.join(save_path,
                     f"volcano_plot_data_{g1}_vs_{g2}_significant_{col_mapping[col].replace(' ', '_')}.csv"))
    # save unique values
    if unique_g1 is not None:
        unique_g1.to_csv(os.path.join(save_path, f"volcano_plot_data_{g1}_vs_{g2}_unique_{g1}.csv"), header=True)
    if unique_g2 is not None:
        unique_g2.to_csv(os.path.join(save_path, f"volcano_plot_data_{g1}_vs_{g2}_unique_{g2}.csv"), header=True)

    def get_volcano_significances(fchange, pval, fchange_threshold):
        if pval > 0.05 or abs(fchange) < np.log2(fchange_threshold):
            return "ns"
        elif fchange >= 0:
            return "up"
        elif fchange < 0:
            return "down"
        else:
            raise ValueError("heisenbug")

    significance_to_color = {"ns": "gray", "up": "red", "down": "blue"}
    significance_to_label = {"ns": "non-significant", "up": f"upregulated in {g2}", "down": f"upregulated in {g1}"}

    # plot
    fig = plt.figure(figsize=(7, 7))

    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 8, 1])
    ax_unique_down = plt.subplot(gs[0])
    ax = plt.subplot(gs[1])
    ax_unique_up = plt.subplot(gs[2])

    # hide the spines between ax and ax2
    ax_unique_down.spines['right'].set_visible(False)
    ax_unique_up.spines['left'].set_visible(False)
    ax_unique_down.yaxis.tick_left()
    ax_unique_up.yaxis.tick_right()
    ax_unique_up.yaxis.set_label_position("right")
    # hide the xticks
    ax_unique_down.tick_params(which='both', bottom=False, labelbottom=False)
    ax_unique_up.tick_params(which='both', bottom=False, labelbottom=False)

    # non sign gray, left side significant blue, right side red
    significances_plot = [get_volcano_significances(log_fold_change, p_val, fchange_threshold)
                          for log_fold_change, p_val in zip(volcano_data["logFC"], volcano_data[col])]
    for regulation in significance_to_color:
        mask = [x == regulation for x in significances_plot]
        ax.scatter(volcano_data["logFC"][mask], -np.log10(volcano_data[col])[mask], s=scatter_size,
                   color=significance_to_color[regulation], label=f"{sum(mask)} {significance_to_label[regulation]}")
    # get axis bounds for vertical and horizontal lines
    ymin, ymax = ax.get_ybound()
    xmin, xmax = ax.get_xbound()
    m = max(abs(xmin), xmax)
    # center the plot around 0
    ax.set_xlim(left=-1 * m, right=m)
    # update the x bounds
    xmin, xmax = ax.get_xbound()
    # add line at significance threshold
    if any(volcano_data[col] < 0.05):
        x_offset = (np.log2(fchange_threshold) / xmax) / 2
        axline_kwargs = dict(linestyle="--", color="black", alpha=0.5, linewidth=1)
        ax.axhline(-np.log10(0.05), **axline_kwargs, xmin=0, xmax=0.5 - x_offset)
        ax.axhline(-np.log10(0.05), **axline_kwargs, xmin=0.5 + x_offset, xmax=1)

    # add lines for minimum fold change threshold
    y_percentage = (-np.log10(0.05) + abs(ymin)) / (ymax + abs(ymin))
    if fchange_threshold > 0:
        ax.axvline(-np.log2(fchange_threshold), **axline_kwargs, ymin=y_percentage, ymax=1)
        ax.axvline(np.log2(fchange_threshold), **axline_kwargs, ymin=y_percentage, ymax=1)
    # plot unique values with mean intensity at over maximum
    ax_unique_down.scatter([0] * len(unique_g1), unique_g1, s=scatter_size, color="dodgerblue",
                           label=f"{len(unique_g1)} unique in {g1}")
    ax_unique_up.scatter([0] * len(unique_g2), unique_g2, s=scatter_size, color="coral",
                         label=f"{len(unique_g2)} unique in {g2}")
    # adjust bounds for unique axis
    ymin_down, ymax_down = ax_unique_down.get_ybound()
    ymin_up, ymax_up = ax_unique_up.get_ybound()
    ax_unique_down.set_ylim(bottom=min(ymin_down, ymin_up), top=max(ymax_down, ymax_up))
    ax_unique_up.set_ylim(bottom=min(ymin_down, ymin_up), top=max(ymax_down, ymax_up))

    # figure stuff
    if show_suptitle:
        fig.suptitle(f"{g1} vs {g2}")
    ax.set_xlabel(f"{intensity_label} Fold Change")
    ax.set_ylabel(r"-$Log_{10}$" + f" {col_mapping[col]}")
    ax_unique_down.set_ylabel(intensity_label)
    ax_unique_up.set_ylabel(intensity_label)
    fig.legend(bbox_to_anchor=(1.02, 0.5), loc="center left", frameon=False)
    res_path = os.path.join(save_path, f"volcano_{g1}_{g2}_no_annotation_{col_mapping[col].replace(' ', '_')}" + FIG_FORMAT)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(res_path, dpi=200, bbox_inches="tight")
    significant_upregulated = volcano_data[
        (volcano_data["logFC"] > np.log2(fchange_threshold)) & (volcano_data[col] < 0.05)
    ].sort_values(by=[col], ascending=True).head(n_labelled_proteins)
    significant_downregulated = volcano_data[
        (volcano_data["logFC"] < -np.log2(fchange_threshold)) & (volcano_data[col] < 0.05)
    ].sort_values(by=[col], ascending=True).head(n_labelled_proteins)
    significant = pd.concat([significant_upregulated, significant_downregulated])
    texts = []
    for log_fold_change, p_val, gene_name in zip(significant["logFC"], significant[col], significant.index):
        texts.append(ax.text(log_fold_change, -np.log10(p_val), gene_name, ha="center", va="center", fontsize=8))
    adjust_text(texts, arrowprops=dict(width=0.15, headwidth=0, color='gray', alpha=0.6), ax=ax)
    res_path = os.path.join(save_path, f"volcano_{g1}_{g2}_annotation_{col_mapping[col].replace(' ', '_')}" + FIG_FORMAT)
    fig.savefig(res_path, dpi=200, bbox_inches="tight")
    # TODO scatter plot of significant genes