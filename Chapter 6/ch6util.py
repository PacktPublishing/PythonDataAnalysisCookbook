from joblib import Memory
from scipy.io import wavfile
import dautil as dl
import numpy as np


memory = Memory(cachedir='.')


@memory.cache
def read_wav():
    wav = dl.data.get_smashing_baby()

    return wavfile.read(wav)


def fit(df):
    slope, _ = np.polyfit(df.index.year, df.values, 1)

    return slope


def diff_median(df, diff_order=1):
    return np.median(np.diff(df.values.flatten(), diff_order))


def amplitude(arr):
    return np.abs(np.fft.fft(arr))
