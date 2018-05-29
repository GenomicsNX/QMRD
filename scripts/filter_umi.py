


import argparse
import pandas as pd
import re
import os,sys



dct=snakemake.params.dct_target
target=snakemake.wildcards.target
sample=snakemake.wildcards.sample
catg=dct['catg']
cutoff=snakemake.params.cutoff

pos_in=dct.get('pos_in',None)
pos_out=dct.get('pos_out',None)
cigar_in=dct.get('cigar_in',None)
cigar_out=dct.get('cigar_out',None)
seq_in=dct.get('seq_in',None)
seq_out=dct.get('seq_out',None)


df=pd.read_csv(snakemake.input[0],sep='\t')
#df.columns=['seq_id','ref','pos','cigar','len1','len2','nM','umi_seq','seq_string']
#df.columns=['seq_id','ref','pos','cigar','umi_seq','seq_string']
df['pos']=df['pos'].astype(str)


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


try:
	# included
	if cigar_in:
		print("here")
		print(df['cigar'])
		df=df[df.apply(lambda x: True if r_cigar_in.search(x['cigar']) else False,axis=1)]
		print(df)
	if pos_in:
		df=df[df.apply(lambda x: True if r_pos_in.search(x['pos']) else False,axis=1)]
	if seq_in:
		df=df[df.apply(lambda x: True if r_seq_in.search(x['seq']) else False,axis=1)]


	# not included 
	if cigar_out:
		df=df[df.apply(lambda x: False if r_cigar_out.search(x['cigar']) else True,axis=1)]
		print(df)
	if pos_out:
		df=df[df.apply(lambda x: False if r_pos_out.search(x['pos']) else True,axis=1)]
	if seq_out:
		df=df[df.apply(lambda x: False if r_seq_out.search(x['seq']) else True,axis=1)]
	

	n2=len(df)
	vv=df.groupby('umi').count()
	vv.reset_index(inplace=True)
	n3=len(vv)
	n4=sum(~vv['umi'].duplicated())
	n5=sum(vv['seqid']>1)
	n6=sum(vv['seqid']>cutoff)

	with open(snakemake.output[0],'w') as fout:
		fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(sample,catg,target,n1,n2,n3,n4,n5,n6))

except:
	print(sys.exc_info())
	#with open(snakemake.output[0],'w') as fout:
	#	fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(sample,catg,target,n1,0,0,0,0,0))
