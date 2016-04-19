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
yaxishigh = 200
in_files = str(sys.argv[1])
number_files = in_files.count(' ') + 1

#number_files = len(sys.argv) - 1
#Plots 1-6 time series files, latency vs. time
if (number_files == 0):
	sys.stderr.write('No files were provided\n') 
elif (number_files > 10):
	sys.stderr.write('more than 10 files provided. Will plot first 10. files provided:')
	sys.stderr.write(str(sys.argv[1]))
	number_files = 10
	
	

#Read all filenames provided
for j in range(number_files): 
	plotx = []
	ploty = []

	filename = in_files.split(' ')[j]
	s_label = filename.split('.')[-2]
	try:
		f = open(filename, 'rb')#import file
		
	#Check for OS and IO errors
	except OSError as o:
		sys.stderr.write('bordermap file error: %s\n' % o)
		#return

	except IOError as i:
		sys.stderr.write('File open failed: %s\n' % i)
		#return
	
	except FileEmptyError as p:
        	sys.stderr.write('bordermap file error: %s\n' %p)
        	#return
	
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
			fig = plt.figure(1, figsize=(9, 6))
			ax = fig.add_subplot(111)
			title = filename.split('.')[1]
			ax.set_title(title)
			s_color = 'r'
		elif j == 1: #Decision tree for series colors
			s_color = 'b'
		elif j == 2:
			s_color = 'g'
		elif j == 3:
			s_color = 'k'
		elif j == 4:
			s_color = 'c'
		elif j == 5:
			s_color = 'm'
		elif j == 6:
			s_color = 'darkolivegreen'
		elif j == 7:
                        s_color = 'gray'
		elif j == 8:
                        s_color = 'hotpink'
		else:
			s_color = 'maroon'
		
		mean = np.mean(ploty)
		median = np.median(ploty)
		first_quartile = np.percentile(ploty, 25)
		third_quartile = np.percentile(ploty, 75)
		top_one_percent = np.percentile(ploty, 99)
		bottom_one_percent = np.percentile(ploty, 1)
		stats_file = filename + '.stats.txt'
		f = open(stats_file,'w+')
		f.write('mean = ' + str(mean))
		f.write('\nmedian = ' + str(median))
		f.write('\npercentile  1 = ' + str(bottom_one_percent))
		f.write('\npercentile 25 = ' + str(first_quartile))
		f.write('\npercentile 75 = ' + str(third_quartile))
		f.write('\npercentile 99 = ' + str(top_one_percent))
		ax.plot_date(plotx, ploty, color = s_color, alpha = 1, marker = ".", markersize = 3,  label = s_label)
		ax.set_xlabel(x_label)
		ax.set_ylabel(y_label)
		ax.set_ylim([yaxislow, yaxishigh])
		# Choose your xtick format string
		#date_fmt = '%m-%d-%y %H:%M:%S'
		date_fmt = '%m-%d-%y'

		# Use a DateFormatter to set the data to the correct format
		date_formatter = mdate.DateFormatter(date_fmt)
		ax.xaxis.set_major_formatter(date_formatter)

	if j == (number_files-1):
		# Sets the tick labels diagonal so they fit easier.
                ax.legend()
		fig.autofmt_xdate()
		fig.tight_layout()
		output = filename + '.pdf'
		fig.savefig(output)
			
		
