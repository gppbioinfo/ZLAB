#!/usr/bin/perl
use Getopt::Long;
use Pod::Usage;

# Program to get read count to specific non-coding RNAs from sam file



########################################################
# USAGE
#
$USAGE =<<USAGE;

     Usage:

         input_samfile noncode_list [-help]

         where:

             samfile: Mapped reads to noncode 
             noncode_list: Non code RNAs list present in standard symbols
           help:  Prints out this helpful message

USAGE
#
######################################################

if ($help) {
    print "$USAGE\n";
    exit 0;
}


#@nctype=("asRNA","lincRNA","miRNA","miRNA_primary_transcript","nc_primary_transcript","ncRNA","piRNA","pre_miRNA","rRNA","snoRNA","snRNA","tRNA");
$asRNA=0,$lincRNA=0,$miRNA=0,$miRNA_primary_transcript=0,$nc_primary_transcript=0,$ncRNA=0,$piRNA=0,$pre_miRNA=0,$rRNA=0,$snoRNA=0,$snRNA=0,$tRNA=0;

#print $nctype[0],"\n";

open(GP, $ARGV[0]) || die;
while($line=<GP>)
{
chomp($line);
@sline=split("\t", $line);
	if($sline[2] ne "*")
	{
	open(GC, $ARGV[1]) || die;
	while($line1=<GC>)
	{
	chomp($line1);
	@biotype=split(" ", $line1);
	
		if($sline[2] eq $biotype[0] && $biotype[1] eq "asRNA")
		{
		@ss=split("_",$sline[0]);
		$ss[2]=~s/x//g;
		#print "$ss[2]\n";
		$asRNA=$asRNA+$ss[2];
#		print $sline[2],"\t",$biotype[1],"\t",$sline[0],"\n";				
		}
		if($sline[2] eq $biotype[0] && $biotype[1] eq "lincRNA")
		{
		@ss=split("_",$sline[0]);
		$ss[2]=~s/x//g;
		#print "$ss[2]\n";
		$lincRNA=$lincRNA+$ss[2];
#		print $sline[2],"\t",$biotype[1],"\t",$sline[0],"\n";				
		}
		if($sline[2] eq $biotype[0] && $biotype[1] eq "miRNA")
		{
		@ss=split("_",$sline[0]);
		$ss[2]=~s/x//g;
		#print "$ss[2]\n";
		$miRNA=$miRNA+$ss[2];
#		print $sline[2],"\t",$biotype[1],"\t",$sline[0],"\n";				
		}
		if($sline[2] eq $biotype[0] && $biotype[1] eq "miRNA_primary_transcript")
		{
		@ss=split("_",$sline[0]);
		$ss[2]=~s/x//g;
		#print "$ss[2]\n";
		$miRNA_primary_transcript=$miRNA_primary_transcript+$ss[2];
#		print $sline[2],"\t",$biotype[1],"\t",$sline[0],"\n";				
		}
		if($sline[2] eq $biotype[0] && $biotype[1] eq "nc_primary_transcript")
		{
		@ss=split("_",$sline[0]);
		$ss[2]=~s/x//g;
		#print "$ss[2]\n";
		$nc_primary_transcript=$nc_primary_transcript+$ss[2];
#		print $sline[2],"\t",$biotype[1],"\t",$sline[0],"\n";				
		}
		if($sline[2] eq $biotype[0] && $biotype[1] eq "ncRNA")
		{
		@ss=split("_",$sline[0]);
		$ss[2]=~s/x//g;
		#print "$ss[2]\n";
		$ncRNA=$ncRNA+$ss[2];
#		print $sline[2],"\t",$biotype[1],"\t",$sline[0],"\n";				
		}
		if($sline[2] eq $biotype[0] && $biotype[1] eq "piRNA")
		{
		@ss=split("_",$sline[0]);
		$ss[2]=~s/x//g;
		#print "$ss[2]\n";
		$piRNA=$piRNA+$ss[2];
#		print $sline[2],"\t",$biotype[1],"\t",$sline[0],"\n";				
		}
		if($sline[2] eq $biotype[0] && $biotype[1] eq "pre_miRNA")
		{
		@ss=split("_",$sline[0]);
		$ss[2]=~s/x//g;
		#print "$ss[2]\n";
		$pre_miRNA=$pre_miRNA+$ss[2];
#		print $sline[2],"\t",$biotype[1],"\t",$sline[0],"\n";				
		}
		if($sline[2] eq $biotype[0] && $biotype[1] eq "rRNA")
		{
		@ss=split("_",$sline[0]);
		$ss[2]=~s/x//g;
		#print "$ss[2]\n";
		$rRNA=$rRNA+$ss[2];
#		print $sline[2],"\t",$biotype[1],"\t",$sline[0],"\n";				
		}
		if($sline[2] eq $biotype[0] && $biotype[1] eq "snRNA")
		{
		@ss=split("_",$sline[0]);
		$ss[2]=~s/x//g;
		#print "$ss[2]\n";
		$snRNA=$snRNA+$ss[2];
#		print $sline[2],"\t",$biotype[1],"\t",$sline[0],"\n";				
		}
		if($sline[2] eq $biotype[0] && $biotype[1] eq "snoRNA")
		{
		@ss=split("_",$sline[0]);
		$ss[2]=~s/x//g;
		#print "$ss[2]\n";
		$snoRNA=$snoRNA+$ss[2];
#		print $sline[2],"\t",$biotype[1],"\t",$sline[0],"\n";				
		}
		if($sline[2] eq $biotype[0] && $biotype[1] eq "tRNA")
		{
		@ss=split("_",$sline[0]);
		$ss[2]=~s/x//g;
		#print "$ss[2]\n";
		$tRNA=$tRNA+$ss[2];
#		print $sline[2],"\t",$biotype[1],"\t",$sline[0],"\n";				
		}
		
	}

	}
	
}

print "asRNA\t$asRNA\nlincRNA\t$lincRNA\nmiRNA\t$miRNA\nmiRNA_primary_transcript\t$miRNA_primary_transcript\nnc_primary_transcript\t$nc_primary_transcript\nncRNA\t$ncRNA\npiRNA\t$piRNA\npre_miRNA\t$pre_miRNA\nrRNA\t$rRNA\nsnoRNA\t$snoRNA\nsnRNA\t$snRNA\ntRNA\t$tRNA\n";

#print "$asRNA\t$lincRNA\t$miRNA\t$miRNA_primary_transcript\t$nc_primary_transcript\t$ncRNA\t$piRNA\t$pre_miRNA\t$rRNA\t$snoRNA\t$snRNA\t$tRNA\n";
