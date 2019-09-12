#!/bin/bash



# Process small RNA-Seq data for isomiR identification



# Folder for output files

mkdir filtered_reads_final_set

# Entering into output folder

cd filtered_reads_final_set_v1

# Input raw reads files 

for i in SRR7257539.fastq SRR7257540.fastq SRR7257541.fastq SRR7257542.fastq SRR7257543.fastq SRR7257544.fastq SRR7257545.fastq SRR7257546.fastq
do

# Check path of output folder

pwd


# Output file name

outname=`echo $i | sed -e 's/.fastq//'`


# Quality check
 
fastqc -o QCS --contaminants contaminant_list.txt --adapters adapter_list.txt $i --threads 20 2>>fastqc_log

# Read filtering and trimming
####
# Parameters : -ao adapter minimum overlap ; -ae error rate; -n processor; -j report log -x 5' trim -y 3' trim
##### 

flexbar -r ../$i -a ../new-adapter.fa -ao 5 -ae 0.1 -t $outname\_filtered -n 20 -j -x 0 -y 0 -qt 25 --fasta-output --adapter-trim-end RIGHT --min-read-length 17 2>$outname\_log1

# Collapse filtered reads for unique representation/tag

collapse_reads_md.pl $outname\_filtered.fasta cel | fasta_formatter - -t 0 | awk -F"\t" '{if(length($2) < 30) print ">"$1"\n"$2}' > $outname\_filtered_uniq.fasta

# Genome mapping output generated into BAM for Alignment visualization

bowtie -n 0 -p 30 --chunkmbs 6000 -f -v 1 -a --best --strata -B 1 -e 80 /media/ganesh/RA1/KSU/WormBase/w269/ensembl/Caenorhabditis_elegans.WBcel235 $outname\_filtered_uniq.fasta -S \
	| samtools view - -b -O BAM | samtools sort - -O BAM -o $outname\_mapping_genomeWtc.bam

# Genome mapping and extract mapped reads only

bowtie -n 0 -p 30 --chunkmbs 6000 -f -v 1 -a --best --strata -B 1 -e 80 /media/ganesh/RA1/KSU/WormBase/w269/ensembl/Caenorhabditis_elegans.WBcel235 --al $outname\_genome_mapped_26 --un $outname\_genome_unmapped_26 $outname\_filtered_uniq.fasta $outname\_mapping_genome_26.bwt -S 2>$outname\_genome_log_last_corrected_26

# Convert genome mapped reads into tab separated format for isomiR-SEA as an input files

fasta_formatter -i $outname\_genome_mapped_26 -t 0 | awk -F"\t" '{if(length($2) < 30) {split($1,a,"_"); gsub(/x/,"",a[3]); print $2"\t"a[3]}}' > $outname\_genome_mapped_uniq.txt


done


# Already filtered samples 


for i in SRR7257539.fastq SRR7257545.fastq
do

echo $i

outname=`echo $i | sed -e 's/.fastq//'` 

awk 'NR%4==1{a=substr($0,2);}NR%4==2{if(length($0) < 30) print ">"a"\n"$0}' ../$i > $outname\_filtered.fasta

collapse_reads_md.pl $outname\_filtered.fasta cel | fasta_formatter - -t 0 | awk -F"\t" '{if(length($2) < 30) print ">"$1"\n"$2}' > $outname\_filtered_uniq.fasta

bowtie -n 0 -p 30 --chunkmbs 6000 -f -v 1 -a --best --strata -B 1 -e 80 /media/ganesh/RA1/KSU/WormBase/w269/ensembl/Caenorhabditis_elegans.WBcel235 $outname\_filtered_uniq.fasta -S \
	| samtools view - -b -O BAM | samtools sort - -O BAM -o $outname\_mapping_genomeWtc.bam


bowtie -n 0 -p 30 --chunkmbs 6000 -f -v 1 -a --best --strata -B 1 -e 80 /media/ganesh/RA1/KSU/WormBase/w269/ensembl/Caenorhabditis_elegans.WBcel235 --al $outname\_genome_mapped_26 --un $outname\_genome_unmapped_26 $outname\_filtered_uniq.fasta $outname\_mapping_genome_26.bwt -S 2>$outname\_genome_log_last_corrected_26


fasta_formatter -i $outname\_genome_mapped_26 -t 0 | awk -F"\t" '{if(length($2) < 30) {split($1,a,"_"); gsub(/x/,"",a[3]); print $2"\t"a[3]}}' > $outname\_genome_mapped_uniq.txt


done



