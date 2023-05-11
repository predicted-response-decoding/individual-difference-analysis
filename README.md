# Analysis for individual differences in brain decodings

This program show individual-difference reflection (IDR) of predictted-response decoding for measured-response decoding.

For detail, please see the paper https://doi.org/10.1101/2022.05.16.492029

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
│   └── subject_data.scv
├── (result)
│   ├── TVAdMovieSet
│   └── WebAdMovieSet
├── config.py
├── labels.py
├── pair_dist.py
├── plot.ipynb
├── plot.py
├── subject_selector.py
└── util.py
```

## Data

There are two different sets of movies, with multiple categories.

We provide predicted decodings by measured and predicted voxel response.

1. Web ad movie set
   - Scene descriptions (data/WebAdMovieSet/{subject}/SceneDescription/, 40 subjects)
   - Impression ratings (data/WebAdMovieSet/{subject}/ImpressionRatings/, 40 subjects)
   - Ad effectiveness indices (data/WebAdMovieSet/{subject}/AdEffectivenessIndices/, 40 subjects)
1. TV ad movie set
   - Scene descriptions (data/TVAdMovieSet/{subject}/SceneDescription/, 28 subjects)
   - Impression ratings (data/TVAdMovieSet/{subject}/ImpressionRatings/, 28 subjects)
   - Ad preference votes (data/TVAdMovieSet/{subject}/AdPreferenceVotes/, 28 subjects)
   - Subjective preference ratings (data/TVAdMovieSet/{subject}/PreferenceRatings/, 14 subjects)

**※In subjective preference ratings, IDR is also calculated for manual ratings, which were annotated from fMRI subjects.**

## How to use

Execute plot.py.

| Option | Description                                               | Choice         |
| ------ | --------------------------------------------------------- | -------------- |
| -m     | Movie set as stimlus                                      | web tv         |
| -t     | Task decoded by predicted- and measured-response decoding | sd ir ae ap pr |

You can execute same program with plot.ipynb.

Code is formatted by Black Formatter in Visual Studio Code.
