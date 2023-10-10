#!usr/bin/env python3

import pandas as pd
import sys
from datetime import datetime
import time
import os

t0 = time.time()

def print_s(line):
    print(line)
    sys.stdout.write("...")
    sys.stdout.write(line)

if(len(sys.argv)>1):
    run_state = str(sys.argv[1])
    run_state = "bash"
else:
    run_state = "not bash"

if(run_state == "bash" or run_state == "-b" or run_state == "b" or run_state == "-bash" or run_state == "--bash"):
    INPUT_control = str(sys.argv[1])
    OUTPUT_control = INPUT_control.replace('.txt', '.bed')
    length = int(sys.argv[2])
    #INPUT_ref = 'infinium.bed'
    INPUT_ref = sys.argv[3]
else:
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    from tkinter.simpledialog import askinteger
    Tk().withdraw()
    print_s("waiting for cg list file")

    INPUT_control = askopenfilename(title="Select cg list")
    print_s("cg list selected")

    OUTPUT_control = INPUT_control.replace('.txt', '.bed')
    print_s("waiting for length for each record ")

    length = askinteger(title='length of each sequence', prompt='length of each sequence')
    print_s("record length input entered")

    INPUT_ref = 'C:/Users/User/Documents/fasta_bed_switch/infimum_no_crx_no_snp.bed'

print_s("initiating CpG id conversion to bed")


#INPUT_control  = str(sys.argv[1])
#OUTPUT_control = str(sys.argv[2])
Control_list = []
Prog_list = []
Control_pos_list = ""

i = 0
#determin length of each sequence
#length = int(sys.argv[3])

for line_control in open(INPUT_control,"r"):
    Control_list.append(line_control.replace('\n',''))

for chunk in pd.read_csv(INPUT_ref,sep='\t',header=0, on_bad_lines='skip').dropna().iterrows():
    chunk_chr = chunk.__getitem__(1).get(0)
    chunk_start = chunk.__getitem__(1).get(1)
    chunk_end = chunk.__getitem__(1).get(2)
    chunk_ID = chunk.__getitem__(1).get(3)

    if chunk_ID in Control_list:
        Control_pos_list += f"{chunk_chr}\t {chunk_start} \t {chunk_end} \t  {chunk_ID} \n "
        i += 1

    if (i > (len(Control_list) + len(Prog_list))):
        break

print_s("finished")
open(OUTPUT_control,"w").close()
open(OUTPUT_control,"w").write(Control_pos_list)
print_s(f"results were saved at {OUTPUT_control}")

timer = f"total time: {time.time()-t0}"
print_s(timer)

now = str(datetime.now()).replace(" ","_").replace(":","-")
folder_pos = os.path.dirname(OUTPUT_control)
open(f"{folder_pos}/log_{now}.txt","x").write(f"input file: {OUTPUT_control}\n " +
                                 f"output file: {OUTPUT_control}\n " +
                                 f"reference file: {INPUT_ref}\n " +
                                 f"length: {length}\n " +
                                 f"{timer}")
print_s(f"log file were saved at {folder_pos}/log_{now}.txt")






