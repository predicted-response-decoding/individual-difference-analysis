import argparse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pair_dist import PairDistPlotter, calc_pair_dist
from util import tofdr, map_list
from labels import *
from config import RC_PARAMS_DEFAULT

plt.rcParams.update(RC_PARAMS_DEFAULT)


def main(msets, tasks):
    dist_all, rvals, pvals = calc_pair_dist(msets=msets, tasks=tasks)
    # FDR correction in all P-values of individual-difference reflection
    pvals_fdr = tofdr(pvals)
    plotter = PairDistPlotter()
    figs = plotter.plot_all_mset_task(dist_all, rvals, pvals_fdr)
    plotter.save_all_mset_task(figs)

    dist_all, rvals, pvals = calc_pair_dist(
        msets=msets, tasks=tasks, is_for_manual=True
    )
    # FDR correction in all P-values of individual-difference reflection
    pvals_fdr = tofdr(pvals)
    plotter = PairDistPlotter()
    plotter.for_manual()
    figs = plotter.plot_all_mset_task(dist_all, rvals, pvals_fdr)
    plotter.save_all_mset_task(figs)


if __name__ == "__main__":
    mset_args = map_list(lambda mset: mset().arg, MOVIE_SET_ALL)
    task_args = map_list(lambda task: task().arg, TASK_ALL)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--movie-set",
        choices=mset_args,
        default=mset_args,
        nargs="+",
        type=str,
    )
    parser.add_argument(
        "-t",
        "--task",
        choices=task_args,
        default=task_args,
        nargs="+",
        type=str,
    )
    args = parser.parse_args()

    msets = map_list(
        lambda mset_arg: MOVIE_SET_ALL[mset_args.index(mset_arg)],
        args.movie_set,
    )
    tasks = map_list(
        lambda task_arg: TASK_ALL[task_args.index(task_arg)],
        args.task,
    )

    print("Movie set:", *map_list(lambda mset: mset.__name__, msets))
    print("Task     :", *map_list(lambda task: task.__name__, tasks))

    main(msets, tasks)
