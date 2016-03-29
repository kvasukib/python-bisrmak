import csv , matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pylab import rcParams
import sys
import os

x_label = 'Time'
y_label = 'rtt (ms)'
number_files = len(sys.argv) - 1
#Plots 1-6 time series files, latency vs. time

if (number_files == 0 or number_files > 6):
	raise error('please provide 1-6 time series files') 

#Read all filenames provided
for j in range(number_files): 
	plotx = []
	ploty = []

	filename = str(sys.argv[j+1]) #start at 1 (not to use script name)

	try:
		f = open(filename, 'rb')#import file
		sys.stderr.write('reading time series file %s\n' % filename)
		reader = csv.reader(f, delimiter=' ') #read file into variable reader

	#Check for OS and IO errors
	except OSError as o:
		sys.stderr.write('bordermap file error: %s\n' % o)
		raise

	except IOError as i:
		sys.stderr.write('File open failed: %s\n' % i)
		raise
	
	except FileEmptyError as p:
        	sys.stderr.write('bordermap file error: %s\n' %p)
        	rais
	
	else:
		sys.stderr.write('reading time series file %s\n' % filename)
                reader = csv.reader(f, delimiter=' ') #read file into variable reader

		for row in reader: 
			x = row[0] #timestamps
			y = row[4]/10 #file has ms*10		
			plotx.append(x)
			ploty.append(y)
		plt.sublot(number_files, 1, (j+1))
		plt.title(str(filename))
		plt.plot(plotx, ploty)
		plt.xlabel(x_label)
		plt.ylabel(y_label)
		plt.show()
			
		
