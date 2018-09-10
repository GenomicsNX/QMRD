


from snakemake.shell import shell
from os import path
import pysam
import pandas as pd
import tempfile


tmpfile=tempfile.mktemp()

bamfile=snakemake.input[0]
target=snakemake.params.target

ref=target['ref']
start=target['start']
end=target['end']

try:
	shell("samtools view {bamfile} > {tmpfile} ")
	df=pd.read_csv(tmpfile,delim_whitespace=True,header=None,usecols=[0,2,3,5,9])
	df.columns=['seqid','ref','pos','cigar','seq']
	print(df)
	df['umi']=df.apply(lambda x: x['seqid'].split('_')[1],axis=1)
	print(df)
	df.to_csv(snakemake.output[0],index=False,sep='\t')
except:
	print(sys.exc_info())
	df=pd.DataFrame(columns=['seqid','ref','pos','cigar','seq'])		
	df.to_csv(snakemake.output[0],index=False,sep='\t')
		
	
		
