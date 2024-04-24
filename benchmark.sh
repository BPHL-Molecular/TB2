#!/usr/bin/bash
#SBATCH --account=bphl-umbrella
#SBATCH --qos=bphl-umbrella
#SBATCH --job-name=sanibel
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20                    
#SBATCH --mem=200gb
#SBATCH --time=48:00:00
#SBATCH --output=sanibel.%j.out
#SBATCH --error=sanibel.err
#SBATCH --mail-user=<EMAIL>
#SBATCH --mail-type=FAIL,END

#module load nextflow
APPTAINER_CACHEDIR=./
export APPTAINER_CACHEDIR


python3 ./bin/benchmark.py