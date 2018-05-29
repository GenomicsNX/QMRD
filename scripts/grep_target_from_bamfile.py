


from snakemake.shell import shell
from os import path
import pysam


bamfile=snakemake.input[0]

ref=snakemake.params.ref
start=snakemake.params.start
end=snakemake.params.end


samf=pysam.AlignmentFile(bamfile)

with open(snakemake.output[0],'w') as fout:
	fout.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format('seqid','chr','pos','cigar','umi','seq'))
	for x in samf.fetch(ref,int(start),int(end)):
		seqid=x.query_name
		pos=x.pos
		cigar=x.cigarstring
		q=x.query
		umi=x.qname.split('_')[1]
		fout.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(seqid,ref,pos,cigar,umi,q))

