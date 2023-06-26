#!/usr/bin/bash

function u1()
{
systemctl status httpd > /dev/null
status_result=$?

## start httpd
if  [ $status_result -eq 0 ]
then
	echo "httpd daemon started"
else
	echo "httpd daemon stopped"
	systemctl start httpd
	sleep 3
	systemctl status httpd > /dev/null
	status_result=$?
       	if [ $status_result -eq 0]
	then
		echo "httpd daemon restarted"
	else
		echo "httpd daemon stopped"
	fi		
fi
}
function u2()
{
###print server hostname
for i in $(cat /tmp/list.txt)
do 
	echo "$i host name=$i"
	ssh $i hostname
	echo ""
done
}

u1   #start httpd daemon
u2   #print hostname (/tmp/list.txt)
