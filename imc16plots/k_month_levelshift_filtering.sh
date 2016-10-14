#crawler to filter far-end files using corresponding
#near-end files
ls *far*out > ~/far_list.txt
for i in `cat ~/far_list.txt`;
do
 ID="$(echo $i | awk -F"." '{print $4}')"
 for j in `ls *near*out | grep $ID`;
 do
  python /home/agamerog/pythoncode/python-bisrmak/imc16plots/filter_levelshift.py $i $j 
 done
done
