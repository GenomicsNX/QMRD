


from snakemake.shell import shell
from os import path


log=snakemake.log_fmt_shell(stdout=True,stderr=True)
sample=snakemake.wildcards.sample

outprefix=path.dirname(snakemake.output[0]) + "/"


shell(
		"""
		STAR --genomeDir {snakemake.params.index} \
			 --readFilesIn {snakemake.input} \
			 --readFilesCommand zcat \
			 --twopassMode Basic \
			 --outReadsUnmapped None \
			 --chimSegmentMin 12 \
			 --chimJunctionOverhangMin 12 \
			 --alignSJDBoverhangMin 10 \
			 --alignMatesGapMax 200000 \
			 --alignIntronMax 200000 \
			 --chimSegmentReadGapMax parameter 3 \
			 --alignSJstitchMismatchNmax 5 -1 5 5 \
			 --runThreadN {snakemake.threads} \
			 --limitBAMsortRAM 31532137230 \
			 --outSAMtype BAM SortedByCoordinate \
			 --outFileNamePrefix {outprefix} 
 
		samtools view -h -q 255 -b {outprefix}Aligned.sortedByCoord.out.bam > {sample}.uniq.bam
		samtools sort {snakemake.params.mem} {sample}.uniq.bam -@ {snakemake.threads} -o {snakemake.output.bam}
		samtools index {snakemake.output.bam}
		rm {sample}.uniq.bam

		samtools view -bS {outprefix}Chimeric.out.sam > {sample}.Chimeric.out.bam
		samtools sort {snakemake.params.mem} {sample}.Chimeric.out.bam -@ {snakemake.threads} -o {snakemake.output.chimeric}
		samtools index {snakemake.output.chimeric}
		rm {sample}.Chimeric.out.bam
		"""
	)

