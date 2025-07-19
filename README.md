# Analysis for individual differences in mental information decoded from predicted voxel response

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
│   ├── TVAdMovieSet
│   └── WebAdMovieSet
├── config.py
├── task.py
├── plot.ipynb
└── util.py
```

## Data

There are two different sets of movies, with multiple categories.

We provide predicted decodings by measured and predicted voxel response.

1. Web ad movie set
   - Scene descriptions (data/WebAdMovieSet/{subject}/SceneDescription/; 40 subjects)
   - Impression ratings (data/WebAdMovieSet/{subject}/ImpressionRatings/; 40 subjects)
   - Ad effectiveness indices (data/WebAdMovieSet/{subject}/AdEffectivenessIndices/; 40 subjects)
1. TV ad movie set
   - Scene descriptions (data/TVAdMovieSet/{subject}/SceneDescription/; 28 subjects)
   - Impression ratings (data/TVAdMovieSet/{subject}/ImpressionRatings/; 28 subjects)
   - Ad preference votes (data/TVAdMovieSet/{subject}/AdPreferenceVotes/; 28 subjects)
   - Subjective preference ratings (data/TVAdMovieSet/{subject}/PreferenceRatings/; 14 subjects)

**※In subjective preference ratings can also be used for the analysis of individidual differences of behavior.**

## Usage

Execute plot.py. The resultant pictures will be stored in `result/` directory.

| Option | Choices | Description |
| - | - | - |
| -m | web tv | Movie set as stimlus |
| -t | sd ir ae ap pr | Task decoded by predicted- and measured-response decoding |

### Example

`python pair_dist.py -m web tv -t sd ir ae ap pr`

You can execute the same program as above with plot.ipynb.

Code is formatted by Black Formatter in Visual Studio Code.
