#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --cpus-per-task=4
#SBATCH --partition=bgmp
#SBATCH --nodes=1
#SBATCH --job-name=dsnvm

conda activate bgmp_py310

#Input for reads without umis and trim without leading
r1_cut="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/second_try/Q20_no_umi_r1.fastq.gz"
r2_cut="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/removed_umi/second_try/Q20_no_umi_r2.fastq.gz"
#Input for reads after trimming
r1_trim="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/trimming/no_leading/trim_Q20_R1.fastq.gz"
r2_trim="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/trimming/no_leading/trim_Q20_R2.fastq.gz"
#Working directory
#raw_dir="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/deepsnv/raw_data/"
cut_dir="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/deepsnv/no_umi_data/"
trim_dir="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/deepsnv/trim_data"
#Bed File
bed_f="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/deepsnv/coordinates_mrd.bed"
#Sam and bwa
sam="/projects/bgmp/isisd/miniconda3/envs/bgmp_py310/bin/samtools"
bwa="/projects/bgmp/isisd/miniconda3/envs/bgmp_py310/bin/bwa"

#Running in trimmed data. Won't have adaptors, but will have the UMI-Linda in the sequence
/usr/bin/time -v ./run_deepseq.pl \
    -read1_fastq $r1_trim -read2_fastq $r2_trim \
    -coord_bed $bed_f \
    -filename_stub trimmed_snv \
    -working_dir $trim_dir \
    -uid_len1 18 -uid_len2 0 \
    -no_adaptor \
    -threads 8 \
    -samtools $sam -bwa $bwa

#Running in cut data. Won't have adaptors, or UMI-Linda in the sequence
/usr/bin/time -v ./run_deepseq.pl \
    -read1_fastq $r1_cut -read2_fastq $r2_cut \
    -coord_bed $bed_f \
    -filename_stub cut_snv \
    -working_dir $cut_dir \
    -no_uid \
    -no_adaptor \
    -threads 8 \
    -samtools $sam -bwa $bwa
