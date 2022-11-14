#!/bin/bash

if [[ -z $1 ]]
then
    echo "Usage: ./get_data.sh file_name"
    echo "Output: {file_name}_preprocessed.txt and {file_name}_processed.txt "
    exit
fi

file_name=$1
cores=$2
shared=$3
preprocessed_file_name=$(basename -s '.txt' ${file_name})_preprocessed.txt 
[ -f $preprocessed_file_name ] && rm $preprocessed_file_name
output_file_name=$(basename -s '.txt' ${file_name})_processed.txt 
[ -f $output_file_name ] && rm $output_file_name 

reversed_file_name=${file_name}_reversed
tac ${file_name} > ${reversed_file_name}
# global mpki
echo $(grep "Simulation Instructions:" ${file_name}) | cut -d ' ' -f 3 >> $preprocessed_file_name

for (( i=0; i<${cores}; i++ ))
do
    echo $(grep -e "CPU ${i} .* MPKI:" ${reversed_file_name}) | cut -d ' ' -f 8 >> $preprocessed_file_name
    echo $(grep "CPU ${i} cumulative IPC" ${reversed_file_name}) | cut -d ' ' -f 5 >> $preprocessed_file_name
    echo $(grep "cpu${i}_L1D TOTAL" ${reversed_file_name}) | cut -d ' ' -f 4,6,8 >> $preprocessed_file_name
    echo $(grep "cpu${i}_L1D AVERAGE" ${reversed_file_name}) | cut -d ' ' -f 5 >> $preprocessed_file_name
    echo $(grep "cpu${i}_L1I TOTAL" ${reversed_file_name}) | cut -d ' ' -f 4,6,8 >> $preprocessed_file_name
    echo $(grep "cpu${i}_L1I AVERAGE" ${reversed_file_name}) | cut -d ' ' -f 5 >> $preprocessed_file_name
    echo $(grep "cpu${i}_L2C TOTAL" ${reversed_file_name}) | cut -d ' ' -f 4,6,8 >> $preprocessed_file_name
    echo $(grep "cpu${i}_L2C AVERAGE" ${reversed_file_name}) | cut -d ' ' -f 5 >> $preprocessed_file_name

    if [[ $shared == 0 ]]
    then 
        echo $(grep "cpu${i}_LLC TOTAL" ${reversed_file_name}) | cut -d ' ' -f 4,6,8 >> $preprocessed_file_name
        echo $(grep "cpu${i}_LLC AVERAGE" ${reversed_file_name}) | cut -d ' ' -f 5 >> $preprocessed_file_name
    else
        line_count=0
        req_line_count=$((cores+i))
        grep "LLC TOTAL" ${file_name} | while read -r line
        do
            echo $line_count $req_line_count
            if [[ $line_count -eq ${req_line_count} ]]
            then
                echo $line
                echo $line | grep "LLC TOTAL" |  cut -d ' ' -f 4,6,8 >> $preprocessed_file_name
                break
            fi
            ((line_count++))
        done

        line_count=0
        req_line_count=$((i))
        grep "LLC AVERAGE" ${file_name} | while read -r line
        do
            echo $line_count $req_line_count
            if [[ $line_count -eq ${req_line_count} ]]
            then
                echo $line
                echo $line | grep "LLC AVERAGE" |  cut -d ' ' -f 5 >> $preprocessed_file_name
                break
            fi
            ((line_count++))
        done
    fi
done

rm ${reversed_file_name}
# ./process_data.py $preprocessed_file_name $output_file_name
