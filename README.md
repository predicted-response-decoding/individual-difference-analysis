# Analysis for individual differences in mental information decoded from predicted voxel responses

This program show individual-difference reflection (IDR) of predictted-response decoding for measured-response decoding.

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
│   └── {DNN set}
│       ├── TVAdMovieSet
│       │   ├── SceneDescription
│       │   ├── ImpressionRatings
│       │   └── AdEffectivenessIndices
│       └── WebAdMovieSet
│           ├── SceneDescription
│           ├── ImpressionRatings
│           ├── AdPreferenceVotes
│           └── PreferenceRatings
├── config.py
├── task.py
├── scatterplot-idr.ipynb
├── scatterplot-idr.py
└── util.py
```

## Data

There are two different sets of movies, with multiple categories.

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

Please execute `scatterplot-idr.py` or `scatterplot-idr.ipynb`.

The resultant figures are stored in `result/` directory.
