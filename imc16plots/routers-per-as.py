#script to print out routers and interfaces of a desired carrier
#Oputput: routers (near and far end) and interfaces to AS
#input: bordermap parsed file, desired AS number
import sys
import re
import os
import getopt
import subprocess
from sets import Set
from  myexceptions import *
from bdrmap_parse import * 
router_number = 0

routers = []
interface2rtr = {}
interface2name = {}

#get filename and desired AS number from user
filename = str(sys.argv[1])
asn = int(sys.argv[2])
output_file = filename + ".AS" + str(asn)
f = open(output_file,'w+')

#parse bordermap output using Amogh's code
#write routers in array of objects
(routers,interface2rtr,interface2name) = read_bdrmap_file(filename)
print("number of routers = " + str(len(routers)))
interface_counter = 0
for j in range(len(routers)):
#for j in range(3):
	#t has list of neighbor router objects
	t = []
	t = list(routers[j].neighbors)

	#crawl list of neighbors looking for desired AS
	for k in range(len(t)):
		
		#look for neighbor routers owned by desired AS
		#print(t[k].owner)
		if( int(t[k].owner) == asn):  
			f.write("---------------------------------------\n")
			f.write("NEAR-side interfaces\n")
			
			#s has list of interfaces of near-side router
			s = []
        		s = list(routers[j].interfaces)
        		for i in range(len(s)):

				#check if interface has been seen on tracerout
                		if(s[i].star):
                        		f.write(s[i].ip)
                        		f.write('\n')
			f.write("neighbor relationship = " + str(t[k].rel) + "\n")
			f.write("FAR-side interfaces\n")
			r = list(t[k].interfaces)
			for l in range(len(r)):
				if(r[l].star):
					f.write(r[l].ip)
					f.write('\n')
					interface_counter += 1
f.write("\n\n Number of interfaces = " + str(interface_counter) + "\n")
f.close()
