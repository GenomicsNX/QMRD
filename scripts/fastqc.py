


from snakemake.shell import shell
from os import path



out_dir=path.dirname(snakemake.output)
log=snakemake.log_fmt_shell(stdout=True,stderr=True)

shell(
	""" 
	set -x
	date
	module load Software/FastQC/0.11.5
	fastqc --extract --outdir {out_dir} {snakemake.input} {log}
	mv {out_dir}/{snakemake.wildcards.sample}.R1_fastqc.html {snakemake.output.html}
	mv {out_dir}/{snakemake.wildcards.sample}.R1_fastqc {out_dir}/{snakemake.wildcards.sample}_fastqc
	""")

