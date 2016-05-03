mon="OWC43DC7A3EDEC"
#check if socket exists
#echo "cp 0"
if socket="$(ls /project/comcast-ping/sockets-bismark/ | grep $mon)"; then
	#check if program running
	#echo "cp 1"
	if ! program="$(ps -aux | grep sc_bdrmap | grep $mon)"; then
		#echo "cp 1"
		#no sc_bdrmap running. gzip warts, run bdrmap, update state
		if [ "$(ls /project/comcast-ping/bdrmap-bismark/$mon/warts/ | grep *.warts | wc -l)" -gt 0 ]; then
			gzip -f /project/comcast-ping/bdrmap-bismark/$mon/warts/*.warts;
		fi
		if [ "$(ls /project/comcast-ping/bdrmap-bismark/$mon/warts/ | grep *.log | wc -l)" -gt 0 ]; then
			gzip -f /project/comcast-ping/bdrmap-bismark/$mon/warts/*.log;
		fi
		#echo "cp 2"
		dat=`date +%s`
		outfile=/project/comcast-ping/bdrmap-bismark/$mon/warts/${mon}.${dat}.bdrmap.warts
		logfile=/project/comcast-ping/bdrmap-bismark/$mon/warts/${mon}.${dat}.bdrmap.log
		#echo "cp 3"
		~/bdrmap/sc_bdrmap -a ~/plots/current.prefix2as -v ~/plots/siblings/${mon}.sibling.txt -x ~/plots/current.peering -R ~/sockets/${socket} -o $outfile > $logfile 2>&1 &
		#echo $(pgrep -f ${mon}.sibling.txt) > /project/comcast-ping/sockets-bismark/state_files/$mon-pid
		echo $socket > /project/comcast-ping/sockets-bismark/state_files/$mon-socket
	else
		#program running, check if socket file exists
		if state="$(cat /project/comcast-ping/sockets-bismark/state_files/$mon-socket)"; then 
			#diff socket file with current Unix socket
			if [ "$state" != "$socket" ]; then
				#echo "cp 4"
				#socket and file are different, kill existing bordermap process and start new
				#update state files for pid and Unix socket. gzip any bordermap files. 
				#(if socket and file are the same, do nothing)
				if pid="$(pgrep -f ${mon}.sibling.txt)"; then
					kill $pid
				fi
				if [ "$(ls /project/comcast-ping/bdrmap-bismark/$mon/warts/*.warts | wc -l)" -gt 0 ]; then
                        		gzip -f /project/comcast-ping/bdrmap-bismark/$mon/warts/*.warts;
                		fi
                		if [ "$(ls /project/comcast-ping/bdrmap-bismark/$mon/warts/*.log | wc -l)" -gt 0 ]; then
                        		gzip -f /project/comcast-ping/bdrmap-bismark/$mon/warts/*.log;
                		fi
				dat=`date +%s`
				outfile=/project/comcast-ping/bdrmap-bismark/$mon/warts/${mon}.${dat}.bdrmap.warts
				logfile=/project/comcast-ping/bdrmap-bismark/$mon/warts/${mon}.${dat}.bdrmap.log
				~/bdrmap/sc_bdrmap -a ~/plots/current.prefix2as -v ~/plots/siblings/${mon}.sibling.txt -x ~/plots/current.peering -R ~/sockets/${socket} -o $outfile > $logfile 2>&1 &
				#echo $(pgrep -f ${mon}.sibling.txt) > /project/comcast-ping/sockets-bismark/state_files/$mon-pid
				echo $socket > /project/comcast-ping/sockets-bismark/state_files/$mon-socket
			fi	
		else
			#socket file does not exist. (kill and re)start bordermap, update state files, gzip warts
			if pid="$(pgrep -f ${mon}.sibling.txt)"; then
                        	kill $pid
                        fi
			if [ "$(ls /project/comcast-ping/bdrmap-bismark/$mon/warts/*.warts | wc -l)" -gt 0 ]; then
                        	gzip -f /project/comcast-ping/bdrmap-bismark/$mon/warts/*.warts;
                	fi
                	if [ "$(ls /project/comcast-ping/bdrmap-bismark/$mon/warts/*.log | wc -l)" -gt 0 ]; then
                        	gzip -f /project/comcast-ping/bdrmap-bismark/$mon/warts/*.log;
                	fi
			dat=`date +%s`
			outfile=/project/comcast-ping/bdrmap-bismark/$mon/warts/${mon}.${dat}.bdrmap.warts
			logfile=/project/comcast-ping/bdrmap-bismark/$mon/warts/${mon}.${dat}.bdrmap.log
			~/bdrmap/sc_bdrmap -a ~/plots/current.prefix2as -v ~/plots/siblings/${mon}.sibling.txt -x ~/plots/current.peering -R ~/sockets/${socket} -o $outfile > $logfile 2>&1 &	
			#echo $(pgrep -f ${mon}.sibling.txt) > /project/comcast-ping/sockets-bismark/state_files/$mon-pid
			echo $socket > /project/comcast-ping/sockets-bismark/state_files/$mon-socket
		fi
	fi
else
	#no Unix socket. Halt any existing bordermap process, and clean pid & socket files.
	if pid="$(pgrep -f ${mon}.sibling.txt)"; then
        	kill $pid
        fi
	if state="$(cat /project/comcast-ping/sockets-bismark/state_files/$mon-socket)"; then
		> /project/comcast-ping/sockets-bismark/state_files/$mon-socket	
	fi
	if [ "$(ls /project/comcast-ping/bdrmap-bismark/$mon/warts/*.warts | wc -l)" -gt 0 ]; then
        	gzip -f /project/comcast-ping/bdrmap-bismark/$mon/warts/*.warts;
        fi
        if [ "$(ls /project/comcast-ping/bdrmap-bismark/$mon/warts/*.log | wc -l)" -gt 0 ]; then
                gzip -f /project/comcast-ping/bdrmap-bismark/$mon/warts/*.log;
        fi
fi
