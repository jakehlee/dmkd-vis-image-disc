#!usr/bin/env python
# Calculate AUC scores of all results

import sys, os
import numpy as np
import csv
import re

# Where all of the DEMUD results are stored
RESULT_DIR = "/path/to/DEMUD/demud/results"
# Number of classes for normalization
N_CLASSES = 20
# Number of selected images to be considered
T = 40
# Results from random simulation
RAND_QTY = [50]*20

def msl_get_class(line):
    return line[2].split('-')[1]

def s9_get_class(line):
    return line[2].split('_')[0]

def in_get_class(line):
    return line[2].split('_')[0]

def uci_get_class(line):
    return line[2]

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

def perf_auc(n, t):
    perf_disc = range(1,n+1) + [n] * (t-n)
    return sum(perf_disc)

def rand_auc(n, t):
    rand_auc = 0
    for i in range(1, len(RAND)+1):
        if i == len(RAND):
            rand_auc += (t - RAND[i-1]) * i
        else:
            rand_auc += (RAND[i] - RAND[i-1]) * i
    return rand_auc * 100.0 / perf_auc(n,t)

def calc_auc(sel_path):
    with open(sel_path, 'r') as f:
        csv_reader = csv.reader(f)
        csv_list = list(csv_reader)
        #skip header
        csv_list = csv_list[1:]
    
    perf = perf_auc(N_CLASSES, T)

    seen = set()
    disc_list = []
    for (linecount, a_line) in enumerate(csv_list):
        # class-specific naming scheme here
        curr_class = s9_get_class(a_line)
        if curr_class not in seen:
            seen.add(curr_class)
        disc_list.append(len(seen))
    return sum(disc_list[:T]) * 100.0 / perf

def auc_for_all(result_dir):
    result_list = os.listdir(result_dir)
    result_list = sorted(result_list)

    k_vals = []
    aucs = []
    for result in result_list:
        try:
            curr_k = int(re.search('img-s9img-k=(.*)-dim', result).group(1))
            k_vals.append(curr_k)
            curr_auc = calc_auc(os.path.join(result_dir, result, "selections-k{}.csv".format(curr_k)))
            aucs.append(curr_auc)
            print result, curr_auc
        except:
            print result, "-"
    print "random", rand_auc(N_CLASSES, T)
    return k_vals, aucs

auc_for_all(RESULT_DIR)
