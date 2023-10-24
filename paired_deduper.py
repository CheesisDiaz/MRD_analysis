#!/usr/bin/env python
import re
import argparse

def get_args():
    parser = argparse.ArgumentParser(description= "This program takes in a sorted by Left most position (Column 4) reads and will remove any PCR duplicates which will be written to a new file")
    parser.add_argument("-f", "--file", help="Input the filename of the sam file to dedupe", type=str, required=True)
    parser.add_argument("-o", "--outfile", help="Input the filename of the new deduped sam file", type=str, required=True)
    parser.add_argument("-u", "--umi", help="Input the filename for the file with the known UMIs", type=str, required=True)
    return parser.parse_args()

args = get_args()
og_sam = args.file
new_sam = args.outfile
umi_file = args.umi


#VARIABLES
ban_set = set()
counting = {"Wrong_UMI":0, "Duplicate":0, "Unique":0}
other = {"Mapped":0, "Unmapped":0, "Unpropperly_Mapped":0, "Supplementary":0}
umi_data = []
umi_dict = {}
record1_set = set()
record2_set = set()

#FUNCTIONS

def mapped(flag:int) -> bool:
    '''This function will take the integer of bit flag and return if the read was mapped, propperly mapped and its not a supplementary alignment'''
    if (int(flag) & 4) == 4:
        #This means that the read is unmapped
        other["Unmapped"] += 1
        return False
    else:
        #Meaning the read is mapped
        other["Mapped"] += 1
        #To check if the read is propperly mapped
        if (int(flag) & 2) == 2:
            #To check if the read is supplementary
            if (int(flag) & 2048) == 2048:
                other["Supplementary"] += 1
                return False
            else:
                #To check if the read is not supplementary
                return True
        #The read is not propperly mapped
        else:
            other["Unpropperly_Mapped"] += 1
            return False

def strand_flag(flag:int) -> str: 
    '''This function will take the integer of bit flag and return the stranded direction'''
    if (int(flag) & 16) == 16:
        strand = "-"
    else:
        strand = "+"
    return(strand)

def read_sam(sam: str) -> list:
    ''''This function will read through the SAM file per record and will return a list with the data we need for deduping'''
    record = sam.readline()
    if record == "":
        return 0
    if re.match("^@", record):
        return (False, record)
    else:
        chrom = record.split("\t")[2]
        pos = record.split("\t")[3]
        b_flag = record.split("\t")[1]
        stranded = strand_flag(b_flag)
        seq = record.split("\t")[9]
        clip = record.split("\t")[5]
        umi = record.split("\t")[0].split(":")[0]
    return (chrom,pos,stranded,b_flag,clip,umi,seq,record)


def pos_clip(pos:int, strand:str, cigar:str) -> int:
    '''This function will consider Left most position the strand direction and the cigar string to return the correct start position of the read (will sum up when on negative strand and remove when on the positive strand)'''
    total = 0
    cigar_dict={"S":0, "M":0, "N":0, "D":0}
    if re.match("[0-9]+S", cigar):
        first_sc = cigar.split("S",1)
        if str(strand) == "+":
            pos = int(pos) - int(first_sc[0])
        elif str(strand) == "-":
            new_cigar = first_sc[1]
            new_cigar = re.split("([0-9]+[A-Z])", new_cigar)
            new_cigar = " ".join(new_cigar).split()
            for letter in new_cigar:
                cig_letter = str(letter[-1])
                if cig_letter in cigar_dict.keys():
                    cigar_dict[cig_letter] += int(letter[:-1])
            for key,values in cigar_dict.items():
                total += int(values)
            pos = int(pos) + int(total)                           
    else:
        if str(strand) == "+":
            pos = int(pos)
        elif str(strand) == "-":
            new_cigar = re.split("([0-9]+[A-Z])", cigar)
            new_cigar = " ".join(new_cigar).split()
            for letter in new_cigar:
                cig_letter = str(letter[-1])
                if str(cig_letter) in cigar_dict.keys():
                    cigar_dict[cig_letter] += int(letter[:-1])
            for key,values in cigar_dict.items():
                total += int(values)
            pos = int(pos) + int(total)
    return(pos)

#CODE
og_f = open(og_sam,"r")
nw_f = open(new_sam,"w")
umi_f = open(umi_file,"r")
new_umi = None
#List of known UMIs
umi_set = set()
for line in umi_f:
    umi_set.add(line.strip())

n=0
while True:
    n += 1 
    S1 = read_sam(og_f)
    if S1 == 0:
        break
    #If the line starts with an @, it means its a header and should be passed to the new file
    if S1[0] == False:
        nw_f.write(S1[1])
    #For the actual records you need to pass it through functions    
    else:
        if n > 195:
            S2 = read_sam(og_f)
        #First need to adjust the position for soft clipping in the original list. 
        curr_chrom, pos, stranded, bflag, cigar, umi, seq, record = S1
        curr_chrom2, pos2, stranded2, bflag2, cigar2, umi2, seq2, record2 = S2
        if mapped(bflag) == True and mapped(bflag2) == True:
            #Renaming variables to better understand the flow
            new_pos1 = pos_clip(pos, stranded, cigar)
            new_pos2 = pos_clip(pos2, stranded2, cigar2)
            #Since we removed supplementary alignments the chromosome of both reads should be the same
            #Checking that R1 and R2 are complementary
            if umi == umi2:
                if umi in umi_set:
                    compare_data = {(umi, curr_chrom, new_pos1, new_pos2):stranded,seq,new_pos2,stranded2,seq2]
                    umi_data.add(compare_data)
                    if umi != new_umi and new_umi == None:
                        new_umi = umi
                        if new_umi != None:
                            #Here check the sequences for those UMIs
                            for item in umi_data:
                                record1_set.add(item[4])
                                record2_set.add(item[7])
                            #Run the code for error correction
                            
                        umi_data.clear()
                        record1_set.clear()
                        record2_set.clear()
        #         nw_f.write(record)


og_f.close()
nw_f.close()
umi_f.close()
