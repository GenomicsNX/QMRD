


from snakemake.shell import shell
import pandas as pd


tmpfile='%s.tmp' %snakemake.output[0]

# make ready for R script 
df=pd.read_csv(snakemake.input[0],sep='\t')
vv=df.groupby('umi')['umi'].count()
vv=pd.DataFrame(vv)
vv.columns=['count']
vv=vv.reset_index()
vv.columns=['UMI','count']
vv=vv[['count','UMI']]
vv.to_csv(tmpfile,sep='\t',index=False,header=False)

r_script=snakemake.params.rscript

shell("Rscript {r_script} {tmpfile} {snakemake.output[0]} {snakemake.output[1]}")
#shell("rm {tmpfile} ")




