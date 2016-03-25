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
#parse bordermap output using Amogh's code
#write routers in array of objects
(routers,interface2rtr,interface2name) = read_bdrmap_file(filename)

#print basic info of router
print "---------------------------------------"
print "id = " + str(routers[router_number].id)
print "owner = " + str(routers[router_number].owner)
temp = "AS" + str(t[i].owner)
#print AS info of router owner

subprocess.call(["whois", "-h", "whois.cymru.com", "-v", temp])
print "relationship = " + str(routers[router_number].rel)
print "interfaces = " 
 
s = []
s = list(routers[router_number].interfaces)
for i in range(len(s)):
	if(s[i].star): #Only print interfaces directly seen in traceroute
		print s[i].ip

#Print information of neighboring routers
t = []
t = list(routers[router_number].neighbors)
print "neighbohr routers = "
for i in range(len(t)):
        #print t[i].owner
	temp = "AS" + str(t[i].owner) 
	#print temp
	subprocess.call(["whois", "-h", "whois.cymru.com", "-v", temp])
	print "--------------"
