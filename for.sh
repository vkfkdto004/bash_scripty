#!/usr/bin/bash

for i in $(cat /tmp/list.txt) 
do
	ssh $i hostname
done
