


from snakemake.shell import shell
from os import path
import pysam
import pandas as pd
from collections import OrderedDict

dct=snakemake.params.dct_target
target=snakemake.wildcards.target
bamfile=snakemake.input[0]
outprefix=snakemake.params.outprefix

samf=pysam.AlignmentFile(bamfile)

ref=dct['r1']['ref']
start=dct['r1']['start']
end=dct['r1']['end']

seqid=[]
pos=[]
cigar=[]
q=[]
umi=[]
chrom=[]
for x in samf.fetch(ref,int(start),int(end)):
	seqid.append(x.query_name)
	pos.append(x.pos)
	cigar.append(x.cigarstring)
	q.append(x.query)
	umi.append(x.qname.split('_')[1])
	chrom.append(ref)
	

df_r1=pd.DataFrame({'seqid':seqid,'chr':chrom,'pos':pos,'cigar':cigar,'umi':umi,'seq':q},
				   columns=['seqid','chr','pos','cigar','umi','seq'])
df_r1.to_csv('%s.r1.txt' %outprefix,sep='\t',index=False)

ref=dct['r2']['ref']
start=dct['r2']['start']
end=dct['r2']['end']

seqid=[]
pos=[]
cigar=[]
q=[]
umi=[]
chrom=[]
for x in samf.fetch(ref,int(start),int(end)):
	seqid.append(x.query_name)
	pos.append(x.pos)
	cigar.append(x.cigarstring)
	q.append(x.query)
	umi.append(x.qname.split('_')[1])
	chrom.append(ref)

df_r2=pd.DataFrame({'seqid':seqid,'chr':chrom,'pos':pos,'cigar':cigar,'umi':umi,'seq':q},
				   columns=['seqid','chr','pos','cigar','umi','seq'])
df_r2.to_csv('%s.r2.txt' %outprefix,sep='\t',index=False)


dfm=pd.merge(df_r1,df_r2,on='seqid',how='inner',suffixes=('_r1', '_r2'))
dfm=dfm[['seqid','chr_r1','pos_r1','umi_r1','cigar_r1','chr_r2','pos_r2','umi_r2','cigar_r2']]
dfm.to_csv('%s.r12.txt'%outprefix,sep="\t",index=False)
