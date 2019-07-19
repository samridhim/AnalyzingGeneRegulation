#imports
import numpy as np 
import warnings
import import_ipynb
import Pipeline_Control as pp2
import DeepBind_Control as db22
import os
import pandas as pd
import sys
#import matplotlib.pyplot as pl				#NOT WORKING ON TERMINAL, WORKS ON JUPYTER
import subprocess
import gc
import random
import simplejson
from Bio import SeqIO
warnings.filterwarnings("ignore")
from guppy import hpy; 
import sys
import json

dir(db22)
dir(pp2)


'''
removing chr1,8,21 from the class1 file to make the class1 test file. remaining chr values (not 1,8,21) form the class1 train file
 '''

def remove_1_8_21_from_class1_file(class1file):

    #class1file has filename + extenstion, here we are simply separating the two
    file1, file_extension1 = os.path.splitext(class1file)
    
    f2 = "inter_bed/class0_11files_only1821_test.bed"
    
    print("here1: ",file1)
    
    #initializing filenames
    class1_test_bed= "inter_bed/class1_"+file1+"_test.bed"

    #copy entries of chr1 to class1_test_bed
    command = '''awk '/chr1\t/' '''+class1file+''' >> '''+class1_test_bed
    subprocess.call(command, shell=True)
    
    #copy entries of chr8 to class1_test_bed
    command = '''awk '/chr8\t/' '''+class1file+''' >> '''+class1_test_bed
    subprocess.call(command, shell=True)
    
    #copy entries of chr21 to class1_test_bed
    command = '''awk '/chr21\t/' '''+class1file+''' >> '''+class1_test_bed
    subprocess.call(command, shell=True)
    
    
    #removing intersections between overall class0_test (chr1,8,21 of 11 files) and class1_test_bed (chr1,8,21 of one file like IFF)
    count, num_in_class0, num_in_class1 = pp2.pipe(class1_test_bed,f2)
    
    
    #remove 1, 8, 21 from class1 file to make class1 train and return 
    command='''sed -i '/chr1\t/d' ./'''+class1file
    subprocess.call(command, shell=True)

    command='''sed -i '/chr8/d' ./'''+class1file
    subprocess.call(command, shell=True)

    command='''sed -i '/chr21/d' ./'''+class1file
    subprocess.call(command, shell=True)
    
    return class1file,  count, num_in_class0, num_in_class1



''' used to make reverse complement of dna sequence- simply takes normal DNA sequence (ACGT), append 10 N's, and then take complements of DNA sequence (TGCA)'''
def converter(sequence):
    new_sequence=[]
    for i in range(len(sequence)):
        if sequence[i]=='a' or sequence[i]=='A':
            new_sequence.append('T')
        elif sequence[i]=='c' or sequence[i]=='C':
            new_sequence.append('G')
        elif sequence[i]=='g' or sequence[i]=='G':
            new_sequence.append('C')
        elif sequence[i]=='t' or sequence[i]=='T':
            new_sequence.append('A')
        
            
    str1 = ''.join(new_sequence)
    str1=''.join(reversed(str1))
    
    return str1



'''f1 is class1 training data which is passed to the classify function. the function removes chr1,8,21 from f1, removes intersections between class1 train and class0 train and makes a call to deepbind to train the model'''

