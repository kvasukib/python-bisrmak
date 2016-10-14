# Kean Freeman
# Script to run parser-levelshift.py on all .ts files in monitor files in 
# /plots-agamerog/

# Import
import pdb
import os
import subprocess

# Global
monitorListFile = \
'/home/amogh/projects/comcast_ping/code/sync/monitor_list_samples.txt'
plotsAgamerogDir = \
'/project/comcast-ping/plots-agamerog/'
parserLevelshiftScript = \
'/home/agamerog/pythoncode/python-bisrmak/parser-levelshift.py'
bMonitors = [ 'OWC43DC7A3EDEC', 'OWE8DE27B72366', 'OW744401937CAA', \
'OWA021B7A9BE39', 'OWA021B7A9BF95', 'OWC43DC79D8EBC', 'OWC43DC7A3EE22',
'OWC43DC7A3F0D4', 'OWE8DE27B708D2', 'OWE8DE27B72513', 'OW04A151A3102E',
'OWC43DC7A3EE34', 'OW74440171A157', 'OW2CB05D873788', 'OWC43DC7B0AE78',
'OW04A151A310A9']

# Main
monitors = bMonitors
with open(monitorListFile) as monitorList:
	for monitor in monitorList:
		monitors.append(monitor[:-1])
tsFileDirs = []
for monitor in monitors:
	if os.path.isdir(plotsAgamerogDir + monitor):
		try:
			with open(os.devnull, 'w') as devnull:
				tsFileDirs += (subprocess.check_output('find ' + \
plotsAgamerogDir + monitor + '/*/*.ts', shell=True, \
stderr=devnull)).split('\n')
		except:
			continue
	else:
		print 'Monitor ' + monitor + ' folder doesn\'t exist'
# Remove invalid files
remove = []
for ts in tsFileDirs:
	if '.ts' not in ts or '.png' in ts or '.txt' in ts or '.ls' in ts or \
'.out' in ts or '.stats' in ts:
		remove.append(ts)
for i in remove:
	tsFileDirs.remove(i)

# completedSHFolders holds strings of monitor + date pairs, to tell if 
# that folder has already been processed and can be skipped
completedSHFolders = []
for ts in tsFileDirs:
	
	## To run only k_month_levelshift_filtering.sh and skip the 
	## parsing, comment out the next 3 lines.
	print 'Processing ' + ts.split('/')[-1]
	commandString = 'python ' + parserLevelshiftScript + ' ' + ts
	os.system(commandString)
print 'Finished converting .ts files'
