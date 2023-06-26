#!/usr/bin/bash

for SERVER in server{a,b}
do
	echo "SERVER disk usage"
	ssh $SERVER df -h /
	echo ""
done
