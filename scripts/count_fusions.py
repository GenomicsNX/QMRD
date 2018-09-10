


import argparse
import pandas as pd
import re
import os


try:
	df=pd.read_csv(snakemake.input.cutoff,delim_whitespace=True,header=None)
	cutoff=int(round(df.at[0,0]))
except:
	cutoff=3

if cutoff<3:
	cutoff=3


dct=snakemake.params.dct_target
target=snakemake.wildcards.target
sample=snakemake.wildcards.sample
catg=dct['catg']


try:
	df=pd.read_csv(snakemake.input.junction,delim_whitespace=True,header=None,usecols=[0,1,3,4,9])
	df.columns=['ref1','pos1','ref2','pos2','seqid']
	df['umi']=df.apply(lambda x: x['seqid'].split('_')[1],axis=1)
	df['pos1']=df['pos1'].astype(int)
	df['pos2']=df['pos2'].astype(int)
	n1=len(df)

	bb1=df['ref1']==dct['ref1']
	bb2=df['pos1']==dct['pos1']
	bb3=df['ref2']==dct['ref2']
	bb4=df['pos2']==dct['pos2']

	
	vv=df[bb1 & bb2 & bb3 & bb4]
	n2=len(vv)
	
	vv2=vv.groupby('umi').count()
	vv2.reset_index(inplace=True)

	#vv2.to_csv(snakemake.output[1],sep='\t')	
	
	n3=len(vv2)
	n4=sum(~vv2['umi'].duplicated())
	n5=sum(vv2['ref1']>1)
	n6=sum(vv2['ref1']>cutoff)
	
except:
	print(sys.exc_info())
	n1=n2=n3=n4=n5=n6=0

with open(snakemake.output[0],'w') as fout:
	fout.write('%s\t%s\t%s\t%s\n' %(sample,target,"all-reads",n1))
	fout.write('%s\t%s\t%s\t%s\n' %(sample,target,"all-umi",n2))
	fout.write('%s\t%s\t%s\t%s\n' %(sample,target,"uniq-umi",n3))
	fout.write('%s\t%s\t%s\t%s\n' %(sample,target,"single-out",n5))
	fout.write('%s\t%s\t%s\t%s\n' %(sample,target,"ABL1-cutoff",cutoff))
	fout.write('%s\t%s\t%s\t%s\n' %(sample,target,"final",n6))
		

