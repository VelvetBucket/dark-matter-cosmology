#!/bin/bash

cards_dir="./cards1/"
param_cards=($(ls "$cards_dir"))

i=1
sp_number=${#param_cards[@]}

# Running over each card
for card in "${param_cards[@]}"
do	
	echo "param_card $i of $sp_number"
	
	cp "$cards_dir$card" "/home/crisanto/Desktop/DarkMatterCosmology/micromegas_6.3.0/scotogenic/SPheno.spc.Scotogenic"
	cd /home/crisanto/Desktop/DarkMatterCosmology/micromegas_6.3.0/scotogenic/
	./main data.par SPheno.spc.Scotogenic
	cp "./m1T-1_vs_sigmaV.txt" "/home/crisanto/Desktop/DarkMatterCosmology/MG5_aMC_v3_6_7/MY_TESTING/micromegas_output/m1T-1_vs_sigmaV-slow/$card"
	cd /home/crisanto/Desktop/DarkMatterCosmology/MG5_aMC_v3_6_7/MY_TESTING/
	
	let "i++"
done
