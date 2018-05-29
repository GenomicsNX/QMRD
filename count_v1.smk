

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
			
			
list_of_genes=['ABL1','WT1','PRAME','NPM1_wt','NPM1_mutant','CBFB-MYH11-rare']
list_of_fusions=['CBFB-MYH11','RUNX1-RUNX1T1','PML-RARA-bcr1','PML-RARA-bcr3','BCR-ABL1_p190','BCR-ABL1_p210']


list_of_targets=list_of_genes+list_of_fusions


if 'tag' in config:
	prj_name=config['tag']
else:
	prj_name=os.getcwd().split('/')[-1]



rule all:
	input:
		#expand("sam/{sample}/{target}.reads.txt",sample=ALL_SAMPLES,target=list_of_genes),
		#expand("cutoff/{sample}/ABL1_cutoff.txt",sample=ALL_SAMPLES),
		expand("counts/{sample}/{target}.counts.txt",sample=ALL_SAMPLES,target=list_of_genes),
		expand("counts/{sample}/{target}.umis.txt",sample=ALL_SAMPLES,target=list_of_genes),
		expand("counts2/{sample}/{target}.counts.txt",sample=ALL_SAMPLES,target=list_of_fusions),
		expand("counts2/{sample}/{target}.umis.txt",sample=ALL_SAMPLES,target=list_of_fusions),		
		#expand("gene_umi_freq/{sample}/{target}.umi_freq.txt",sample=ALL_SAMPLES,target=list_of_genes),		
		#"report/final_report_%s.xlsx" %prj_name,
		#"report/final_report_detailed_%s.xlsx" %prj_name,


		
				
rule grep_target_region:
	input:
		"mapped/{sample}/UniquelyMappedSorted.bam",
	output:
		"sam/{sample}/{target}.reads.txt"
	params:
		target= lambda wildcards: config[wildcards.target],
		outprefix="sam/{sample}/{target}"
	benchmark:
		"Output/benchmarks/grep_target_samfile_{sample}"
	script:
		scriptPath+"grep_target_from_bamfile.py"
		

		
rule find_cutoff:
	input:
		"sam/{sample}/ABL1.reads.txt"
	output:
		"cutoff/{sample}/ABL1_cutoff.txt",
		"cutoff/{sample}/ABL1_UMI_Dist_Plot.pdf"
	params:
		rscript=scriptPath+"InflectionPoint.r",
		pattern=config['ABL1']['cigar_in']
	script:
		scriptPath+"find_cutoff.py"

		
		
rule filter_umi:
	input:
		"sam/{sample}/{target}.reads.txt",
		"cutoff/{sample}/ABL1_cutoff.txt",		
	output:
		"counts/{sample}/{target}.counts.txt",
		"counts/{sample}/{target}.umis.txt",		
	params:
		dct_target=lambda wildcards: config[wildcards.target],
		fixed_cutoff=0
	benchmark:
		"Output/benchmarks/filter_umi_{sample}"
	script:
		scriptPath+"filter_umi.py"




rule filter_umi_fusion:
	input:
		"mapped/{sample}/Chimeric.out.junction",
		"cutoff/{sample}/ABL1_cutoff.txt",		
	output:
		"counts2/{sample}/{target}.counts.txt",
		"counts2/{sample}/{target}.umis.txt",		
	params:
		dct_target=lambda wildcards: config[wildcards.target],
		fixed_cutoff=0
	benchmark:
		"Output/benchmarks/filter_umi_fusion_{sample}"
	script:
		scriptPath+"filter_umi_fusion.py"

		

		
rule calculate_umi_freq:
	input:
		"sam/{sample}/{target}.reads.txt",
	output:
		"gene_umi_freq/{sample}/{target}.umi_freq.txt"
	params:
		target=lambda wildcards: config[wildcards.target],
	benchmark:
		"Output/benchmarks/calculate_umi_freq_{sample}"
	script:
		scriptPath+"calculate_umi_freq.py"
		

		
rule report_counts:
	input:
		res=[expand('counts/{sample}/{target}.counts.txt',sample=ALL_SAMPLES,target=list_of_genes),
		 expand('counts2/{sample}/{target}.counts.txt',sample=ALL_SAMPLES,target=list_of_fusions)],
	output:
		"report/final_report_%s.xlsx" %prj_name
	params:
		#meta=None,
		meta='sample_info.csv',		
		lst_genes=list_of_genes,
		lst_fusions=list_of_fusions,
	script:
		scriptPath+"make_final_report.py"

		

rule report_counts_detailed:
	input:
		res=[expand('counts/{sample}/{target}.counts.txt',sample=ALL_SAMPLES,target=list_of_genes),
		 expand('counts2/{sample}/{target}.counts.txt',sample=ALL_SAMPLES,target=list_of_fusions)],
	output:
		"report/final_report_detailed_%s.xlsx" %prj_name
	params:
		lst_genes=list_of_genes,
		lst_fusions=list_of_fusions,
	script:
		scriptPath+"make_final_report_detailed.py"


		

