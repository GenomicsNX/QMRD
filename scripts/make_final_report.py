


import pandas as pd
from snakemake.shell import shell
from collections import defaultdict
import tempfile


tmpfile=tempfile.mktemp()

for f in snakemake.input.res:
	shell("cat {f} >> {tmpfile}")
		

t_list_genes=snakemake.params.lst_genes
t_list_fusions=snakemake.params.lst_fusions

	
df=pd.read_table(tmpfile,header=None)
df[3]=df[3].astype(int)
df.columns=['sample_id','target','catg','count']
gg=df.groupby(['sample_id','target','catg'])

ss_samples=list(set(df['sample_id'].values))



dd=dict()
for s in ss_samples:
	dd[s]=dict()
	dd[s]['cutoff']=[]	
	for t in t_list_genes+t_list_fusions:
		dd[s][t]=gg.get_group((s,t,'final')).iloc[0,3]
		dd[s]['cutoff'].append(gg.get_group((s,t,'ABL1-cutoff')).iloc[0,3])


		
for s in ss_samples:
	cutoff=list(set(dd[s]['cutoff']))[0]
	if len(list(set(dd[s]['cutoff'])))>1:
		print(dd[s]['cutoff'])
	dd[s]['cutoff']=cutoff


	
dfm=pd.DataFrame()
dfm=dfm.from_dict(dd,orient='index')
dfm.reset_index(inplace=True)
dfm.rename(columns={'index':'sample_id'},inplace=True)

cols_order=['sample_id']
cols_order=cols_order+t_list_genes+t_list_fusions
cols_order=cols_order+['cutoff']
	
	
dfm=dfm.loc[:,cols_order]
dfm.to_csv(snakemake.output[0],sep='\t')



