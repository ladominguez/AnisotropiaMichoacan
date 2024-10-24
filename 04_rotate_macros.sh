#!/bin/sh

for north in $(find ./20* -name "*HN.sac" | cut -c 3- );do
	east=$(echo $north | sed 's/HN/HE/g')
	radial=$(echo $north | sed 's/HN/HR/g')
	transversal=$(echo $north | sed 's/HN/HT/g')
	echo "sac << END" 
	echo "read " $north $east
	echo "rmean"
	echo "rtrend"
	echo "rmean"
	echo "rotate to gcp normal"
	echo "write " $radial $transversal
	echo "quit"
	echo "END"
	echo " "
done

echo "sac << END"
echo "read 2*/*HHR*sac"
echo "ch kcmpnm HHR"
echo "wh"
echo "quit"
echo "END"
echo ""

echo "sac << END"
echo "read 2*/*HHT*sac"
echo "ch kcmpnm HHT"
echo "wh"
echo "quit"
echo "END"
echo ""
