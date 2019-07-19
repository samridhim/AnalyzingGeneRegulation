import pandas as pd
import os
import subprocess

def make_test_file(chr_number):
    
    #creating intermediate file names
    inter_bedfile="inter_bed/sliding_window_big_test_chr"+str(chr_number)+".bed"
    fasta_file="inter_fa/sliding_window_big_test_chr"+str(chr_number)+".fa"
    
    chromosomeid = []
    start = []
    end = []
    
    
    #setting chromosome start seed
    if chr_number==1:
        c=1600000
    elif chr_number==8:
        c=168939078
    elif chr_number==21:
        c=36035174
        
    #creating chr id, chr start and chr end fields    
    while c<=1800000:
        chromosomeid.append("chr"+str(chr_number))
        start.append(c)
        end.append(c+200)
        c = c+1
        
        
    dict1 = {'chr': chromosomeid, 'start': start, 'end' : end}
    
    
    #adding chr id, start, end fields to a dataframe 
    df = pd.DataFrame(dict1)
    cols = list(df.columns.values)
    print cols
    cols = ['chr', 'start', 'end']
    df = df[cols]
    df.to_csv(inter_bedfile, sep='\t',index=None,header=None)
    
    
    print df
    
    
    #appending a random 4th column to prepare the file for twoBitToFa 
    command=''' echo "$(awk '{print $1, $2, $3,100}' '''+inter_bedfile+''' )" >  '''+inter_bedfile 
    subprocess.call(command, shell=True)
    
    
    #replacing spaces with tabs
    command=''' echo "$(tr ' ' \\\\t <  '''+inter_bedfile+''' )" > '''+inter_bedfile 
    subprocess.call(command, shell=True)
    
    
    #converting bed to fasta
#     command=''' twoBitToFa hg19.2bit -bed='''+inter_bedfile+''' '''+fasta_file
#     subprocess.call(command, shell=True)
    command=''' twoBitToFa hg19.2bit -bed=inter_bed/sliding_window_big_test_chr1.bed sliding_window_big_test_chr1.fa'''
    subprocess.call(command, shell=True)


make_test_file(1)
