#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --cpus-per-task=4
#SBATCH --partition=bgmp
#SBATCH --nodes=1
#SBATCH --job-name=bwa_script_isis

conda activate /projects/bgmp/shared/groups/2022/79K/salish/envs/Salish

# Input file
in_f="/projects/bgmp/shared/groups/2022/79K/salish/isisd/data/bwa/third_try/aligned_Q20.sam"
# Output file
ou_f="/projects/bgmp/shared/groups/2022/79K/salish/isisd/data/bwa/third_try/umi_aligned_Q20.sam"
# Sorted file
s_ou_f="/projects/bgmp/shared/groups/2022/79K/salish/isisd/data/bwa/third_try/sorted_aligned_Q20.sam"
s_ou_b="/projects/bgmp/shared/groups/2022/79K/salish/isisd/data/bwa/third_try/sorted_aligned_Q20.bam"

/usr/bin/time -v python3 sam_rename.py \
    -f $in_f \
    -o $ou_f \

samtools sort -n $ou_f -o $s_ou_f

samtools view -h -o $s_ou_f $s_ou_b