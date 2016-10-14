#usage: python levelshift_plotter.py "<time_series_filename> <levelshift_filename>"
#.ts and .out respectively
#Plots time-series files and detected levelshifts. Used to calibrate levelshift -B and -L parameters
#outputs plot with first filename and .out.png extension
import csv , matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pylab import rcParams, figure, axes, pie, title, show
import sys
import os
import datetime as dt
import matplotlib.dates as mdate

#Specify directory to save output files.
#Script will save at dir/mon_name/yyyymm
#path = '/project/comcast-ping/plots-agamerog/'
path = ''
x_label = 'Date and Time'
y_label = 'rtt (ms)'
yaxislow = 0
yaxishigh = 500
in_files = str(sys.argv[1])
number_files = in_files.count(' ') + 1

#number_files = len(sys.argv) - 1
#Plots 1-6 time series files, latency vs. time
if (number_files == 0):
	sys.stderr.write('No files were provided\n') 
elif (number_files > 2):
	sys.stderr.write('more than 2 files provided. Will plot first 2. files provided:')
	sys.stderr.write(str(sys.argv[1]))
	number_files = 2

#Read all filenames provided
for j in range(number_files): 
	plotx = []
	ploty = []
	#Get information about file from inputs
	filename = in_files.split(' ')[j]
	
	#series labels
	if j == 0: 
		#s_label = filename.split('.')[-2]
		#s_label = s_label[:-1] #remove interface # from label
		s_label = 'time-series'
	else:
		s_label = 'levelshift'

	month = filename.split('.')[2]
	monitor = filename.split('.')[0]
	#file_path = path + monitor + '/' + month + '/'
	file_path = ''
	filename = file_path + in_files.split(' ')[j]
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
		if j == 0: #space-separated file
                	reader = csv.reader(f, delimiter=' ') #read file into variable reader
		else: 
			reader = csv.reader(f, delimiter='	')
		#Read values from file
		for row in reader: 
			secs = mdate.epoch2num(float(row[0]))
			
			#First file with time-series
			if j == 0: 
				y = (int(row[1]))
			
			#Second file with levelshifts 
			else:
				y = (abs(int(float(row[2]))))*10 #to use same vertical axis 		
			plotx.append(secs)
			ploty.append(y)

		#Change plot options
		#print plotx[0]
		if j == 0: 
			fig = plt.figure(1, figsize=(9, 6))
			ax = fig.add_subplot(111)
			title = filename.split('.')[0] + ' <---> ' + filename.split('.')[1]
			ax.set_title(title)
			s_color = 'r'
		elif j == 1: #Decision tree for series colors
			s_color = 'b'
		
		#bigger marker for levelshift
		ax.plot_date(plotx, ploty, color = s_color, alpha = 0.7, \
			marker = ".", markersize = (j*5+3),  label = s_label) 
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
		output = filename + '.png'
		fig.savefig(output)
		#output = filename + '.pdf'
                #fig.savefig(output)
			
		
