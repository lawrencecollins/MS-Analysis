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

def set_spectra_colors(spectra, cmap = 'rainbow', x1=0, x2=1):
    """assign colour as class attribute in list of objects"""
    cmap = plt.get_cmap(cmap)
    colors = cmap(np.linspace(x1, x2, len(spectra)))
    for i, s in enumerate(spectra):
        s.color = colors[i]


def get_cmap(length, cmap = 'rainbow', x1 = 0, x2 = 1):

    cmap = plt.get_cmap(cmap)
    return cmap(np.linspace(x1, x2, length))


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


def _spectrum_plotter(x,y, title = None, axs = None, fig = None,
                     xlabel = None, window = [None, None], *args, **kwargs):

    if axs is None:
        axs = plt.gca()
    if fig is None and axs is None:
        fig, axs = plt.subplots(subplot_dict)


    out = axs.plot(x, y, *args, **kwargs)
    axs.set_title(title)
    axs.spines['right'].set_visible(False)
    axs.spines['top'].set_visible(False)
    axs.spines['left'].set_visible(False)
    axs.yaxis.set_tick_params(labelleft=False)
    axs.set_yticks([])
    axs.set_xlim(window[0], window[1])
    axs.grid(False)
    axs.set_xlabel(xlabel, weight = "bold")

    if peaks is not None:
        axs.scatter(peaks[:, 0], peaks[:, 1], color = colors)

    return out

def export_spectrum(fig, name):
    figpath= os.path.join(eng.directory, "UniDec_Figures_and_Files", name+"_img.png")

    plt.savefig(figpath)
    print("Fig exported to: ", figpath)

def plot_peaks(peaks, axs = None, show_all = False, label = True):

    if axs is None:
        axs = plt.gca()


    for p in peaks:
        if show_all:
            axs.scatter(p.mass, p.height, color = p.color, marker=p.marker)
        elif show_all is False:
            if p.label != "":
                axs.scatter(p.mass, p.height, color = p.color, marker=p.marker)
        if label:
            axs.text(p.mass, p.height, p.label, color = p.color, rotation = 0, ha = "center", va = 'bottom',
                    fontsize = 'small', style = 'italic')



def plot_spectra_separate(spectra, attr = 'massdat', xlabel = 'Mass [Da]',
                          export = True, window = [None, None], show_peaks = False, show_all_peaks = False,
                          label_peaks=True,
                          *args, **kwargs):
    """Spectra plotted on individual figure"""



    if type(spectra) != list:
        spectra = [spectra]

    for i, s in enumerate(spectra):
        fig,axs = plt.subplots()

        x, y = getattr(s, attr)[:, 0], getattr(s, attr)[:, 1]

        _spectrum_plotter(x, y, xlabel=xlabel, axs = axs, fig=fig,title = s.name, window = window, *args, **kwargs)
        if show_peaks:
            plot_peaks(s.pks.peaks, axs = axs, show_all = show_all_peaks, label = label_peaks)
        if export:
            export_spectrum(fig, s.name+"_"+attr)



def plot_spectra_combined(spectra, attr = 'massdat', title = "", show_titles = True):
    pass