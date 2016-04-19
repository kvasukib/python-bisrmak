import csv , matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pylab import rcParams, figure, axes, pie, title, show
import sys
import os
import datetime as dt
import matplotlib.dates as mdate

x_label = 'Date and Time'
y_label = 'rtt (ms)'
yaxislow = 0
yaxishigh = 100
number_files = len(sys.argv) - 1
#Plots 1-6 time series files, latency vs. time

if (number_files == 0 or number_files > 6):
	raise error('please provide 1-6 time series files') 

#Read all filenames provided
for j in range(number_files): 
	plotx = []
	ploty = []

	filename = str(sys.argv[j+1]) #start at 1 (not to use script name)
	s_label = filename.split('.')[-2] + "-end"
	try:
		f = open(filename, 'rb')#import file
		
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

		#Read values from file
		for row in reader: 
			secs = mdate.epoch2num(float(row[0]))
			#x = time.gmtime(float(row[0])) #timestamps
			y = (int(row[4]))/10 #file has ms*10		
			plotx.append(secs)
			ploty.append(y)

		#Change plot options
		#print plotx[0]
		if j == 0: 
			fig = plt.figure(1, figsize=(9, 4))
			ax = fig.add_subplot(111)
			#title = filename.split('.')[0]
			#ax.set_title(title)
			s_color = 'r'
		elif j == 1: #Decision tree for series colors
			s_color = 'b'
		elif j== 2:
			s_color = 'g'
		elif j == 3:
			s_color = 'k'
		elif j == 4:
			s_color = 'c'
		else:
			s_color = 'm'
		
		ax.plot_date(plotx, ploty, color = s_color, alpha = 1, marker = ".", markersize = 3,  label = s_label)
		ax.set_xlabel(x_label, fontsize=17)
		ax.set_ylabel(y_label, fontsize=17)
		ax.set_ylim([yaxislow, yaxishigh])
		ax.set_xlim([dt.date(2016, 1, 11), dt.date(2016, 1, 20)])
		# Choose your xtick format string
		date_fmt = '%m-%d'

		# Use a DateFormatter to set the data to the correct format
		date_formatter = mdate.DateFormatter(date_fmt)
		ax.xaxis.set_major_formatter(date_formatter)
		#ax.set_xlim([dt.date(2016, 2, 12), dt.date(2016, 2, 19)])
	if j == (number_files-1):
		# Sets the tick labels diagonal so they fit easier.
                ax.legend()
		fig.autofmt_xdate()
		fig.tight_layout()
		output = filename + '.pdf'
		fig.savefig(output)
			
		
