
######## Snakemake header ########
import sys; sys.path.insert(0, "/home/tunci/miniconda3/envs/cfDNA/lib/python3.5/site-packages"); import pickle; snakemake = pickle.loads(b'\x80\x03csnakemake.script\nSnakemake\nq\x00)\x81q\x01}q\x02(X\x05\x00\x00\x00inputq\x03csnakemake.io\nInputFiles\nq\x04)\x81q\x05X&\x00\x00\x00trimmed/LD-2802-S8.R1.trimmed.fastq.gzq\x06a}q\x07X\x06\x00\x00\x00_namesq\x08}q\tsbX\t\x00\x00\x00wildcardsq\ncsnakemake.io\nWildcards\nq\x0b)\x81q\x0cX\n\x00\x00\x00LD-2802-S8q\ra}q\x0e(X\x06\x00\x00\x00sampleq\x0fh\rh\x08}q\x10X\x06\x00\x00\x00sampleq\x11K\x00N\x86q\x12subX\x04\x00\x00\x00ruleq\x13X\x0b\x00\x00\x00umi_extractq\x14X\x06\x00\x00\x00configq\x15}q\x16X\t\x00\x00\x00resourcesq\x17csnakemake.io\nResources\nq\x18)\x81q\x19(K\x01K\x01e}q\x1a(X\x06\x00\x00\x00_coresq\x1bK\x01h\x08}q\x1c(h\x1bK\x00N\x86q\x1dX\x06\x00\x00\x00_nodesq\x1eK\x01N\x86q\x1fuh\x1eK\x01ubX\x06\x00\x00\x00paramsq csnakemake.io\nParams\nq!)\x81q"(X\x0c\x00\x00\x00NNNNNNNNNNNNq#K\nX\x12\x00\x00\x00umi/LD-2802-S8.logq$e}q%(X\x07\x00\x00\x00patternq&h#X\x11\x00\x00\x00quality_thresholdq\'K\nh\x08}q((h&K\x00N\x86q)h\'K\x01N\x86q*X\x03\x00\x00\x00logq+K\x02N\x86q,uh+h$ubX\x06\x00\x00\x00outputq-csnakemake.io\nOutputFiles\nq.)\x81q/X\x1b\x00\x00\x00umi/LD-2802-S8.umi.fastq.gzq0a}q1h\x08}q2sbX\x07\x00\x00\x00threadsq3K\x01h+csnakemake.io\nLog\nq4)\x81q5}q6h\x08}q7sbub.')
######## Original script #########



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

