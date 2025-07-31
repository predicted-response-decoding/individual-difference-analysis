#!/usr/bin/env python
# coding: utf-8

# In[16]:


import numpy as np
from scipy.stats import f_oneway, sem, ttest_rel
from statsmodels.stats.multitest import fdrcorrection
import pandas as pd
import matplotlib.pyplot as plt

import mytask
from config import RCPARAMS_DEFAULT


get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams.update(RCPARAMS_DEFAULT)


# In[17]:


# Parameters
nnmodel = "VGG16"
nnmodel_layers = [
    "VGG16_pool1",
    "VGG16_pool2",
    "VGG16_pool3",
    "VGG16_pool4",
    "VGG16_pool5",
    "VGG16_fc6",
    "VGG16_fc7",
    "VGG16_fc8",
]
# nnmodel = "ResNet50"
# nnmodel_layers = [
#     "ResNet50_pool1",
#     "ResNet50_res2a",
#     "ResNet50_res2c",
#     "ResNet50_res3a",
#     "ResNet50_res3d",
#     "ResNet50_res4a",
#     "ResNet50_res4f",
#     "ResNet50_res5a",
#     "ResNet50_res5c",
#     "ResNet50_pool5",
#     "ResNet50_fc1000",
# ]
# nnmodel = "ViT_B_16"
# nnmodel_layers = [
#     "ViT_B_16_attn1",
#     "ViT_B_16_attn2",
#     "ViT_B_16_attn3",
#     "ViT_B_16_attn4",
#     "ViT_B_16_attn5",
#     "ViT_B_16_attn6",
#     "ViT_B_16_attn7",
#     "ViT_B_16_attn8",
#     "ViT_B_16_attn9",
#     "ViT_B_16_attn10",
#     "ViT_B_16_attn11",
#     "ViT_B_16_attn12",
# ]
# nnmodel = "SoundNet"
# nnmodel_layers = [
#     "SoundNet_conv1",
#     "SoundNet_conv2",
#     "SoundNet_conv3",
#     "SoundNet_conv4",
#     "SoundNet_conv5",
#     "SoundNet_conv6",
#     "SoundNet_conv7",
# ]
tasks = [
    mytask.SceneDescriptions,
    mytask.ImpressionRatings,
    mytask.AdEffectivenessIndices,
    mytask.AdPreferenceVotes,
    mytask.PreferenceRatings,
]
idr_metric = "spearmanr"


# In[21]:


n_layer = len(nnmodel_layers)
idrvals_full = []
for t in tasks[::-1]:
    for m in t.msets:
        fname_idr = f"./result/{nnmodel}/{m.__name__}/{t.__name__}/idr.csv"
        df_idr = pd.read_csv(fname_idr)
        idrvals_full.extend(df_idr.idr)

mean_idr = np.mean(idrvals_full)
sem_idr = sem(idrvals_full)
fig, ax = plt.subplots(figsize=(4, 3))
fig.subplots_adjust(wspace=0.04)
ax.fill_between(
    np.arange(-1, n_layer + 1),
    np.repeat(mean_idr - sem_idr, n_layer + 2),
    np.repeat(mean_idr + sem_idr, n_layer + 2),
    alpha=0.2, zorder=-10
)
ax.plot(np.arange(-1, n_layer + 1), np.repeat(mean_idr, n_layer + 2))

pvals = []
idrval_layers = []
for nnmodel_layer in nnmodel_layers:
    idrvals_layer = []
    for t in tasks[::-1]:
        for m in t.msets:
            fname_idr = f"./result/{nnmodel_layer}/{m.__name__}/{t.__name__}/idr.csv"
            df_idr = pd.read_csv(fname_idr)
            idrvals_layer.extend(df_idr.idr)

    _, pval = ttest_rel(idrvals_full, idrvals_layer)
    pvals.append(pval)
    idrval_layers.append(np.array(idrvals_layer))

"""
Let's check oneway anova result to check layer effect within a DNN
"""
anova_result = f_oneway(*idrval_layers)
print(f"{anova_result=}")

_, pvals = fdrcorrection(pvals)
mean_idr_layers = np.mean(idrval_layers, axis=1)
sem_idr_layers = sem(idrval_layers, axis=1)
upper_wiskers = mean_idr_layers + sem_idr_layers
ax.errorbar(np.arange(n_layer), mean_idr_layers, yerr=sem_idr_layers, c="k")
for i_layer, (upper_wisker, pval) in enumerate(zip(upper_wiskers, pvals)):
    if pval < 0.0001:
        ax.text(i_layer, upper_wisker, "***", ha="center")
        continue
    if pval < 0.001:
        ax.text(i_layer, upper_wisker, "**", ha="center")
        continue
    if pval < 0.05:
        ax.text(i_layer, upper_wisker, "*", ha="center")

ax.set_xlim(-0.5, n_layer - 0.5)
ax.set_xticks(np.arange(n_layer))
ax.set_xticklabels([nnmodel_layer.removeprefix(nnmodel + "_") for nnmodel_layer in nnmodel_layers], rotation=45, ha="right", rotation_mode="anchor")


# In[ ]:




