# Visualizing Image Content to Explain Novel Image Discovery
### Jake Lee, Kiri Wagstaff
### In Preparation

This repository contains supplemental scripts and data used in the experiments presented in the paper.

## data/

##### ImageNet-Random
`data/build-imagenet-random` provides the scripts necessary to compile the ImageNet-Random balanced and imbalanced subsets of the ILSVRC2012 training set. The ILSVRC2012 training set must be downloaded. `random_classes.txt` contains the class definitions for the ImageNet-Random data set.

`python reprod_balanced.py` will reproduce the balanced variant of the ImageNet-Random data set used for experiments in the paper. `python reprod_imbalanced` will reproduce the imbalanced variant.

* `ilsvrc` defines the directory path of the ILSVRC2012 training set.
* `output` defines the directory in which the data set will be compiled.
* `filenames` defines the filepath of the exact images to be compiled. This should be `balanced_filenames.txt` or `imbalanced_filenames.txt`.

`python build_balanced.py` will compile the balanced variant of the ImageNet-Random data set using different images from the same classes. `python build_imbalanced.py` will compile the imbalanced variant. The following parameters must be set within the script.

* `ilsvrc` defines the directory path of the ILSVRC2012 training set.
* `output` defines the directory in which the data set will be compiled.
* `targets` defines the filepath of the class definitions. For ImageNet-Random, this should be `random_classes.txt`.

----

##### ImageNet-Yellow

`data/build-imagenet-yellow` provides the scripts necessary to compile the ImageNet-Yellow subset of the ILSVRC2012 training set. The ILSVRC2012 training set must be downloaded. `yellow_classes.txt` contains the class definitions for the ImageNet-Yellow data set.

`python reprod_yellow.py` will reproduce the ImageNet-Yellow data set used for experiments in the paper. The same parameters as above must be set within the script. `filenames` should be set to `yellow_filenames.txt`

`python build_yellow.py` will compile the ImageNet-Yellow data set using different images form the same classes. The same parameters as `build_balanced.py` must be set within the script. `target` should be set to `yellow_casses.txt`

----

##### Mars-Curiosity
24 classes of the Mars-Curiosity data set can be accessed on Zenodo at https://zenodo.org/record/1049137. An additional class of 21 images, "sun", was added for our experiments, for a total of 25 classes with 6712 images. This additional class is included in `data/mars-sun-class/`

----

##### STONEFLY9
The STONEFLY9 data set can be access at http://web.engr.oregonstate.edu/~tgd/bugid/stonefly9/.

----

##### Extracted features

Features extracted from the data set are provided in the following directories:

* `data/build-imagenet-random/balanced_feats`
* `data/build-imagenet-random/imbalanced_feats`
* `data/build-imagenet-yellow/yellow_feats`
* `data/mars_feats`
* `data/STONEFLY9_feats`

Each directory contains three `.csv` files with extracted features. These features were extracted using the instructions described in the README in the root of this repository.











