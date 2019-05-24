import argparse
import subprocess
import os
import sys
import re
# Initiate the parser
parser = argparse.ArgumentParser()

# add long and short arguement

parser.add_argument("--seqType", "-sT", help="Select read sequence protocal either RNA-Seq or smallRNA-seq or WGS/Bisulfite/ChIP-Seq/CLIP/CLASH")
parser.add_argument("--protocal", "-p", help="Select read type either Single end (SE) or Paired end (PE)")
#parser.add_argument("--infile", "-f", action='store', dest='alist', type=str, nargs='*', default=['item1', 'item2', 'item3'], help="Read input file in fastq/fq format. Multiple file list accepted in space separate form")
parser.add_argument('--infile', '-f', nargs='+', help="Examples: -i item1 item2, -i item3")
parser.add_argument("--barcode", "-b", help="Barcode generated data answer in Yes/No")
parser.add_argument("--barcode-file", "-bf", help="Provide barcode file in fasta format")
parser.add_argument("--adapter", "-ad", help="Provide adapter sequence according to protocol in fasta format")
parser.add_argument("--adapterfile", "-adf", help="Provide adapter sequences file according to protocol")
parser.add_argument("--quality-score","-QS", help="Quality score for read filtering")
parser.add_argument("--mismatch","-ms", help="Mismatch in adapter alignment")
parser.add_argument("--aligner","-al", help="Alignment program Tophat2/Hisat2/Bowtie2/BWA")
parser.add_argument("--aligner-path","-alpath", help="Please provide the executable path of Tophat2/Hisat2/Bowtie2/BWA")
parser.add_argument("--genome","-g", help="Reference genome file")
parser.add_argument("--transcriptome","-ts", help="Reference transcriptome file for RSEM expression analysis")
parser.add_argument("--index","-id", help="Genome index name. Tophat2/bowtie2 takes bowtie2 index while others generated using their program /Hisat2/Bowtie2/BWA")
parser.add_argument("--gfffile","-gff", help="Reference genome annotation file GFF3")
parser.add_argument("--gtffile","-gtf", help="Reference genome GTF file")
parser.add_argument("--quantification","-qt", help="Quantification/assembly by Cufflink/HTseq count utility/RSEM expression calculation")
parser.add_argument("--processor","-n", help="Number of processor")
# read arguments from the command line

args = parser.parse_args()

# check for --width
#os.system("source ~/.bashrc")
os.system("mkdir QC")


