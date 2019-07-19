#purpose of this file is to create class 0 containing only chr1,8,21, by taking 10,000 rows from all the files

#imports

import sys
import os
import subprocess



#initializing array of filenames from where class0 is to be created
filenames1 = ['ENCFF127XXD_H3K4me3.bed','ENCFF099LMD_H3K4me2.bed', 'ENCFF139CKE_H4K20me1.bed', 'ENCFF183UQD_H3K4me1.bed','ENCFF322IFF_H3K27me3.bed','ENCFF498CMP_H3K36me3.bed', 'ENCFF578UBP_H3K27ac.bed', 'ENCFF624XRN_H2AFZ.bed', 'ENCFF737AMS_H3K4me3.bed', 'ENCFF894VEM_H3K9me3.bed']



#creating class0 bed file w chr 1,8,21 using 10,000 random rows from the 11 files
for i in range(len(filenames1)):
    command=''' shuf -n 10000 '''+ filenames1[i] + ''' >> class0.bed'''
    subprocess.call(command, shell=True)

    
#initializing filenames
class0_11files_only1821_bed= "inter_bed/class0_11files_only1821_test.bed"



#copy entries of chr1 from class0.bed to overall_chr1_class0.bed
command = '''awk '/chr1\t/' class0.bed >> '''+class0_11files_only1821_bed
subprocess.call(command, shell=True)
    
    
    
#copy entries of chr8 to overall_chr8_class0.bed
command = '''awk '/chr8\t/' class0.bed >> '''+class0_11files_only1821_bed
subprocess.call(command, shell=True)
    
    
    
#copy entries of chr21 to overall_chr21_class0.bed
command = '''awk '/chr21\t/' class0.bed  >> '''+class0_11files_only1821_bed
subprocess.call(command, shell=True)



#removing 1,8,21 from class0.bed because class0 will then be used to make training dataset and hence cannot have chr1,8,21
command='''sed -i '/chr1\t/d' ./class0.bed'''
subprocess.call(command, shell=True)

command='''sed -i '/chr8/d' ./class0.bed'''
subprocess.call(command, shell=True)

command='''sed -i '/chr21/d' ./class0.bed'''
subprocess.call(command, shell=True)



#converting bed file of 10 columns to 4 column file, with 100 upstream/downstream
command=''' echo "$(awk '{print $1, $2+$10-100, $2+$10+100, $4}' class0.bed)" > class0.bed'''
subprocess.call(command, shell=True)




#dropping peak info column and storing only 1st 3 columns
# command=''' echo "$(awk '{print $1, $2, $3}' class0.bed)" > class0.bed '''
# subprocess.call(command, shell=True)




#replacing spaces with tabs
command=''' echo "$(tr ' ' \\\\t < class0.bed)" > class0.bed '''
subprocess.call(command, shell=True)

command=''' echo "$(awk '{print $1, $2, $3,100}' class0.bed)" > class0.bed'''
subprocess.call(command, shell=True)

