#!/user/bin/env python
# extract images from the training set into folders
# Jake Lee, 1/13/18

import sys, os
import urllib
import socket
import shutil
import cv2
import numpy as np

localdir = os.path.dirname(os.path.abspath(__file__))
ilsvrc = '/path/to/ILSVRC2012/train/'
output = 'yellow_imageset/'
targets = 'yellow_classes.txt'
qty = 50
cutoff = 150

yellow_bgr = np.asarray([0,255,255])

if __name__ == '__main__':
	with open(targets, 'r') as f:
		counter = 0
		for an_entry in f.readlines():
			# for unbalanced only
			classname = an_entry.split(' ')[0]
			print "going through " + classname
			if not os.path.exists(os.path.join(ilsvrc, classname)):
				print "error, class doesn't exist"
				sys.exit(0)
			if not os.path.exists(os.path.join(output, str(counter))):
				os.makedirs(os.path.join(output, str(counter)))	
			i = 0
			for an_image in os.listdir(os.path.join(ilsvrc, classname)):
				img = cv2.imread(os.path.join(ilsvrc, classname, an_image))
				avg_color = [img[:,:,a].mean() for a in range(img.shape[-1])]
				avg_color = np.asarray(avg_color)
				dist = np.linalg.norm(avg_color - yellow_bgr)

				if dist < cutoff:
					print "copying " + an_image
					shutil.copy2(os.path.join(ilsvrc, classname, an_image),
						os.path.join(output, str(counter), an_image))
					i += 1
				if i == qty:
					break
			if i < 5: 
					for an_image in os.listdir(os.path.join(ilsvrc, classname)):
						img = cv2.imread(os.path.join(ilsvrc, classname, an_image))
						avg_color = [img[:,:,a].mean() for a in range(img.shape[-1])]
						avg_color = np.asarray(avg_color)
						dist = np.linalg.norm(avg_color - yellow_bgr)


						if dist < cutoff+20:
							print "copying " + str(counter) + '_' + str(i) + '.jpg = ' + str(dist)
							shutil.copy2(os.path.join(ilsvrc, classname, an_image),
								os.path.join(output, str(counter), str(counter)+'_'+str(i)+'.jpg'))
							i += 1
						if i == qty:
							break
			counter += 1


