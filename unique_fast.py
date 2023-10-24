#!/usr/bin/env python
import re
import argparse
import gzip

def get_args():
    parser = argparse.ArgumentParser(description="This program will take two paired-end fastq files and will keep only unique reads based on the UMI")
    parser.add_argument("-r1", "--fastqr1", help="Input the filename for Read 1 (fastq)", type=str, required=True)
    parser.add_argument("-r2", "--fastqr2", help="Input the filename for Read 2 (fastq)", type=str, required=True)
    parser.add_argument("-or1", "--outputr1", help="Input the output filename for Read 1 (fastq)", type=str, required=True)
    parser.add_argument("-or2", "--outputr2", help="Input the output filename for Read 2 (fastq)", type=str, required=True)
    return parser.parse_args()

args = get_args()
fast = args.fastqr1
fast2 = args.fastqr2
out_r1_file = args.outputr1
out_r2_file = args.outputr2


#Variables
existing_umi=set()
existing_probes={}

#Functions
def read_file(f:str) -> list:
    '''This function will take in a fastq file and return a list containing the data of a record'''
    head = f.readline().strip()
    seq = f.readline().strip()
    sep = f.readline().strip()
    qsc = f.readline().strip()
    if head == "":
        return 0
    return [head,seq,sep,qsc]

#Opening files
f_or1 = open(out_r1_file, "w")
f_or2 = open(out_r2_file, "w")
report = "umi_report.txt"
probes_set = set()

with open("probes.csv","r") as fp:
    for line in fp:
        probe = line.strip()
        probes_set.add(probe)


#Actual Code
n=0
with gzip.open(fast,"rt") as fhr1, gzip.open(fast2,"rt") as fhr2:
    while True:
        R1=read_file(fhr1)
        R2=read_file(fhr2)
        #If the read 1 encounters an empty line it will stop reading and break the loop
        if R1 == 0:
            break
        n+=1
        #Changing variable name to make it easier to follow
        head_r1,seq_r1,sep,qsc_r1 = R1
        head_r2,seq_r2,sep,qsc_r2 = R2
        #Obtain global UMI
        umi = head_r1.split(":")[7].split()[0]
        if umi not in existing_umi:
            existing_umi.add(umi)
            f_or1.write("\n".join(R1)+"\n")
            f_or2.write("\n".join(R2)+"\n")
            for thing in probes_set:
                if thing in seq_r1:
                    existing_probes[thing] = 1

with open(report,"w") as fr:
    fr.write("Stats from Getting Unique reads\n\n")
    fr.write("The Ammount of reads is: " + str(n) + "\n\n")
    for key in existing_probes:
        fr.write(str(key) + "\t" + str(existing_probes[key]) + "\t" + str(round(existing_probes[key]/n * 100, 2)) + "%\n")
    fr.write("The Ammount unique reads is: " + str(len(existing_umi)) + "\n\n")


f_or1.close()
f_or2.close()