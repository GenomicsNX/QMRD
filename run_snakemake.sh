#!/bin/bash



snakemake -pr  --keep-going -d $1 --configfile config2.json --cluster-config cluster_config.json -j 100 --latency-wait 120 --cluster "sbatch --cpus-per-task={cluster.cpus} --mem={cluster.mem} --time={cluster.time} -o {cluster.out}.out -e {cluster.out}.error -J {cluster.jobname}"



