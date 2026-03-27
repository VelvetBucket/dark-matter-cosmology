#!/bin/bash

cards_dir="./cards/"
param_cards=($(ls "$cards_dir"))

i=1
sp_number=${#param_cards[@]}

# Running over each card
for card in "${param_cards[@]}"
do	
	echo "param_card $i of $sp_number"
	
	cp "$cards_dir$card" "/home/crisanto/Desktop/micromegas_6.3.0/scotogenic/SPheno.spc.Scotogenic"
	cd /home/crisanto/Desktop/micromegas_6.3.0/scotogenic/
	./main data.par SPheno.spc.Scotogenic
	cp "./m1T-1_vs_sigmaV.txt" "/home/crisanto/Desktop/MG5_aMC_v3_6_6/MY_TESTING1/micromegas_output/m1T-1_vs_sigmaV-0500/$card"
	cd /home/crisanto/Desktop/MG5_aMC_v3_6_6/MY_TESTING1/
	
	let "i++"
done
