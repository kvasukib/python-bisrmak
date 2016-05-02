#script to print out routers and interfaces of a desired carrier
#Oputput: routers (near and far end) and interfaces to AS
#input: bordermap parsed file, desired AS number
import sys
import re
import os
import getopt
import subprocess
#import plot_link
from sets import Set
from  myexceptions import *
from bdrmap_parse import * 

routers = []
interface2rtr = {}
interface2name = {}

#get filename and desired AS number from user
filename = str(sys.argv[1])
asn = int(sys.argv[2])#AS Number
mon = str(sys.argv[3]) #Monitor name
dates = str(sys.argv[4]) #dates in yyyymm format
asname = str(sys.argv[5]) #AS name string

#Specify directory to save output files.
#Script will save at dir/mon_name/yyyymm
file_path = '/project/comcast-ping/plots-agamerog/' + mon + '/' + dates + '/'
filename = file_path + str(sys.argv[1])
#parse bordermap output using Amogh's code
#write routers in array of objects
(routers,interface2rtr,interface2name) = read_bdrmap_file(filename)
proceed = 0 #boolean to store whether or not VP router is connected to desired AS

far_plotting_list = []
far = 0 #boolean - non-empty far-side interface files
file_prefix = mon + "." + str(asname) + "." + dates + "."

#cycles for troubleshooting
#       if(int(routers[j].id)==712):
#               temp = j
#for j in range(500):
 
for j in range(len(routers)):
	#t has list of neighbor router objects
	proceed = 0 #booleans for non-empty output near and far side
	far = 0
	plot = 0

	t = []
	t = list(routers[j].neighbors)

	#crawl list of neighbors looking for desired AS
	for k in range(len(t)):
	#look for neighbor routers owned by desired AS
	#for those routers, look for starred interfaces
	#if at least one starred present, continue 
		#print(t[k].owner)
		if( int(t[k].owner) == asn): 
			r = []
			r = list(t[k].interfaces)
			for l in range(len(r)):
				if(r[l].star):
					proceed = 1
	
	#look for desired interfaces and write to file
	if(proceed):
		far_ip_list = []
		far_filename_list = []
		far_plotter_list = []
		for k in range(len(t)):

                        #for all neighbor routers
                        #check if it belongs to desired AS
                        if( int(t[k].owner) == asn ):

                                #Get far-end interfaces (IP) for those routers and append to file
                                r = []
                                r = list(t[k].interfaces)

                                for l in range(len(r)):
				
					#For Akamai, look at non-starred interfaces as well
                                        if(r[l].star or asn == 20940):
                                                far_ip_list.append(r[l].ip)
						#mon.AS.dates.router_id.farN		
						ip_file = file_prefix + str(routers[j].id) + ".far" + str((l+1))
						far_filename_list.append(ip_file)
		#Now we query the database for those IP addresses in date range
		#For that we need a text file with the IP address to query
		#continue if at least one queary yields non-empty output
		for m in range(len(far_ip_list)):
			ip_formatted = str(far_ip_list[m])
			ip_filename = file_path + str(far_filename_list[m])
			g = open(ip_filename,'w+')
			g.write(ip_formatted)
			g.close()
			#nothing = subprocess.call(["echo", ip_formatted, ">", str(far_filename_list[m])])
			#print nothing
        		output = bytearray()
			output = subprocess.check_output(["perl", "create_ts.pl", mon, ip_filename, dates])
			if len(output) > 0:
				far = 1
				output_file = ip_filename + ".ts"
				f = open(output_file,'w+')
				f.write(output)
				f.close()
				far_plotter_list.append(output_file)
			else:
				os.remove(ip_filename)
	
	#Look for interfaces on the near-end to plot
	if(far):
	#if(0):
		#s has list of interfaces of near-side router
		s = []
		s = list(routers[j].interfaces)
		near_plotter_list = []
		for i in range(len(s)):
			if(s[i].star):
				ip_formatted = str(s[i].ip)
				ip_filename = file_path + file_prefix + str(routers[j].id) + ".near" + str((i+1))
				h = open(ip_filename,'w+')
				h.write(ip_formatted)
				h.close()
				#nothing = subprocess.call(["echo", ip_formatted, ">", str(far_filename_list[m])])
				#print nothing
				output = bytearray()
				output = subprocess.check_output(["perl", "create_ts.pl", mon, ip_filename, dates])
				if len(output) > 0:
					plot = 1
					output_file = ip_filename + ".ts"
					f = open(output_file,'w+')
					f.write(output)
					f.close()
					near_plotter_list.append(output_file)
				else:
					os.remove(ip_filename)
	
	if(plot):
	#if(1):
		#extract filenames from arrays into char buffer. 
		#then use as_plot_all.py to plot time-series
		#which takes just the filename (no path information)
		plotter = ''
		for i in range(len(far_plotter_list)):
			if i == 0:
				plotter = plotter + str(far_plotter_list[i]).split('/')[-1]
			else:
				plotter = plotter + ' ' + str(far_plotter_list[i]).split('/')[-1]
		for i in range(len(near_plotter_list)):
                       plotter = plotter + ' ' + str(near_plotter_list[i]).split('/')[-1]
		nothing = subprocess.check_output(["python","as_plot_all.py",plotter])
		#print(plotter)
		print(nothing)
		
