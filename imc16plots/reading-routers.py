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
print len(routers)
for j in range(len(routers)):
#print basic info of router
	f.write("---------------------------------------\n")
	f.write("Router ID = " + str(routers[j].id) + '\n')
	f.write("owner = " + str(routers[j].owner))
	f.write('\n')
	temp = "AS" + str(routers[j].owner)
	#print AS info of router owner

	f.seek(0, os.SEEK_END)
	subprocess.call(["whois", "-h", "whois.cymru.com", "-v", temp, "2>/dev/null"], stdout = f)

	f.write("relationship = " + str(routers[router_number].rel))
	f.write("\n")
	f.write("interfaces = ")
	f.write('\n')
	 
	s = []
	s = list(routers[router_number].interfaces)
	for i in range(len(s)):
		if(s[i].star): #Only print interfaces directly seen in traceroute
			f.write(s[i].ip)
			f.write('\n')

	#Print information of neighboring routers
	t = []
	t = list(routers[router_number].neighbors)
	f.write("neighbor routers = \n")
	for k in range(len(t)):
		#print t[i].owner
		temp = "AS" + str(t[k].owner) 
		#print AS name (owner) to file
		f.seek(0, os.SEEK_END)
		subprocess.call(["whois", "-h", "whois.cymru.com", "-v", temp], stdout=f)
		f.seek(0, os.SEEK_END)
		f.write("---------------------------------------\n")
f.close()
