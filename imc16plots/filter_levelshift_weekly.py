#usage: python levelshift_plotter.py <far_end_levelshift_filename> <near_levelshift_filename>
#.out files
#Filters far-end levelshifts with overlapping windows
#Flags files with at least 8 levelshifts for further processing
import csv
import numpy as np
import sys
import os
processed = 0 #boolean to determine whether or not a file has been processed 
number_files = 2
filter_window = 900 #number of seconds on either side
#Read all filenames provided
far = []
near = []
priority = '/project/comcast-ping/plots-agamerog/priority_files_weekly.txt'
#for loop discards values of levelshift on far-side with 
#a corresponding shift on the near-side within 30 mins
#on either side

for j in range(number_files):
	#Get information about file from inputs
	far_filename = str(sys.argv[1])
	near_filename = str(sys.argv[2])
	#Probably remove the below once successful run 
	#month = filename.split('.')[2]
	#monitor = filename.split('.')[0]
	#file_path = path + monitor + '/' + month + '/'
	file_path = ''
	if j == 0:
		filename = far_filename
	else:
		filename = near_filename

	try:
		f = open(filename, 'r+')#import file	
	#Check for OS and IO errors
	except OSError as o:
		sys.stderr.write('levelshift file error: %s\n' % o)
		f.close
	except IOError as i:
		sys.stderr.write('File open failed: %s\n' % i)
		f.close
	except FileEmptyError as p:
        	sys.stderr.write('levelshift file error: %s\n' %p)
		f.close
	else:
		sys.stderr.write('reading levelshift file %s\n' % filename)
		reader = csv.reader(f, delimiter='	')
		if j == 0:
			processed = 1
		#Read values from file
		for row in reader: 
			#File has far-end timestamps
			if j == 0: 
				far.append(float(row[0]))#save raw timestamp	
			#Second file with levelshifts 
			else:
				near.append(float(row[0]))
		#print "initial number of values:"
		#print len(far)
		if (len(far) > 0 and len(near) > 0):
			for i in (range(len(far)-1)):
				discard = 0
				try:
					lower = far[i] - filter_window
					upper = far[i] + filter_window
				except IndexError:
					lower = 9999999999
					upper = 9999999999 #If index error, ensure algorithm ignores value
				for k in range(len(near)):
					if (near[k] > lower and near[k] < upper):
						discard = 1
						#print "near = " + str(near[k])
						#print "far = " + str(far[i])
				if discard == 1:
					del far[i]
					#print "discarding value"
		f.close
#Determine action to do on file depending on how many levelshifts 
#dtected (as long as the far-end file was read correctly)

if(processed): 	
	if (len(far) < 2):
		sys.stderr.write('Less than 2 shifts. Ignoring.\n')
	else:
		sys.stderr.write('Potential congestion, adding files to priority list\n')
		g = open(priority, 'a')
		g.write(far_filename)
		g.write('\n')
		g.write(near_filename)
		g.write('\n')
		g.close
		#print "number of values left: "
		#print len(far)
	
