# Kean Freeman
# Assumes that processMonData.py has been run, runs either 
# single_interface_plotter.py or bismark_plotter.py on every month of that 
# monitor's router-block data, depending on whether 
# the monitor is a bismark monitor or an Ark monitor

# Imports
import os
import pdb
import subprocess
from multiprocessing import Pool

# Globals
#
# Dictionary used for remembering ASNs for AS's
ASNs = { 'Netflix':2906, 'Google':15169, 'Akamai':20940, 'Cogent':174, \
'Level3':3356, 'Tata':6453 }
#
# List that contains the names of all the Bismark Monitors
bMonitors = [ 'OWC43DC7A3EDEC', 'OWE8DE27B72366', 'OW744401937CAA', \
'OWA021B7A9BE39', 'OWA021B7A9BF95', 'OWC43DC79D8EBC', 'OWC43DC7A3EE22',
'OWC43DC7A3F0D4', 'OWE8DE27B708D2', 'OWE8DE27B72513', 'OW04A151A3102E',
'OWC43DC7A3EE34', 'OW74440171A157', 'OW2CB05D873788', 'OWC43DC7B0AE78',
'OW04A151A310A9']
#
# Directories
arkMonitorListDir = \
'/home/amogh/projects/comcast_ping/code/sync/monitor_list_samples.txt'
plotsAgamerogDir = \
'/project/comcast-ping/plots-agamerog/'
interfacePlotterDir = \
'/home/agamerog/pythoncode/python-bisrmak/imc16plots/'

# Helper Functions

# Main
#
def main():
	# Unify monitors into 1 monitor list
	monitorList = []
	monitorList += bMonitors
	with open(arkMonitorListDir) as arkMonitors:
		for monitor in arkMonitors:
			# Removes newline char
			monitorList.append(monitor[:-1])
	
	# Find every router-blocks folder within these folders
	routerBlocks = []
	for monitor in monitorList:
		if os.path.isdir(plotsAgamerogDir + monitor):
			routerBlocks += (subprocess.check_output('find ' + \
plotsAgamerogDir + monitor + '/*/*.router-blocks', shell=True)).split('\n')
		else:
			print 'Monitor ' + monitor + ' folder doesn\'t exist'
	
	# Make sure every element is a router-blocks file
	routerBlocksCopy = routerBlocks
	for block in routerBlocksCopy:
		if '.router-blocks' not in block:
			routerBlocks.remove(block)
	# For each item in routerBlocks, either single_interface_plotter.py or 
	# bismark_plotter.py needs to be run on it (depending on whether the 
	# monitor name is in bMonitors or not). Each one needs to be run with 
	# each AS name, of which there are 6. This should be done with parallel
	
	myPool = Pool(15)
	commandsList = []
	for block in routerBlocks:
		if '201607' not in block:
			continue
		splitted = block.split('/')
		fileName = splitted[6]
		for AS in ASNs:
			commandsList.append('python ' + interfacePlotterDir + \
'single_interface_plotter.py ' + fileName + ' ' + str(ASNs[AS]) + \
' ' + AS)

	print 'Converting router-blocks to .ts files...'
	myPool.map(os.system, commandsList)
	print 'Done'
	
main()
