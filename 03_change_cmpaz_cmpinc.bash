#!/bin/sh

for north in $(find ./2* -name "*HN.sac" | cut -c 3- );do
	echo "sac << END" 
	echo "r " $north
	echo "ch cmpinc 90 cmpaz 0 o 0 lcalda true"
	echo "wh" 
	echo "quit"
	echo "END"
	echo " "
done

for east in $(find ./2* -name "*HE.sac" | cut -c 3- );do
	echo "sac << END" 
	echo "rh " $east
	echo "ch cmpinc 90 cmpaz 90 o 0 lcalda true"
	echo "wh" 
	echo "quit"
	echo "END"
	echo " "
done


