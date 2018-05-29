


from snakemake.shell import shell
from os import path


log=snakemake.log_fmt_shell(stdout=True,stderr=True)

shell(
	""" 
	set -x
	date
	module load Software/cutadapt/1.12
	cutadapt {snakemake.params}  --too-short-output {snakemake.output.short} -o {snakemake.output.fastq} {snakemake.input[0]} > {snakemake.output.qc}  {log}
	""")

