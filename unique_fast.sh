#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --cpus-per-task=4
#SBATCH --partition=bgmp
#SBATCH --nodes=1
#SBATCH --job-name=umi

conda activate bgmp_py310

# r1_read="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/trimming/no_leading/trim_Q20_R1.fastq.gz"
# r2_read="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/trimming/no_leading/trim_Q20_R2.fastq.gz"
# r1_out="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/second_try/Q20_no_umi_r1.fastq.gz"
# r2_out="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/second_try/Q20_no_umi_r2.fastq.gz"
# folder="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/second_try/"

r1_read="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/umi_Q20_R1.fastq.gz"
r2_read="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/umi_Q20_R2.fastq.gz"
r1_out="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/unique_r1.fastq"
r2_out="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/unique_r2.fastq"


/usr/bin/time -v python3 unique_fast.py \
    -r1 $r1_read \
    -r2 $r2_read \
    -or1 $r1_out \
    -or2 $r2_out 

