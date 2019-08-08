#!usr/bin/env python
# Plot discovery plots of all results

import sys, os
import numpy as np
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import seaborn as sns
import csv
import re
import random

sns.set()
sns.set_style("whitegrid")
sns.set_context("paper", font_scale = 1.2, rc={'lines.markeredgewidth':1})


# Where all of the DEMUD results are stored
RESULT_DIR = "/path/to/folder/of/DEMUD/results/"
# Look for DEMUD results with note balfc*
EXP_CODE = "bal"
# Number of classes in the data set, for oracle calculation
N_CLASSES = 20
# Number of images to be considered
T = 70
# Interval for x-ticks
INTERVAL = 10
# Title for plot
TITLE = ""
# Quantity of images per class, for random simulation
RAND_QTY = [50]*20

# Color constants from colorbrewer
lorange = "#fdae6b"
morange = "#f16913"
horange = "#8c2d04"
lgreen = "#a1d99b"
mgreen = "#41ab5d"
hgreen = "#005a32"
lpurple = "#bcbddc"
mpurple = "#807dba"
hpurple = "#4a1486"
hgrey = "#252525"
hblue = "#084594"
hred = "#de2d26"

# functions for retrieving class name from the selections.csv line

def msl_get_class(line):
    return line[2].split('-')[1]

def s9_get_class(line):
    return line[2].split('_')[0]

def in_get_class(line):
    return line[2].split('_')[0]

GET_CLASS = in_get_class

def rand_sim(qty):
    items = []
    counter = 0
    for aqty in qty:
        items = items + [counter] * aqty
        counter += 1
    nums = []
    for i in range(1000):
        random.shuffle(items)
        counter = 0
        found = set()
        temp = []
        for item in items:
            counter += 1
            if item not in found:
                found.add(item)
                temp.append(counter)
        nums.append(temp)
    nums = np.asarray(nums)
    output = np.mean(nums, axis=0)
    return output.tolist()

RAND_SIM = rand_sim(RAND_QTY)

def perf_disc(n, t):
    return range(1, n+1), range(1,n+1)

def get_disc(sel_path):
    with open(sel_path, 'r') as f:
        csv_reader = csv.reader(f)
        csv_list = list(csv_reader)
        #skip header
        csv_list = csv_list[1:]
    
    seen = set()
    disc_index = []
    disc_list = []
    for (linecount, a_line) in enumerate(csv_list):
        if linecount == T:
            break
        curr_class = GET_CLASS(a_line)
        if curr_class not in seen:
            seen.add(curr_class)
            disc_index.append(linecount+1)
            disc_list.append(len(seen))
    return disc_index, disc_list

