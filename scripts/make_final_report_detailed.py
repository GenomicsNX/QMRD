


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

dd=defaultdict(list)
cc=0
for s in ss_samples:
	for t in t_list_genes:
		for c in ['all-umi','uniq-umi','single-out','ABL1-cutoff','final']:
			dd[s].append(gg.get_group((s,t,c)).iloc[0,3])
			if cc==0:
				dd['targets'].append(t)
				dd['counts'].append(c)
	cc=1

cc=0
for s in ss_samples:
	for t in t_list_fusions:
		for c in ['all-umi','uniq-umi','single-out','ABL1-cutoff','final']:
			dd[s].append(gg.get_group((s,t,c)).iloc[0,3])
			if cc==0:
				dd['targets'].append(t)
				dd['counts'].append(c)
	cc=1


dfm=pd.DataFrame(dd)
dfm.set_index(keys=['targets','counts'],inplace=True)
dfm.to_csv(snakemake.output[0],sep='\t')

