import argparse

from labels import *
from pair_dist import PairDistPlotter, calc_pair_dist
from util import map_list, tofdr


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
    mset_args = map_list(
        lambda mset_class: mset_class.arg, MOVIE_SET_CLASS_ALL
    )
    task_args = map_list(lambda task_class: task_class.arg, TASK_CLASS_ALL)

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
        lambda mset_arg: MOVIE_SET_CLASS_ALL[mset_args.index(mset_arg)](),
        args.movie_set,
    )
    tasks = map_list(
        lambda task_arg: TASK_CLASS_ALL[task_args.index(task_arg)](),
        args.task,
    )

    print("Movie set:", *map_list(lambda mset: mset.name, msets))
    print("Task     :", *map_list(lambda task: task.name, tasks))

    main(msets, tasks)
