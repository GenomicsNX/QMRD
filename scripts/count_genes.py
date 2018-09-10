


import argparse
import pandas as pd
import re
import os,sys
from snakemake.shell import shell



def write_to_file(n1,n2,n3,n4,n5,cutoff):
	with open(snakemake.output[0],'w') as fout:
		fout.write('%s\t%s\t%s\t%d\n' %(sample,target,"all-reads",n1))
		fout.write('%s\t%s\t%s\t%d\n' %(sample,target,"all-umi",n2))
		fout.write('%s\t%s\t%s\t%d\n' %(sample,target,"uniq-umi",n3))
		fout.write('%s\t%s\t%s\t%d\n' %(sample,target,"single-out",n4))
		fout.write('%s\t%s\t%s\t%d\n' %(sample,target,"ABL1-cutoff",cutoff))
		fout.write('%s\t%s\t%s\t%d\n' %(sample,target,"final",n5))
	
		
try:
	df=pd.read_csv(snakemake.input.cutoff,delim_whitespace=True,header=None)
	cutoff=int(round(df.at[0,0]))
except:
	cutoff=3

# minimum cutoff=3
if cutoff<3:
	cutoff=3

	
dct=snakemake.params.dct_target
target=snakemake.wildcards.target
sample=snakemake.wildcards.sample
catg=dct['catg']

pos_in=dct.get('pos_in',None)
pos_out=dct.get('pos_out',None)
cigar_in=dct.get('cigar_in',None)
cigar_out=dct.get('cigar_out',None)
seq_in=dct.get('seq_in',None)
seq_out=dct.get('seq_out',None)


try:
	df=pd.read_csv(snakemake.input.reads,delim_whitespace=True)

	# make compiled regular expressions for cigar,pos,seq
	if pos_in:
		r_pos_in=re.compile(pos_in)
	if pos_out:
		r_pos_out=re.compile(pos_out)
		
	if cigar_in:
		r_cigar_in=re.compile(cigar_in)
	if cigar_out:
		r_cigar_out=re.compile(cigar_out)

	if seq_in:
		r_seq_in=re.compile(seq_in)
	if seq_out:
		r_seq_out=re.compile(seq_out)


	n1=len(df)


	# included
	if cigar_in:
		df=df[df.apply(lambda x: True if r_cigar_in.search(x['cigar']) else False,axis=1)]
	if pos_in:
		df=df[df.apply(lambda x: True if r_pos_in.search(x['pos']) else False,axis=1)]
	if seq_in:		
		df=df[df.apply(lambda x: True if r_seq_in.search(x['seq']) else False,axis=1)]


	# not included 
	if cigar_out:
		df=df[df.apply(lambda x: False if r_cigar_out.search(x['cigar']) else True,axis=1)]
	if pos_out:
		df=df[df.apply(lambda x: False if r_pos_out.search(x['pos']) else True,axis=1)]
	if seq_out:
		df=df[df.apply(lambda x: False if r_seq_out.search(x['seq']) else True,axis=1)]


	n2=len(df)
	vv=df.groupby('umi').count()
	vv.reset_index(inplace=True)
	#vv.to_csv(snakemake.output[1],sep='\t')

	n3=len(vv)
	n4=sum(~vv['umi'].duplicated())
	n5=sum(vv['seqid']>1)
	n6=sum(vv['seqid']>cutoff)

except:
	print(sys.exc_info())
	n1=n2=n3=n4=n5=n6=0

write_to_file(n1,n2,n3,n5,n6,cutoff)
	
	
	
		
