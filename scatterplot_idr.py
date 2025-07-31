#!/usr/bin/env python
# coding: utf-8

# # Scatter plotting of IDR
# 
# Please execute `python calc_idr_pval.py -m` beforehand to calculate permutation test P-values, which takes time.

# In[ ]:


import os
from statsmodels.stats.multitest import fdrcorrection
import pandas as pd
import matplotlib.pyplot as plt

from calc_idr import calc_idr
import mystim
import mytask
from config import get_manual_rating, get_meas_resp_dec, get_pred_resp_dec, RCPARAMS_DEFAULT
from util import pval_order


get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams.update(RCPARAMS_DEFAULT)


# In[4]:


# Parameters
nnmodels = [
    # Multimodal models
    "VGG16_SoundNet",
    "ResNet50_SoundNet",
    "ViT_B_16_SoundNet",
    # Unimodal models
    "VGG16",
    "ResNet50",
    "ViT_B_16",
    "SoundNet",
    # Single layer models
    "VGG16_pool1",
    "VGG16_pool2",
    "VGG16_pool3",
    "VGG16_pool4",
    "VGG16_pool5",
    "VGG16_fc6",
    "VGG16_fc7",
    "VGG16_fc8",
    "ResNet50_pool1",
    "ResNet50_res2a",
    "ResNet50_res2c",
    "ResNet50_res3a",
    "ResNet50_res3d",
    "ResNet50_res4a",
    "ResNet50_res4f",
    "ResNet50_res5a",
    "ResNet50_res5c",
    "ResNet50_pool5",
    "ResNet50_fc1000",
    "ViT_B_16_attn1",
    "ViT_B_16_attn2",
    "ViT_B_16_attn3",
    "ViT_B_16_attn4",
    "ViT_B_16_attn5",
    "ViT_B_16_attn6",
    "ViT_B_16_attn7",
    "ViT_B_16_attn8",
    "ViT_B_16_attn9",
    "ViT_B_16_attn10",
    "ViT_B_16_attn11",
    "ViT_B_16_attn12",
    "SoundNet_conv1",
    "SoundNet_conv2",
    "SoundNet_conv3",
    "SoundNet_conv4",
    "SoundNet_conv5",
    "SoundNet_conv6",
    "SoundNet_conv7",
]
tasks = [
    mytask.SceneDescriptions,
    mytask.ImpressionRatings,
    mytask.AdEffectivenessIndices,
    mytask.AdPreferenceVotes,
    mytask.PreferenceRatings,
]


# In[5]:


for nnmodel in nnmodels:
    pvals = []
    for t in tasks:
        for m in t.msets:
            subjs = t.get_subjects(mset=m)
            pstims_meas = [
                get_meas_resp_dec(mset=m.__name__, task=t.__name__, subj=subj)
                for subj in subjs
            ]
            pstims_pred = [
                get_pred_resp_dec(mset=m.__name__, task=t.__name__, nnmodel=nnmodel, subj=subj)
                for subj in subjs
            ]
            idrval_labels, a_labels, b_labels = calc_idr(pstims_meas, pstims_pred, is_vector=t.is_vector)
            fname_idr = f"./result/{nnmodel}/{m.__name__}/{t.__name__}/idr.csv"
            df_idr = pd.read_csv(fname_idr)
            pvals.extend(df_idr.pval)

    _, pvals = fdrcorrection(pvals)
    for t in tasks:
        for m in t.msets:
            subjs = t.get_subjects(mset=m)
            pval_labels = pvals[:len(t.item_names)]
            pvals = pvals[len(t.item_names):]
            pstims_meas = [
                get_meas_resp_dec(mset=m.__name__, task=t.__name__, subj=subj)
                for subj in subjs
            ]
            pstims_pred = [
                get_pred_resp_dec(mset=m.__name__, task=t.__name__, nnmodel=nnmodel, subj=subj)
                for subj in subjs
            ]
            idrval_labels, a_labels, b_labels = calc_idr(pstims_meas, pstims_pred, is_vector=t.is_vector)
            for i_label, (idrval, item_name, pval, a, b) in enumerate(zip(idrval_labels, t.item_names, pval_labels, a_labels, b_labels)):
                fig, ax = plt.subplots(figsize=(3, 3))
                ax.set_title(f"Movie set: {m.__name__}\nCategory: {t.__name__}\nLabel: {item_name}")
                ax.set_xlabel(f"Pair dissimilarity\nof measured-response decoding")
                ax.set_ylabel(f"Pair dissimilarity\nof predicted-response decoding")
                ax.scatter(a, b, s=8)
                ax.text(0.02, 0.98, f"IDR = {idrval:.3f}\n{pval_order(pval)}", ha="left", va="top", transform=ax.transAxes)
                fname_fig = f"./result/{nnmodel}/{m.__name__}/{t.__name__}/idr{i_label:02}.jpg"
                print(f"Saving {fname_fig}")
                os.makedirs(os.path.dirname(fname_fig), exist_ok=True)
                fig.savefig(fname_fig, dpi=200, bbox_inches="tight")
                plt.close(fig)


# ## Behavioral IDR 
# 
# FDR correction is done along DNN sets.

# In[6]:


nnmodels = [
    "VGG16_SoundNet",
    "ResNet50_SoundNet",
    "ViT_B_16_SoundNet",
]
msets = [mystim.TVAdMovieSet]
tasks = [mytask.PreferenceRatings]


# In[7]:


for t in tasks:
    for m in t.msets:
        pvals = []
        for nnmodel in nnmodels:
            fname_idr = f"./result/{nnmodel}/{m.__name__}/{t.__name__}/behavioral-idr.csv"
            df_idr = pd.read_csv(fname_idr)
            pvals.extend(df_idr.pval)

        _, pvals = fdrcorrection(pvals)
        for nnmodel in nnmodels:
            subjs = t.get_subjects(mset=m)
            pval_labels = pvals[:len(t.item_names)]
            pvals = pvals[len(t.item_names):]
            pstims_behavioral = [
                get_manual_rating(mset=m.__name__, task=t.__name__, subj=subj)
                for subj in subjs
            ]
            pstims_pred = [
                get_pred_resp_dec(mset=m.__name__, task=t.__name__, nnmodel=nnmodel, subj=subj)
                for subj in subjs
            ]
            idrval_labels, a_labels, b_labels = calc_idr(pstims_behavioral, pstims_pred, is_vector=t.is_vector)
            for i_label, (idrval, item_name, pval, a, b) in enumerate(zip(idrval_labels, t.item_names, pval_labels, a_labels, b_labels)):
                fig, ax = plt.subplots(figsize=(3, 3))
                ax.set_title(f"Movie set: {m.__name__}\nCategory: {t.__name__}\nLabel: {item_name}")
                ax.scatter(a, b, s=8)
                ax.text(0.02, 0.98, f"IDR = {idrval:.3f}\n{pval_order(pval)}", ha="left", va="top", transform=ax.transAxes)
                ax.set_xlabel(f"Pair dissimilarity\nof manual ratings")
                ax.set_ylabel(f"Pair dissimilarity\nof predicted-response decoding")
                fname_fig = f"./result/{nnmodel}/{m.__name__}/{t.__name__}/behavioral-idr{i_label:02}.jpg"
                print(f"Saving {fname_fig}")
                os.makedirs(os.path.dirname(fname_fig), exist_ok=True)
                fig.savefig(fname_fig, dpi=200, bbox_inches="tight")
                plt.close(fig)


# In[ ]:




