#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from statsmodels.stats.multitest import fdrcorrection
import matplotlib.pyplot as plt

from calc_idr import calc_idr
from manteltest import manteltest
import movieset
import task
from config import get_manual_rating, get_meas_resp_dec, get_pred_resp_dec, RC_PARAMS_DEFAULT
from util import pval_order


get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams.update(RC_PARAMS_DEFAULT)


# In[ ]:


nnmodels = [
    "VGG16_SoundNet",
    "ResNet50_SoundNet",
    "ViT_B_16_SoundNet",
    "VGG16",
    "ResNet50",
    "ViT_B_16",
    "SoundNet",
]
msets = [movieset.WebAdMovieSet, movieset.TVAdMovieSet]
tasks = [
    task.SceneDescriptions,
    task.ImpressionRatings,
    task.AdEffectivenessIndices,
    task.AdPreferenceVotes,
    task.PreferenceRatings,
]


# In[ ]:


for nnmodel in nnmodels:
    pvals = []
    for m in msets:
        for t in tasks:
            if m not in t.colors: continue
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
            pval_labels = manteltest(a_labels, b_labels)
            pvals.extend(pval_labels)

    _, pvals = fdrcorrection(pvals)
    for m in msets:
        for t in tasks:
            if m not in t.colors: continue
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
                ax.scatter(a, b, s=8)
                ax.text(0.02, 0.98, f"IDR = {idrval:.3f}\n{pval_order(pval)}", ha="left", va="top", fontsize=8, transform=ax.transAxes)
                fname_fig = f"./result/{nnmodel}/{m.__name__}/{t.__name__}/idr{i_label:02}.jpg"
                print(f"Saving {fname_fig}")
                os.makedirs(os.path.dirname(fname_fig), exist_ok=True)
                fig.savefig(fname_fig, dpi=200, bbox_inches="tight")
                plt.close(fig)


# ## Behavioral IDR

# In[ ]:


nnmodels = ["VGG16_SoundNet", "ResNet50_SoundNet", "ViT_B_16_SoundNet"]
msets = [movieset.TVAdMovieSet]
tasks = [task.PreferenceRatings]


# In[ ]:


for m in msets:
    for t in tasks:
        if m not in t.colors: continue
        pvals = []
        for nnmodel in nnmodels:
            subjs = t.get_subjects(mset=m)
            # NOTE: Referenced Pair dissimilarity matrix was changed into subjective reports
            pstims_meas = [
                get_manual_rating(mset=m.__name__, task=t.__name__, subj=subj)
                for subj in subjs
            ]
            pstims_pred = [
                get_pred_resp_dec(mset=m.__name__, task=t.__name__, nnmodel=nnmodel, subj=subj)
                for subj in subjs
            ]
            idrval_labels, a_labels, b_labels = calc_idr(pstims_meas, pstims_pred, is_vector=t.is_vector)
            pval_labels = manteltest(a_labels, b_labels)
            pvals.extend(pval_labels)

        _, pvals = fdrcorrection(pvals)
        for nnmodel in nnmodels:
            if m not in t.colors: continue
            subjs = t.get_subjects(mset=m)
            pval_labels = pvals[:len(t.item_names)]
            pvals = pvals[len(t.item_names):]
            pstims_meas = [
                get_manual_rating(mset=m.__name__, task=t.__name__, subj=subj)
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
                ax.scatter(a, b, s=8)
                ax.text(0.02, 0.98, f"IDR = {idrval:.3f}\n{pval_order(pval)}", ha="left", va="top", fontsize=8, transform=ax.transAxes)
                fname_fig = f"./result/{nnmodel}/{m.__name__}/{t.__name__}/behavioral-idr{i_label:02}.jpg"
                print(f"Saving {fname_fig}")
                os.makedirs(os.path.dirname(fname_fig), exist_ok=True)
                fig.savefig(fname_fig, dpi=200, bbox_inches="tight")
                plt.close(fig)


# In[ ]:




