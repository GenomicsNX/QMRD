#!/bin/bash


outdir=$1
njobs=$2  # number of jobs 

# submit to cluster
#snakemake -k -d $outdir -j $njobs --latency-wait 120 --configfile config.yaml --cluster-config cluster_config.yaml --cluster "sbatch --cpus-per-task={cluster.cpus} --mem={cluster.mem} --time={cluster.time} -o {cluster.out}.out -e {cluster.out}.error -J {cluster.jobname}"


# run locally
snakemake -k -d $outdir -j $njobs --configfile config.yaml

