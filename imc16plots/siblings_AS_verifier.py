#Script to verify if an AS is in a siblings file for a given monitor
#Oputput: boolean: 1 if AS is in file. 0 if it is NOT or there is an error
#input: asnumber, monitor name (examples below)
#python siblings_AS_verifier.py <as_n> <monitor>
#python siblings_AS_verifier.py 15169 bed-us
import sys
import re
import os
import getopt
import subprocess
#import plot_link
from sets import Set
import csv

path = "/project/comcast-ping/TSP/adaptive/siblings/"
def as_verifier(asn,monitor):

	file_name = path + monitor + ".sibling.txt"
	try:
		f = open(file_name, 'rb')#import file

	#Check for OS and IO errors
	except OSError as o:
		sys.stderr.write('siblings file error: %s\n' % o)
		return 0

	except IOError as i:
		sys.stderr.write('File open failed: %s\n' % i)
		return 0

	except FileEmptyError as p:
		sys.stderr.write('siglings file error: %s\n' %p)
		return 0

	else:
		reader = csv.reader(f, delimiter=' ')
		for row in reader:
			as_row = int(row[0])
			if asn == as_row:
				return 1 #asn IS in siblings file
	return 0 #asn is NOT in siblings file 
