import numpy as np
from functools import partial
import dautil as dl


def plot_times(ax, serial, parallel):
    cp = dl.plotting.CyclePlotter(ax)
    x = 2 ** np.arange(9)
    cp.plot(x, serial, label='Serial')
    cp.plot(x, parallel, label='Parallel')
    ax.set_xlabel('# Bootstraps')
    ax.set_ylabel('Time (s)')
    ax.set_title('Execution Time of Bootstrapping')
    ax.legend(loc='best')


def plot_distro(ax, boot_vals, observed):
    dl.plotting.hist_norm_pdf(ax, boot_vals)
    ax.axvline(observed, color='k', lw=3,
               label='Observed')


def time_many(code, n=1):
    times = []

    for i in range(9):
        times.append(dl.perf.time_once(partial(code, n=2 ** i), n))

    return times


def bootstrap(arr):
    n = len(arr)
    indices = np.random.choice(n, size=n)

    return arr[indices]
