


import argparse
import pandas as pd
import re
import os



dct=snakemake.params.dct_target
cutoff=snakemake.params.cutoff
target=snakemake.wildcards.target
sample=snakemake.wildcards.sample
catg=dct['catg']


with open(snakemake.output[0],'w') as fout:
	try:
		df1=pd.read_csv(snakemake.input[0],sep='\t')
		r_cigar1=re.compile(dct['r1'].get('cigar_in',None))
		n1=len(df1)
		df1=df1[df1.apply(lambda x: True if r_cigar1.search(x['cigar']) else False,axis=1)]
		n2=len(df1)
		vv=df1.groupby('umi').count()
		vv.reset_index(inplace=True)
		n3=len(vv)
		n4=sum(~vv['umi'].duplicated())
		n5=sum(vv['seqid']>1)
		n6=sum(vv['seqid']>cutoff)


		fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(sample,"r1",catg,target,n1,n2,n3,n4,n5,n6))
	except:
		fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(sample,"r1",catg,target,n1,0,0,0,0,0))
		
	try:
		df2=pd.read_csv(snakemake.input[1],sep='\t')
		r_cigar2=re.compile(dct['r2'].get('cigar_in',None))
		n1=len(df2)
		df2=df2[df2.apply(lambda x: True if r_cigar2.search(x['cigar']) else False,axis=1)]
		n2=len(df2)
		vv=df2.groupby('umi').count()
		vv.reset_index(inplace=True)
		n3=len(vv)
		n4=sum(~vv['umi'].duplicated())
		n5=sum(vv['seqid']>1)
		n6=sum(vv['seqid']>cutoff)

		fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(sample,"r2",catg,target,n1,n2,n3,n4,n5,n6))
	except:
		fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(sample,"r2",catg,target,n1,0,0,0,0,0))

	try:
		dfm=pd.read_csv(snakemake.input[2],sep='\t')
		n1=len(dfm)
		dfm=dfm[dfm.apply(lambda x: True if r_cigar1.search(x['cigar_r1']) else False,axis=1)]
		dfm=dfm[dfm.apply(lambda x: True if r_cigar2.search(x['cigar_r2']) else False,axis=1)]
		n2=len(dfm)
		vv=dfm.groupby('umi_r1').count()
		vv.reset_index(inplace=True)
		n3=len(vv)
		n4=sum(~vv['umi_r1'].duplicated())
		n5=sum(vv['seqid']>1)
		n6=sum(vv['seqid']>cutoff)

		fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(sample,"r12",catg,target,n1,n2,n3,n4,n5,n6))

	except:
		fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(sample,"r12",catg,target,n1,0,0,0,0,0))
