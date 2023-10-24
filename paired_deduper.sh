#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --cpus-per-task=4
#SBATCH --partition=bgmp
#SBATCH --nodes=1
#SBATCH --time=0-10:00:00
#SBATCH --job-name=deduping

conda activate /projects/bgmp/shared/groups/2022/79K/salish/envs/Salish


# /usr/bin/time -v ./Deduper.py \
#     -f "test/unit_test.sam" \
#     -o "test/unit_test_result.sam" \
#     -u "STL96.txt"

input="/projects/bgmp/shared/groups/2022/79K/salish/isisd/data/bwa/third_try/sorted_test_Q20.sam"
output="/projects/bgmp/shared/groups/2022/79K/salish/isisd/data/bwa/third_try/dedup_sorted_test_Q20.sam"
umi="/projects/bgmp/shared/groups/2022/79K/salish/isisd/data/removed_umi/third_try/known_umi.txt"


/usr/bin/time -v ./paired_deduper.py \
    -f $input \
    -o $output \
    -u $umi


