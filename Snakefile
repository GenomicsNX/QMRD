

####################################################  
#  Snakemake for AML MD residual analysis
#  Feb,13,2018
####################################################

import pandas as pd
import sys
import os


__author__ = "Ilker Tunc"
__copyright__ = "Copyright 2018, Ilker Tunc"
__license__ = "NIH"



os.makedirs(config['jobs_out'],exist_ok=True)
SAMPLES,=glob_wildcards('reads/{sample}.fastq.gz')



out_qc=expand('qc/{sample}/{sample}_fastqc',sample=SAMPLES)
out_trim=expand("cutadapt_trim/{sample}/{sample}.trimmed.fastq.gz",sample=SAMPLES)
out_umi=expand('umi_trim/{sample}/{sample}.umi.fastq.gz',sample=SAMPLES)
out_bam=expand('bam/{sample}/UniquelyMappedSorted.bam',sample=SAMPLES)
out_target_bam=expand('target_bam/{sample}/{target}.bam',sample=SAMPLES,target=config['list_of_genes']+config['list_of_fusions'])
out_target_reads=expand('target_reads/{sample}/{target}.reads.txt',sample=SAMPLES,target=config['list_of_genes'])
out_cutoff=expand("cutoff/{sample}/ABL1_cutoff.txt",sample=SAMPLES)
out_counts=expand("counts/{sample}/{target}.counts.txt",sample=SAMPLES,target=config['list_of_genes'])
out_counts_fusion=expand("counts_fusion/{sample}/{target}.counts.txt",sample=SAMPLES,target=config['list_of_fusions'])
out_final_report="report/final_report.tsv" 
out_final_report2="report/final_report_detailed.tsv" 
	

	
rule all:
	input:
		#out_qc,
		out_trim,
		out_umi,
		out_bam,
		out_target_bam,
		out_target_reads,
		out_cutoff,
		out_counts,
		out_counts_fusion,
		out_final_report,
		out_final_report2
		
		

		
rule fastqc:
	input:
		"reads/{sample}.fastq.gz"		
	output:
		"qc/{sample}/{sample}_fastqc",
	run:
		out_dir=os.path.dirname(output[0])
		shell("fastqc --extract --outdir {out_dir} {input} ")


		
rule cutadapt:
	input:
		"/home/tunci/Hourigon_AML/new_version/00-final/reads/{sample}.fastq.gz",
	output:
		fastq="cutadapt_trim/{sample}/{sample}.trimmed.fastq.gz",
		qc="cutadapt_trim/{sample}/{sample}.qc.txt",
		short="cutadapt_trim/{sample}/{sample}.short.fastq.gz"
	params:
		"-a GGACTCCAATACGCTAAGAA -g AATGTACAGTATTGCGTTTTG -m 100"
	run:
		shell("cutadapt {params}  --too-short-output {output.short} "
		  "-o {output.fastq} {input[0]} > {output.qc}")

		
		
rule trim_umi:
	input:
		"cutadapt_trim/{sample}/{sample}.trimmed.fastq.gz",
	output:
		"umi_trim/{sample}/{sample}.umi.fastq.gz",
	params:
		q_threshold=10
	script:
		config['scriptPath']+"/trim_umi.py"


		
rule star:
	input:
		"umi_trim/{sample}/{sample}.umi.fastq.gz",
	output:
		bam="bam/{sample}/UniquelyMappedSorted.bam",
		chimeric="bam/{sample}/Chimeric.out.sorted.bam",
		junction="bam/{sample}/Chimeric.out.junction",		
	threads: 8
	params:
		index=config['StarIndex'],
		mem="-m 4G"
	script:
		config['scriptPath']+"/star.py"

		

rule extract_bam:
	input:
		bam="bam/{sample}/UniquelyMappedSorted.bam",
		chimeric="bam/{sample}/Chimeric.out.sorted.bam"
	output:
		"target_bam/{sample}/{target}.bam"		
	params:
		target= lambda wildcards: config[wildcards.target],
	script:
		config['scriptPath']+"/extract_bam.py"


		
rule grep_target_region:
	input:
		"target_bam/{sample}/{target}.bam",
	output:
		"target_reads/{sample}/{target}.reads.txt"
	params:
		target= lambda wildcards: config[wildcards.target],
	script:
		config['scriptPath']+"/grep_target_reads.py"
		
	
	   		
rule find_cutoff:
	input:
		"target_reads/{sample}/ABL1.reads.txt"
	output:
		"cutoff/{sample}/ABL1_cutoff.txt",
		"cutoff/{sample}/ABL1_UMI_Dist_Plot.pdf"
	params:
		rscript=config['scriptPath']+"/InflectionPoint.r",
		pattern=config['ABL1']['cigar_in']
	script:
		config['scriptPath']+"/find_cutoff.py"



rule count_genes:
	input:
		reads="target_reads/{sample}/{target}.reads.txt",
		cutoff="cutoff/{sample}/ABL1_cutoff.txt",		
	output:
		"counts/{sample}/{target}.counts.txt",
	params:
		dct_target=lambda wildcards: config[wildcards.target],
	script:
		config['scriptPath']+"/count_genes.py"

				

rule count_fusions:
	input:
		junction="bam/{sample}/Chimeric.out.junction",
		bam="target_bam/{sample}/{target}.bam",		
		cutoff="cutoff/{sample}/ABL1_cutoff.txt",		
	output:
		"counts_fusion/{sample}/{target}.counts.txt",
	params:
		dct_target=lambda wildcards: config[wildcards.target],
		fixed_cutoff=3
	script:
		config['scriptPath']+"/count_fusions.py"


		
rule report_counts:
	input:
		res=[expand('counts/{sample}/{target}.counts.txt',sample=SAMPLES,target=config['list_of_genes']),
		 expand('counts_fusion/{sample}/{target}.counts.txt',sample=SAMPLES,target=config['list_of_fusions'])],
	output:
		"report/final_report.tsv"
	params:
		lst_genes=config['list_of_genes'],
		lst_fusions=config['list_of_fusions'],
	script:
		config['scriptPath']+"/make_final_report.py"


		
rule report_counts_detailed:
	input:
		res=[expand('counts/{sample}/{target}.counts.txt',sample=SAMPLES,target=config['list_of_genes']),
		 expand('counts_fusion/{sample}/{target}.counts.txt',sample=SAMPLES,target=config['list_of_fusions'])],
	output:
		"report/final_report_detailed.tsv"
	params:
		lst_genes=config['list_of_genes'],
		lst_fusions=config['list_of_fusions'],
	script:
		config['scriptPath']+"/make_final_report_detailed.py"
