#!/bin/bash


if [ $# -lt 3 ]; then
	printf "Usage:\n\nsmall RNA-Seq reads quality control and filtering\n \n"$0" input_dir fastq/gz quality_score quality_score [minLen(10-16, default:16)] [adaptor(default:TGGAATTCTCGGGTGCCAAGG)] [leftTrim(0-5, default:2)] [rightTrim(0-5, default:2) ]\n";
	printf "Detail options:\nLeft trim read from 5' end upto 5bp\n";
	printf "Right trim read from 5' end upto 5bp\n\n";	
	exit;
fi


indir=$1   # Read file input directory given on command line
ext=$2
qs=$3
qT=$4
mrl=$5
adp=$6
ltrim=$7
rtrim=$8


if[ $3 -ge 3]; then



for i in $(ls $indir)
do

printf "Started quality assessment and filtering for "$i"\n"
inputfolder=`echo $i | sed 's/\//\t/' | awk '{print $1}'`
inputfile=`echo $i | sed 's/\//\t/' | awk '{print $2}'`
outfile=`echo $inputfile | sed -e 's/.gz//g'`


zcat $i | fastq_quality_filter -q 25 -p 70 | fastx_clipper -l 16 -a TGGAATTCTCGGGTGCCAAGG -M 10 | fastx_trimmer -f 5 -m 18 | fastx_trimmer -t 4 -m 18 > $inputfolder/$outfile
zcat $i | fastq_quality_filter -q 25 -p 70 | fastx_clipper -l 16 -a TGGAATTCTCGGGTGCCAAGG -M 10 | fastx_trimmer -f 5 -m 18 > $inputfolder/$outfile

fastx_collapser -i $inputfolder/$outfile -o $smRead/collapse/$outfile

#fastqc -o $smRead/FQC --contaminants $smRead/contaminant_list.txt --adapters $smRead/adapter_list.txt $inputfolder/$outfile -t 2


printf "Completed\n"

done

fi
