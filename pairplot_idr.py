#!/usr/bin/env python
# coding: utf-8

# # Pair plotting of IDR
# 
# Please execute `python calc_idr_pval.py -m` beforehand to calculate permutation test P-values, which takes time.

# In[1]:


from itertools import combinations
import numpy as np
from scipy.stats import f_oneway, ttest_rel
from statsmodels.stats.multitest import fdrcorrection
import pandas as pd
import matplotlib.pyplot as plt

import mytask
from config import RCPARAMS_DEFAULT
from util import pval_order, binrange_bins0_1


get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams.update(RCPARAMS_DEFAULT)


# In[2]:


# Parameters
nnmodels = [
    "VGG16_SoundNet",
    "ResNet50_SoundNet",
    "ViT_B_16_SoundNet",
]
tasks = [
    mytask.SceneDescriptions,
    mytask.ImpressionRatings,
    mytask.AdEffectivenessIndices,
    mytask.AdPreferenceVotes,
    mytask.PreferenceRatings,
]
ticklabels = [0, 0.2, 0.4, 0.6, 0.8]


# In[12]:


n_nnmodel = len(nnmodels)
fig, axes = plt.subplots(n_nnmodel, n_nnmodel, figsize=(3 * n_nnmodel, 3 * n_nnmodel))
uppper_triangle_mask = np.array([*combinations(range(n_nnmodel), 2)]).T
for ax in axes[*uppper_triangle_mask]: ax.set_visible(False)
lower_triangle_mask = uppper_triangle_mask[::-1]
idrvals_nnmodels = []
pvals_nnmodels = []
for nnmodel in nnmodels:
    idrvals = []
    pvals = []
    for t in tasks[::-1]:
        for m in t.msets:
            fname_idr = f"./result/{nnmodel}/{m.__name__}/{t.__name__}/idr.csv"
            df_idr = pd.read_csv(fname_idr)
            idrvals.extend(df_idr.idr)
            pvals.extend(df_idr.pval)

    idrvals_nnmodels.append(np.array(idrvals))
    _, pvals = fdrcorrection(pvals)
    pvals_nnmodels.append(pvals)

"""
Let's check oneway anova result
"""
anova_result = f_oneway(*idrvals_nnmodels)
print(f"{anova_result=}")

"""
Histgram plots
"""
# Speculate binrange and number of bin from the results of all DNN sets
binrange, bins = binrange_bins0_1(np.array(idrvals_nnmodels).flatten())
for i_nnmodel, (idrvals, pvals) in enumerate(zip(idrvals_nnmodels, pvals_nnmodels)):
    idrvals_signif_hist = []
    idrvals_nonsignif_hist = []
    colors_signif_hist = []
    colors_nonsignif_hist = []
    for t in tasks[::-1]:
        n_labels = len(t.item_names) * len(t.msets)
        idrval_labels = idrvals[:n_labels]
        idrvals = idrvals[n_labels:]
        pval_labels = pvals[:n_labels]
        pvals = pvals[n_labels:]
        idrvals_signif_hist.append(idrval_labels[pval_labels < 0.05])
        idrvals_nonsignif_hist.append(idrval_labels[0.05 <= pval_labels])
        colors_signif_hist.append(t.color)
        colors_nonsignif_hist.append(t.color + "60")

    idrvals_hist = idrvals_signif_hist + idrvals_nonsignif_hist
    colors_hist = colors_signif_hist + colors_nonsignif_hist
    ax = axes[i_nnmodel, i_nnmodel]
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlim(binrange[0] - 0.05, binrange[1] + 0.05)
    ax.set_xticks(ticklabels)
    ax.set_xticklabels(ticklabels)
    ax.hist(idrvals_hist, bins=bins, range=binrange, stacked=True, color=colors_hist, edgecolor="k")

"""
Scatter plots
"""
# Get FDR corrected p-value
pvals_wilcoxon = []
for idrvals_i, idrvals_j in combinations(idrvals_nnmodels, 2):
    _, pval = ttest_rel(idrvals_i, idrvals_j)
    pvals_wilcoxon.append(pval)

_, pvals_wilcoxon = fdrcorrection(pvals_wilcoxon)
colors_scatter = [t.color for t in tasks[::-1] for _ in range(len(t.item_names) * len(t.msets))]
for i_comb, (ax, ((i_nnmodel, idrvals_i), (j_nnmodel, idrvals_j))) in enumerate(zip(axes[*lower_triangle_mask], combinations(enumerate(idrvals_nnmodels), 2))):
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlim(binrange[0] - 0.05, binrange[1] + 0.05)
    ax.set_ylim(binrange[0] - 0.05, binrange[1] + 0.05)
    ax.set_xticks(ticklabels)
    ax.set_xticklabels(ticklabels)
    ax.set_yticks(ticklabels)
    ax.set_yticklabels(ticklabels)
    ax.scatter(idrvals_i, idrvals_j, c=colors_scatter, lw=0.4)
    ax.plot([-2, 2], [-2, 2], c="k", alpha=0.6, zorder=-100)
    ax.text(0.98, 0.02, pval_order(pvals_wilcoxon[i_comb]), va="bottom", ha="right", transform=ax.transAxes)


# In[11]:


fig, ax = plt.subplots(figsize=(0, 0))
fig.patch.set_alpha(0)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
ax.tick_params("x", length=0, which="major")
ax.tick_params("y", length=0, which="major")
ax.scatter([], [], color="w", edgecolors="w", label=" ")
for task in tasks:
    ax.hist([], color=task.color, lw=0.4, edgecolor="k", label="  ")

ax.scatter([], [], color="w", edgecolors="w", label=" ")
for task in tasks:
    ax.hist([], color=task.color + "60", lw=0.4, edgecolor="k", label=" ")

ax.scatter([], [], color="w", edgecolors="w", label=" ")
for task in tasks:
    ax.scatter([], [], lw=0.4, color=task.color, edgecolor="k", label=f"{task.title}")

ax.legend(ncol=3, handletextpad=0, columnspacing=0, borderpad=1.2)

