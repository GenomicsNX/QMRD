



from snakemake.shell import shell
from os import path
import tempfile


log=snakemake.log_fmt_shell(stdout=True,stderr=True)
target=snakemake.params.target


if target['catg']=="expr":
	ref=target['ref']
	start=target['start']
	end=target['end']
	bamfile=snakemake.input.bam

	tmpfile=tempfile.mktemp()
	shell(
		"samtools view -b {bamfile} {ref}:{start}-{end} > {tmpfile} ;"
		"samtools sort {tmpfile} >  {snakemake.output[0]} ;"	
		"samtools index {snakemake.output[0]} "
	)


if target['catg']=="fusion":
	ref1=target['r1']['ref']
	start1=target['r1']['start']
	end1=target['r1']['end']
	bamfile=snakemake.input.chimeric

	ref2=target['r2']['ref']
	start2=target['r2']['start']
	end2=target['r2']['end']

	tmpfile=tempfile.mktemp()
	shell(
		"samtools view -b {bamfile} {ref1}:{start1}-{end1} {ref2}:{start2}-{end2} > {tmpfile}  ;"
		"samtools sort {tmpfile} > {snakemake.output[0]}  ;"
		"samtools index {snakemake.output[0]} "
	)

