#crawler to filter far-end files using corresponding
#near-end files
ls *far*out > /tmp/far_list.txt
for i in `cat /tmp/far_list.txt`;
do
ID="$(echo $i | awk -F"." '{print $4}')"
NEAR="$(ls *near*out | grep $ID)"
python ~/imc/filter_levelshift.py $i $NEAR 
done
