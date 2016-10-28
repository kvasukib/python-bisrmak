#v1.0
#script to print out routers and interfaces of a desired carrier
#Oputput: routers (near and far end) and interfaces to AS
#input: bordermap parsed filename, asnumber, asname (examples below)
#python single_interface_plotter.py <filename> <as_n> <as_name>
#python single_interface_plotter.py mry-us.201512.router-blocks 2906 Netflix
import sys
import re
import os
import getopt
import subprocess
#import plot_link
from sets import Set
from  myexceptions import *
from bdrmap_parse import * 
from siblings_AS_verifier import *

routers = []
interface2rtr = {}
interface2name = {}

far_filename_list = []
far_plotter_list = []
far_plotting_list = []
far_ip_list = []
far_filename_list = []
far_plotter_list = []
far_ip_tags = []
#get filename and desired AS number from user
filename = str(sys.argv[1])
asname = str(sys.argv[3]) #AS name string
asn = int(sys.argv[2])

mon = filename.split('.')[0] #Monitor name
dates = filename.split('.')[1] #dates in yyyymm format

#Specify directory to save output files.
#Script will save at dir/mon_name/yyyymm
file_path = '/project/comcast-ping/plots-agamerog/' + mon + '/' + dates + '/'
filename = file_path + str(sys.argv[1])
#parse bordermap output using Amogh's code
#write routers in array of objects
file_read = 0 #boolean for file errors 

proceed = 0 #boolean to store whether or not VP router is connected to desired AS
non_empty_near_end = 0

far_plotting_list = []
far = 0 #boolean - non-empty far-side interface files
file_prefix = mon + "." + str(asname) + "." + dates + "."
#File for storing interfaces from router-blocks
summary_filename = file_path + mon + "." + str(asname) + "." + dates + ".interfaces.txt" 
try:
        (routers,interface2rtr,interface2name) = read_bdrmap_file(filename)
        file_read = 1
	os.remove(summary_filename)
except OSError or FileEmptyError or FileEmptyError or IOError:
        file_read = 0
        print ("error opening file: " + filename)
summary_file = open(summary_filename, 'a+') 


if (file_read):
	near_ends = []
	non_empty_near_end = 0
	#first find all the near-end routers
	for loop_counter in range(len(routers)):
		router_owner = int(routers[loop_counter].owner)
		if as_verifier(router_owner,mon) == 1:
			near_ends.append(routers[loop_counter])	
			non_empty_near_end = 1
 
