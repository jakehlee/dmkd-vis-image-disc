# This script inverts feature vectors output by DEMUD.
#
# Alexey Dosovitskiy, 2016
# Modified by Jake Lee, 2017/18

import sys

# uncomment and change the path to make python use specific caffe version
#sys.path.insert(0, '/home/dosovits/MATLAB/toolboxes/caffe-fr-chairs/python')
#print sys.path
import os
os.environ['GLOG_minloglevel'] = '2' 
import caffe
import numpy as np
import patchShow
import scipy.misc
import scipy.io
import csv
import copy

print(caffe.__file__)

if len(sys.argv) == 4:
  net_name = sys.argv[1]
  exp_path = sys.argv[2]
  exp_name = sys.argv[3]
else:
  raise Exception('Usage: vis_DEMUD.py NET_NAME EXP_PATH EXP_NAME')

# set up the inputs for the net: 
image_size = (3,227,227)
batch_size = 64
shift_flag = True

# subtract the ImageNet mean
matfile = scipy.io.loadmat('ilsvrc_2012_mean.mat')
image_mean = matfile['image_mean']

topleft = ((image_mean.shape[0] - image_size[1])/2, (image_mean.shape[1] - image_size[2])/2)
del matfile

#initialize the caffenet to extract the features
caffe.set_mode_gpu() # replace by caffe.set_mode_cpu() to run on a CPU

# find CSV files
filelist = os.listdir(exp_path)
for afile in filelist:
	if 'recon-cnn' in afile:
		recon_csv = np.genfromtxt(os.path.join(exp_path, afile), delimiter=",")
	elif 'resid-cnn' in afile:
		resid_csv = np.genfromtxt(os.path.join(exp_path, afile), delimiter=",")
	elif 'select-cnn' in afile:
		select_csv = np.genfromtxt(os.path.join(exp_path, afile), delimiter=",")
	elif 'selections' in afile or 'demud.log' in afile:
		continue
	else:
		raise Exception('No result CSVs found in EXP_PATH ' + exp_path)

print "DEMUD result CSVs found."
datalength = len(select_csv)
print "Number of selections = " + str(datalength)

# mean shift residuals to mean of recon_csv
if shift_flag:
	shifted_resid_csv = np.zeros(resid_csv.shape)
	for i in range(datalength):
		select_feat = select_csv[i].copy()
		select_mean = select_feat.mean()
		resid_feat = resid_csv[i].copy()
		resid_mean = resid_feat.mean()
		print str(resid_mean) + ", " + str(select_mean) + ", -16.037"
		shifted_resid_feat = resid_feat - (resid_mean - select_mean)
		shifted_resid_csv[i] = shifted_resid_feat
else:
	shifted_resid_csv = resid_csv

# stack the features into a single array
csv_imported = np.concatenate((select_csv, recon_csv, shifted_resid_csv),\
	axis=0)
totallength = datalength * 3

# add zero-buffer for batch splitting
numzeros = batch_size - (totallength % batch_size)
print csv_imported.shape
csv_imported = np.concatenate((csv_imported, np.zeros((numzeros, len(csv_imported[0])), dtype='float32')), axis=0)


# run recon net in batches
net = caffe.Net(net_name + '/generator.prototxt', net_name + '/generator.caffemodel', caffe.TEST)
master_recon = np.asarray([])
itr = 0
while itr < totallength:
	batch = csv_imported[itr:itr+batch_size]
	generated = net.forward(feat=batch)
	recon = np.copy(generated['generated'][:,::-1,topleft[0]:topleft[0]+image_size[1], topleft[1]:topleft[1]+image_size[2]])
	print recon.shape
	if master_recon.size == 0:
		master_recon = recon
	else:
		master_recon = np.concatenate((master_recon, recon), axis=0)
	itr += batch_size
del net

print master_recon.shape

# save results to a file
mypath = os.path.dirname(os.path.realpath(__file__))

select_results = master_recon[0:datalength]
select_filepath = os.path.join(mypath, exp_name, 'select')
recon_results = master_recon[datalength:2*datalength]
recon_filepath = os.path.join(mypath, exp_name, 'recon')
resid_results = master_recon[2*datalength:3*datalength]
resid_filepath = os.path.join(mypath, exp_name, 'resid')


if not os.path.exists(os.path.join(mypath, exp_name)):
	os.makedirs(os.path.join(mypath, exp_name))
	os.makedirs(select_filepath)
	os.makedirs(recon_filepath)
	os.makedirs(resid_filepath)

c = 0
for animage in select_results:
	tempimage = patchShow.normalize(animage)
	try:
		scipy.misc.imsave(select_filepath+'/'+str(c)+'.png', tempimage.transpose((1,2,0)))
	except ValueError:
		pass
	c+=1

c = 0
for animage in recon_results:
	tempimage = patchShow.normalize(animage)
	try:
		scipy.misc.imsave(recon_filepath+'/'+str(c)+'.png', tempimage.transpose((1,2,0)))
	except ValueError:
		pass
	c+=1

c = 0
for animage in resid_results:
	tempimage = patchShow.normalize(animage)
	try:
		scipy.misc.imsave(resid_filepath+'/'+str(c)+'.png', tempimage.transpose((1,2,0)))
	except ValueError:
		pass
	c+=1
