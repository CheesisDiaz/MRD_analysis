#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --cpus-per-task=4
#SBATCH --partition=bgmp
#SBATCH --nodes=1
#SBATCH --job-name=2_sent_30

conda activate bgmp_py310

# Q20 UMI TRIMMED
# r1_read="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/second_try/umi_Q20_R1.fastq"
# r2_read="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/second_try/umi_Q20_R2.fastq"
# r1_out="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/mutants/Q20_no_umi/full_seq/"
# RAW DATA
# r1_read="/projects/bgmp/shared/groups/2022/79K/salish/raw_data/Project-62-1_S1_L001_R1_001.fastq.gz"
# r2_read="/projects/bgmp/shared/groups/2022/79K/salish/raw_data/Project-62-1_S1_L001_R2_001.fastq.gz"
# r1_out="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/mutants/raw/"
#TEST FILES
# r1_read="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/unit_tests/20nt_r1.fastq"
# r2_read="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/unit_tests/20nt_r2.fastq"
# r1_out="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/unit_tests/out_sentinels/"
#Q35 UMI TRIMMED
# r1_read="/projects/bgmp/shared/groups/2022/79K/salish/ladriani/proj_salish_cfdna/cutting_linda/Isis/Q35_LIN18_R1.fq"
# r2_read="/projects/bgmp/shared/groups/2022/79K/salish/ladriani/proj_salish_cfdna/cutting_linda/Isis/Q35_LIN18_R2.fq"
# r1_out="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/mutants/Q35_no_umi/full_sequence"
#Q30 UMI TRIMMED
r1_read2="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/Q30/umi_trimmed_R1.fastq"
r2_read2="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/Q30/umi_trimmed_R2.fastq"
r1_out2="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/mutants/Q30_no_umi/"

#Q25 UMI TRIMMED
# r1_read2="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/Q25/umifiltered_1P_25.fq"
# r2_read2="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/Q25/umifiltered_2P_25.fq"
# r1_out2="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/mutants/Q25_no_umi/"


# /usr/bin/time -v python3 full_sentinels.py \
#     -r1 $r1_read \
#     -r2 $r2_read \
#     -o $r1_out 

/usr/bin/time -v python3 full_sentinels.py \
    -r1 $r1_read2 \
    -r2 $r2_read2 \
    -o $r1_out2 