if args.seqType:
  if args.seqType == "smallRNA" :
    print("Quality assessment for %s-Seq reads" % args.seqType)
    #if len(args.infile) > 1:
      #print("More than one sample for analysis")
      #if args.barcode:
       # print("Multiplexed read files")	
      #elif args.barcode-file:
       # print("Barcode file is provided in fasta format")
      #else:
     # 	print("No barcode provided")
    #else:
      #print("Single sample for analysis")
      #if args.barcode:
        #print("Multiplexed read files")
	
      #elif args.barcode-file:
        #print("Barcode file is provided in fasta format")
      #else:
      	#print("No barcode provided")      
  elif args.seqType == "RNA" :
    print("Quality assessment for %s-Seq reads" % args.seqType)
    # Check inputfile size
    #print("Number of files %s " % len(args.infile))
    if len(args.infile) > 1:
      print("Multiple files as input")
      libName=[]
      for ifile in args.infile:
        print(ifile)
        outname1=ifile.strip()    
        outname=re.sub(".fastq|.fa|.FASTQ|.FQ","", outname1)
        #outname=outname.replace(".fq","")
        print("Output file name is %s" % outname)      
        print("############# Quality check is started ###############")
        os.system("fastqc -o QC --contaminants contaminant_list.txt --adapters adapter_list.txt "+outname1+" --threads "+args.processor)
        print("\nQuality check is finished\n")
        if args.adapter:
          print("########### Quality filtering is started ##############")
          os.system("flexbar -r "+outname1+" -as "+args.adapter+" -ao "+args.mismatch+" -ae 0.1 -j -t "+outname+"_filtered -n "+args.processor)
          print("\nQuality check is finished\n")
        elif args.adapterfile:
          print("########### Quality filtering is started ##############")
          os.system("flexbar -r "+outname1+" -a "+args.adapterfile+" -ao "+args.mismatch+" -ae 0.1 -j -t "+outname+"_filtered -n "+args.processor)
          print("\nQuality filtering is finished\n")          
        
        if args.aligner == "Tophat2":
          print("########### Tophat alignment is started ##############")
      
          print("########### Tophat alignment is finished ##############")      
        elif args.aligner == "Hisat2":      
          if args.index:
            os.system("hisat2_extract_splice_sites.py "+args.gtf+" > splicesites.txt")	        
            os.system("hisat2 -x "+args.index+" -U "+outname+"_filtered.fastq -q --min-intronlen 500 --max-intronlen 100000 --known-splicesite-infile splicesites.txt --novel-splicesite-outfile "+outname+"_genomesplice.txt --novel-splicesite-infile genomesplice.txt --rna-strandness F --downstream-transcriptome-assembly --dta-cufflinks -t -p "+args.processor+" --no-head --summary-file "+outname+".log --new-summary  | samtools view - -T "+args.genome+" -F 4 --threads "+args.processor+" -b | samtools sort - --threads "+args.processor+" -o "+outname+"_sorted.bam")      
            LibName.append(outname+"_sorted.bam")
          else:
            indexname=args.genome.strip()
            indexname=re.sub(".fasta|.fa|.FASTA|.FA", "", indexname)
            #indexname=indexname.replace(".fa", "")
            #indexname=indexname.replace(".FASTA", "")
            #indexname=indexname.replace(".FA", "")
            print("########### Building index from genome ##############")
            indexpath=os.path.dirname(args.genome)	    
            if os.path.isfile(indexname+'.1.ht2'): 
              print("Index already present")
            else:
              os.system("hisat2-build "+args.genome+" "+indexname)	   	   
              print("%s" % (indexname))  
	                 
            os.system("hisat2_extract_splice_sites.py "+args.gtffile+" > splicesites.txt")
            print("########### Hisat2 alignment is started ##############")
            os.system("hisat2 -x "+indexname+" -U "+outname+"_filtered.fastq -q --min-intronlen 500 --max-intronlen 100000 --known-splicesite-infile splicesites.txt --novel-splicesite-outfile "+outname+"_genomesplice.txt --novel-splicesite-infile genomesplice.txt --rna-strandness F --downstream-transcriptome-assembly --dta-cufflinks -t -p "+args.processor+" --no-head --summary-file "+outname+".log --new-summary  | samtools view - -b -T "+args.genome+" -F 4 --threads "+args.processor+" | samtools sort - --threads "+args.processor+" -o "+outname+"_sorted.bam")
            print("########### Hisat2 alignment is finished ##############")
        elif args.aligner == "Bowtie2":
          print("########### Bowtie2 alignment is started ##############")
          print("########### Bowtie2 alignment is finished ##############")
        elif args.aligner == "BWA":
          print("########### Tophat alignment is started ##############")
          print("########### Tophat alignment is finished ##############")             
          #check assembly type
        if re.findall("Cufflink|cufflink|CUFFLINK", args.quantification):
          print("Transcript assembly started")
          os.system("cufflinks -p "+args.processor+" --library-type fr-unstranded -o "+outname+"_cuff -G "+args.gfffile+" "+outname+"_sorted.bam")
          if os.path.isfile("./assembly.txt"):
            print("File already generated for assembly")
          else:
            os.system("echo $(pwd)/"+outname+"_cuff/transcripts.gtf >> assembly.txt");          
            print("Transcript assembly finished")  
        elif re.findall("htseq|HTSeq|Htseq", args.quantification): 
          print("htseq read count started")
          os.system("htseq-count -f bam -s reverse -t gene -i Name --additional-attr ID -m union --nonunique all -q "+outname+"_sorted.bam "+args.gfffile+" > "+outname+".count")
          print("htseq read count finished") 
        elif re.findall("rsem|RSEM|Rsem", args.quantification):
          print("RSEM started")
          tsindex=indexname=re.sub(".fasta|.fa|.FASTA|.FA", "", args.transcriptome)
          os.system("rsem-generate-ngvector "+args.transcriptome+" "+tsindex)
          os.system("rsem-calculate-expression -p "+args.processor+" --bowtie2 --bowtie2-path "+args.bowtie2-path+" --estimate-rspd --append-names --output-genome-bam "+outname+"_sorted.bam "+tsindex+" "+outname+"_rsem.txt")
          print("RSEM finished")
	  
	  
      print("Cuffmerg is in process")
      os.system("python2.7 /home/ganesh/biotools/cufflinks-2.2.1.Linux_x86_64/cuffmerge -o current_assembly -g "+args.gfffile+" -p "+args.processor+" assembly.txt")
      print("Cuffmerg generated the transcriptome")
      Sample = str(" ".join(map(str, args.infile)))
      Sample = re.sub(".fastq", "_sorted.bam",Sample)
      libcount = list(range(1,(len(args.infile)+1)))
      libcount = str(",".join(map(str, libcount)))
      print("Differential expression is in progress")     
      os.system("cuffdiff -o current_diff -L "+libcount+" -b "+args.genome+" -u current_assembly/merged.gtf -p "+args.processor+" --library-type fr-unstranded -c 5 --library-norm-method classic-fpkm "+Sample)		  	            
      print("Differential expression analysis is done!")
    else:
      # Single input file processing          
      outname=args.infile.strip()    
      outname=re.sub(".fastq|.fa|.FASTQ|.FQ","", outname)
      #outname=outname.replace(".fq","")
      print("Output file name is %s" % outname)
      
      print("############# Quality check is started ###############")
      #os.system("fastqc -o QC --contaminants contaminant_list.txt --adapters adapter_list.txt "+args.infile+" --threads "+args.processor)
      print("\nQuality check is finished\n")
      if args.adapter:
        print("########### Quality filtering is started ##############")
        #os.system("flexbar -r "+args.infile+" -as "+args.adapter+" -ao "+args.mismatch+" -ae 0.1 -j -t "+outname+"_filtered -n "+args.processor)
        print("\nQuality check is finished\n")
      elif args.adapterfile:
        print("########### Quality filtering is started ##############")
        #os.system("flexbar -r "+args.infile+" -a "+args.adapterfile+" -ao "+args.mismatch+" -ae 0.1 -j -t "+outname+"_filtered -n "+args.processor)
        print("\nQuality filtering is finished\n")          
      if args.aligner == "Tophat2":
        print("########### Tophat alignment is started ##############")
      
        print("########### Tophat alignment is finished ##############")      
      elif args.aligner == "Hisat2":      
        if args.index:
          os.system("hisat2_extract_splice_sites.py "+args.gtf+" > splicesites.txt")	        
          os.system("hisat2 -x "+args.index+" -U "+outname+"_filtered.fastq -q --min-intronlen 500 --max-intronlen 100000 --known-splicesite-infile splicesites.txt --novel-splicesite-outfile "+outname+"_genomesplice.txt --novel-splicesite-infile genomesplice.txt --rna-strandness F --downstream-transcriptome-assembly --dta-cufflinks -t -p "+args.processor+" --no-head --summary-file "+outname+".log --new-summary  | samtools view - -T "+args.genome+" -F 4 --threads "+args.processor+" -b | samtools sort - --threads "+args.processor+" -o "+outname+"_sorted.bam")      
        else:
          indexname=args.genome.strip()
          indexname=re.sub(".fasta|.fa|.FASTA|.FA", "", indexname)
          #indexname=indexname.replace(".fa", "")
          #indexname=indexname.replace(".FASTA", "")
          #indexname=indexname.replace(".FA", "")
          print("########### Building index from genome ##############")
          indexpath=os.path.dirname(args.genome)
          if os.path.isfile(indexname+'.1.ht2'):
            print("Index already present")
          else:
            os.system("hisat2-build "+args.genome+" "+indexname)	   	   
            print("%s" % (indexname))
	            
		    
          os.system("hisat2_extract_splice_sites.py "+args.gtffile+" > splicesites.txt")
          print("########### Hisat2 alignment is started ##############")
          #os.system("hisat2 -x "+indexname+" -U "+outname+"_filtered.fastq -q --min-intronlen 500 --max-intronlen 100000 --known-splicesite-infile splicesites.txt --novel-splicesite-outfile "+outname+"_genomesplice.txt --novel-splicesite-infile genomesplice.txt --rna-strandness F --downstream-transcriptome-assembly --dta-cufflinks -t -p "+args.processor+" --no-head --summary-file "+outname+".log --new-summary  | samtools view - -b -T "+args.genome+" -F 4 --threads "+args.processor+" | samtools sort - --threads "+args.processor+" -o "+outname+"_sorted.bam")
          print("########### Hisat2 alignment is finished ##############")
      elif args.aligner == "Bowtie2":
        print("########### Bowtie2 alignment is started ##############")
        print("########### Bowtie2 alignment is finished ##############")
      elif args.aligner == "BWA":
        print("########### Tophat alignment is started ##############")
        print("########### Tophat alignment is finished ##############")             
        #check assembly type
      if re.findall("Cufflink|cufflink|CUFFLINK", args.quantification):
        print("Transcript assembly started")
        os.system("cufflinks -p "+args.processor+" --library-type fr-unstranded -o "+outname+"_cuff -G "+args.gfffile+" "+outname+"_sorted.bam")
        print("Transcript assembly finished")
        if os.path.isfile("./assembly.txt"):
          print("File already generated for assembly")
        else:
          os.system("echo $(pwd)/"+outname+"_cuff/transcripts.gtf >> assembly.txt");          
          print("Transcript assembly finished") 
      elif re.findall("htseq|HTSeq|Htseq", args.quantification): 
        print("htseq read count started")
        os.system("htseq-count -f bam -s reverse -t gene -i Name --additional-attr ID -m union --nonunique all -q "+outname+"_sorted.bam "+args.gfffile+" > "+outname+".count")
        print("htseq read count finished") 
      elif re.findall("rsem|RSEM|Rsem", args.quantification):
        print("RSEM started")
        tsindex=indexname=re.sub(".fasta|.fa|.FASTA|.FA", "", args.transcriptome)
        os.system("rsem-generate-ngvector "+args.transcriptome+" "+tsindex)
        os.system("rsem-calculate-expression -p "+args.processor+" --bowtie2 --bowtie2-path "+args.bowtie2-path+" --estimate-rspd --append-names --output-genome-bam "+outname+"_sorted.bam "+tsindex+" "+outname+"_rsem.txt")
        print("RSEM finished") 	
  elif args.seqType == "" :
    print("Please input read type smallRNA/RNA")
    

