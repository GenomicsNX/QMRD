


from snakemake.shell import shell
from os import path


log=snakemake.log_fmt_shell(stdout=True,stderr=True)


shell(
	"umi_tools extract "
	"--stdin={snakemake.input} "
	"--bc-pattern={snakemake.params.pattern} "
	"--log={snakemake.params.log} "
	"--stdout={snakemake.output} "
	"--quality-filter-threshold {snakemake.params.quality_threshold} "
	"--quality-encoding phred33 "
	)

