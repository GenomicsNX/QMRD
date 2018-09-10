


from snakemake.shell import shell
import pandas as pd
import re
import tempfile

tmpfile=tempfile.mktemp()
pattern=snakemake.params.pattern


df=pd.read_csv(snakemake.input[0],delim_whitespace=True)

# make ready for R script 
vv=df.groupby('umi')['umi'].count()
vv=pd.DataFrame(vv)
vv.columns=['count']
vv=vv.reset_index()
vv.columns=['UMI','count']
vv=vv[['count','UMI']]
vv.to_csv(tmpfile,sep='\t',index=False,header=False)

r_script=snakemake.params.rscript

# if error then just put 0 to cutoff
shell("Rscript {r_script} {tmpfile} {snakemake.output[0]} {snakemake.output[1]} || echo '0' > {snakemake.output[0]} ")




