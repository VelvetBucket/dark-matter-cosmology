#!/bin/bash

# Defining foldere variables
mg5_output_folder="../DM_test"
working_folder=$(pwd)

# copying lib and src folders to working directory
cp -Tfr "$mg5_output_folder/src" "$working_folder/src" 
cp -Tfr "$mg5_output_folder/lib" "$working_folder/lib" 

wait

# Editing the src files
#sed -i -e 's/    std::cout << "Opened slha file " /    \/\/std::cout << "Opened slha file " /g' "$working_folder/src/read_slha.cc"
#sed -i -e 's/ if(verbose)/ \/\/if(verbose)/g' "$working_folder/src/read_slha.cc"

#wait

# Run make 
make -s -C "./src"

# extracting subprocess folders name 
cd "$mg5_output_folder/SubProcesses"
unfiltered_processes=($(ls -d */))

particle_file="$working_folder/allowed_particles.txt"
if [[ -s $particle_file ]]; then
    	echo "OVERSEER: Particles file exists."
    	mapfile -t particles < $particle_file
    	#echo "${particles[@]}"
    
	subprocess_folders=()
	for process in "${unfiltered_processes[@]}"; do
		for in1 in "${particles[@]}"; do
			for in2 in "${particles[@]}"; do
				if [[ "$process" == *"_$in1$in2_"* ]]; then
					#echo $process
					subprocess_folders+=("$process")
		    			break 2
				fi
			done
	    	done
	done
else
	echo "OVERSEER: Particles file does not exist. Running all processes."
	subprocess_folders=("${unfiltered_processes[@]}")
fi

## Moving back to working directory
cd "$working_folder"

i=1
sp_number=${#subprocess_folders[@]}

echo "OVERSEER: Processes to evaluate: $sp_number"

# Running over each subprocess
for sp_folder in "${subprocess_folders[@]}"
do
	# Removing "/" to name the files
	sp_folder="${sp_folder%/*}"
	
	# Moving the CPPProcess files
	cp "$mg5_output_folder/SubProcesses/$sp_folder/CPPProcess.cc" "$working_folder/process/"
	cp "$mg5_output_folder/SubProcesses/$sp_folder/CPPProcess.h" "$working_folder/process/"
	
	# Editing the CPPProcess files
	#sed -i -e 's/void CPPProcess::sigmaKin()/double CPPProcess::sigmaKin(double s, double theta)/g' "$working_folder/process/CPPProcess.cc"
	#sed -i -e 's/    matrix_element\[i\] \/\= denominators\[i\]\;/    matrix_element\[i\] \/\= denominators\[i\]\;\n  return matrix_element\[0\]\*std::sin(theta)\;/g' "$working_folder/process/CPPProcess.cc"
	#sed -i -e 's/pars->print/\/\/pars->print/g' "$working_folder/process/CPPProcess.cc"
	# sed -i -e 's/\/\/ Calculate all amplitudes/for (auto* ptr \: p) \{\n    delete ptr\;\n  \}\n  p\.clear()\;/g' "$working_folder/process/CPPProcess.cc"
	
	#sed -i -e 's/void sigmaKin()/double sigmaKin(double s, double theta)/g' "$working_folder/process/CPPProcess.h"
	wait
	# Run make
	make -s check
	
	# Run over param_cards
	param_cards=($(ls "./cards/"))
	
	for card in "${param_cards[@]}"
	do
		card0="${card%.*}"
		mkdir -p "./output/$card0/"
		
		# Running the check
		if [[ $i -eq 1 ]];
		then
			command=$(./check "./cards/$card" "./output/$card0/neq.dat")
		else
			command=$(./check "./cards/$card")
		fi
		
		#Creating output file and saving data 
		#echo "$card"
		#free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }'
		echo "$command" > "./output/$card0/$sp_folder.dat"
		wait
		unset command
	done

	# Print the number of completed processes
	echo "Subprocess $i of $sp_number completed"
	let "i++"
done

output_folders=($(ls -d ./output/*))
for out_folder in "${output_folders[@]}"
do
	out_files=$(ls $out_folder/P*.dat)
	totals=$(sort -g $out_files | datamash -W --format=%.8e groupby 1 sum 2 )
	echo "$totals" > "$out_folder/TOTALS_T.dat"
done

for out_folder in "${output_folders[@]}"
do
	out_files=$(ls $out_folder/P*n1n1*.dat)
	totals=$(sort -g $out_files | datamash -W --format=%.8e groupby 1 sum 2 )
	echo "$totals" > "$out_folder/TOTALS_n1.dat"
done

for out_folder in "${output_folders[@]}"
do
	out_files=$(ls $out_folder/P*etretr*.dat)
	totals=$(sort -g $out_files | datamash -W --format=%.8e groupby 1 sum 2 )
	echo "$totals" > "$out_folder/TOTALS_etr.dat"
done
