#script to analyze output of bordermap in human-readable format

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

filename = str(sys.argv[1])
output_file = filename + ".parsed"
f = open(output_file,'w+')

#parse bordermap output using Amogh's code
#write routers in array of objects
(routers,interface2rtr,interface2name) = read_bdrmap_file(filename)
print("number of routers = " + str(len(routers)))

for j in range(len(routers)):
#for j in range(50):
	#print basic info of router
	f.write("---------------------------------------\n")
	f.write("---------------------------------------\n")
	f.write("---------------------------------------\n")
	f.write("Router ID = " + str(routers[j].id) + '\n')
	f.write("owner = " + str(routers[j].owner))
	f.write('\n')
	temp = "AS" + str(routers[j].owner)
	#print AS info of router owner
	
	#declare buffer / empty for next use
	output = bytearray()
	
	#Query whois database for AS number seen in router
	output = subprocess.check_output(["whois", "-h", "whois.cymru.com", "-v", temp])
	
	f.write("relationship = " + str(routers[j].rel))
	f.write("\n")
	f.write(str(output))
	f.write("interfaces = ")
	f.write('\n')
	
	#Print interfaces
	s = []
	s = list(routers[j].interfaces)
	for i in range(len(s)):
		if(s[i].star): #Only print interfaces directly seen in traceroute
			f.write(s[i].ip)
			f.write('\n')

	#Print information of neighboring routers
	t = []
	t = list(routers[j].neighbors)
	#print ("this is t\n")
	#print (t)
	f.write("\nneighbor routers:\n")
	for k in range(len(t)):
		#print t[i].owner
		f.write("Neighbor ID = " + str(t[k].id) + '\n')
		temp = "AS" + str(t[k].owner) 
		#print AS name (owner) to file
		output = bytearray()
		output = subprocess.check_output(["whois", "-h", "whois.cymru.com", "-v", temp])
		f.write(str(output))
		f.write('\n')
f.close()