def classify(f1):

    #initializing the columns which the final df will have
    df_final = pd.DataFrame(columns=['File1','File2','Accuracy', 'Scores_Array'])
    count=0

	#calling function to remove chr1,8,21 from class1 train i.e. f1
    f1,  num_intersections, num_in_class0, num_in_class1 = remove_1_8_21_from_class1_file(f1)     #f1=class1_train.bed w/o 1,8,21
    f2 = "./class0.bed"        


    print("f1: ",f1)
    print("f2: ",f2)


	#removing intersections between class1 train and class0 train
    num_intersections_train, num_in_class0_train, num_in_class1_train = pp2.pipe("./"+f1,f2)

    file1, file_extension1 = os.path.splitext(f1)
    f1=file1.split("/")
    print("f1 is:",f1[0])


	#initializing filenames and filepaths
    class0_train= "inter_fa/class0.fa"
    class1_train= "inter_fa/"+f1[0]+".fa"
    class0_test="inter_fa/class0_11files_only1821_test.fa"
    class1_test = "inter_fa/class1_"+f1[0] +"_test.fa" 

    list0=[]
    list1=[]


    #making dataframe for train data

	#adding class0 sequences to training dataframe- sequence is in the form of 'orginal dna sequence + NNNNNNNNNN + reverse dna sequence' 
    for record in SeqIO.parse(class0_train, "fasta"):
        if 'N' not in str(record.seq):
            sequence=str(record.seq)+"NNNNNNNNNN"+str(converter(record.seq))
            list0.append(sequence)

	#adding class1 sequences to training dataframe- sequence is in the form of 'orginal dna sequence + NNNNNNNNNN + reverse dna sequence' 
    for record in SeqIO.parse(class1_train, "fasta"):
        if 'N' not in str(record.seq):
            sequence=str(record.seq)+"NNNNNNNNNN"+str(converter(record.seq))
            list1.append(sequence)
    
	target=[]

   #appending class label 0/1 for all the sequences
    for t in range(len(list0)):
        target.append(0)

    for m in range(len(list1)):
        target.append(1)

    sequences=list0+list1
    
    
    dictionary = {'seq': sequences, 'target': target}
    df_train = pd.DataFrame(dictionary)

    del list0
    del list1 

    list0=[]
    list1=[]


    #making dataframe for test data

	#adding class0 sequences to testing dataframe- sequence is in the form of 'orginal dna sequence + NNNNNNNNNN + reverse dna sequence' 
    for record in SeqIO.parse(class0_test, "fasta"):
        if 'N' not in str(record.seq):
            sequence=str(record.seq)+"NNNNNNNNNN"+str(converter(record.seq))
            list0.append(sequence)

	#adding class1 sequences to testing dataframe- sequence is in the form of 'orginal dna sequence + NNNNNNNNNN + reverse dna sequence' 
    for record in SeqIO.parse(class1_test, "fasta"):
        if 'N' not in str(record.seq):
            sequence=str(record.seq)+"NNNNNNNNNN"+str(converter(record.seq))
            list1.append(sequence)
    target=[]

    
    print "F1 IS" + str(f1)

	#UBP cannot test on entire file size due to memory issues, hence the test set of UBP is limited to 11,000 sequences
    if(f1[0]=="ENCFF578UBP_H3K27ac"):
        list1= list1[:11000]


	#appending class label 0/1 for all the sequences
    for t in range(len(list0)):
        target.append(0)

    for m in range(len(list1)):
        target.append(1)

    sequences=list0+list1

    dictionary = {'seq': sequences, 'target': target}
    df_test = pd.DataFrame(dictionary)

    print(df_train.shape)
    print(df_test.shape)


    #calling deepbind
    accuracy,scores= db22.deepbind1(df_train,df_test,f1)
    print("File1: ",f1,"\n")
    print("File2: ",f2,"\n")
    print("Accuracy: ",accuracy,"\n")
    print("Prob: ",scores,"\n")
    print ("Scores size array" , len(scores), "\n")
    print("Probability: ",scores,"\n")
 


    file2, file_extension2 = os.path.splitext(f2)
    f2=file2.split("/")
    print("f2 is:",f2[1])


    '''
    #histogram stuff
    title1="Class0 num: "+str(num_in_class0)+" Class1 num: "+str(num_in_class1)+" Num. of intersections: "+str(num_intersections)
    plot_title= "histograms/"+str(f1)+"_"+str(f2[1])+".png"
    pl.figure(figsize=(7,7))

    n1,bins1,patches1 = pl.hist(scores[0:num_in_class0],bins=10, density = False, edgecolor='black',alpha=0.5,label = "class0-red")
    n2,bins2,patches2 = pl.hist(scores[num_in_class0+1:],bins=10, density = False, edgecolor='black',alpha=0.5, label = "class1-black")
    for p in patches1:
        pl.text(p.get_x() + p.get_width()/2., p.get_height(), '%d' % int(p.get_height()),fontsize=12, color='red', ha='center', va='bottom')
    for p in patches2:
	pl.text(p.get_x() + p.get_width()/2., p.get_height(), '%d' % int(p.get_height()),fontsize=12, color='black', ha='center', va='bottom')
    pl.title(title1)
    pl.xlabel("Predicted probabilities")
    pl.ylabel("Frequency")
    pl.legend(loc='upper left') 
    pl.savefig(plot_title)
    #pl.clf()
    '''

	
	#printing stats to check memory usage, and deleting and freeing all data structures used to ensure that there is no memory error
    print("Printing Stats")
    h=hpy()
    print(h.heap())
    print("\n")
    del list0
    del list1
    del df_train
    del df_test
    gc.collect()
    

	#count is used to maintain the count of the models
    count=count+1
    
    return accuracy,scores
