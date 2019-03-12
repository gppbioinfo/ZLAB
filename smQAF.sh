#!/bin/bash

##############################################
# Developed by Ganesh Panzade, ZLAB
##############################################

indir=$1   # Read file input directory given on command line
ext=$2
qs=$3
qT=$4
mrl=$5
adp=$6
ltrim=$7
rtrim=$8
gzc="gz"



if [ $# -le 1 ]; then
	se	
	printf "Usage:\n\nsmall RNA-Seq reads quality control and filtering\n \n"$0" \nCompulsory option:\n input_dir\n fastq/gz\n quality_score\n quality_thresholds\n [minLen(10-16, default:16)]\n [adaptor(default:TGGAATTCTCGGGTGCCAAGG)]\n [leftTrim(0-5, default:2)] [rightTrim(0-5, default:2) ]\n";
	printf "Detail options:\n Left trim read from 5' end upto 5bp\n";
	printf " Right trim read from 5' end upto 5bp\n\n";	
	printf "\nMinimum two options is required, 1. input_directory 2. file extension\n\n";
	exit;
else
	printf "Error. Required atleast two parameters, 1. input_dir of read files, 2. extension of read files\n";
fi


if [ $# -ge 2 ]; then
	echo "Provided more than 2"
	 # Input directory and extenstionof read files
	 
	 if [ -d "$indir" ] && [ "$ext" = "$gzc" ]; then
	 	cd $indir
		 pwd
			 ts=10
  			pss="%"
		 		for rfile in $(ls *fastq.gz); do   							   				 
				  sleep .1
				  ts=$((ts+=10))						 						 	
					outfile=`echo $rfile | sed -e 's/.gz//g'`
					printf "\nJob is still running, %d%s completed\n" "$ts" "$pss"							
					zcat $rfile | fastq_quality_filter -q 25 -p 70 | fastx_clipper -l 16 -a $adp -M 10 | fastx_trimmer -f 2 -m 18 | fastx_trimmer -t 2 -m 18 | fastx_collapser -o $outfile\.fa																		
					printf "\nJob is 100%s completed!\n" "$pss"																																			 						 
				done	
	 fi	 
fi 
