#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --cpus-per-task=4
#SBATCH --partition=bgmp
#SBATCH --nodes=1
#SBATCH --job-name=umi


# r1_read="/projects/bgmp/shared/groups/2022/79K/salish/raw_data/first_mil_R1.fastq.gz"
# r2_read="/projects/bgmp/shared/groups/2022/79K/salish/raw_data/first_mil_R2.fastq.gz"
# r1_out="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/test_small/mil_r1.fastq.gz"
# r2_out="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/test_small/mil_r2.fastq.gz"
# folder="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/test_small/"

r1_read="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/trimming/no_leading/trim_Q20_R1.fastq.gz"
r2_read="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/trimming/no_leading/trim_Q20_R2.fastq.gz"
r1_out="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/third_try/umi_Q20_R1.fastq.gz"
r2_out="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/third_try/umi_Q20_R2.fastq.gz"
folder="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/third_try"



/usr/bin/time -v python3 remove_umi.py \
    -r1 $r1_read \
    -r2 $r2_read \
    -or1 $r1_out \
    -or2 $r2_out \
    -of $folder

