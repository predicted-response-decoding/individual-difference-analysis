import os
import mystim
import mytask


msets = [mystim.WebAdMovieSet, mystim.TVAdMovieSet]
tasks = [
    mytask.SceneDescriptions,
    mytask.ImpressionRatings,
    mytask.AdEffectivenessIndices,
    mytask.AdPreferenceVotes,
    mytask.PreferenceRatings,
]

for m in msets:
    subjs = m.get_subjects()
    for subj in subjs:
            for t in tasks:
                if m not in t.msets: continue
                dirname = f'./data/{m.__name__}/{subj}/{t.__name__}'
                os.system(f'git add {dirname}')
                os.system(f'git commit -m \'upload {dirname}\'')
                os.system('git push')

print("Done")