def plot_layers():
    layers_dir = os.path.join(RESULT_DIR, EXP_CODE+"-layers")
    result_list = os.listdir(layers_dir)
    
    discoveries = {}
    for result in result_list:
        curr_k = int(re.search('-k=(.*)-dim', result).group(1))
        selpath = os.path.join(layers_dir, result, "selections-k{}.csv".format(curr_k))
        if result[-9:] == "fc6static":
           temp = {}
           x, y = get_disc(selpath)
           temp['x'] = x
           temp['y'] = y
           discoveries['6s'] = temp
        elif result[-9:] == "fc7static":
           temp = {}
           x, y = get_disc(selpath)
           temp['x'] = x
           temp['y'] = y
           discoveries['7s'] = temp
        elif result[-9:] == "fc8static":
           temp = {}
           x, y = get_disc(selpath)
           temp['x'] = x
           temp['y'] = y
           discoveries['8s'] = temp
        elif result[-3:] == "fc6":
           temp = {}
           x, y = get_disc(selpath)
           temp['x'] = x
           temp['y'] = y
           discoveries['6'] = temp
        elif result[-3:] == "fc7":
           temp = {}
           x, y = get_disc(selpath)
           temp['x'] = x
           temp['y'] = y
           discoveries['7'] = temp
        elif result[-3:] == "fc8":
           temp = {}
           x, y = get_disc(selpath)
           temp['x'] = x
           temp['y'] = y
           discoveries['8'] = temp
    
    # perfect discovery
    perf_x, perf_y = perf_disc(N_CLASSES, T)

    # random discovery
    rand_x = RAND_SIM
    rand_y = range(1, N_CLASSES+1)
    
    # begin plotting
    fig, ax = plt.subplots()
    ax.plot(perf_x, perf_y, label="Oracle", marker='', color=hred, \
        linestyle=':')
    ax.plot(rand_x, rand_y, label="Random", marker='', color='k', \
        linestyle=':')
    ax.plot(discoveries['6']['x'], discoveries['6']['y'], \
        label="DEMUD CNN fc6", marker='o', color=lgreen)
    ax.plot(discoveries['7']['x'], discoveries['7']['y'], \
        label="DEMUD CNN fc7", marker='o', color=mgreen)
    ax.plot(discoveries['8']['x'], discoveries['8']['y'], \
        label="DEMUD CNN fc8", marker='o', color=hgreen)

    #fig2, ax2 = plt.subplots()
    #ax.plot(perf_x, perf_y, label="Oracle", marker='', color=hred, \
    #    linestyle=':')
    #ax.plot(rand_x, rand_y, label="Random", marker='', color='k', \
    #    linestyle=':')
    ax.plot(discoveries['6s']['x'], discoveries['6s']['y'], \
        label="SVD CNN fc6", marker='+', markersize=10, \
        color=lgreen, linestyle='--')
    ax.plot(discoveries['7s']['x'], discoveries['7s']['y'], \
        label="SVD CNN fc7", marker='+', markersize=10, \
        color=mgreen, linestyle='--')
    ax.plot(discoveries['8s']['x'], discoveries['8s']['y'], \
        label="SVD CNN fc8", marker='+', markersize=10, \
        color=hgreen, linestyle='--')
    
    # set x range from 1 to T in intervals of 50, including 1
    ax.set_xlim(1, T)
    ax.xaxis.set_ticks([1]+range(INTERVAL, T+1, INTERVAL))
    # force y ticks to use integers and set max
    ymax = max(perf_y)
    ax.set_ylim(bottom=1)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    yt = ax.get_yticks()
    yt = np.append(yt, 1)
    ax.set_yticks(yt)
    ax.set_ylim(1, ymax)
    
    #ax2.set_xlim(1, T)
    #ax2.xaxis.set_ticks([1]+range(10, T+1, 10))
    #ax2.set_ylim(bottom=1)
    #ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    #ax2.set_yticks(yt)
    #ax2.set_ylim(1, ymax)
    
    # titles and labels
    ax.set_title(TITLE)
    ax.set_xlabel("Number of selected items")
    ax.set_ylabel("Number of classes discovered")
    ax.legend(loc="lower right")
    #ax2.set_title(TITLE)
    #ax2.set_xlabel("Number of selected items")
    #ax2.set_ylabel("Number of classes discovered")
    #ax2.legend(loc="lower right")
    
    fig.tight_layout()
    fig.savefig("discplots/"+EXP_CODE+"-layer.png")
    #fig2.tight_layout()
    #fig2.savefig("discplots/"+EXP_CODE+"-layer2.png")

