import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import matplotlib.transforms as mtransforms
import matplotlib
import re

matplotlib.rcParams['font.family'] = 'serif'


def ascii_to_txt(directory):

    for dname, dirs, files in os.walk(directory):

        for fname in files:
            if fname[-5:] == "ascii":

                os.rename(dname+fname, dname+fname[:-5]+"txt")
                fname = fname[:-5]+"txt"
                fpath = os.path.join(dname, fname)
                with open(fpath) as f:
                    s = f.read()
                    s = s.replace(" ", "\n")
                    with open(fpath, "w") as f:
                        f.write(s)


def get_txt_files(directory):
    paths = [p for p in os.listdir(directory) if p[:-4] == ".txt"]

    return paths


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def sort_files(files, key = natural_keys):
    return files.sort(key = key)

def find_peaks_(x, y, threshold, distance):

    thresh = np.max(y1)*threshold
    peaksi, _ = find_peaks(y1, height = thresh, distance = distance)
    peaksx = [x[p] for p in peaksi]
    return peaksi, peaksx


def match_peaks2(theory_df, data_masses, window = 10):
    species, expected = np.array(theory_df['Species']), np.array(theory_df['Mass'])



    # match algorithm
    tm, dm = np.meshgrid(expected, data_masses)
    if len(expected) ==1 or len(data_masses) == 1:
        tm, dm = tm[0], dm[0]
    diff = abs(tm - dm)
    diff[diff>window] = np.nan
    pmatch = {}
    for i, d in enumerate(diff):
        if np.isnan(d).all()==False:
            minimum = np.nanargmin(d)
            data_peak = data_masses[i]

            pmatch[data_peak] = species[minimum]
    return pmatch


def plot_spectra(files, window = None, threshold = 0.02, distance,*args, **kwargs):
    if type(files) !=list:
        files = [files]









