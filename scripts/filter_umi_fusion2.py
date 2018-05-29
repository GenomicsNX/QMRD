


import argparse
import pandas as pd
import re
import os



dct=snakemake.params.dct_target
cutoff=snakemake.params.cutoff
target=snakemake.wildcards.target
sample=snakemake.wildcards.sample
catg=dct['catg']


try:
	df=pd.read_csv(snakemake.input[0],sep='\t',header=None)

	df['umi']=df.apply(lambda x: x[9].split('_')[1],axis=1)
	n1=len(df)

	bb1=df[0]==dct['ref1']
	bb2=df[1]==dct['pos1']
	bb3=df[3]==dct['ref2']
	bb4=df[4]==dct['pos2']

	vv=df[bb1 & bb2 & bb3 & bb4]
	n2=len(vv)

	vv2=vv.groupby('umi').count()
	vv2.reset_index(inplace=True)
	n3=len(vv2)
	n4=sum(~vv2['umi'].duplicated())
	n5=sum(vv2[0]>1)
	n6=sum(vv2[0]>cutoff)


	with open(snakemake.output[0],'w') as fout:
		fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(sample,"junction",catg,target,n1,n2,n3,n4,n5,n6))

except:
	fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(sample,"junction",catg,target,n1,0,0,0,0,0))
