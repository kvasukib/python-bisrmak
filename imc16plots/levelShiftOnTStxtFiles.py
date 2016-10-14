# Kean Freeman
# Runs the levelshift executable (from this directory) on all 
# *.ls.txt files in the monitor folders

# Import
import pdb
import os
import subprocess
from multiprocessing import Pool

# Global
monitorListFile = \
'/home/amogh/projects/comcast_ping/code/sync/monitor_list_samples.txt'
plotsAgamerogDir = \
'/project/comcast-ping/plots-agamerog/'
levelshiftExecutable = \
'/home/freeman/testing/levelShiftStuff/levelshift'
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

lsFileDirs = []
# Collect *.ls.txt files in monitor folders
for monitor in monitors:
	if os.path.isdir(plotsAgamerogDir + monitor):
		try:
			# Suppresses error message if no subdirectory
			with open(os.devnull, 'w') as devnull:
				lsFileDirs += (subprocess.check_output('find ' + \
plotsAgamerogDir + monitor + '/*/*.ls.txt', shell=True, \
stderr=devnull)).split('\n')
		except:
			continue
	else:
		print 'Monitor ' + monitor + ' folder doesn\'t exist'

# Remove invalid files
remove = []
for ls in lsFileDirs:
	if '.ls' not in ls:
		remove.append(ls)
for i in remove:
	lsFileDirs.remove(i)

# Run levelshift on every file in lsFileDirs
myPool = Pool(12)
commandsList = []
for ls in lsFileDirs:
	outputFileName = ls + '.out'
	command = 'cat ' + ls + ' | ' + levelshiftExecutable + \
' -B 300 -L 12 > ' + outputFileName
	print 'Creating ' + outputFileName
	commandsList.append(command)
	myPool.apply_async(os.system(command))
myPool.join()
print 'Finished'
