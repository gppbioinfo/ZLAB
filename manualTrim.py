#!/usr/bin/python -w

######################################################################################
# This program performs the manual trimming and clipping of small RNA-Seq reads
# Written by Ganesh Panzade
# github private link : https://github.com/gppbioinfo/ZLAB/blob/master/manualTrim.py
######################################################################################

import fileinput
import sys
import os
import regex
import argparse

parser = argparse.ArgumentParser(description='Run program as => python manualTrim.py input_file output_file')

parser.add_argument('input file', action="store") #, type=int)
parser.add_argument('output file', action="store")

print parser.parse_args()
outfile = open(sys.argv[2], "w")	
file = open(sys.argv[1],"r")
lines =  file.read().splitlines()
for i in range(len(lines)):
     line = lines[i]
     if ">" in line:
     	next_line = lines[i+1]
     	#print(line,"\n",next_line, i, i+1)
	if len(next_line) > 30:
		#print(line,"\n",next_line, i, i+1)
		adpMatch=regex.findall("(TGGAATTCTCGGGTGCCAAGG){e<=5}", next_line)
		adpMatchstart=regex.search("(TGGAATTCTCGGGTGCCAAGG){e<=5}", next_line)
		
		if not adpMatch:
			#print(line+"\n"+next_line)
			trimread=next_line[0:25]
			outfile.write(line+"\n"+trimread+"\n")
		else:
			startpos=adpMatchstart.start()
			subRead=next_line[0:startpos]
			if len(subRead) > 17:
				outfile.write(line+"\n"+subRead+"\n")
	else:
		outfile.write(line+"\n"+next_line+"\n")
			
			
			#print(adpMatchstart.group(1)) #,adpMatchstart.start())
