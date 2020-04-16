#!/bin/bash
#SBATCH --time=0-00:10
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem=63G
#SBATCH --output=10k8corei.out

module load python/3.6
source ~/ENV/bin/activate


mpirun python mpipy.py out_ 10k 10000 10000