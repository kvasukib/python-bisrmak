#check if program running
if ! program="$(ps -aux | grep sc_remoted | grep tka)"; then
	logfile=/project/comcast-ping/bdrmap-bismark/sc_remoted.log.txt
	#echo "not running"
	date
	echo "No program found. Restarting sc_remoted"
	cd /home/agamerog/sockets; rm OW*
	cd /home/agamerog/scamper/scamper-backup-20160718/bin
	./sc_remoted -4 -P 31337 -U /project/comcast-ping/sockets-bismark/ -O tka -O allowother -O allowgroup >> $logfile 2>&1 &
#else
	#date
	#echo "running"
fi 
