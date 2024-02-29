import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import matplotlib.transforms as mtransforms
import matplotlib
import re

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


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
                     xlabel = None, window = [None, None],
                     show_title = False, *args, **kwargs):


    if axs is None:
        axs = plt.gca()
    if fig is None and axs is None:
        fig, axs = plt.subplots(subplot_dict)


    out = axs.plot(x, y, *args, **kwargs)
    if show_title:
        axs.set_title(title)
    axs.spines['right'].set_visible(False)
    axs.spines['top'].set_visible(False)
    axs.spines['left'].set_visible(False)
    axs.yaxis.set_tick_params(labelleft=False)
    axs.set_yticks([])
    axs.set_xlim(window[0], window[1])
    axs.grid(False)
    axs.set_xlabel(xlabel, weight = "bold")



    return out

def export_figure(fig, name, directory, fmt='svg'):
    figpath= os.path.join(directory, "UniDec_Figures_and_Files", name+"_img"+"."+fmt)


    plt.savefig(figpath,bbox_inches='tight',format=fmt)

    print("Fig exported to: ", figpath)

def plot_peaks(peaks, axs = None, show_all = False, label = True, legend=True):

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
    if legend:
        labels  = [str(p.label)+" "+str(p.mass)+" Da" for p in peaks if p.label!= "" ]
        nl = '\n'
        # text = f"Species: {nl}{nl.join(labels)}"
        text = f"{nl.join(labels)}"
        bbox = dict(boxstyle='round', fc='lavender', ec='teal', alpha=0.5)
        axs.text(1, 0.8, text, fontsize=9, bbox=bbox,
                transform=axs.transAxes, horizontalalignment='left')



def plot_spectra_separate(spectra, attr = 'massdat', xlabel = 'Mass [Da]',
                          export = True, window = [None, None], show_peaks = False, show_all_peaks = False,
                          label_peaks=True, legend = False, directory = "", show_titles = True,fmt='svg',
                          *args, **kwargs):
    """Spectra plotted on individual figure"""



    if type(spectra) != list:
        spectra = [spectra]

    for i, s in enumerate(spectra):
        fig,axs = plt.subplots()

        x, y = getattr(s, attr)[:, 0], getattr(s, attr)[:, 1]

        _spectrum_plotter(x, y, xlabel=xlabel, axs = axs, fig=fig,title = s.name,
                          window = window, show_title=show_titles,*args, **kwargs)
        if show_peaks:
            plot_peaks(s.pks.peaks, axs = axs, show_all = show_all_peaks, label = label_peaks, legend = legend)
        fig.tight_layout()

        window_name = ""
        if window[0] is not None:
            window_name = window_name + "_" +str(window[0])
        if window[1] is not None:
            window_name = window_name+"_"+str(window[1])
        if export:
            export_figure(fig, s.name+"_"+attr+window_name, directory, fmt=fmt)
        plt.close(fig)



def plot_spectra_combined(spectra, attr = 'massdat', title = "", show_titles = True,
                          cmap='viridis', show_peaks = True,window = [None, None],
                          xlabel="Mass [Da]", show_all_peaks=False,label_peaks=True, legend=True,
                          fade=True,xoffval = 7.5, yoffval = 20,export=True,directory="",fmt='svg',
                          *args, **kwargs):

    if fade:
        alpha = np.linspace(1, 0.6, len(spectra))
    else:
        alpha = np.linspace(1, 1, len(spectra))
    # gray_cmap = get_cmap(len(spectra), cmap = "gray", x1 = 0, x2 = 0.7)
    set_spectra_colors(spectra, cmap =cmap, x1 = 0, x2 = 0.7)

    fig = plt.figure()

    fig.suptitle(title, weight = 'bold')
    for i,s in enumerate(spectra):
        xoff = i/xoffval
        yoff= i/yoffval +0.05
        x, y = getattr(s, attr)[:, 0], getattr(s, attr)[:, 1]
        axs=fig.add_axes([xoff,yoff,0.65,0.65], zorder=-i)

        _spectrum_plotter(x, y, xlabel=xlabel, axs = axs, fig=fig,
                          window = window, c=s.color,*args, **kwargs)
        if show_peaks :
            plot_peaks(s.pks.peaks, axs = axs, show_all = show_all_peaks, label = label_peaks, legend = False)
        if show_titles:
            axs.set_title(s.name, alpha = alpha[i], backgroundcolor = 'white')
        if i != 0:
            axs.spines['bottom'].set_visible(False)
            axs.xaxis.set_tick_params(labelleft=False)
            axs.set_xticks([])
            axs.set_xlabel("")
        if show_peaks and i == len(spectra)-1:
            plot_peaks(s.pks.peaks, axs = axs, show_all = show_all_peaks, label = label_peaks, legend = legend)

        axs.patch.set_alpha(0)
    # fig.tight_layout()
    if export:
        if title == "":
            title = os.path.split(directory)[-1]


        window_name = ""
        if window[0] is not None:
            window_name = window_name + "_" +str(window[0])
        if window[1] is not None:
            window_name = window_name+"_"+str(window[1])
        title = title+window_name
        export_figure(fig, title, directory, fmt=fmt)

def file_to_df(path):
    extension = os.path.splitext(path)[1]
    if extension == ".csv":
        df = pd.read_csv(path)
    elif extension == ".xlsx" or extension == ".xls":
        df = pd.read_excel(path)
    else:
        print('Extension Not Recognized', extension)
        df = None
    return df