if(non_empty_near_end):	 
	for j in range(len(near_ends)):
		far_ip_tags = [] #this list needs resetting per router
		#t has list of neighbor router objects
		proceed = 0 #booleans for non-empty output near and far side
		far = 0
		plot = 0
		m = 0
		i = 0
		t = []
		t = list(near_ends[j].neighbors)
	
		for k in range(len(t)):
		#look for neighbor routers owned by desired AS
		#for those routers, look for starred interfaces
		#if at least one starred present, continue 

			if( int(t[k].owner) == asn): 
				r = []
				r = list(t[k].interfaces)
				for l in range(len(r)):
					if(r[l].star):
						proceed = 1
		
		#look for desired interfaces and write to file
		if(proceed):
	
			for k in range(len(t)):

				#for all neighbor routers
				#check if it belongs to desired AS
				if( int(t[k].owner) == asn ):

					#Get far-end interfaces (IP) for those routers and append to file
					r = []
					r = list(t[k].interfaces)

					for l in range(len(r)):
						if r[l].ip not in far_ip_list:
							far_ip_list.append(r[l].ip)
							print r[l].ip
							summary_file.write(str(r[l].ip))
							summary_file.write("\n")
							#Use IP address in format AAABBBCCCDDD (force left zeroes)
							IP = str(r[l].ip)
							A = (IP.split(".")[0]).zfill(3) 
							B = (IP.split(".")[1]).zfill(3)
							C = (IP.split(".")[2]).zfill(3)
							D = (IP.split(".")[3]).zfill(3)
							far_ip = A + B + C + D
							#filename format: mon.AS.dates.router_id.farN		
							ip_file = file_prefix + far_ip + ".far"
							far_ip_tags.append(far_ip)
							far_filename_list.append(ip_file)
			
			#Now we query the database for those IP addresses in date range
			#For that we need a text file with the IP address to query
			#continue if at least one query yields non-empty output
			#for m in range(len(far_ip_list)):
			while ( (m < len(far_ip_list))):
				#verify if file has been queried already. If so, ignore.
				ip_filename = file_path + str(far_filename_list[m])
				output_file = ip_filename + ".ts"
				try:
        				file_present = subprocess.check_call(["ls", output_file])
        				print "file already present, ignoring"
				except:
        				print "file NOT present, querying"
					ip_formatted = str(far_ip_list[m])
					g = open(ip_filename,'w+')
					g.write(ip_formatted)
					g.close()
					#nothing = subprocess.call(["echo", ip_formatted, ">", str(far_filename_list[m])])
					#print nothing
					output = bytearray()
					output = subprocess.check_output(["perl", \
"/home/agamerog/imc/bismark_create_ts.pl", mon, ip_filename, dates])
					if len(output) > 0:
						far = 1
						output_file = ip_filename + ".ts"
						f = open(output_file,'w+')
						f.write(output)
						f.close()
						far_plotter_list.append(output_file)
					else:
						os.remove(ip_filename)
				m = m+1 #loop counter

		#Look for interfaces on the near-end to plot
		if(far):
		#if(0):
			#s has list of interfaces of near-side router
			s = []
			s = list(near_ends[j].interfaces)
			near_plotter_list = []
			for i in range(len(s)):
				if(s[i].star):
				#In the starred interfaces, look for those not queried yet
					IPN = str(s[i].ip)
                                        AN = (IPN.split(".")[0]).zfill(3)
                                        BN = (IPN.split(".")[1]).zfill(3)
                                        CN = (IPN.split(".")[2]).zfill(3)
                                        DN = (IPN.split(".")[3]).zfill(3)
                                        near_suffix = AN + BN + CN + DN
                                        ip_formatted = str(s[i].ip)
					#For each far-end, find all the near-ends below. Query those preveiously unqueried
					for n in range(len(far_ip_tags)):
                                                output_file = file_path + \
file_prefix + far_ip_tags[n] + "." + near_suffix + ".ts"
                                        	ip_filename = file_path + \
file_prefix + far_ip_tags[n] + "." + near_suffix
						verifier = "ls " + file_path + "*" + near_suffix + ".ts"
						proc = subprocess.Popen( verifier, shell=True, \
stdout=subprocess.PIPE, stderr=subprocess.PIPE)
						out,err = proc.communicate()
						if len(out > 1):
							print "file already queried, copying to this file"
							line = str(out)
							file_to_copy = line.splitlines()[0]
							copying_command = "cp " + file_to_copy + " " + output_file
							try:
								proc = subprocess.Popen( copying_command, shell=True, \
	stdout=subprocess.PIPE, stderr=subprocess.PIPE)
							except:
								print "error copying file"			
							continue
						#If near_end hasn't been queried before, query it now
						h = open(ip_filename,'w+')
						h.write(ip_formatted)
						h.close()	
						output = bytearray()
						output = subprocess.check_output(["perl", \
"/home/agamerog/imc/bismark_create_ts.pl", mon, ip_filename, dates])
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
			#extract first filenames from arrays into char buffer. 
			#then use as_plot_all.py to plot time-series
			#which takes just the filename (no path information)
			#only the first near-interface found will be plotted
			plotter = ''
			plotter = plotter + str(far_plotter_list[0]).split('/')[-1]
			plotter = plotter + ' ' + str(near_plotter_list[0]).split('/')[-1]
			try:
				nothing = subprocess.check_output(["python","/home/agamerog/imc/as_plot_all.py",plotter])
			except:
				print("could not plot files " + plotter) 
			#print(plotter)
