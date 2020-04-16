#!/bin/bash
#SBATCH --ntasks=8
#SBATCH --time=0-00:1
#SBATCH --mem-per-cpu=400M
#SBATCH --output=10k8core.out
srun ./test 10000 10000