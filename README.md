# Analysis for individual differences in mental information decoded from predicted voxel responses

This program performs calculation of individual-difference reflection (IDR) of predictted-response decoding.

```
.
├── data
│   ├── TVAdMovieSet
│   │   └── {subject}
│   │       ├── SceneDescription
│   │       ├── ImpressionRatings
│   │       └── AdEffectivenessIndices
│   ├── WebAdMovieSet
│   │   └── {subject}
│   │       ├── SceneDescription
│   │       ├── ImpressionRatings
│   │       ├── AdPreferenceVotes
│   │       └── PreferenceRatings
│   └── subjects.scv
├── (result)
    └── {DNN set}
        ├── TVAdMovieSet
        │   ├── SceneDescription
        │   ├── ImpressionRatings
        │   └── AdEffectivenessIndices
        └── WebAdMovieSet
            ├── SceneDescription
            ├── ImpressionRatings
            ├── AdPreferenceVotes
            └── PreferenceRatings
```

## Data

There are two different sets of movies, with multiple categories of labels.

We provide results decoded from measured and predicted voxel responses.

1. Web ad movie set
   - Scene descriptions (data/WebAdMovieSet/{subject}/SceneDescription/; 40 subjects)
   - Impression ratings (data/WebAdMovieSet/{subject}/ImpressionRatings/; 40 subjects)
   - Ad effectiveness indices (data/WebAdMovieSet/{subject}/AdEffectivenessIndices/; 40 subjects)
1. TV ad movie set
   - Scene descriptions (data/TVAdMovieSet/{subject}/SceneDescription/; 28 subjects)
   - Impression ratings (data/TVAdMovieSet/{subject}/ImpressionRatings/; 28 subjects)
   - Ad preference votes (data/TVAdMovieSet/{subject}/AdPreferenceVotes/; 28 subjects)
   - Subjective preference ratings (data/TVAdMovieSet/{subject}/PreferenceRatings/; 14 subjects)

**※Subjective preference ratings can also be used for the analysis of individidual differences of behavior.**

## Usage

1. Please execute `calc_idr_pval.py` first for calculating permutation test, which takes time.

```bash
python calc_idr_pval.py -m
```

2. Now you can execute all ipynb files (or py files with the same names), each of which corresponds to main result in the following paper [Kawahata et al. 2022 bioRxiv].

Kawahata, K., Wang, J., Blanc, A., Maeda, N., Nishimoto, S., & Nishida, S. (2022). Decoding individual differences in mental information from human brain response predicted by convolutional neural networks. bioRxiv, 2022-05. https://doi.org/10.1101/2022.05.16.492029

The resultant figures are stored in `result/` directory.