def plot_reps():
    reps_dir = os.path.join(RESULT_DIR, EXP_CODE+"-reps")
    result_list = os.listdir(reps_dir)
    
    discoveries = {}
    for result in result_list:
        curr_k = int(re.search('-k=(.*)-dim', result).group(1))
        selpath = os.path.join(reps_dir, result, "selections-k{}.csv".format(curr_k))
        if result[:3] == "cnn" and result[-6:] == "static" and \
            "sift" not in result[-15:]:
           temp = {}
           x, y = get_disc(selpath)
           temp['x'] = x
           temp['y'] = y
           discoveries['cnns'] = temp
        elif result[:3] == "cnn" and result[-6:] != "static" and \
            "sift" not in result[-15:]:
           temp = {}
           x, y = get_disc(selpath)
           temp['x'] = x
           temp['y'] = y
           discoveries['cnn'] = temp
        elif result[:3] == "cnn" and result[-6:] == "static" and \
            "sift" in result[-15:]:
           temp = {}
           x, y = get_disc(selpath)
           temp['x'] = x
           temp['y'] = y
           discoveries['sifts'] = temp
        elif result[:3] == "cnn" and result[-6:] != "static" and \
            "sift" in result[-15:]:
           temp = {}
           x, y = get_disc(selpath)
           temp['x'] = x
           temp['y'] = y
           discoveries['sift'] = temp
        elif result[:3] == "img" and result[-6:] == "static":
           temp = {}
           x, y = get_disc(selpath)
           temp['x'] = x
           temp['y'] = y
           discoveries['pixs'] = temp
        elif result[:3] == "img" and result[-6:] != "static":
           temp = {}
           x, y = get_disc(selpath)
           temp['x'] = x
           temp['y'] = y
           discoveries['pix'] = temp
    
    # perfect discovery
    perf_x, perf_y = perf_disc(N_CLASSES, T)

    # random discovery
    rand_x = RAND_SIM
    rand_y = range(1, N_CLASSES+1)
    
    # begin plotting
    fig, ax = plt.subplots()
    ax.plot(perf_x, perf_y, label="Oracle", marker='', color=hred, \
        linestyle=':')
    ax.plot(rand_x, rand_y, label="Random", marker='', color='k', \
        linestyle=':')
    ax.plot(discoveries['pix']['x'], discoveries['pix']['y'], \
        label="DEMUD Pixel", marker='o', color=mpurple)
    ax.plot(discoveries['sift']['x'], discoveries['sift']['y'], \
        label="DEMUD SIFT", marker='o', color=morange)
    ax.plot(discoveries['cnn']['x'], discoveries['cnn']['y'], \
        label="DEMUD CNN", marker='o', color=hgreen)

    #fig2, ax2 = plt.subplots()
    #ax.plot(perf_x, perf_y, label="Oracle", marker='', color=hred, \
    #    linestyle=':')
    #ax.plot(rand_x, rand_y, label="Random", marker='', color='k', \
    #    linestyle=':')
    ax.plot(discoveries['pixs']['x'], discoveries['pixs']['y'], \
        label="SVD Pixel", marker='+', markersize=10, \
        color=mpurple, linestyle='--')
    ax.plot(discoveries['sifts']['x'], discoveries['sifts']['y'], \
        label="SVD SIFT", marker='+', markersize=10, \
        color=morange, linestyle='--')
    ax.plot(discoveries['cnns']['x'], discoveries['cnns']['y'], \
        label="SVD CNN", marker='+', markersize=10, \
        color=hgreen, linestyle='--')

    # set x range from 1 to T in intervals of 50, including 1
    ax.set_xlim(1, T)
    ax.xaxis.set_ticks([1]+range(INTERVAL, T+1, INTERVAL))
    # force y ticks to use integers and set max
    ymax = max(perf_y)
    ax.set_ylim(bottom=1)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    yt = ax.get_yticks()
    yt = np.append(yt, 1)
    ax.set_yticks(yt)
    ax.set_ylim(1, ymax)
    
    # set x range from 1 to T in intervals of 50, including 1
    #ax2.set_xlim(1, T)
    #ax2.xaxis.set_ticks([1]+range(10, T+1, 10))
    # force y ticks to use integers and set max
    #ax2.set_ylim(bottom=1)
    #ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    #ax2.set_yticks(yt)
    #ax2.set_ylim(1, ymax)

    # titles and labels
    ax.set_title(TITLE)
    ax.set_xlabel("Number of selected items")
    ax.set_ylabel("Number of classes discovered")
    ax.legend(loc="lower right")
    #ax2.set_title(TITLE)
    #ax2.set_xlabel("Number of selected items")
    #ax2.set_ylabel("Number of classes discovered")
    #ax2.legend(loc="lower right")
    
    fig.tight_layout()
    fig.savefig("discplots/"+EXP_CODE+"-rep.png")
    #fig2.tight_layout()
    #fig2.savefig("discplots/"+EXP_CODE+"-rep2.png")

plot_layers()
plot_reps()
