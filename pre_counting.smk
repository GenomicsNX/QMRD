

####################################################  
#  Snakemake for AML MD residual analysis
#  Feb,13,2018
####################################################

import pandas as pd
import sys,os
from Bio.Seq import  Seq
from snakemake.utils import report

__author__ = "Ilker Tunc"
__copyright__ = "Copyright 2018, Ilker Tunc"
__license__ = "NIH"


JOBS_OUTPUT_DIR="Output/jobs_files"
BENCHMARK_OUTPUT_DIR="Output/benchmarks"


if not os.path.exists(JOBS_OUTPUT_DIR):
	print("Creating jobs output directory: %s" % (JOBS_OUTPUT_DIR) )
	os.makedirs(JOBS_OUTPUT_DIR)

if not os.path.exists(BENCHMARK_OUTPUT_DIR):
	print("Creating benchmarks output directory: %s" % (BENCHMARK_OUTPUT_DIR) )
	os.makedirs(BENCHMARK_OUTPUT_DIR)



ALL_SAMPLES,=glob_wildcards('reads/{sample}.fastq.gz')
ALL_SAMPLES_W_COUNTS,=glob_wildcards('reads/{sample}.fastq.gz')


scriptPath="/home/tunci/Hourigon_AML/new_version/scripts/"
StarIndex="/home/tunci/Hourigon_AML/reference/GRCh38_gencode_v24_CTAT_lib_Mar292017_prebuilt/ref_genome.fa.star.idx"



#include: "seqs.py"
#configfile: "/home/tunci/Hourigon_AML/new_version/config3.json"
configfile: "/home/tunci/Hourigon_AML/new_version/config.yml"
			

if 'tag' in config:
	prj_name=config['tag']
else:
	prj_name=os.getcwd().split('/')[-1]


			
rule all:
	input:
		expand('qc/{sample}/{sample}_fastqc',sample=ALL_SAMPLES),
		expand("trimmed/{sample}.trimmed.fastq.gz",sample=ALL_SAMPLES),
		expand('umi/{sample}/{sample}.umi.fastq.gz',sample=ALL_SAMPLES),
		expand('mapped/{sample}/UniquelyMappedSorted.bam',sample=ALL_SAMPLES),
		expand("fusion_umi_freq/{sample}/junction_summary.txt",sample=ALL_SAMPLES),
		expand("fusion_umi_freq/{sample}/cigars_for_top.txt",sample=ALL_SAMPLES),		
		#expand("downsample/{sample}_{N}M.fastq.gz",sample=ALL_SAMPLES)
		#"report/report_star_%s.txt" %prj_name


	
		
rule fastqc:
	input:
		"reads/{sample}.fastq.gz"		
	output:
		"qc/{sample}/{sample}_fastqc",
	benchmark:
		"Output/benchmarks/fastqc_{sample}"
	script:
		scriptPath+"fastqc.py"


		
rule cutadapt:
	input:
		"reads/{sample}.fastq.gz",
	output:
		fastq="trimmed/{sample}.trimmed.fastq.gz",
		qc="trimmed/{sample}.qc.txt",
		short="trimmed/{sample}.short.fastq.gz"
	benchmark:
		"Output/benchmarks/cutadapt_{sample}"
	params:
		"-a GGACTCCAATACGCTAAGAA -g AATGTACAGTATTGCGTTTTG -m 100"
	script:
		scriptPath+"cutadapt.py"


		
rule umi_extract:
	input:
		"trimmed/{sample}.trimmed.fastq.gz",
	output:
		"umi/{sample}/{sample}.umi.fastq.gz",
	benchmark:
		"Output/benchmarks/umi_extract_{sample}"
	params:
		pattern="NNNNNNNNNNNN",
		quality_threshold=10,
		log="umi/{sample}.log"
	script:
		scriptPath+"umi_extract.py"

		

rule star:
	input:
		"umi/{sample}/{sample}.umi.fastq.gz",
	output:
		bam="mapped/{sample}/UniquelyMappedSorted.bam",
		chimeric="mapped/{sample}/Chimeric.out.sorted.bam",
		junction="mapped/{sample}/Chimeric.out.junction",		
	benchmark:
		"Output/benchmarks/star_{sample}"
	threads: 8
	params:
		index=StarIndex,
		mem="-m 4G"
	script:
		scriptPath+"star.py"

		

		
rule analyze_chimeric_junctions:
	input:
		"mapped/{sample}/Chimeric.out.junction"
	output:
		reads="fusion_umi_freq/{sample}/junction_summary.txt",
		cigar="fusion_umi_freq/{sample}/cigars_for_top.txt"		
	script:
		scriptPath+"analyze_junction_file.py"




rule random_fastq:
	input:
		"reads/{sample}.fastq.gz"		
	output:
		"downsample/{sample}_{N}M.fastq.gz"
	params:
		N=lambda wildcards: float(wildcards.N)*1e6,
		prefix="downsample/{sample}_{N}M"	
	benchmark:
		"Output/benchmarks/random_{sample}_{N}"
	script:
		scriptPath+"random_fastq.py"



		
