
import os
import sys
import tempfile
from snakemake.shell import shell
import numpy as np

tmpfile1=tempfile.mktemp()
tmpfile2=tempfile.mktemp()

q_threshold=snakemake.params.q_threshold

# unzip to prepare for script below
shell("zcat {snakemake.input} > {tmpfile1}")

with open(tmpfile1, "r") as fin:
	with open(tmpfile2, "w") as fout:
		for line in fin:
			if line.startswith("@"):
				sequence = fin.readline()
				new_seq = sequence[12:].rstrip() # get sequence from the 12 position till end
				umi = sequence[:12]
				sign = fin.readline().rstrip()
				quality = fin.readline().rstrip()
				new_quality = quality[12:]
				umi_quality = quality[:12]
				readName='+'.join(line.rstrip().split()) + "_" + umi
				# check quality
				xx=np.array(list(map(ord,list(umi_quality))))
				xx=xx-33
				if any(xx<q_threshold):
					continue
			else:
				sequence = fin.readline()
				sign = fin.readline()
				quality = fin.readline()
			fout.write("{}\n{}\n{}\n{}\n".format(readName, new_seq, sign, new_quality))
		  
shell("gzip -c {tmpfile2} > {snakemake.output}")
