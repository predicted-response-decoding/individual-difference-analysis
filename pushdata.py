import os
import movieset


stims = [movieset.WebAdMovieSet, movieset.TVAdMovieSet]

for stim in stims:
    subjs = stim.get_subjects()
    for subj in subjs:
        dirname = f'./data/{stim.__name__}/{subj}/'
        os.system(f'git add {dirname}')
        os.system(f'git commit -m \'upload {dirname}\'')
        os.system('git push')

print("Done")
