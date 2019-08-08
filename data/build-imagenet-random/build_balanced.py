#!/user/bin/env python
# extract images from the training set into folders
# Jake Lee, 1/13/18

import sys, os
import urllib
import socket
import shutil

localdir = os.path.dirname(os.path.abspath(__file__))
ilsvrc = '/path/to/ILSVRC2012/train/'
output = 'ilsvrc_random_balanced/'
targets = 'random_classes.txt'
qty = 50

if __name__ == '__main__':
	with open(targets, 'r') as f:
		counter = 0
		for an_entry in f.readlines():
			classname = an_entry.split(' ')[0]
			if not os.path.exists(os.path.join(ilsvrc, classname)):
				print "error, class doesn't exist"
				sys.exit(0)
			if not os.path.exists(os.path.join(output, classname)):
				os.makedirs(os.path.join(output, classname))	
			i = 0
			for an_image in os.listdir(os.path.join(ilsvrc, classname)):
				print "copying " + classname + '_' + str(i) + '.jpg'
				shutil.copy2(os.path.join(ilsvrc, classname, an_image),
					os.path.join(output, classname, classname+'_'+str(i)+'.jpg'))
				i += 1
				if i == qty:
					break
			counter += 1


