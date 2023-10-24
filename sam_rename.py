#usr/bin/env python
import re
import argparse

#ARGPARSE
def get_args():
    parser = argparse.ArgumentParser(description= "This program takes in a sam file with UMIs and renames the QNAME column to include the UMI at the beggining")
    parser.add_argument("-f", "--file", help="Input the filename of the sam file to dedupe", type=str, required=True)
    parser.add_argument("-o", "--outfile", help="Input the filename of the new renamed sam file", type=str, required=True)
    return parser.parse_args()

args = get_args()
og_sam = args.file
new_sam = args.outfile

# FUNCTIONS
def read_sam(sam: str) -> list:
    ''''This function will read through the SAM file per record and will return a list with the data for QNAME'''
    record = sam.readline()
    if record == "":
        return 0
    if re.match("^@", record):
        return (record)
    else:
        umi = record.split()[0].split(":")[-1]
        header = record.split()[0].removesuffix(":"+ umi)
        new_header = [umi + ":" + header]
        new_record = record.split()[1:]
        new_header.extend(new_record)
        final_record = "\t".join(new_header)
        final_record = final_record + "\n"
    return (final_record)

#OPENING FILES
og_f = open(og_sam, "r")
nw_f = open(new_sam, "w")

#CODING
while True:
    new_file = read_sam(og_f)
    if new_file == 0:
        break
    #If the line starts with an @, it means its a header and should be passed to the new file or is the actual record  
    else:
        nw_f.write(str(new_file))


og_f.close()
nw_f.close()