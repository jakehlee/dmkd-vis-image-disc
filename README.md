# Visualizing Image Content to Explain Novel Image Discovery
### Jake Lee, Kiri Wagstaff
### In Preparation

This repository contains supplemental scripts and data used in the experiments presented in the paper.

## Step-by-step instructions for running experiments

1. **Compile the image data set** - It is recommended that the image filename include the class information. The images can be in class subfolders or in a single folder.

2. **Preprocess the imageset** - We recommend scaling and center-cropping your images to 227x227 first.

	We used imagemagick: `mogrify -path imageset/# -format jpg -resize "227x227^" -gravity center -crop 227x227+0+0 +repage imageset/#/*.jpg`

	Caffe also provides a tool: https://github.com/BVLC/caffe/blob/master/tools/extra/resize_and_crop_images.py

3. **Download and install DEMUD** - Available at https://github.com/wkiri/DEMUD

4. **Extract features** - Extract features from the images using `DEMUD/scripts/cnn_feat_extraction/feat_csv.py`. The extracted features will be saved as a CSV, with the first column being the image name.

	You will need to install Caffe and specify the trained Caffe model from which the features will be extracted.  We used Caffe's pre-trained model called `bvlc_reference_caffenet` with a modified `deploy.prototxt`.

	The pre-trained model is available at https://github.com/BVLC/caffe/tree/master/models/bvlc_reference_caffenet.

	The modified prototxt is available in this repository at `src/extract/deploy.prototxt`.

5. **Run DEMUD on features** - Configure DEMUD by adding the path to the feature CSV in `demud.config` at the `floatdatafile` line.

	Run DEMUD. An example run: `python demud.py -v --init-item=svd --n=300 --k=4096 --svdmethod=increm-brand --note=balfc6`

	- `-v` indicates this is a run on CNN features in a CSV
	- `--init-item=svd` sets the first item initialization to full SVD initialization.
	- `--n=300` sets DEMUD to select the first 300 items.
	- `--k=4096` sets the number of principal components used during SVD to a maximum of 4096.
	- `--svdmethod=increm-brand` sets the SVD method to incremental SVD as described by Brand, 2002.
	- `--note=balfc6` will append "balfc6" to the end of the results directory.

6. **Visualize the explanations** - Use `src/visualize/vis_DEMUD.py` to generate visualizations of the explanations. This script and its associated models were modified and trained from code provided for Dosovitskiy and Brox, 2016 (NIPS). The original source is available [here](https://lmb.informatik.uni-freiburg.de/resources/software.php).

7. **Calculate and plot discovery rates** - Use `src/util/calc_auc.py` and `src/util/plot_exp.py` to calculate nAUCt scores and generate discovery plots.

8. **Organize results** - Use `src/util/gen_html.py` to generate PDFs to display selected images and visualized explanations.

## Itemized documentation

Documentation for each file and script is available in their respective sub-directories.
