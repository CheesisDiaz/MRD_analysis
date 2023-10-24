#!/usr/bin/env python
import re
import argparse
import gzip
import numpy as np

def get_args():
    parser = argparse.ArgumentParser(description= "This program takes in two fastq files, and will determine the number of matches for the data on the input file. This is meant for mutants")
    parser.add_argument("-r1", "--r1_file", help="Input the filename of the fastq r1 file to look through", type=str, required=True)
    parser.add_argument("-r2", "--r2_file", help="Input the filename of the fastq r2 file to look through", type=str, required=True)
    parser.add_argument("-o", "--out_folder", help="Input the direction of where you want the report to be saved at. Folder must already exist", type=str, required=True)
    return parser.parse_args()

args = get_args()
r1_f = args.r1_file
r2_f = args.r2_file
o_fold = args.out_folder

#VARIABLES
mut_seq = set()
double_mut_count = {}
init_mut_count = {}
fin_mut_count = {}
no_mut_count = 0
mut_number = 0
in_2f="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/mut_sequences/full_sequence_2mut.csv"
in_init_f="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/mut_sequences/full_sequence_init_mut.csv"
in_fin_f="/projects/bgmp/shared/groups/2022/79K/salish/isisd/Data/mut_sequences/full_sequence_fin_mut.csv"
report= o_fold + "mutants_report.txt"
two_r2_count_val: int = 0
two_r1_count_val: int = 0
init_r2_count_val: int = 0
init_r1_count_val: int = 0
fin_r1_count_val: int = 0
fin_r2_count_val: int = 0

#FUNCTIONS
def read_file(f:str) -> list:
    '''This function will take in a fastq file and return a list containing the data of a record'''
    head = f.readline().strip()
    seq = f.readline().strip()
    sep = f.readline().strip()
    qsc = f.readline().strip()
    if head == "":
        return 0
    return [head,seq,sep,qsc]

def create_list(f:str, name:str) -> set:
    '''This function will take in a file and create a set named after "name" containing each line of the file'''
    name = set()
    while True:
        mut = f.readline().strip()
        name.add(mut)
        if mut == "":
            break
    name.remove('')
    return(name)


def finding_mut(seq_r1:str, seq_r2:str, x_men:set, mut_count):
    '''This function will take the sequence for R1 and R2 and the set of mutants and will return a dictionary of all mutants found and a count of no mutants and mutants'''
    mut_cr1 = 0
    mut_cr2 = 0
    for mutant in x_men:
        if mutant in seq_r1:
            #To identify how many mutants we see in r1 against r2 
            #are they the same number?
            mut_r1= mutant + "_r1"
            mut_cr1 +=1
            if mut_r1 in mut_count:
                mut_count[mut_r1] += 1
            elif mut_r1 not in mut_count:
                mut_count[mut_r1] = 1
        if mutant in seq_r2:
            #To identify how many mutants we see in r1 against r2
            mut_r2= mutant + "_r2"
            mut_cr2 += 1
            if mut_r2 in mut_count:
                mut_count[mut_r2] += 1
            elif mut_r2 not in mut_count:
                mut_count[mut_r2] = 1
    return(mut_count, mut_cr1, mut_cr2)



#Opening files
mut_2f = open(in_2f, "r")
mut_inf = open(in_init_f, "r")
mut_finf = open(in_fin_f, "r")


#Creating lists
mut_2 = create_list(mut_2f, "mut_2")
mut_in = create_list(mut_inf, "mut_in")
mut_fin = create_list(mut_finf, "mut_fin")


#Code
n=0
with open(r1_f, "rt") as f1, open(r2_f, "rt") as f2:
    while True:
        R1 = read_file(f1)
        R2 = read_file(f2)
        if R1 == 0:
            break
        #Keep track of how many records we're parsing through
        n+=1
        head_r1,seq_r1,sep_r1,qsc_r1 = R1
        head_r2,seq_r2,sep_r2,qsc_r2 = R2
        #Having the list of different mutants we can cross check in our sequence
        #for two mutations
        
        two_mut_dict, two_r1_count, two_r2_count = finding_mut(seq_r1, seq_r2, mut_2, double_mut_count)
        two_mut_number = sum(two_mut_dict.values())
        # #for initial mutation only
        init_mut_dict, init_r1_count, init_r2_count = finding_mut(seq_r1, seq_r2,mut_in, init_mut_count)
        init_mut_number = sum(init_mut_dict.values())
        #for final mutation only
        fin_mut_dict, fin_r1_count, fin_r2_count = finding_mut(seq_r1,seq_r2, mut_fin, fin_mut_count)
        fin_mut_number = sum(fin_mut_dict.values())
        #storing and incrementinb count values to a variable
        two_r2_count_val += two_r2_count
        two_r1_count_val += two_r1_count
        init_r2_count_val += init_r2_count
        init_r1_count_val += init_r1_count
        fin_r1_count_val += fin_r1_count
        fin_r2_count_val += fin_r2_count


nothing = (n*2) - (two_mut_number+init_mut_number+fin_mut_number)
#Creating the report
with open(report,"w") as fr:
    fr.write("Stats from Looking for Mutants\n\n")
    fr.write("Summary: " + str(n) + "\n\n")
    fr.write("The Ammount of records is: " + str(n) + "\n")
    fr.write("Double-mutants in record r1 & r2 is: " + str(two_mut_number) + " - " + str(round(two_mut_number/(n*2),2)*100) + "%" + "\n")
    fr.write("Intial-mutants in record r1 & r2 is: " + str(init_mut_number) + " - " + str(round(init_mut_number/(n*2),2)*100) + "%"+ "\n")
    fr.write("Final-mutants in record r1 & r2 is: " + str(fin_mut_number) + " - " + str(round(fin_mut_number/(n*2),2)*100) + "%"+ "\n")
    fr.write("No Mutants in record r1 & r2 is: " + str(nothing) + " - " + str(round(nothing/(n*2),2)*100) + "%"+ "\n\n")
    fr.write("Full counts of r1 sequence found for two mutants: " + str(two_r1_count_val) + "\n")
    fr.write("Full counts of r2 sequence found for two mutants: " + str(two_r2_count_val) + "\n")
    fr.write("Full counts of sequence found for two mutants: " + str(two_mut_number) + "\n\n")
    for key in two_mut_dict:
        fr.write(str(key) + "\t" + str(two_mut_dict[key]) + "\n")
    fr.write("\n\n"+"Full counts of r1 sequence found for initial mutants: " + str(init_r1_count_val) + "\n")
    fr.write("Full counts of r2 sequence found for initial mutants: " + str(init_r2_count_val) + "\n")
    fr.write("Full counts of sequence found for inital mutants: "+ str(init_mut_number) + "\n\n")
    for key in init_mut_dict:
        fr.write(str(key) + "\t" + str(init_mut_dict[key]) + "\n")
    fr.write("\n\n"+"Full counts of r1 sequence found for final mutants: " + str(fin_r1_count_val) + "\n")
    fr.write("Full counts of r2 sequence found for final mutants: " + str(fin_r2_count_val) + "\n")
    fr.write("Full counts of sequence found for final mutants: "+ str(fin_mut_number) + "\n\n")
    for key in fin_mut_dict:
        fr.write(str(key) + "\t" + str(fin_mut_dict[key]) + "\n")

#Closing files
mut_2f.close()
mut_inf.close()
mut_finf.close()