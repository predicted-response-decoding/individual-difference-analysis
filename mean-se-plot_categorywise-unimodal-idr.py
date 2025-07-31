#!/usr/bin/env python
# coding: utf-8

# # Scatter plotting of IDR

# In[6]:


import numpy as np
from scipy.stats import sem
from statsmodels.stats.multitest import fdrcorrection
import pandas as pd
import matplotlib.pyplot as plt

import mystim
import mytask
from config import RCPARAMS_DEFAULT


get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams.update(RCPARAMS_DEFAULT)


# In[13]:


# Parameters
nnmodels_multimodal = [
    "VGG16_SoundNet",
    "ResNet50_SoundNet",
    "ViT_B_16_SoundNet",
]
nnmodel_unimodal_dict = {
    "VGG16_SoundNet": ["VGG16", "SoundNet"],
    "ResNet50_SoundNet": ["ResNet50", "SoundNet"],
    "ViT_B_16_SoundNet": ["ViT_B_16", "SoundNet"],
}
colors_dict = {
    "VGG16_SoundNet": {mystim.WebAdMovieSet: "#f00", mystim.TVAdMovieSet: "#800"},
    "ResNet50_SoundNet": {mystim.WebAdMovieSet: "#0f0", mystim.TVAdMovieSet: "#080"},
    "ViT_B_16_SoundNet": {mystim.WebAdMovieSet: "#00f", mystim.TVAdMovieSet: "#008"},
}
tasks = [
    mytask.SceneDescriptions,
    mytask.ImpressionRatings,
    mytask.AdEffectivenessIndices,
    mytask.AdPreferenceVotes,
    mytask.PreferenceRatings,
]


# In[41]:


for t in tasks:
    print(t.__name__)
    x = 2
    fig, ax = plt.subplots(figsize=(x, x))
    ax.set_aspect("equal")
    ax.plot([-2, 2], [-2, 2], c="k", alpha=0.6, zorder=-100)
    minmax = []
    for m in t.msets:
        for nnmodel_multimodal in nnmodels_multimodal:
            for m in t.msets:
                fname_idr = f"./result/{nnmodel_multimodal}/{m.__name__}/{t.__name__}/idr.csv"
                df_idr = pd.read_csv(fname_idr)
                idrvals_multimodal = df_idr.idr

                idrvals_unimodal = []
                for nnmodel_unimodal in nnmodel_unimodal_dict[nnmodel_multimodal]:
                    fname_idr = f"./result/{nnmodel_unimodal}/{m.__name__}/{t.__name__}/idr.csv"
                    df_idr = pd.read_csv(fname_idr)
                    idrvals_unimodal.append(df_idr.idr)

                idrvals_unimodal = np.max(idrvals_unimodal, axis=0)
                mean_x = np.mean(idrvals_unimodal)
                mean_y = np.mean(idrvals_multimodal)
                if len(t.item_names) == 1:
                    ax.scatter(mean_x, mean_y, color=colors_dict[nnmodel_multimodal][m])
                    minmax.extend([mean_x, mean_y])
                else:
                    sem_x = sem(idrvals_unimodal)
                    sem_y = sem(idrvals_multimodal)
                    ax.errorbar(mean_x, mean_y, xerr=sem_x, yerr=sem_y, fmt="o", color=colors_dict[nnmodel_multimodal][m])
                    minmax.extend([mean_x + sem_x, mean_x - sem_x, mean_y + sem_y, mean_y - sem_y])

    minval = min(minmax)
    maxval = max(minmax)
    span = maxval - minval
    upper_lim = maxval + span * 0.05
    lower_lim = minval - span * 0.05
    ax.set_xlim([lower_lim, upper_lim])
    ax.set_ylim([lower_lim, upper_lim])
    plt.show()


# In[ ]:




