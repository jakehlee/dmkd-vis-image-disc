#!/usr/bin/env python
# reproduce Random-Balanced data set 
# Jake Lee, 8/13/19

import sys, os
import shutil

localdir = os.path.dirname(os.path.abspath(__file__))
ilsvrc = '/path/to/ILSVRC2012/train/'
output = 'ilsvrc_random_balanced/'
filenames = 'balanced_filenames.txt'

if __name__ == '__main__':
    with open(filenames, 'r') as f:
        for an_entry in f.readlines():
            classname = an_entry.split('/')[0]
            if not os.path.exists(os.path.join(output, classname)):
                os.makedirs(os.path.join(output, classname))
            shutil.copy2(os.path.join(ilsvrc, an_entry.rstrip('\n')), \
                os.path.join(output, an_entry.rstrip('\n')))
